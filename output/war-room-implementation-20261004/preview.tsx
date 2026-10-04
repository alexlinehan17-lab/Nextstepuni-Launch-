import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import WarRoom from '../../components/WarRoom';
import IllustrationTheme from '../../components/IllustrationTheme';
import KobraScope, { Button } from '../../components/approved-ui-runtime';
import { ReviewProvider, profile, completions } from './review-data';
import '../../index.css';

function Review() {
  const [dark, setDark] = useState(document.documentElement.classList.contains('dark'));
  const [phone, setPhone] = useState(false);
  const [message, setMessage] = useState('Implemented product views / existing demo data / changes stay in memory');
  return <><IllustrationTheme /><KobraScope sound={false} className="review-tools"><strong>War Room / Implemented</strong><div><Button variant="outline" size="sm" onClick={() => { document.documentElement.classList.toggle('dark', !dark); setDark(!dark); }}>{dark ? 'Light' : 'Dark'} view</Button><Button variant="outline" size="sm" onClick={() => setPhone(value => !value)}>{phone ? 'Desktop' : 'Phone'} view</Button></div></KobraScope><p className="review-caption" role="status">{message}</p><div className="review-product" style={{ maxWidth: phone ? 390 : 1000 }}><ReviewProvider><WarRoom uid="demo-student" profile={profile} timetableCompletions={completions}
    onStudyNow={block => setMessage(`Study Room handoff: ${block.subject}, ${block.durationMinutes} minutes of ${block.sessionType}. Scheduled block ${block.blockId}.`)}
    onStudyTopic={selection => setMessage(`Study Room handoff: ${selection.subjectId}, ${selection.topicIds.length ? 'selected topic' : 'whole subject'}.`)}
    onPracticeTopic={(subject, topic, level) => setMessage(`Topic Atlas handoff: ${subject} / ${topic} / ${level}.`)}
  /></ReviewProvider></div></>;
}
createRoot(document.getElementById('root')!).render(<Review />);
