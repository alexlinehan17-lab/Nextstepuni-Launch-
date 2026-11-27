/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useRef, useState } from 'react';
import { type GCStudentFullData } from './gcTypes';
import { type CourseData } from '../Library';
import {
  generateStudentProgressCSV,
  generateAttendanceCSV,
  generateSubjectHealthCSV,
  generateStudentDetailCSV,
  downloadCSV,
} from '../../utils/exportCsv';
import { generateReport } from '../../utils/exportPdf';
import { Button } from '../ui/Button';
import { ChoiceTile } from '../ui/Choice';
import { Sheet } from '../ui/Sheet';
import { useWide } from './gcView';

interface GCExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  studentData: GCStudentFullData[];
  allCourses: CourseData[];
  school: string;
}

const GCExportModal: React.FC<GCExportModalProps> = ({ isOpen, onClose, studentData, allCourses, school }) => {
  const wide = useWide();
  const choicesRef = useRef<HTMLDivElement>(null);
  const [includeProgress, setIncludeProgress] = useState(true);
  const [includeAttendance, setIncludeAttendance] = useState(true);
  const [includeSubjectHealth, setIncludeSubjectHealth] = useState(true);
  const [includeIndividual, setIncludeIndividual] = useState(false);
  const [selectedStudentUid, setSelectedStudentUid] = useState<string>('');

  const selectedStudent = studentData.find(s => s.user.uid === selectedStudentUid) ?? undefined;
  const sortedStudents = [...studentData].sort((a, b) => a.user.name.localeCompare(b.user.name));

  const handleExportCSV = () => {
    const dateStr = new Date().toISOString().split('T')[0];

    if (includeProgress) {
      downloadCSV(generateStudentProgressCSV(studentData, allCourses), `progress-summary-${dateStr}.csv`);
    }
    if (includeAttendance) {
      downloadCSV(generateAttendanceCSV(studentData), `attendance-${dateStr}.csv`);
    }
    if (includeSubjectHealth) {
      downloadCSV(generateSubjectHealthCSV(studentData), `subject-health-${dateStr}.csv`);
    }
    if (includeIndividual && selectedStudent) {
      const safeName = selectedStudent.user.name.replace(/\s+/g, '-').toLowerCase();
      downloadCSV(generateStudentDetailCSV(selectedStudent, allCourses), `student-${safeName}-${dateStr}.csv`);
    }

    onClose();
  };

  const handleExportPDF = async () => {
    await generateReport({
      school,
      students: studentData,
      allCourses,
      includeProgress,
      includeAttendance,
      includeSubjectHealth,
      individualStudent: includeIndividual ? selectedStudent : undefined,
    });

    onClose();
  };

  const hasSelection = includeProgress || includeAttendance || includeSubjectHealth || (includeIndividual && !!selectedStudent);

  // A sheet from the bottom on a phone (a centred dialog from 640px): the four parts as choices with
  // the ink tick, Export PDF the charcoal button and CSV beside it (board r5-counsellor-dashboard).
  const missing = !hasSelection ? { sentence: 'Choose what to export.', goTo: choicesRef } : undefined;
  return (
    <Sheet
      open={isOpen}
      title="Export data"
      onClose={onClose}
      footer={
        <div className="gc8-pair">
          <Button size="lg" onClick={() => { if (hasSelection) handleExportCSV(); }} aria-disabled={!hasSelection || undefined}>Export CSV</Button>
          <Button kind="main" size="lg" missing={missing} onClick={() => { void handleExportPDF(); }}>Export PDF</Button>
        </div>
      }
    >
      <div className="gc8-sheet-body">
        <div className="gc8-msgs" ref={choicesRef} role="group" aria-label="What to export">
          <ChoiceTile kind="several" chosen={includeProgress} label="Student progress summary" onClick={() => setIncludeProgress(!includeProgress)} />
          <ChoiceTile kind="several" chosen={includeAttendance} label="Attendance patterns" onClick={() => setIncludeAttendance(!includeAttendance)} />
          <ChoiceTile kind="several" chosen={includeSubjectHealth} label="Subject health" onClick={() => setIncludeSubjectHealth(!includeSubjectHealth)} />
          <ChoiceTile kind="several" chosen={includeIndividual} label="Individual student detail" onClick={() => setIncludeIndividual(!includeIndividual)} />
        </div>

        {/* Student picker — appears when individual is toggled on (a form's own picker) */}
        {includeIndividual && (
          <label className="ui-part ui-field">
            <span className="ui-field-label">Student</span>
            <select className="ui-field-input" value={selectedStudentUid} onChange={e => setSelectedStudentUid(e.target.value)}>
              <option value="">Select a student...</option>
              {sortedStudents.map(s => (
                <option key={s.user.uid} value={s.user.uid}>{s.user.name}</option>
              ))}
            </select>
          </label>
        )}

        <p className="gc8-meta">Exporting data for {studentData.length} student{studentData.length !== 1 ? 's' : ''}</p>
        {!wide && (
          <div className="gc8-laptopnote">
            <p className="gc8-label">Best on a laptop</p>
            <p className="gc8-sub">The CSV is a spreadsheet with a column for every figure, easier to read on a bigger screen. Both still export from here.</p>
          </div>
        )}
      </div>
    </Sheet>
  );
};

export default GCExportModal;
