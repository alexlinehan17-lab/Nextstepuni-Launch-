import React, { useEffect, useState } from 'react';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  CarouselPrevious,
  CarouselNext,
  type CarouselApi,
} from '../approved-ui-runtime';
import { Card, CardContent } from '../approved-ui-runtime';
import { RadioGroup, RadioGroupItem } from '../approved-ui-runtime';
import SubjectAvatar from '../SubjectAvatar';
import ThemeArtwork from '../ThemeArtwork';
import { getSubjectStarCrew } from '../../data/subjectStarCrew';

export function StudySubjectArtwork({ subject, size = 165 }: { subject: string; size?: number }) {
  const artwork = getSubjectStarCrew(subject);
  return artwork && artwork.frame.tile === undefined ? (
    <ThemeArtwork src={artwork.src} alt="" className="ks-subject-art" width={size} height={size} />
  ) : (
    <SubjectAvatar subject={subject} className="ks-subject-art" />
  );
}

export default function StudySubjectPicker({
  subjects,
  selected,
  onSelect,
}: {
  subjects: string[];
  selected: string;
  onSelect: (subject: string) => void;
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
  return (
    <div className="ks-subject-picker">
      <Carousel opts={options} setApi={setApi} className="ks-carousel" aria-label="Your subjects">
        <CarouselContent>
          {subjects.map((subject) => (
            <CarouselItem key={subject} className="ks-carousel-item">
              <Card className="ks-subject-card nsu-paper-card" data-selected={selected === subject}>
                <CardContent>
                  <button
                    type="button"
                    aria-label={`Study ${subject}`}
                    aria-pressed={selected === subject}
                    onClick={() => choose(subject)}
                  >
                    <StudySubjectArtwork subject={subject} />
                    <strong>{subject}</strong>
                    <span>{selected === subject ? 'Your subject' : 'Choose subject'}</span>
                  </button>
                </CardContent>
              </Card>
            </CarouselItem>
          ))}
        </CarouselContent>
        <div className="ks-carousel-controls">
          <CarouselPrevious aria-label="Previous subject" />
          <p aria-live="polite">{selected || 'Choose your subject'}</p>
          <CarouselNext aria-label="Next subject" />
        </div>
      </Carousel>
      <RadioGroup
        value={selected}
        onValueChange={(value) => choose(String(value))}
        aria-label="Your subject"
        className="ks-subject-choices"
      >
        {subjects.map((subject) => (
          <label className="ks-choice" data-selected={selected === subject} key={subject}>
            <RadioGroupItem value={subject} />
            <span>{subject}</span>
          </label>
        ))}
      </RadioGroup>
    </div>
  );
}
