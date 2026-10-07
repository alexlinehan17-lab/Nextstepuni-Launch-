import { AnimatePresence,motion,useIsPresent } from 'framer-motion';
import { createContext,useContext,useEffect,useId,useLayoutEffect,useRef,useState } from 'react';
import { createPortal } from 'react-dom';
const PopContext=createContext<any>(null);
export function Popover({children}:any){
 const[open,setOpen]=useState(false),trigger=useRef<HTMLButtonElement>(null),content=useRef<HTMLSpanElement>(null),id=useId();
 useEffect(()=>{const other=(e:Event)=>{if((e as CustomEvent).detail!==id)setOpen(false)};document.addEventListener('module-definition-open',other);return()=>document.removeEventListener('module-definition-open',other)},[id]);
 useEffect(()=>{if(!open)return;const outside=(e:PointerEvent)=>{if(!trigger.current?.contains(e.target as Node)&&!content.current?.contains(e.target as Node))setOpen(false)},escape=(e:KeyboardEvent)=>{if(e.key==='Escape'){setOpen(false);trigger.current?.focus()}};document.addEventListener('pointerdown',outside);document.addEventListener('keydown',escape);return()=>{document.removeEventListener('pointerdown',outside);document.removeEventListener('keydown',escape)}},[open]);
 return <PopContext.Provider value={{open,setOpen,trigger,content,id}}><span className="mr-definition-anchor">{children}</span></PopContext.Provider>;
}
export function PopoverTrigger({children,...props}:any){const p=useContext(PopContext);return <button {...props} ref={p.trigger} type="button" aria-expanded={p.open} aria-controls={p.open?p.id:undefined} onClick={()=>{if(!p.open)document.dispatchEvent(new CustomEvent('module-definition-open',{detail:p.id}));p.setOpen(!p.open)}}>{children}</button>}
function DefinitionContent({children,...props}:any){
 const present=useIsPresent();
 return <motion.span {...props} role="note" aria-hidden={!present || undefined} initial={{opacity:0,y:4}} animate={{opacity:1,y:0}} exit={{opacity:0,y:2}} transition={{duration:.16}}>{children}</motion.span>;
}
export function PopoverContent({children,...props}:any){
 const p=useContext(PopContext),[position,setPosition]=useState({left:16,top:16,width:224});
 useLayoutEffect(()=>{if(!p.open)return;const update=()=>{const anchor=p.trigger.current?.getBoundingClientRect();if(!anchor)return;const width=Math.min(224,innerWidth-32),height=p.content.current?.getBoundingClientRect().height||120,left=Math.max(16,Math.min(anchor.left,innerWidth-width-16)),below=anchor.bottom+8,top=below+height<=innerHeight-16?below:Math.max(16,anchor.top-height-8);setPosition({left,top,width})};update();window.addEventListener('resize',update);window.addEventListener('scroll',update,true);return()=>{window.removeEventListener('resize',update);window.removeEventListener('scroll',update,true)}},[p.open,p.trigger,p.content]);
 return createPortal(<AnimatePresence>{p.open&&<DefinitionContent {...props} ref={p.content} id={p.id} style={{...position,position:'fixed'}}>{children}</DefinitionContent>}</AnimatePresence>,document.body);
}
