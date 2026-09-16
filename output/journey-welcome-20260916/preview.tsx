import React, {useState} from 'react';
import {createRoot} from 'react-dom/client';
import '../../index.css';
import JourneyWelcome from '../../components/journey/JourneyWelcome';
function Review(){
 const [width,setWidth]=useState(320),[seen,setSeen]=useState(false);
 const embedded=new URLSearchParams(location.search).has('embedded');
 return embedded?<JourneyWelcome hasSeenWelcome={seen} onDismissWelcome={()=>setSeen(true)}/>:<div style={{background:'white',minHeight:'100vh',fontFamily:'DM Sans,sans-serif'}}><header style={{padding:16,display:'flex',gap:24,justifyContent:'center'}}><strong>Journey introduction · Phone preview</strong>{[320,390,700].map(w=><button key={w} onClick={()=>setWidth(w)}>{w}px</button>)}</header><iframe key={width} title="Responsive Journey introduction" src={new URLSearchParams(location.search).has('app')?'/?view=my-journey':'?embedded=1'} style={{display:'block',width,maxWidth:'100%',height:780,margin:'0 auto',border:'1px solid #ddd'}}/></div>
}
createRoot(document.getElementById('root')!).render(<Review/>);
