# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
The user is able to search listing data from thrift stores. They user can filter and categorize by description, size, and price. The tool will rank matching items based of user's selected filters/categories. Essentialy finding a "fit" (outfit) for the user, utilising thrift store listings.



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does: Searches thrift store listing data for items that match users description and other optional paramaters such as price and size, and ranks them by keyword overlap.**
- **Inputs:'description' (str), 'size' (str | None), 'max_price' (float | None)** <!-- name and type each: `max_price` (float), not "a price" -->
- **Returns:A list[dict] of matching listing dictionaries, ordered from best match to worst match, limited to config.SEARCH_RESULT_LIMIT. Each listing contains the following fields: (id, title, description, category, style_tags, size, condition, price, colors, brand, platform)**
- **When it has nothing: Returns an empty list**

### `suggest_outfit`

- **What it does: Uses the selected thrift listing and the user's wadrobe to generate one or two outfit suggestions. **
- **Inputs: 'new item' (dict), 'wardrobe' (dict)**
- **Returns: A non empty string (str) containing outfit suggestions. If wardrobe items are available it should also name pieces the user already owns**
- **When it has nothing: Returns general styling advice rather then failing and returning an empty string**

### `create_fit_card`

- **What it does:Turns the selected listing and outfit suggestion into a short caption someone could post about the find.**
- **Inputs: 'outfit' (str), 'new_item' (dict)**
- **Returns: A non empty string (str) containing a 2 to 4 sentence caption that mentions the item, price, platform, and overall outfit vibe.**
- **When it has nothing:**

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule: If search_listings returns an empty list, the agent stores a message in session["error"] explaining that no listings were matched and that user should change the description, size, or maximum price. The agent then stops without calling suggest_outfit or create_fit_card. If atleast one listing is returned, the agent stores them in session["search_results"] and selects the highest ranked result, stores it in the session["selected_item"], uses it with session["wardrobe"] to call suggest_outfit and stores it in session["outfit_suggestion"]. Then uses that session to call create_fit_card and stores the final caption in session["fit_card"] .**

**Where it lives:'agent.py::run_agent'** `agent.py::run_agent`

**How the query is parsed: The query is parsed determinstically using string/regex parsing.** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:The parsed search values are stored in session["parsed"] and used to call search_listings. The search results are stored in session["search_listings"] and the highest ranked result as session["selected_item"]. That selected item is then read back from the session alongside session["wardrobe"]and passed to suggest_outfit, whose result is stored as session["outfit_suggestion"]. Then session["outfit_suggestion"] and session["selected_item"] are read from the session and passed to create_fit_card, and the resulting caption is stored as session["fit_card"]** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'vintage graphic tee under $30'
Output:
Found: Y2K Baby Tee — Butterfly Print — $18.0 on depop

Outfit: Here are two outfit ideas using your new Y2K baby tee and items from your wardrobe:

Outfit 1: Casual Streetwear Y2K
- Baggy straight-leg jeans
- Black cropped zip hoodie
- Chunky white sneakers
- Black crossbody bag

Outfit 2: Edge Meets Vintage
- Wide-leg khaki trousers
- Vintage black denim jacket
- Black combat boots

Fit card: Channeling major early 2000s energy with this dreamy butterfly print Y2K baby tee. Grab it now on Depop for just $18.00 to instantly upgrade your rotation. Pair it with baggy denim and chunky sneakers for the ultimate off-duty streetwear look, or toughen it up with combat boots for a sweet-meets-edgy vibe.

```
```
extra: testing branch where search returns nothing:
$ python app.py ask 'designer ballgown size XXS under $5'2000s
Output:
No listings matched your search. Try broadening the description, changing the size, or raising the maximum price.

0 model calls this session
```
**The three tools, tested one at a time**


```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
Output:
[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]

```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
Output: 
**Outfit 1: Classic Streetwear Casual**
*   **Top:** White ribbed tank top
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   *Why it works:* Tucking the fitted white tank into the mid-rise vintage Levi's creates a clean silhouette, while the black denim jacket and chunky white sneakers lean into the streetwear aesthetic.

**Outfit 2: Cozy Layered Look**
*   **Top:** Oversized grey crewneck sweatshirt 
*   **Accessories:** Brown leather belt, Black crossbody bag
*   **Shoes:** Black combat boots
*   *Why it works:* Cinch the Levi's with the brown leather belt, do a half-tuck with the oversized grey crewneck for balanced proportions, and finish with black combat boots to add a subtle edge.


```

```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
Output:
Nothing beats the effortless streetwear vibe of a truly broken-in pair of denim. These Vintage Levi's 501 Jeans in a medium wash are up on my depop for just $38.00. Throw them on with your favorite crisp white sneakers for the ultimate classic casual look.

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for: How to avoid simple substring match, since a request for L should not automatically XL*
- *What came back: AI suggested tokenizing the listing size with a regular expression so sizes such as L, XL, S/M, and numeric sizes could be compared as separate tokens instead of raw substrings.*
- *What I changed: I added a _size_matches() helper that normalizes the requested size and listing size, extracts size tokens with regex, and checks membership against those tokens.*

**Moment 2**

- *What I asked for:Help debugging why suggest_outfit() was returning an empty string for both a normal wardrobe and an empty wardrobe.*
- *What came back: AI first helped isolate the model adapter by testing generate() directly. After that worked, I inspected the actual suggest_outfit() function being executed and found that the file still contained the starter stub returning "".*
- *What I changed:I saved the actual suggest_outfit() implementation into tools.py, then reran both the normal-wardrobe and empty-wardrobe tests and confirmed that both returned useful outfit suggestions.*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->
Unit 4 Stretch Feature

For the stretch feature, I am moving a second tool onto MCP. In addition to search_listings, I will expose suggest_outfit through the MCP server and have the agent call both tools through the MCP client. create_fit_card will remain a local tool.

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion                             | Target |Try 1|Try 2|Try 3|Try 4|Try 5| Verdict |
|---                                        |---|-------|----|----|----|------ |----------|
| 1.Matching query completes all three tools|4/5|PASS   |PASS|PASS|PASS|PASS   |MET (5/5) |
| 2.Impossible query stops before second tool|5/5|PASS  |PASS|PASS|PASS|PASS   |MET (5/5) |
| 3. Selected item is preserved through state|5/5|PASS  |PASS|PASS|PASS|PASS   |MET (5/5) |
| 4. Fit card includes price/platform and is 2–4 sentences|5/5|PASS|PASS|PASS|PASS|PASS| MET (5/5)|
| 5. Search respects max_price               |5/5|PASS  |PASS|PASS|PASS|PASS   |MET (5/5) |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```
results/run_2026-10-14_1353_before.md
Produced by: run_eval.py::main
Loop: agent.py::run_agent
Output:
selected item preserved through state  (example wardrobe)
  query: vintage polo shirt under $25

[1] search_listings (via MCP)
      in:  description='vintage polo shirt', size=None, max_price=25.0
      out: 10 items: Vintage Polo Shirt — Forest Green, Oversized Flannel Shirt — Plaid Red/Black, Y2K Baby Tee — Butterfly Print … +7 more

[2] suggest_outfit (via MCP)
      in:  new_item_id=lst_024, wardrobe_items=10
      out: Here are two ways to style your new forest green vintage polo shirt using items from your wardrobe:  **1. Retr…

[3] create_fit_card
      in:  new_item_id=lst_024, outfit_chars=815
      out: Scored this vintage polo shirt on thredUp for just $18.00 and I am already obsessed with the rich forest green…

  try 1: completed — fit card 289 chars
```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion                              | Target         | Verdict | How I decided |
|--------------------------------------------|----------------|---------|---------------|
| 1 |Matching query completes all three tools|4/5             |MET (5/5)|All five matching-query runs completed search_listings, suggest_outfit, and create_fit_card and returned a fit card.|
| 2 |Impossible query stops before the second tool|5/5        |MET (5/5)|All five runs returned an empty search result and stopped before suggest_outfit or create_fit_card ran.|
| 3 |Selected item is preserved through state|5/5             |MET (5/5)|In all five runs, session["selected_item"]["id"] was lst_024, and the trace showed new_item_id=lst_024 entering suggest_outfit.|
| 4 |Fit card includes price/platform and is 2–4 sentences|5/5|MET (5/5)|All five fit cards included the selected item's $42 price and Poshmark platform and were three sentences long.|
| 5 |Search respects max_price               |5/5             |MET (5/5)|Every search result in all five runs was at or below the parsed maximum price of $20.|

**Diagnoses**
None of the five acceptance criteria missed their targets in the baseline run.

The result does show that Criterion 1 is weaker than I would use again. It checks whether a matching query completes the whole agent, but it does not check whether the highest-ranked search result is actually the most relevant result. The baseline still selected the Y2K Baby Tee for vintage graphic tee under $30, even though a listing explicitly named Graphic Tee — 2003 Tour Bootleg Style was also returned. I would tighten this criterion in a future version to measure search-result relevance rather than only successful completion.


---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**
Calling function: 'app.py → agent.py::run_agent'
```
$ python app.py ask 'vintage graphic tee under $30' --trace
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 10 items: Y2K Baby Tee — Butterfly Print, Graphic Tee — 2003 Tour Bootleg Style, Vintage Band Tee — Faded Grey … +7 more
[2] suggest_outfit (via MCP)
      in:  dict with keys: new_item, wardrobe
      out: Here are two outfit ideas using your new Y2K baby tee and items from your wardrobe:  **Outfit 1: Casual Street…
[3] create_fit_card
      in:  dict with keys: outfit, new_item
      out: Channeling major early 2000s energy with this dreamy butterfly print Y2K baby tee. Grab it now on Depop for ju…

  Found:    Y2K Baby Tee — Butterfly Print — $18.0 on depop

  Outfit:   Here are two outfit ideas using your new Y2K baby tee and items from your wardrobe:

**Outfit 1: Casual Streetwear Y2K**
*   **Bottoms:** Baggy straight-leg jeans
*   **Outerwear:** Black cropped zip hoodie
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag
*   *Why it works:* The fitted silhouette of the baby tee balances the baggy jeans, and the cropped hoodie layered on top plays into classic Y2K proportions.

**Outfit 2: Edge Meets Vintage**
*   **Bottoms:** Wide-leg khaki trousers
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Black combat boots
*   *Why it works:* The tough black combat boots and denim jacket add an edgy contrast to the soft pink and purple butterfly print on the tee, while the khaki trousers keep the look grounded.

  Fit card: Channeling major early 2000s energy with this dreamy butterfly print Y2K baby tee. Grab it now on Depop for just $18.00 to instantly upgrade your rotation. Pair it with baggy denim and chunky sneakers for the ultimate off-duty streetwear look, or toughen it up with combat boots for a sweet-meets-edgy vibe.

0 model calls this session, 1 served from cache
```

**Empty search**
Calling function: 'app.py → agent.py::run_agent'
```
$ python app.py ask 'diamond spacesuit size XXS under $1' --trace
[1] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)

  No listings matched your search. Try broadening the description, changing the size, or raising the maximum price.

0 model calls this session
```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->
I moved search_listings and as a stretch feature suggest_outfit behind MCP. agent.py::run_agent now calls both through mcp_client.call_tool, while create_fit_card remains a local function call. Normal successful behavior stayed the same after the rewire. One architectural difference is that a model failure inside the MCP-hosted suggest_outfit reaches the parent agent through the MCP error boundary rather than directly as ModelUnavailable.


---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**
I changed the scoring inside search_listings so words matching the listing title receive additional weight. Previously, every matching token contributed equally regardless of whether it appeared in the title or another searchable field. The new score keeps the general keyword-overlap score but adds extra weight for title matches.

**Which failure it was meant to fix:**
None of my five original acceptance criteria missed their targets, but the baseline exposed a search-quality problem that Criterion 1 did not measure well. For the query vintage graphic tee under $30, the baseline ranked Y2K Baby Tee — Butterfly Print above Graphic Tee — 2003 Tour Bootleg Style, even though the second listing's title directly matched both "graphic" and "tee." I changed only the ranking calculation to address that problem.

### Run Log — After

| Criterion                                          | Target |Try 1|Try 2|Try 3|Try 4|try 5| Verdict |
|---------------------------------------------------------|---|-----|-----|-----|-----|-----|---------|
| 1. Matching query completes all three tools             |4/5|PASS |PASS |PASS |PASS |PASS |MET (5/5)|
| 2. Impossible query stops before second tool            |5/5|PASS |PASS |PASS |PASS |PASS |MET (5/5)|
| 3. Selected item is preserved through state             |5/5|PASS |PASS |PASS |PASS |PASS |MET (5/5)|
| 4. Fit card includes price/platform and is 2–4 sentences|5/5|PASS |PASS |PASS |PASS |PASS |MET (5/5)|
| 5. Search respects max_price                            |5/5|PASS |PASS |PASS |PASS |PASS |MET (5/5)|

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->
Yes. Before the change, Graphic Tee — 2003 Tour Bootleg Style ranked second and the agent selected lst_002, the Y2K Baby Tee. After the change, the Graphic Tee ranked first in all five runs and the agent selected lst_006 each time. The original acceptance-criteria pass counts remained the same, but the ranking behavior improved in the specific area identified by the baseline diagnosis. During Criterion 5 Try 3, create_fit_card temporarily could not reach the model. I still marked Criterion 5 as PASS because its criterion only measures whether every result returned by search_listings respects max_price. The search had already returned seven listings, all at or below the $20 maximum, before the unrelated downstream model failure occurred.

---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->
Search relevance is better after weighting title matches, but search_listings is still based on token overlap rather than semantic meaning. A listing can therefore rank because it shares several words with a query without actually being the best interpretation of what the user wanted. Model-backed tools can also fail because of an external model or API problem. The agent now handles that failure without crashing and gives the user a useful message, but it cannot make the external model available again itself.





<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**

## Capstone Unit 9

**What This Extends**

This capstone extends FitFindr, the Python thrift-shopping assistant I built in AI201 Units 3 and 4. The existing command-line flow searches sample thrift listings through MCP, generates outfit suggestions, and writes a fit-card caption. My new user-facing capability is a browser page that submits searches to that same agent and displays the selected listing, suggested outfit, caption, and other matches. The CLI, original planning loop, and MCP tools remain in place.

**The Shape**

I chose Shape C - Extend one capability. The bounded feature is the browser-based search/results experience; hosting, documentation, logging, and cost measurements accompany it as Unit 9 requirements. I plan to deploy to Render and preserve a reproducible local run path in `RUNNING.md`. Out of scope: building a new recommendation model, replacing Gemini or the MCP protocol, implementing purchases or user accounts, or constructing a persistent wardrobe database. These would be separate capabilities, not part of this extension. I am declaring all three chosen stretch features before testing: 1: a second independently measured improvement with a separate after-run; 2: a measured breakdown of end-to-end latency across stages; and 3: a load observation comparing the normal request rate with ten times that arrival rate. For the load observation I will state the rate and sample size, record queue waits/errors and token usage, and avoid exceeding the available Gemini quota. No results or acceptance targets have been written in advance of measurement.

**Running It**
- Hosted app: https://fit-findr.onrender.com/
- Source: https://github.com/gabrielc1317/ai201-project2-fitfindr-starter-v2026
- Prerequisites: Python 3.12, dependencies from requirements.txt, and a GEMINI_API_KEY environment variable (never commit the key).
- Local: pip install -r requirements.txt followed by python serve.py; open http://localhost:5000/.
- API: POST /ask with a JSON object such as {"query":"vintage graphic tee under $30"}; GET /health is the readiness check. Example:
curl -sS -X POST https://fit-findr.onrender.com/ask \
  -H 'Content-Type: application/json' \
  -d '{"query":"vintage graphic tee under $30"}'
- Render start command: gunicorn --bind 0.0.0.0:$PORT --workers 1 --worker-class gthread --threads 3 --timeout 120 serve:app.

The single worker keeps memory use lower, the threads allow lightweight health checks during longer requests, and an existing threading.Lock serializes agent execution. A free Render instance may experience cold starts. RUNNING.md contains the full setup and deployment procedure.


**Instrumentation**

I added observability.py hooks around /ask and per-stage timing in the agent. Each JSONL record includes a UTC timestamp, unique request ID, input summary, HTTP status, selected item ID, error/success fields, total server duration, time waiting on the in-process agent lock (queue_ms), and an applicable stages_ms breakdown (parse, mcp_search, mcp_outfit, fit_card). Records are written to logs/capstone_requests.jsonl on the instance and to Render stdout because the free-tier disk is not a durable logging store.

Log audit: My after2 Render export contains 60/60 complete structured /ask records, with unique IDs: 30 successful complete workflows (four stages), 15 no-result responses (parse/search only), and 15 invalid requests (HTTP 400 and empty stage timings). Ten records, including failures/rejections, are pasted verbatim below and stored in [`results/capstone_log_samples.jsonl`](results/capstone_log_samples.jsonl); the full audit is in [`results/capstone_logging_audit.md`](results/capstone_logging_audit.md).

```json
{"timestamp": "2026-11-18T04:18:19.511418+00:00", "request_id": "05bf64fa12a24612b6d26d2bbf9d3bf1", "input": {"query": "", "wardrobe_provided": false}, "output": {"http_status": 400, "selected_item_id": null, "error": "Send JSON with a non-empty string 'query'.", "success": false}, "duration_ms": 0.4, "queue_ms": 0, "stages_ms": {}}
{"timestamp": "2026-11-18T04:18:19.875137+00:00", "request_id": "c14c6889b49c463da065ad9d2fa4af17", "input": {"query": "   ", "wardrobe_provided": false}, "output": {"http_status": 400, "selected_item_id": null, "error": "Send JSON with a non-empty string 'query'.", "success": false}, "duration_ms": 0.2, "queue_ms": 0, "stages_ms": {}}
{"timestamp": "2026-11-18T04:18:20.090749+00:00", "request_id": "2673172f6de24e34ba5968b8177ff9b0", "input": {"query": "", "wardrobe_provided": false}, "output": {"http_status": 400, "selected_item_id": null, "error": "Send JSON with a non-empty string 'query'.", "success": false}, "duration_ms": 0.22, "queue_ms": 0, "stages_ms": {}}
{"timestamp": "2026-11-18T04:18:31.438903+00:00", "request_id": "0b478c184d6b4464b6d20fb98578a516", "input": {"query": "designer ballgown size XXS under $5", "wardrobe_provided": false}, "output": {"http_status": 200, "selected_item_id": null, "error": "No listings matched your search. Try broadening the description, changing the size, or raising the maximum price.", "success": false}, "duration_ms": 10028.24, "queue_ms": 0.0, "stages_ms": {"parse": 0.72, "mcp_search": 10026.79}}
{"timestamp": "2026-11-18T04:19:02.039337+00:00", "request_id": "ee805f3d7da44715bc90fbb691ebc17a", "input": {"query": "antique kimono under $3", "wardrobe_provided": false}, "output": {"http_status": 200, "selected_item_id": null, "error": "No listings matched your search. Try broadening the description, changing the size, or raising the maximum price.", "success": false}, "duration_ms": 4082.55, "queue_ms": 0.0, "stages_ms": {"parse": 0.03, "mcp_search": 4081.88}}
{"timestamp": "2026-11-18T04:19:33.038207+00:00", "request_id": "86083b18ec8d4bb6b2eb57e92ca04909", "input": {"query": "cashmere scarf under $1", "wardrobe_provided": false}, "output": {"http_status": 200, "selected_item_id": null, "error": "No listings matched your search. Try broadening the description, changing the size, or raising the maximum price.", "success": false}, "duration_ms": 4285.66, "queue_ms": 0.0, "stages_ms": {"parse": 0.03, "mcp_search": 4284.83}}
{"timestamp": "2026-11-18T04:19:56.334023+00:00", "request_id": "c702b4690bec499dbe2c9e24129e6713", "input": {"query": "vintage graphic tee under $30", "wardrobe_provided": false}, "output": {"http_status": 200, "selected_item_id": "lst_006", "error": null, "success": true}, "duration_ms": 23154.1, "queue_ms": 0.0, "stages_ms": {"parse": 0.03, "mcp_search": 4053.07, "mcp_outfit": 13680.69, "fit_card": 5419.53}}
{"timestamp": "2026-11-18T04:22:34.375924+00:00", "request_id": "1770edffc1f346dfb22312a41b724739", "input": {"query": "vintage band tee under $20", "wardrobe_provided": false}, "output": {"http_status": 200, "selected_item_id": "lst_033", "error": null, "success": true}, "duration_ms": 21751.21, "queue_ms": 0.0, "stages_ms": {"parse": 0.03, "mcp_search": 4108.1, "mcp_outfit": 16825.99, "fit_card": 816.35}}
{"timestamp": "2026-11-18T04:23:34.435948+00:00", "request_id": "3adf98d9291e44f380dce04765673757", "input": {"query": "corduroy pants under $35", "wardrobe_provided": false}, "output": {"http_status": 200, "selected_item_id": "lst_005", "error": null, "success": true}, "duration_ms": 8426.85, "queue_ms": 0.0, "stages_ms": {"parse": 0.03, "mcp_search": 3929.44, "mcp_outfit": 4496.32, "fit_card": 0.3}}
{"timestamp": "2026-11-18T04:25:26.143987+00:00", "request_id": "42c63870eec9420db9521e7ef75b7a02", "input": {"query": "vintage band tee under $20", "wardrobe_provided": false}, "output": {"http_status": 200, "selected_item_id": "lst_033", "error": null, "success": true}, "duration_ms": 8683.04, "queue_ms": 0.0, "stages_ms": {"parse": 0.03, "mcp_search": 4577.48, "mcp_outfit": 4104.49, "fit_card": 0.27}}
```
The stage durations measure elapsed time, not pure CPU use. In sequential tests queue_ms was near zero; it does not capture time spent at Render's proxy or waiting in a client queue. For malformed non-string queries, the current logger replaces input.query with an empty string, so the malformed type is not retained even though the HTTP rejection is correct.


**What It Costs**

I analyzed ten actual successful, complete requests from the first after2 matching trial, using the server logs rather than invented benchmark timings. The observed total server wall time was 179.889 seconds, or 17.989 seconds/request (median 16.829 seconds; range 16.055–23.154 seconds). Average per-stage durations were: mcp_search 4.195 s, mcp_outfit 12.204 s, and fit_card 1.590 s (parsing was negligible). The MCP outfit stage contributed roughly 68% of measured server time. The detailed ten run evidence is in [`results/capstone_cost_10run.md`] and [`results/capstone_cost_10run.csv`].

Two model calls are expected for a successful uncached request: one in the MCP suggest_outfit subprocess and one in parent-process create_fit_card. The exported structured logs do not include complete Gemini usage metadata from both processes. Consequently actual input/output token totals and provider-billed charges for these ten runs are not measured, and 17.989 seconds must not be represented as CPU billing or model cost. Later trials were faster partly because application caching reused responses, so they are not independent uncached cost samples.

For the configured gemini-3.5-flash-lite model, Google's Gemini Developer API Standard paid-tier published rates are $0.30/million input tokens and $2.50/million output tokens (including thinking tokens). See Google's official pricing. Free-tier usage may have no token charge within applicable quotas, but my account's actual billing was not verified.

100-user/day planning scenario (not observed traffic): if each user runs one successful uncached search, that's 100 searches/day, approximately 200 Gemini model calls/day before retries, and 100 × 17.989 s = 1,798.9 seconds (~30 minutes) of cumulative serialized server wall time. Traffic bursts could create waits even if the daily average is low. If a future measurement captures both processes' average token use per search, the estimated paid-tier daily API expense is:

100 × (avg_input_tokens × $0.30 + avg_output_tokens × $2.50) / 1,000,000.

Illustrative sensitivity only (not measured usage): assuming 3,000 input tokens and 1,000 output tokens across both model calls combined per search would produce approximately $0.0034/search and $0.34 per 100 searches at those paid rates. This is not a claim about what FitFindr actually billed.


**Run Log and Verdicts**

I committed the five numerical Unit 9 acceptance criteria in criteria.md before formal baseline testing. The harness capstone_baseline.py ran three trials per group against the deployed /ask endpoint, preserving request-level JSONL and Markdown summaries in results/capstone_{before,after1,after2}_*.{jsonl,md}. Its C1/C3/C5 results are HTTP/client-timing proxies, not automated verification of the browser's rendered DOM.

### Acceptance Criteria — Before and After Improvements

| Criterion (Original Threshold) | Before (Trials 1/2/3) | After Improvement 1 | After Improvement 2 | Finding |
|---|---|---|---|---|
| **C1. Browser Completion (10/10)** | 2/10, 0/10, 0/10 | 10/10, 10/10, 10/10 | 10/10, 10/10, 10/10 | HTTP workflow proxy met after fixes; browser rendering requires separate verification. |
| **C2. Input Validation (5/5)** | 3/5, 3/5, 3/5 | 3/5, 3/5, 3/5 | 5/5, 5/5, 5/5 | Invalid numeric and array queries now return HTTP 400 instead of HTTP 500. |
| **C3. No-Result Handling (5/5)** | 5/5, 5/5, 5/5 | 5/5, 5/5, 5/5 | 5/5, 5/5, 5/5 | Correct broadening message; no invented listing or fit card. |
| **C4. Observability (10/10 Logs)** | No complete independent audit | Not separately scored | 60/60 complete | All 60 audited after2 requests contained the required structured fields. |
| **C5. Response Under 30s (9/10)** | 2/10, 0/10, 0/10 | 10/10, 10/10, 10/10 | 10/10, 10/10, 10/10 | Completed-and-timely HTTP proxy met; actual browser click-to-render timing was not automated. |



**Diagnosis**: The initial matching baseline encountered a Render instance failure after two successful calls, causing one 502 during agent execution and 27 near-immediate gateway 502 responses. Render reported that its HTTP health check timed out at five seconds. A lone synchronous Gunicorn worker blocked on 15–30-second MCP/Gemini requests, preventing timely /health responses. Separately, malformed query values such as 123 or ["vintage tee"] caused AttributeError at serve.py's .strip() call, returning HTTP 500 instead of 400. These are observed failures—not deleted or relabeled successes. The initial 502 cascade is one infrastructure incident, not 28 independent agent defects.

**The Improvement**

**Improvement 1 — Hosting reliability:**. I changed the Render start command from a single synchronous Gunicorn worker to one gthread worker with three threads, keeping the existing agent lock. This lets /health respond while one thread handles a long agent request without running multiple Gemini agents in parallel. A concurrent probe produced 12/12 HTTP 200 health checks in 0.101–0.355 seconds, while a real 90s track jacket size M request completed its outfit and fit card. The formal after1 evaluation then completed 30/30 matching workflows with no 502s, versus 2/30 in the interrupted before run. This demonstrates a concrete improvement in availability during the test; it does not prove all future outages are eliminated.

**Stretch Improvement 2 — Defensive query validation:** I updated serve.py to verify the incoming JSON body is an object and query is a nonempty string before stripping or invoking the agent. Invalid bodies now return a helpful HTTP 400 response. A local Flask test using a mocked run_agent produced 5/5 HTTP 400 results and zero agent calls. After deployment, the three-trial invalid-request score rose from 3/5 per trial to 5/5 per trial, while the other HTTP acceptance-test groups continued to pass. The structured rejected-request logs have empty stage lists, consistent with no agent work performed.

**Stretch — Stage timing breakdown:** Timers isolate parsing, MCP search, MCP outfit generation, and fit-card generation. In the ten-run sample, the outfit stage averaged 12.204 s versus 4.195 s for search and 1.590 s for the fit card. These timings include process startup and waiting on external services; they are not isolated CPU utilization.

**Stretch — 1× versus 10× offered arrival rate.** I performed two bounded experiments without deliberately creating dozens of Gemini generations:

### 10× Load Observation — Results

| Workload | Offered Rate (1× → 10×) | Completed | Mean Client Latency (1× → 10×) | Achieved 10× Dispatch Rate | Health Checks |
|---|---|---:|---|---:|---:|
| Invalid JSON (no agent) | 0.5 → 5.0 req/s (20 per phase) | 40/40 | 116.91 → 103.33 ms | 5.0 req/s | 39/39 |
| Impossible search (MCP only) | 0.1 → 1.0 req/s (6 per phase) | 12/12 | 5.46 → 7.76 s | 0.287 req/s | 73/73 |


The validation path sustained the full tenfold offered rate without failed requests. The MCP path completed all requests but exhibited approximately 42% higher mean latency and client-side backpressure: the maximum dispatch delay reached 12.39 s under the two-in-flight client cap. This is evidence of client/backpressure constraints with serialized MCP processing, not an independently measured maximum server throughput. The smaller MCP experiment has only six requests per phase; neither experiment measures full Gemini outfit-generation throughput. Raw reports are in [`results/capstone_load_invalid.md`]and [`results/capstone_load_zero.md`]

**What's Still Broken**
Search relevance still relies on deterministic token overlap; it can rank a shared-word listing above a semantically better match. The outfit text is inserted as plain text in the browser, so model-generated Markdown formatting such as **Top:** can appear literally. Gemini/API outages, rate limits, and Render cold starts remain external reliability risks. Agent requests remain serialized, creating throughput/backpressure limitations under bursts despite responsive health checks. Full provider usage from both parent and MCP subprocesses has not been included in request logs, limiting exact cost accounting. Finally, this run's automated scoring checks HTTP behavior, not visual DOM correctness; visual browser checks and peer feedback must be documented separately rather than claimed without evidence.

**How I Used AI**

I used ChatGPT as a programming and evaluation assistant, while making the final design choices and running and interpreting the tests myself. One concrete debugging moment was the Render failure: I supplied the 502 sequence, Gunicorn logs, and Render's five-second health-check timeout. AI suggested investigating a blocked synchronous worker; I changed the deployment to gthread while preserving serialization and verified it with concurrent health checks and three-trial reruns. A second moment was the invalid-request bug: after sharing the Python AttributeError for numeric and list queries, AI suggested explicit JSON and string-type validation; I applied the fix, ran a mocked local test, and reran the deployed acceptance suite. AI also helped structure test scripts, but I reviewed the generated analysis against real request logs instead of treating AI output as evidence on its own.

