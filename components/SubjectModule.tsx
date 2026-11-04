/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { Compass, Target, TrendingUp, AlertTriangle, BrainCircuit, Rocket } from 'lucide-react';
import { type ModuleProgress, type ModuleTheme } from '../types';
import { ReadingSection, MicroCommitment } from './ModuleShared';
import { ModuleLayout } from './ModuleLayout';
import { renderSubjectText as renderParagraph } from './SubjectText';
import {
  amberTheme, blueTheme, roseTheme, emeraldTheme, orangeTheme,
  tealTheme, cyanTheme, slateTheme, skyTheme, redTheme,
  purpleTheme, fuchsiaTheme, indigoTheme, violetTheme,
  pinkTheme, limeTheme, yellowTheme, grayTheme
} from '../moduleThemes';
import { SUBJECT_MODULE_CONTENT } from '../subjectModuleData';

const SECTION_ICONS = [Compass, Target, TrendingUp, AlertTriangle, BrainCircuit, Rocket];

const THEME_MAP: Record<string, ModuleTheme> = {
  amber: amberTheme, blue: blueTheme, rose: roseTheme, emerald: emeraldTheme,
  orange: orangeTheme, teal: tealTheme, cyan: cyanTheme, slate: slateTheme,
  sky: skyTheme, red: redTheme, purple: purpleTheme, fuchsia: fuchsiaTheme,
  indigo: indigoTheme, violet: violetTheme, pink: pinkTheme, lime: limeTheme,
  yellow: yellowTheme, gray: grayTheme,
};

interface SubjectModuleProps {
  subjectId: string;
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}

const SubjectModule: React.FC<SubjectModuleProps> = ({ subjectId, onBack, progress, onProgressUpdate }) => {
  const content = SUBJECT_MODULE_CONTENT[subjectId];

  if (!content) {
    return <div className="p-8 text-center text-red-500">Module content not found for: {subjectId}</div>;
  }

  const theme = THEME_MAP[content.themeName] || grayTheme;

  const sections = content.sections.map((section, idx) => ({
    id: `section-${idx}`,
    title: section.title,
    eyebrow: section.eyebrow,
    icon: SECTION_ICONS[idx] || Compass,
  }));

  return (
    <ModuleLayout
      moduleNumber={content.moduleNumber}
      moduleTitle={content.moduleTitle}
      moduleSubtitle={content.moduleSubtitle}
      moduleDescription={content.moduleDescription}
      theme={theme}
      sections={sections}
      onBack={onBack}
      progress={progress}
      onProgressUpdate={onProgressUpdate}
      references={content.references}
      finishButtonText={content.finishButtonText}
    >
      {(activeSection) => (
        <>
          {content.sections.map((section, idx) =>
            activeSection === idx && (
              <ReadingSection
                key={idx}
                title={section.title}
                eyebrow={section.eyebrow}
                icon={SECTION_ICONS[idx] || Compass}
                theme={theme}
              >
                {section.paragraphs.map((para, pIdx) => (
                  <p key={pIdx}>{renderParagraph(para, section.highlights, theme)}</p>
                ))}
                {section.bullets && (
                  <ul className="list-disc list-inside space-y-2 my-4">
                    {section.bullets.map((bullet, bIdx) => (
                      <li key={bIdx} className="text-zinc-600 dark:text-zinc-300">{renderParagraph(bullet, section.highlights, theme)}</li>
                    ))}
                  </ul>
                )}
                {section.commitmentText && (
                  <MicroCommitment theme={theme}>
                    <p>{renderParagraph(section.commitmentText, section.highlights, theme)}</p>
                  </MicroCommitment>
                )}
              </ReadingSection>
            )
          )}
        </>
      )}
    </ModuleLayout>
  );
};

/**
 * Factory function for creating lazy-loadable subject module components.
 * Used by moduleRegistry.ts to create entries for each subject.
 */
export function createSubjectModuleComponent(subjectId: string): React.FC<{
  onBack: () => void;
  progress: ModuleProgress;
  onProgressUpdate: (progress: ModuleProgress) => void;
}> {
  const WrappedComponent: React.FC<{
    onBack: () => void;
    progress: ModuleProgress;
    onProgressUpdate: (progress: ModuleProgress) => void;
  }> = (props) => {
    return <SubjectModule subjectId={subjectId} {...props} />;
  };
  return WrappedComponent;
}

export default SubjectModule;
