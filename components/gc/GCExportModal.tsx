/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { createPortal } from 'react-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { MotionDiv } from '../Motion';
import { X, FileDown, FileText, ChevronDown } from 'lucide-react';
import { GCStudentFullData } from './gcTypes';
import { CourseData } from '../Library';
import {
  generateStudentProgressCSV,
  generateAttendanceCSV,
  generateSubjectHealthCSV,
  generateStudentDetailCSV,
  downloadCSV,
} from '../../utils/exportCsv';
import { generateReport } from '../../utils/exportPdf';

interface GCExportModalProps {
  isOpen: boolean;
  onClose: () => void;
  studentData: GCStudentFullData[];
  allCourses: CourseData[];
  school: string;
}

const ACCENT = '#2A7D6F';

const GCExportModal: React.FC<GCExportModalProps> = ({ isOpen, onClose, studentData, allCourses, school }) => {
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

  const handleExportPDF = () => {
    generateReport({
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

  return createPortal(
    <AnimatePresence>
      {isOpen && (
        <MotionDiv
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          className="fixed inset-0 z-[200] flex items-center justify-center bg-black/50 backdrop-blur-sm p-4"
          onClick={onClose}
        >
          <MotionDiv
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            transition={{ duration: 0.2 }}
            className="bg-white dark:bg-zinc-900 rounded-2xl shadow-xl w-full max-w-lg overflow-hidden"
            onClick={(e: React.MouseEvent) => e.stopPropagation()}
          >
            {/* Header */}
            <div className="flex items-center justify-between px-6 py-5 border-b border-zinc-100 dark:border-zinc-800">
              <div className="flex items-center gap-3">
                <div
                  className="w-9 h-9 rounded-xl flex items-center justify-center dark:!bg-[rgba(77,184,164,0.1)]"
                  style={{ backgroundColor: 'rgba(42,125,111,0.1)' }}
                >
                  <FileDown size={18} style={{ color: ACCENT }} className="dark:!text-[#4DB8A4]" />
                </div>
                <h2 className="text-base font-semibold text-zinc-900 dark:text-white">Export Data</h2>
              </div>
              <button
                onClick={onClose}
                className="w-8 h-8 flex items-center justify-center rounded-lg text-zinc-400 hover:text-zinc-600 hover:bg-zinc-100 dark:hover:text-zinc-300 dark:hover:bg-zinc-800 transition-colors"
              >
                <X size={16} />
              </button>
            </div>

            {/* Body */}
            <div className="px-6 py-5 space-y-3">
              {/* Toggle options */}
              <ToggleOption
                label="Student Progress Summary"
                checked={includeProgress}
                onChange={setIncludeProgress}
              />
              <ToggleOption
                label="Attendance Patterns"
                checked={includeAttendance}
                onChange={setIncludeAttendance}
              />
              <ToggleOption
                label="Subject Health"
                checked={includeSubjectHealth}
                onChange={setIncludeSubjectHealth}
              />
              <ToggleOption
                label="Individual Student Detail"
                checked={includeIndividual}
                onChange={setIncludeIndividual}
              />

              {/* Student dropdown — appears when individual is toggled on */}
              {includeIndividual && (
                <div className="ml-1 mt-1">
                  <div className="relative">
                    <select
                      value={selectedStudentUid}
                      onChange={e => setSelectedStudentUid(e.target.value)}
                      className="w-full appearance-none bg-zinc-50 dark:bg-zinc-800 border border-zinc-200 dark:border-zinc-700 rounded-xl px-3 py-2.5 pr-8 text-sm text-zinc-800 dark:text-white focus:outline-none focus:border-[rgba(42,125,111,0.5)]"
                    >
                      <option value="">Select a student...</option>
                      {sortedStudents.map(s => (
                        <option key={s.user.uid} value={s.user.uid}>{s.user.name}</option>
                      ))}
                    </select>
                    <ChevronDown size={14} className="absolute right-3 top-1/2 -translate-y-1/2 pointer-events-none text-zinc-400" />
                  </div>
                </div>
              )}

              {/* Preview count */}
              <p className="text-xs text-zinc-400 dark:text-zinc-500 pt-1">
                Exporting data for {studentData.length} student{studentData.length !== 1 ? 's' : ''}
              </p>
            </div>

            {/* Footer */}
            <div className="flex gap-3 px-6 py-4 border-t border-zinc-100 dark:border-zinc-800">
              <button
                onClick={handleExportCSV}
                disabled={!hasSelection}
                className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-semibold text-white disabled:opacity-40 disabled:cursor-not-allowed transition-colors dark:!bg-[#4DB8A4]"
                style={{ backgroundColor: ACCENT }}
              >
                <FileText size={14} />
                Export CSV
              </button>
              <button
                onClick={handleExportPDF}
                disabled={!hasSelection}
                className="flex-1 flex items-center justify-center gap-2 py-2.5 rounded-xl text-sm font-semibold text-white disabled:opacity-40 disabled:cursor-not-allowed transition-colors dark:!bg-[#4DB8A4]"
                style={{ backgroundColor: ACCENT }}
              >
                <FileDown size={14} />
                Export PDF
              </button>
            </div>
          </MotionDiv>
        </MotionDiv>
      )}
    </AnimatePresence>,
    document.body
  );
};

// ─── Toggle pill component ──────────────────────────────────────────────────

function ToggleOption({ label, checked, onChange }: { label: string; checked: boolean; onChange: (v: boolean) => void }) {
  return (
    <button
      type="button"
      onClick={() => onChange(!checked)}
      className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium transition-all ${
        checked
          ? 'bg-[rgba(42,125,111,0.08)] text-zinc-800 dark:bg-[rgba(77,184,164,0.1)] dark:text-white'
          : 'bg-zinc-50 text-zinc-500 dark:bg-zinc-800/50 dark:text-zinc-400'
      }`}
    >
      <div
        className={`w-5 h-5 rounded-md flex items-center justify-center flex-shrink-0 transition-colors ${
          checked
            ? 'dark:!bg-[#4DB8A4]'
            : 'bg-zinc-200 dark:bg-zinc-700'
        }`}
        style={checked ? { backgroundColor: ACCENT } : undefined}
      >
        {checked && (
          <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
            <path d="M2.5 6L5 8.5L9.5 3.5" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        )}
      </div>
      {label}
    </button>
  );
}

export default GCExportModal;
