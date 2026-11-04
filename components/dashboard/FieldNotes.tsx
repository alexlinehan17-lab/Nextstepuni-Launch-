import React from 'react';
import { motion } from 'motion/react';
import { ArrowUpRight } from 'lucide-react';
import type { StudySessionRecord } from '../../studySessionData';
import ThemeArtwork from '../ThemeArtwork';
import KobraScope from '../approved-ui-runtime';
import { Button } from '../approved-ui-runtime';
import { Tooltip, TooltipTrigger, TooltipContent } from '../approved-ui-runtime';
import { fieldNotesData } from './fieldNotesData';
import './field-notes.css';

export default function FieldNotes({
  sessions,
  onProgress,
}: {
  sessions: StudySessionRecord[];
  onProgress: () => void;
}) {
  const week = fieldNotesData(sessions);
  const max = Math.max(1, ...week.days.map((day) => day.seconds));
  return (
    <KobraScope sound={false} className="field-notes-scope">
      <aside className="field-notes nsu-paper-card" aria-label="Your week so far">
        <p className="fn-eyebrow">Your week so far</p>
        <div className="fn-heading">
          <div>
            <h2>{week.sessions ? 'Making time.' : 'A fresh start.'}</h2>
            <div
              className="fn-time"
              aria-label={`${Math.floor(week.minutes / 60)} hours ${week.minutes % 60} minutes`}
            >
              <strong>
                {Math.floor(week.minutes / 60)}
                <small>h</small>
              </strong>
              <strong>
                {week.minutes % 60}
                <small>m</small>
              </strong>
            </div>
            <p>
              {week.sessions
                ? `${week.sessions} session${week.sessions === 1 ? '' : 's'} of focused study.`
                : 'Your record grows as you go.'}
            </p>
          </div>
          <ThemeArtwork
            src="/assets/star-crew/companions/thinker.png"
            alt=""
            width={130}
            height={130}
          />
        </div>
        <div className="fn-rhythm" aria-label="Study days this week">
          {week.days.map((day, index) => {
            const detail = `${day.label}: ${day.future ? 'coming up' : `${day.minutes} minutes across ${day.sessions} session${day.sessions === 1 ? '' : 's'}`}`;
            return (
              <Tooltip key={day.key}>
                <TooltipTrigger
                  render={<button type="button" className="fn-day" aria-label={detail} />}
                >
                  <span className="fn-bar-space">
                    <motion.span
                      className="fn-bar"
                      style={{ height: `${(day.seconds / max) * 100}%` }}
                      initial={{ scaleY: 0, opacity: 0 }}
                      animate={{ scaleY: 1, opacity: 1 }}
                      transition={{
                        duration: 0.65,
                        delay: index * 0.045,
                        ease: [0.23, 1, 0.32, 1],
                      }}
                    />
                  </span>
                  <span>{day.label}</span>
                </TooltipTrigger>
                <TooltipContent>{detail}</TooltipContent>
              </Tooltip>
            );
          })}
        </div>
        <div className="fn-facts">
          <span>
            <strong>{week.activeDays}</strong> active {week.activeDays === 1 ? 'day' : 'days'}
          </span>
          <span>
            <strong>{week.streak}</strong>-day study streak
          </span>
        </div>
        <Button variant="ghost" className="fn-progress" onClick={onProgress}>
          Your progress <ArrowUpRight />
        </Button>
      </aside>
    </KobraScope>
  );
}
