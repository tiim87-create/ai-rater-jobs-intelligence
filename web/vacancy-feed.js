/* AI Rater Insider — external vacancy data adapter. No WordPress-specific credentials. */
(function(){
'use strict';
const BASE='https://raw.githubusercontent.com/tiim87-create/ai-rater-jobs-intelligence/main/data/';
const VENDORS=new Set(['RWS','Welo Data','TELUS Digital']);
async function load(name){
 const response=await fetch(BASE+name,{cache:'no-store'});
 if(!response.ok)throw Error(name+': HTTP '+response.status);
 return response.json();
}
function safeDate(value){return typeof value==='string'?value.slice(0,10):'';}
function family(title){
 const t=(title||'').toLowerCase();
 if(/search engine evaluator|search quality|personalized internet assessor|content reviewer/.test(t))return 'Search Quality Rating';
 if(/internet safety|content evaluator/.test(t))return 'Internet Safety';
 if(/ads assessor|ads quality|personalized internet ads/.test(t))return 'Ads Evaluation';
 if(/online data analyst|maps analyst/.test(t))return 'Maps & Local';
 if(/speech/.test(t))return 'Speech Evaluation';
 if(/linguistic/.test(t))return 'Linguistic Evaluation';
 if(/annotat|label/.test(t))return 'Data Annotation';
 if(/ai|llm|prompt|model/.test(t))return 'AI Evaluation';
 return 'Other / Unclassified';
}
function normalize(j,events){
 const history=events.filter(e=>e.id===j.id);
 const recent=history.length?history[history.length-1]:null;
 const kind=recent&&recent.type;
 const state=j.status==='active'?(kind==='new'?'New':kind==='updated'?'Updated':'Active'):'Closed';
 return {id:j.id,vendor:j.vendor,title:j.title||'',country:j.country||'Unmapped',
 countries:Array.isArray(j.countries)?j.countries:[],url:j.url||'',
 family:family(j.title),status:state,firstSeen:safeDate(j.first_seen),
 lastSeen:safeDate(j.last_seen),closedAt:safeDate(j.disappeared_at||j.closed_at),
 lastChange:recent?safeDate(recent.at):'',sourceStatus:j.status};
}
async function fetchVacancies(){
 const [jobsData,historyData]=await Promise.all([load('jobs.json'),load('history.json')]);
 if(!Array.isArray(jobsData.jobs)||!Array.isArray(historyData.events))throw Error('Invalid vacancy dataset');
 const records=jobsData.jobs.filter(j=>VENDORS.has(j.vendor)).map(j=>normalize(j,historyData.events));
 if(!records.some(j=>j.vendor==='RWS')||!records.some(j=>j.vendor==='Welo Data')||!records.some(j=>j.vendor==='TELUS Digital'))throw Error('Missing vendor in dataset');
 return {generatedAt:jobsData.generated_at,records};
}
window.AIRaterVacancyFeed=Object.freeze({fetchVacancies});
})();