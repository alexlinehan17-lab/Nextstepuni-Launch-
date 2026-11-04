import { motion,useReducedMotion } from 'framer-motion';
import { ArrowRight,Check,X } from 'lucide-react';
import { useId,useState } from 'react';
import { Button } from '../approved-ui-runtime';
import { ExerciseHeading } from './BrandedFeatures';
const W=440,H=230,L=28,R=18,T=16,B=32;
const x=(i:number)=>L+i/5*(W-L-R),y=(v:number)=>T+(1-v)*(H-T-B);
function line(data:number[]){let d=`M ${x(0)} ${y(data[0])}`;for(let i=1;i<data.length;i++){const dx=x(i)-x(i-1);d+=` C ${x(i-1)+dx*.4} ${y(data[i-1])}, ${x(i-1)+dx*.6} ${y(data[i])}, ${x(i)} ${y(data[i])}`;}return d;}
function area(data:number[]){return line(data)+` L ${x(5)} ${y(0)} L ${x(0)} ${y(0)} Z`;}
function ComparisonChart({title,primary,secondary,areaData,labels,phases,tone,primaryLabel,secondaryLabel}:any){
 const id=useId().replace(/:/g,''),reduced=useReducedMotion();
 const color=tone==='green'?'var(--module-chart-green)':'var(--module-chart-red)';
 return <article className="bf-chart-card"><header><h4>{title}</h4><div className="bf-chart-legend"><span><i style={{background:color}}/>{primaryLabel}</span><span><i className="dashed"/>{secondaryLabel}</span></div></header><svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={`${title}: ${primaryLabel} and ${secondaryLabel} over time`}>
  <defs><linearGradient id={id} x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stopColor={color} stopOpacity=".22"/><stop offset="100%" stopColor={color} stopOpacity=".025"/></linearGradient></defs>
  {[.25,.5,.75,1].map(v=><line key={v} x1={L} x2={W-R} y1={y(v)} y2={y(v)} stroke="var(--module-line)" strokeWidth=".7" strokeDasharray="3 4" opacity=".55"/>)}
  <line x1={L} x2={W-R} y1={y(0)} y2={y(0)} stroke="var(--module-line)"/>
  <motion.path d={area(areaData||primary)} fill={`url(#${id})`} initial={reduced?false:{opacity:0}} animate={{opacity:1}} transition={{duration:.9}}/>
  <motion.path d={line(primary)} fill="none" stroke={color} strokeWidth="2.8" strokeLinecap="round" initial={reduced?false:{pathLength:0}} animate={{pathLength:1}} transition={{duration:1.1,ease:'easeOut'}}/>
  <motion.path d={line(secondary)} fill="none" stroke="var(--module-orange)" strokeWidth="2" strokeDasharray="5 4" strokeLinecap="round" initial={reduced?false:{opacity:0}} animate={{opacity:1}} transition={{duration:.8,ease:'easeOut',delay:.2}}/>
  {primary.map((v:number,i:number)=><motion.circle key={i} cx={x(i)} cy={y(v)} r="3.5" fill={color} initial={reduced?false:{opacity:0}} animate={{opacity:1}} transition={{delay:.14*i}}/>)}
  <text x="2" y={y(1)+4} className="bf-chart-axis">High</text><text x="4" y={y(0)-3} className="bf-chart-axis">Low</text>
  {labels.map((label:string,i:number)=><text key={label} x={x(i)} y={H-9} textAnchor={i===0?'start':i===5?'end':'middle'} className="bf-chart-axis bf-chart-axis-desktop">{label}</text>)}
  {[0,3,5].map(i=><text key={i} x={x(i)} y={H-6} textAnchor={i===0?'start':i===5?'end':'middle'} className="bf-chart-axis bf-chart-axis-mobile">{labels[i]}</text>)}
 </svg><div className="bf-chart-phases">{phases.map((phase:string,i:number)=><span key={phase}><small>0{i+1}</small>{phase}</span>)}</div></article>;
}
const noteCharts=[{title:'Verbatim Notes',primary:[.90,.88,.85,.82,.78,.75],secondary:[.55,.42,.30,.22,.15,.10],phases:['Feels productive','Confident','Exam shock'],tone:'red'},{title:'Generative Notes',primary:[.35,.38,.40,.42,.45,.48],secondary:[.45,.50,.55,.60,.62,.65],phases:['Feels slow','Processing','Locked in'],tone:'green'}];
const guiltCharts=[{title:'The Guilt Spiral',primary:[.25,.38,.52,.70,.85,.97],secondary:[.50,.40,.28,.18,.10,.05],areaData:[.25,.38,.52,.70,.85,.97],phases:['Guilt hits','Avoidance grows','Paralysis'],tone:'red'},{title:'The Self-Forgiveness Path',primary:[.25,.45,.30,.18,.12,.08],secondary:[.50,.30,.45,.55,.62,.68],areaData:[.50,.30,.45,.55,.62,.68],phases:['Acknowledge','Forgive & plan','Back on track'],tone:'green'}];
function Comparison({kind}: {kind:'note'|'guilt'}){
 const[revealed,setRevealed]=useState(false),reduced=useReducedMotion(),note=kind==='note';
 const labels=note?['Lecture','Day 1','Day 3','Day 7','Day 14','Day 30']:['Trigger','+1hr','+3hr','+1 day','+3 days','+1 week'];
 return <section className="bf-exercise bf-comparison"><ExerciseHeading title={note?'The Note-Taking Paradox':'The Guilt Divergence'}>{note?'Two students. Same lecture. Opposite strategies.':'Same procrastination event. Two completely different outcomes.'}</ExerciseHeading>{!revealed?<div className="bf-chart-reveal"><p>{note?'Most students try to capture every word. What does that actually do to understanding over time?':"After procrastinating, most students beat themselves up. But what if the data shows that’s the worst possible response?"}</p><Button variant="push" onClick={()=>setRevealed(true)} className="bf-reveal-button" data-sound="open">{note?'Reveal the Paradox':'Reveal the Divergence'}<ArrowRight size={16}/></Button></div>:<motion.div initial={reduced?false:{opacity:0,y:10}} animate={{opacity:1,y:0}}><div className="bf-charts">{(note?noteCharts:guiltCharts).map(chart=><ComparisonChart key={chart.title} {...chart} labels={labels} primaryLabel={note?'Note volume':'Negative emotion'} secondaryLabel={note?'Understanding':'Productivity'}/>)}</div><div className="bf-chart-notes"><article><p className="bf-chart-note-title"><X size={16}/>{note?'Verbatim':'Self-punishment'}</p><p>{note?'Feels productive but bypasses understanding. Your hand is busy, but your brain is on autopilot.':"After procrastinating, this feels like you’re being responsible, but it just makes things worse. Guilt → avoidance → more guilt. Within days, you feel completely stuck."}</p></article><article><p className="bf-chart-note-title"><Check size={16}/>{note?'Generative':'Self-forgiveness'}</p><p>{note?'Feels slower but forces the processing that creates lasting knowledge. Less ink, more thinking.':'Breaks the loop. When you accept the slip without hammering yourself, your brain calms down enough to actually get back to work. People who forgive themselves for procrastinating end up procrastinating less next time.'}</p></article></div><Button variant="ghost" className="bf-text-button" onClick={()=>setRevealed(false)}>Replay comparison<ArrowRight size={14}/></Button></motion.div>}</section>;
}
export const BrandedNoteComparison=()=> <Comparison kind="note"/>;
export const BrandedGuiltComparison=()=> <Comparison kind="guilt"/>;
