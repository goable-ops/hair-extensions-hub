/* Hair Extensions Hub scheduling pilot. No client records or live calendar access. */
(function(root){
"use strict";
const parseTime=t=>{if(!/^\d{2}:\d{2}$/.test(t))throw Error("Invalid time");const [h,m]=t.split(":").map(Number);if(h>23||m>59)throw Error("Invalid time");return h*60+m};
const formatTime=m=>String(Math.floor(m/60)).padStart(2,"0")+":"+String(m%60).padStart(2,"0");
const overlaps=(a,b)=>a.start<b.end&&b.start<a.end;
function available({windows,busy,minutes,buffer=30,step=30}){
 if(!Number.isInteger(minutes)||minutes<15||minutes>480||!Number.isInteger(buffer)||buffer<0||buffer>120||!Number.isInteger(step)||step<5||step>60)throw Error("Invalid configuration");
 const convert=x=>{const start=parseTime(x.start),end=parseTime(x.end);if(start>=end)throw Error("Invalid interval");return {start,end}};
 const blocks=busy.map(convert),slots=new Map();
 for(const window of windows.map(convert)){
 for(let start=window.start;start+minutes+buffer<=window.end;start+=step){
 const end=start+minutes,occupied={start,end:end+buffer};
 if(!blocks.some(b=>overlaps(occupied,b)))slots.set(start,{start:formatTime(start),end:formatTime(end),bufferEnd:formatTime(end+buffer)});
 }}
 return [...slots.entries()].sort((a,b)=>a[0]-b[0]).map(pair=>pair[1]);
}
function reserve(config,selected){
 const candidate=available(config).find(s=>s.start===selected);if(!candidate)return {ok:false,reason:"That slot is no longer available."};
 return {ok:true,slot:candidate,busy:[...config.busy,{start:candidate.start,end:candidate.bufferEnd}]};
}
root.HairScheduling=Object.freeze({available,reserve});
})(globalThis);