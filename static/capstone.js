'use strict';
const form=document.getElementById('search-form');
const description=document.getElementById('description');
const size=document.getElementById('size');
const budget=document.getElementById('budget');
const emptyWardrobe=document.getElementById('empty-wardrobe');
const submit=document.getElementById('submit');
const result=document.getElementById('result');
const feedback=document.getElementById('feedback');
const success=document.getElementById('success');

function node(tag,cls,text){
  const el=document.createElement(tag);
  if(cls) el.className=cls;
  if(text!==undefined) el.textContent=String(text);
  return el;
}
function showMessage(message,isError=false){
  result.classList.remove('hidden');
  success.classList.add('hidden');
  feedback.classList.toggle('error',isError);
  feedback.textContent=message;
}
function asPrice(value){
  const num=Number(value);
  return Number.isFinite(num)?num.toLocaleString('en-US',{style:'currency',currency:'USD'}):'Price unavailable';
}
function showResults(data){
  const item=data.selected_item;
  if(!item){showMessage('No listings matched. Try another search or increase your budget.',true);return;}
  const card=document.getElementById('selected');card.replaceChildren();
  card.append(node('div','small',item.platform||'Thrift listing'));
  card.append(node('h3',null,item.title||'Untitled item'));
  card.append(node('div','price',asPrice(item.price)));
  const details=[item.size?`Size ${item.size}`:null,item.condition,item.category].filter(Boolean).join('  •  ');
  card.append(node('div','meta',details));
  document.getElementById('outfit').textContent=data.outfit_suggestion||'No outfit suggestion generated.';
  document.getElementById('fit-card').textContent=data.fit_card||'No fit card generated.';
  const more=document.getElementById('other-matches');more.replaceChildren();
  const extras=(Array.isArray(data.search_results)?data.search_results:[]).filter(x=>x&&x.id!==item.id).slice(0,6);
  if(!extras.length)more.append(node('p',null,'No additional matches for this search.'));
  for(const x of extras){
    const tile=node('article','item');tile.append(node('strong',null,x.title||'Listing'));
    tile.append(node('span',null,`${asPrice(x.price)} · ${x.platform||'Thrift listing'}`));more.append(tile);
  }
  feedback.classList.remove('error');feedback.textContent='Found a match. Here is the selected item and an AI-generated styling idea.';
  result.classList.remove('hidden');success.classList.remove('hidden');
}
function buildQuery(){
  const words=description.value.trim();
  if(!words)return '';
  const parts=[words];
  if(size.value.trim())parts.push(`size ${size.value.trim()}`);
  if(budget.value.trim())parts.push(`under $${budget.value.trim()}`);
  return parts.join(' ');
}
form.addEventListener('submit',async event=>{
  event.preventDefault();if(submit.disabled)return;
  const query=buildQuery();
  if(!query){description.focus();showMessage('Enter an item or style to search for.',true);return;}
  const price=budget.value.trim();if(price&&(!Number.isFinite(Number(price))||Number(price)<=0)){
    budget.focus();showMessage('Maximum price must be a positive number.',true);return;
  }
  submit.disabled=true;submit.textContent='Finding your fit…';
  showMessage('Searching listings and generating your styling suggestion. Model calls can take a little longer.');
  try{
    const body={query};if(emptyWardrobe.checked)body.wardrobe={items:[]};
    const response=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
    const data=await response.json();
    if(!response.ok)throw Error(data.error||`Request failed (HTTP ${response.status})`);
    if(data.error){showMessage(data.error,true);return;}
    showResults(data);
  }catch(err){showMessage(`We couldn't complete that request: ${err.message}`,true);}
  finally{submit.disabled=false;submit.replaceChildren(document.createTextNode('Find my fit '),node('span',null,'↗'));result.scrollIntoView({behavior:'smooth',block:'start'});}
});
for(const button of document.querySelectorAll('.example'))button.addEventListener('click',()=>{
  const query=button.dataset.query||'';
  description.value=query;size.value='';budget.value='';form.requestSubmit();
});
