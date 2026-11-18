#!/usr/bin/env python3
"""Controlled 1x vs 10x offered-arrival-rate experiment for FitFindr.

Standard library only. Default scenario is invalid input (HTTP 400), which
bypasses Gemini/MCP, so it tests Flask/HTTP routing, not AI throughput.

Usage (recommended low-risk first pass):
  python capstone_load.py --dry-run
  python capstone_load.py --scenario invalid --count 20 --base-interval 2

Optional search/MCP path (no matches -> no Gemini, but each costs ~4s server
wall time; 2 client workers preserve one of 3 gthread slots for health):
  python capstone_load.py --scenario zero --count 6 --base-interval 10 --workers 2

These are *offered* arrival rates; a saturated client pool may delay actual
HTTP dispatches. Both rates are explicitly reported. Back off if 502/503.
"""
import argparse
import datetime as dt
import json
import statistics
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

QUERY_ZERO = 'designer ballgown size XXS under $5'
NO_MATCH = ('No listings matched your search. Try broadening the description, '
            'changing the size, or raising the maximum price.')


def get(base, path, timeout):
    req = Request(base.rstrip('/')+path, headers={'User-Agent':'FitFindr-Capstone-Load/1.0'})
    t0 = time.perf_counter()
    try:
        with urlopen(req, timeout=timeout) as r:
            status = r.status
            raw = r.read()
    except HTTPError as exc:
        status, raw = exc.code, exc.read()
    except (URLError, OSError, TimeoutError) as exc:
        return {'status':None,'elapsed_ms':round((time.perf_counter()-t0)*1000,2), 'error':str(exc)}
    try:
        body=json.loads(raw)
    except (json.JSONDecodeError,UnicodeDecodeError):
        body=None
    return {'status':status,'elapsed_ms':round((time.perf_counter()-t0)*1000,2), 'body':body}


def post(base, scenario, timeout):
    payload={'query':123} if scenario=='invalid' else {'query':QUERY_ZERO}
    req=Request(base.rstrip('/')+'/ask', data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type':'application/json','User-Agent':'FitFindr-Capstone-Load/1.0'},method='POST')
    start=time.perf_counter()
    try:
        with urlopen(req,timeout=timeout) as r:
            status,raw=r.status,r.read()
    except HTTPError as exc:
        status,raw=exc.code,exc.read()
    except (URLError,TimeoutError,ConnectionError,OSError) as exc:
        return {'http_status':None,'elapsed_ms':round((time.perf_counter()-start)*1000,2),'transport_error':str(exc),'passed':False}
    try:
        data=json.loads(raw) if raw else None
    except (json.JSONDecodeError,UnicodeDecodeError):
        data=None
    if scenario=='invalid':
        passed=(status==400 and isinstance(data,dict) and isinstance(data.get('error'),str))
    else:
        passed=(status==200 and isinstance(data,dict) and data.get('error')==NO_MATCH
                and not data.get('selected_item') and not data.get('fit_card') and not data.get('outfit_suggestion'))
    return {'http_status':status, 'elapsed_ms':round((time.perf_counter()-start)*1000,2),
            'transport_error':None,'passed':bool(passed), 'agent_error':data.get('error') if isinstance(data,dict) else None}


def percentile(xs,p):
    ordered=sorted(xs)
    if not ordered:return None
    index=(len(ordered)-1)*p/100
    i=int(index); fraction=index-i
    return ordered[i]*(1-fraction)+ordered[min(i+1,len(ordered)-1)]*fraction


def run_phase(name, args, interval):
    stop=threading.Event()
    phase_start=time.perf_counter()
    health=[]
    rows=[]
    row_lock=threading.Lock()
    inflight=0
    peak_inflight=0

    def monitor_health():
        while not stop.is_set():
            sample=get(args.base,'/health',args.timeout)
            sample['phase']=name
            sample['t_since_start_s']=round(time.perf_counter()-phase_start,3)
            health.append({k:v for k,v in sample.items() if k!='body'})
            if sample['status']!=200:
                stop.set()
                return
            stop.wait(args.health_interval)

    health_thread=threading.Thread(target=monitor_health,daemon=True)
    health_thread.start()

    def work(index,scheduled_at):
        nonlocal inflight,peak_inflight
        if stop.is_set():
            return {'index':index,'skipped':True,'reason':'abort after unhealthy service'}
        sent_at=time.perf_counter()
        with row_lock:
            inflight+=1
            peak_inflight=max(peak_inflight,inflight)
        try:
            result=post(args.base,args.scenario,args.timeout)
        finally:
            with row_lock:
                inflight-=1
        result.update({'index':index,'phase':name,'timestamp_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
                       'planned_offset_s':round(scheduled_at-phase_start,3),
                       'actual_dispatch_offset_s':round(sent_at-phase_start,3),
                       'client_dispatch_delay_ms':round((sent_at-scheduled_at)*1000,2)})
        if result.get('http_status') in (502,503,504) or result.get('http_status') is None:
            stop.set()
        return result

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures=[]
        for i in range(args.count):
            deadline=phase_start+i*interval
            delay=deadline-time.perf_counter()
            if delay>0: time.sleep(delay)
            if stop.is_set(): break
            futures.append(executor.submit(work,i+1,deadline))
        for future in futures:
            rows.append(future.result())
    stop.set()
    health_thread.join(timeout=args.timeout+2)
    rows.sort(key=lambda r:r['index'])
    return {'phase':name,'scenario':args.scenario,'intended_interval_s':interval,
            'intended_rps':round(1/interval,4),'count_requested':args.count,'count_sent':sum(not r.get('skipped') for r in rows),
            'peak_client_inflight':peak_inflight,'rows':rows,'health':health}


def summarize(result):
    rows=[x for x in result['rows'] if not x.get('skipped')]
    durations=[r['elapsed_ms'] for r in rows]
    failures=[r for r in rows if not r.get('passed')]
    dispatches=sorted(r['actual_dispatch_offset_s'] for r in rows)
    achieved=(len(dispatches)-1)/(dispatches[-1]-dispatches[0]) if len(dispatches)>1 and dispatches[-1]!=dispatches[0] else None
    return {'completed':len(rows),'passed':len(rows)-len(failures),'failures':len(failures),
            'mean_ms':round(statistics.mean(durations),2) if durations else None,
            'p50_ms':round(percentile(durations,50),2) if durations else None,
            'p95_ms':round(percentile(durations,95),2) if durations else None,
            'max_ms':max(durations) if durations else None,
            'intended_rps':result['intended_rps'],'achieved_dispatch_rps':round(achieved,3) if achieved else None,
            'health_ok':sum(h.get('status')==200 for h in result['health']),
            'health_total':len(result['health']), 'peak_inflight':result['peak_client_inflight'],
            'max_dispatch_delay_ms':round(max((r['client_dispatch_delay_ms'] for r in rows),default=0),2)}


def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--scenario',choices=('invalid','zero'),default='invalid')
    p.add_argument('--count',type=int,default=20)
    p.add_argument('--base-interval',type=float,default=2.0,help='seconds between planned normal-rate arrivals; 10x uses one tenth')
    p.add_argument('--workers',type=int,default=2,help='max client in-flight requests (2 protects gthread health-check capacity)')
    p.add_argument('--health-interval',type=float,default=1.0)
    p.add_argument('--base',default='https://fit-findr.onrender.com/')
    p.add_argument('--timeout',type=float,default=40)
    p.add_argument('--out',type=Path,default=Path('results'))
    p.add_argument('--dry-run',action='store_true')
    args=p.parse_args()
    if not(2<=args.count<=50):p.error('Use 2–50 requests per phase.')
    if args.base_interval<=0 or args.workers<1 or args.health_interval<=0:p.error('Intervals and worker count must be positive.')
    if args.scenario=='zero' and args.workers>2:p.error('Use --workers 2 or 1 with zero-result MCP requests to keep health checks responsive.')
    if args.scenario=='zero' and args.count>10:p.error('Limit zero-result experiment to <=10 requests/phase to minimize resource pressure.')
    if args.scenario=='zero' and args.base_interval<5:p.error('Use --base-interval >=5s for zero-result MCP experiments.')
    if args.scenario=='invalid' and args.base_interval<1:p.error('Use --base-interval >=1s for this small safe observation.')
    out=args.out
    raw=out/f'capstone_load_{args.scenario}.json'
    md=out/f'capstone_load_{args.scenario}.md'
    if raw.exists() or md.exists():p.error('Output exists, do not overwrite prior evidence. Move it first or use --out.')
    print(f'Scenario={args.scenario}, {args.count} requests/phase, max in-flight={args.workers}')
    print(f'1x offered interval {args.base_interval:.2f}s ({1/args.base_interval:.3f} req/s), 10x interval {args.base_interval/10:.2f}s ({10/args.base_interval:.3f} req/s).')
    print('No Gemini calls expected on these specific request paths.')
    if args.dry_run:return
    initial=get(args.base,'/health',args.timeout)
    if initial.get('status')!=200:p.error('Health check failed, aborting without load.')
    normal=run_phase('1x',args,args.base_interval)
    a=summarize(normal)
    print('1x:',a)
    if a['health_ok']!=a['health_total'] or a['failures']:
        print('Unhealthy or failed 1x; skipping 10x to protect deployment.')
        all_phases=[normal]
    else:
        print('Beginning 10x offered-arrival-rate phase.')
        high=run_phase('10x',args,args.base_interval/10)
        all_phases=[normal,high]
        print('10x:',summarize(high))
    out.mkdir(parents=True,exist_ok=True)
    raw.write_text(json.dumps({'scenario':args.scenario,'date_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
                               'phases':all_phases},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# FitFindr — 1× versus 10× arrival-rate observation','',
           f'- Scenario: `{args.scenario}`; requests per phase: {args.count}; client maximum in flight: {args.workers}.',
           f'- 1× offered rate: {1/args.base_interval:.3f} requests/s (every {args.base_interval:.2f}s).',
           f'- 10× offered rate: {10/args.base_interval:.3f} requests/s (every {args.base_interval/10:.2f}s).',
           '- All requests target the hosted Render `/ask`; a background client probes `/health` once per interval.',
           '- Zero Gemini calls expected: invalid bodies are rejected before agent execution; impossible zero-result searches stop before outfit generation.',
           '- This is an offered-rate experiment; dispatch backlog in the client executor reduces actual HTTP send rate under saturation.',
           '- Health probes, application logs, and client HTTP timing measure different layers; server `queue_ms` cannot measure reverse proxy waits.','',
           '| Metric | 1× | 10× |','|---|---:|---:|']
    summary=[summarize(r) for r in all_phases]
    for key,label in [('intended_rps','Offered requests/s'),('achieved_dispatch_rps','Achieved initial HTTP dispatches/s'),
                      ('completed','Requests completed'),('passed','Expected HTTP results'),('failures','Unexpected responses'),
                      ('mean_ms','Mean client latency (ms)'),('p50_ms','p50 client latency (ms)'),('p95_ms','p95 client latency (ms)'),
                      ('max_ms','Maximum client latency (ms)'),('health_ok','Successful /health checks'),('health_total','Total /health checks'),
                      ('peak_inflight','Peak client in-flight requests'),('max_dispatch_delay_ms','Maximum client-dispatch delay (ms)')]:
        v1=summary[0].get(key,'N/A')
        v2=summary[1].get(key,'NOT RUN') if len(summary)>1 else 'NOT RUN'
        lines.append(f'| {label} | {v1} | {v2} |')
    lines += ['', '## Interpretation limits','',
              '- Invalid-request scenario measures fast validation and HTTP responsiveness **only**. It does not represent full Gemini+MCP search throughput.',
              '- Zero-result scenario executes MCP search without creating outfits, but it is not a full successful agent workload.',
              '- A local thread-pool limit is a client-side safety mechanism, not a server concurrency result. Compare achieved dispatch rate with offered rate.',
              '- If 10× is skipped due to health or 5xx failure, that is a valid observed limitation and should not be filled with invented values.','']
    md.write_text('\n'.join(lines),encoding='utf-8')
    print(f'Saved evidence {raw} and {md}')

if __name__=='__main__':main()
