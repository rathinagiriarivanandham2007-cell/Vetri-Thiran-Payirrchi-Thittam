const state = {type:"home"};

const fields = {
 home: {
  title:"Home Interior Planner",
  html:`<label>Room type<select id="room"><option>Living Room</option><option>Bedroom</option><option>Kitchen</option><option>Multiple Rooms</option></select></label>
  <label>What do you need?<input id="needs" placeholder="e.g. 2 lights, 1 fan, dining table"></label>
  <label>Style<select id="style"><option>Modern</option><option>Minimal</option><option>Traditional</option><option>Budget-friendly</option></select></label>`
 },
 party: {
  title:"AI Party Budget Planner",
  html:`<label>Guest count<input id="guests" type="number" value="30" min="1"></label>
  <label>Event type<select id="event"><option>Birthday</option><option>Wedding</option><option>Corporate</option><option>Family Function</option></select></label>
  <label>Venue / location<input id="venue" placeholder="e.g. Karur"></label>`
 },
 jewelry: {
  title:"Jewelry Budget Planner",
  html:`<label>Occasion<select id="occasion"><option>Wedding</option><option>Festival</option><option>Party</option><option>Casual</option></select></label>
  <label>Style preference<select id="jstyle"><option>Elegant</option><option>Traditional</option><option>Minimal</option><option>Trendy</option></select></label>
  <label>Outfit color<input id="outfit" placeholder="e.g. dark blue"></label>`
 }
};

document.querySelectorAll(".planner").forEach(btn=>{
 btn.onclick=()=>{
   document.querySelectorAll(".planner").forEach(x=>x.classList.remove("active"));
   btn.classList.add("active");
   state.type=btn.dataset.type;
   document.getElementById("formTitle").textContent=fields[state.type].title;
   document.getElementById("dynamic").innerHTML=fields[state.type].html;
 }
});
document.getElementById("dynamic").innerHTML=fields.home.html;

function collect(){
 const ids=["room","needs","style","guests","event","venue","occasion","jstyle","outfit"];
 const p={};
 ids.forEach(id=>{const e=document.getElementById(id);if(e)p[id]=e.value});
 return p;
}
function money(n){return "₹"+Number(n||0).toLocaleString("en-IN")}

document.getElementById("generate").onclick=async()=>{
 const budget=Number(document.getElementById("budget").value);
 if(!budget||budget<=0){alert("Enter a valid budget.");return}
 const btn=document.getElementById("generate");
 btn.disabled=true;btn.textContent="✨ Creating your plan...";
 try{
  const res=await fetch("/api/plan",{method:"POST",headers:{"Content-Type":"application/json"},
   body:JSON.stringify({planner:state.type,budget,preferences:collect()})});
  const data=await res.json();
  if(!res.ok)throw new Error(data.error||"Request failed");
  render(data,budget);
 }catch(e){alert(e.message)}
 finally{btn.disabled=false;btn.textContent="✨ Generate Smart Plan"}
};

function render(data,budget){
 const box=document.getElementById("resultBox");
 const recs=data.recommendations||[];
 const allocated=data.allocated||{};
 const allocHtml=Object.entries(allocated).map(([k,v])=>`<span>${k.replaceAll("_"," ")}: <b>${typeof v==="number"?money(v):v}</b></span>`).join(" · ");
 box.innerHTML=`<div class="result-summary"><h3>${data.summary||"Your personalized plan"}</h3><p>${allocHtml}</p><small>${data.note||""}</small></div>
 <div class="result-grid">${recs.map(r=>`<article class="rec"><div class="rec-top"><div><h3>${r.name||"Recommendation"}</h3><div class="platform">${r.platform||"Platform"}</div></div><div class="price">${money(r.estimated_price??r.price)}</div></div><p>${r.reason||""}</p></article>`).join("")}</div>`;
 document.getElementById("results").classList.remove("hidden");
 document.getElementById("results").scrollIntoView({behavior:"smooth"});
}
