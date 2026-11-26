import React, { useEffect, useState, type Ref } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  type CarouselApi,
} from '../approved-ui-runtime';
import SubjectAvatar from '../SubjectAvatar';
import ThemeArtwork from '../ThemeArtwork';
import { getSubjectStarCrew } from '../../data/subjectStarCrew';
import { Button, Glyph } from '../ui/Button';
import { ChoiceTile, SelectionMark, useRovingRadios } from '../ui/Choice';

/** A subject's Star Crew character, bare on the page: no tile behind it. */
export function StudySubjectArtwork({ subject, size = 165 }: { subject: string; size?: number }) {
  const artwork = getSubjectStarCrew(subject);
  return artwork && artwork.frame.tile === undefined ? (
    <ThemeArtwork src={artwork.src} alt="" className="ks-subject-art" width={size} height={size} transparentBackground />
  ) : (
    <SubjectAvatar subject={subject} className="ks-subject-art" bare />
  );
}

/** The subject carousel (today's, kept), and the names under it: tapping a
 *  name moves the carousel to it. A swipe still picks the subject it lands on. */
export default function StudySubjectPicker({
  subjects,
  selected,
  onSelect,
  namesRef,
}: {
  subjects: string[];
  selected: string;
  onSelect: (subject: string) => void;
  /** The names under the carousel: where Start session takes a student who has not chosen yet. */
  namesRef?: Ref<HTMLDivElement>;
}) {
  const [api, setApi] = useState<CarouselApi>();
  const [options] = useState(() => ({
    align: 'center' as const,
    loop: subjects.length > 1,
    startIndex: Math.max(0, subjects.indexOf(selected)),
  }));
  useEffect(() => {
    if (!api) return;
    const sync = () => {
      const subject = subjects[api.selectedScrollSnap()];
      if (subject && subject !== selected) onSelect(subject);
    };
    api.on('select', sync);
    return () => {
      api.off('select', sync);
    };
  }, [api, subjects, selected, onSelect]);
  useEffect(() => {
    const index = subjects.indexOf(selected);
    if (api && index >= 0 && api.selectedScrollSnap() !== index) api.scrollTo(index);
  }, [api, subjects, selected]);
  const choose = (subject: string) => {
    onSelect(subject);
    api?.scrollTo(subjects.indexOf(subject));
  };
  const roving = useRovingRadios(subjects.length, subjects.indexOf(selected), index => choose(subjects[index]));
  return (
    <div className="ks-subject-picker sset-picker">
      <Carousel opts={options} setApi={setApi} className="ks-carousel" aria-label="Your subjects">
        <CarouselContent>
          {subjects.map((subject) => (
            <CarouselItem key={subject} className="ks-carousel-item">
              <button
                type="button"
                className="sset-subj"
                aria-label={`Study ${subject}`}
                aria-pressed={selected === subject}
                onClick={() => choose(subject)}
              >
                <SelectionMark on={selected === subject} />
                <StudySubjectArtwork subject={subject} size={140} />
                <strong>{subject}</strong>
                <span>{selected === subject ? 'Your subject' : 'Tap to choose'}</span>
              </button>
            </CarouselItem>
          ))}
        </CarouselContent>
      </Carousel>
      <div className="sset-carnav">
        <Button className="sset-arrow" aria-label="Previous subject" onClick={() => api?.scrollPrev()}><Glyph icon={ChevronLeft} size={20} /></Button>
        <p aria-live="polite" className={selected ? undefined : 'sset-carname-empty'}>{selected || 'Choose your subject'}</p>
        <Button className="sset-arrow" aria-label="Next subject" onClick={() => api?.scrollNext()}><Glyph icon={ChevronRight} size={20} /></Button>
      </div>
      <div ref={namesRef} role="radiogroup" aria-label="Your subject" className="sset-step sset-names" data-study-step="subject">
        {subjects.map((subject, index) => (
          <ChoiceTile
            key={subject}
            ref={element => { roving.refs.current[index] = element; }}
            chosen={selected === subject}
            label={subject}
            tabIndex={roving.tabIndexOf(index)}
            onKeyDown={event => roving.onKeyDown(event, index)}
            onClick={() => choose(subject)}
          />
        ))}
      </div>
    </div>
  );
}
