//
//  StudyTimerAttributes.swift
//
//  The study timer's Live Activity (Lock Screen and Dynamic Island), shared by
//  the app, which starts and updates it (StudyLiveActivityPlugin.swift), and
//  the StudyTimerWidget extension, which draws it. Compiled into BOTH targets.
//
//  Everything that changes lives in ContentState, so one activity can follow a
//  session through pause, resume and "keep going" without being replaced.
//
//  SPDX-License-Identifier: Apache-2.0
//

import Foundation
#if canImport(ActivityKit)
import ActivityKit

@available(iOS 16.1, *)
public struct StudyTimerAttributes: ActivityAttributes {
    public typealias ContentState = State

    public enum Phase: String, Codable, Hashable {
        case running
        case paused
        case done
    }

    public struct State: Codable, Hashable {
        /// "Biology"
        public var subject: String
        /// "25 min · Practice", "Open-ended · Revision"
        public var detail: String
        public var phase: Phase
        /// False for an open-ended session, which counts up.
        public var countsDown: Bool
        /// Wall-clock start, shifted forward by paused time.
        public var startedAt: Date
        /// End of a running countdown.
        public var endsAt: Date?
        /// While paused: seconds left (countdown) or studied (count-up).
        public var pausedSeconds: Int
        /// The countdown's full length or the open-ended session's safety cap.
        public var totalSeconds: Int
        /// "Time’s up" or "Ready to log".
        public var doneLabel: String

        /// One deadline for the system-drawn clock and ActivityKit's stale state.
        /// The fallback supports an activity created by an older client which
        /// sent zero for an open-ended session's four-hour cap.
        public var timerEndsAt: Date? {
            guard phase == .running else { return nil }
            if countsDown { return endsAt }
            return startedAt.addingTimeInterval(TimeInterval(totalSeconds > 0 ? totalSeconds : 4 * 3600))
        }

        public var completionLabel: String {
            phase == .done ? doneLabel : (countsDown ? "Time’s up" : "Ready to log")
        }

        public init(subject: String, detail: String, phase: Phase, countsDown: Bool, startedAt: Date,
                    endsAt: Date?, pausedSeconds: Int, totalSeconds: Int, doneLabel: String) {
            self.subject = subject
            self.detail = detail
            self.phase = phase
            self.countsDown = countsDown
            self.startedAt = startedAt
            self.endsAt = endsAt
            self.pausedSeconds = pausedSeconds
            self.totalSeconds = totalSeconds
            self.doneLabel = doneLabel
        }
    }

    public init() {}
}
#endif
