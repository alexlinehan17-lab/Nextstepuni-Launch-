import React from 'react';
import { ArrowRight, BookOpenCheck, FileSearch, Layers3, ListChecks } from 'lucide-react';
import './waysIn.css';

interface WaysInHubProps {
  onOpenTool: (toolId: string) => void;
}

const ModePreview: React.FC<{
  number: string;
  title: string;
  description: string;
  kind: 'steps' | 'map';
}> = ({ number, title, description, kind }) => (
  <article className="wi-hub-mode">
    <div className={`wi-choice-art wi-choice-art--${kind}`} aria-hidden="true">
      {kind === 'steps' ? <><i /><i /><i /><i /></> : <><i /><i /><i /></>}
    </div>
    <p className="wi-eyebrow">{number} · A different route</p>
    <h3>{title}</h3>
    <p>{description}</p>
  </article>
);

const WaysInHub: React.FC<WaysInHubProps> = ({ onOpenTool }) => (
  <div className="wi-hub">
    <header className="wi-hub-hero">
      <div>
        <p className="wi-eyebrow">Learn your way</p>
        <h1>Find a way into any question.</h1>
        <p>
          Ways In keeps the real exam question beside you, then makes its structure easier to work with—without changing the task or revealing the answer.
        </p>
      </div>
      <div className="wi-hub-mark" aria-hidden="true">
        <span /><i /><i /><i />
      </div>
    </header>

    <section className="wi-hub-section" aria-labelledby="wi-hub-modes">
      <div className="wi-hub-section-heading">
        <p className="wi-eyebrow">Two ways in</p>
        <h2 id="wi-hub-modes">Choose support at the moment you need it.</h2>
      </div>
      <div className="wi-hub-modes">
        <ModePreview
          number="01"
          title="One step at a time"
          description="Read one line, find the job, collect the boundaries, shape an attempt and return to the exact wording."
          kind="steps"
        />
        <ModePreview
          number="02"
          title="Show me"
          description="Turn the question into a task map, an empty answer shape and a colour-coded view of what each phrase is doing."
          kind="map"
        />
      </div>
    </section>

    <section className="wi-hub-section" aria-labelledby="wi-hub-source">
      <div className="wi-hub-section-heading">
        <p className="wi-eyebrow">Start with a real question</p>
        <h2 id="wi-hub-source">The source stays in charge.</h2>
        <p>Open a question in either tool, then choose <strong>Ways In</strong>. Your attempt and plan return with you.</p>
      </div>
      <div className="wi-hub-sources">
        <button type="button" onClick={() => onOpenTool('mark-bank')}>
          <span className="wi-hub-source-icon"><ListChecks size={25} /></span>
          <span>
            <small>Structured question bank</small>
            <strong>Choose from Mark Bank</strong>
            <em>Exact wording, figures, marks and answer shape.</em>
          </span>
          <ArrowRight size={18} />
        </button>
        <button type="button" onClick={() => onOpenTool('paper-trail')}>
          <span className="wi-hub-source-icon"><FileSearch size={25} /></span>
          <span>
            <small>Past-paper archive</small>
            <strong>Choose from Paper Trail</strong>
            <em>Use a verified question crop in Revise by Topic.</em>
          </span>
          <ArrowRight size={18} />
        </button>
      </div>
    </section>

    <footer className="wi-hub-principles">
      <div><BookOpenCheck size={19} /><span><strong>Original always visible</strong>Wording and diagrams remain the authority.</span></div>
      <div><Layers3 size={19} /><span><strong>Scaffold, then remove</strong>Every route ends back at the real question.</span></div>
      <div><ListChecks size={19} /><span><strong>No answer leak</strong>The marking scheme stays closed until normal self-marking.</span></div>
    </footer>
  </div>
);

export default WaysInHub;
