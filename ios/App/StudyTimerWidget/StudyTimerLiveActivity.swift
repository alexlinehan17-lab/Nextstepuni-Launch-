//
//  StudyTimerLiveActivity.swift
//
//  How the running study timer looks on the Lock Screen and in the Dynamic
//  Island. The countdown is drawn by the system from two dates
//  (Text(timerInterval:)), so it keeps time with the app asleep.
//
//  Identity: white paper and ink with the brand orange (dark mode: ink paper),
//  the app icon's figure stepping onto the star, serif subject. No emojis.
//
//  SPDX-License-Identifier: Apache-2.0
//

import SwiftUI
import WidgetKit
#if canImport(ActivityKit)
import ActivityKit

/// Fixed colours, chosen from the view's own colour scheme. Asset-catalog
/// colours were resolved in two different appearances on the iOS 26 Lock
/// Screen (background light, text dark), which left near-white text on a
/// white card; one static palette keeps every part in step.
private struct Palette {
    let paper: Color
    let ink: Color
    let muted: Color
    let accent: Color
    let success: Color

    static let light = Palette(paper: .rgb(0xFFFFFF), ink: .rgb(0x1A1A1A), muted: .rgb(0x6F6963),
                               accent: .rgb(0xF26B1F), success: .rgb(0x3A8D5F))
    static let dark = Palette(paper: .rgb(0x1C1C1B), ink: .rgb(0xF7F5F1), muted: .rgb(0xB7B2AB),
                              accent: .rgb(0xFF862C), success: .rgb(0x5DB884))

    static func `for`(_ scheme: ColorScheme) -> Palette { scheme == .dark ? dark : light }

    /// The Dynamic Island is always black.
    static let islandAccent = Color.rgb(0xFF862C)
    static let islandMuted = Color.white.opacity(0.62)
}

private extension Color {
    static func rgb(_ hex: UInt32) -> Color {
        Color(red: Double((hex >> 16) & 0xFF) / 255, green: Double((hex >> 8) & 0xFF) / 255, blue: Double(hex & 0xFF) / 255)
    }
}

/// Opens the study room (handled by StudyLiveActivityPlugin).
private let studyRoomURL = URL(string: "nextstepuni://study")

@available(iOS 16.1, *)
struct StudyTimerLiveActivity: Widget {
    var body: some WidgetConfiguration {
        ActivityConfiguration(for: StudyTimerAttributes.self) { context in
            LockScreenView(state: context.state, stale: context.isStaleCompat)
                .widgetURL(studyRoomURL)
        } dynamicIsland: { context in
            let state = context.state
            let stale = context.isStaleCompat
            return DynamicIsland {
                DynamicIslandExpandedRegion(.leading) {
                    AppMark(size: 40)
                        .padding(.leading, 4)
                }
                DynamicIslandExpandedRegion(.trailing) {
                    VStack(alignment: .trailing, spacing: 1) {
                        if state.phase == .done || stale {
                            Text(state.phase == .done ? state.doneLabel : "Time’s up")
                                .font(.system(size: 20, weight: .semibold, design: .serif))
                                .foregroundColor(.white)
                                .minimumScaleFactor(0.7)
                        } else {
                            TimerText(state: state)
                                .font(.system(size: TimerText.long(state) ? 26 : 30, weight: .medium).monospacedDigit())
                                .foregroundColor(state.phase == .running ? .white : Palette.islandMuted)
                                .multilineTextAlignment(.trailing)
                                .frame(width: TimerText.long(state) ? 112 : 92, alignment: .trailing)
                                .minimumScaleFactor(0.8)
                            Text(TimerText.caption(state))
                                .font(.system(size: 10, weight: .semibold))
                                .tracking(0.6)
                                .foregroundColor(state.phase == .paused ? Palette.islandAccent : Palette.islandMuted)
                        }
                    }
                    .lineLimit(1)
                    .padding(.trailing, 4)
                }
                DynamicIslandExpandedRegion(.center) {
                    VStack(alignment: .leading, spacing: 2) {
                        Text(state.subject)
                            .font(.system(size: 17, weight: .semibold, design: .serif))
                            .foregroundColor(.white)
                            .minimumScaleFactor(0.75)
                        Text(state.phase == .done || stale ? "Tap to log your session" : state.detail)
                            .font(.system(size: 12))
                            .foregroundColor(Palette.islandMuted)
                            .minimumScaleFactor(0.85)
                    }
                    .lineLimit(1)
                    .frame(maxWidth: .infinity, alignment: .leading)
                }
                DynamicIslandExpandedRegion(.bottom) {
                    if state.countsDown {
                        SessionBar(state: state, stale: stale, fill: Palette.islandAccent, done: Palette.dark.success)
                            .padding(.horizontal, 4)
                            .padding(.top, 6)
                    }
                }
            } compactLeading: {
                AppMark(size: 22)
            } compactTrailing: {
                if state.phase == .done || stale {
                    // Finished reads as complete (success green), not brand orange.
                    Image(systemName: "checkmark")
                        .font(.system(size: 14, weight: .bold))
                        .foregroundColor(Palette.dark.success)
                        .accessibilityLabel(state.phase == .done ? state.doneLabel : "Time’s up")
                } else {
                    TimerText(state: state)
                        .font(.system(size: 15, weight: .semibold).monospacedDigit())
                        .foregroundColor(state.phase == .paused ? Palette.islandMuted : Palette.islandAccent)
                        .multilineTextAlignment(.trailing)
                        .frame(width: state.countsDown ? 50 : 62, alignment: .trailing)
                }
            } minimal: {
                MinimalRing(state: state, stale: stale)
            }
            .widgetURL(studyRoomURL)
            .keylineTint(Palette.islandAccent)
        }
    }
}

// MARK: - Lock Screen

@available(iOS 16.1, *)
private struct LockScreenView: View {
    let state: StudyTimerAttributes.ContentState
    let stale: Bool
    @Environment(\.colorScheme) private var colorScheme

    private var finished: Bool { state.phase == .done || stale }

    var body: some View {
        let palette = Palette.for(colorScheme)
        VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .center, spacing: 12) {
                AppMark(size: 44)
                VStack(alignment: .leading, spacing: 2) {
                    Text("STUDY ROOM")
                        .font(.system(size: 10, weight: .bold))
                        .tracking(1.2)
                        .foregroundColor(palette.muted)
                    Text(state.subject)
                        .font(.system(size: 21, weight: .semibold, design: .serif))
                        .foregroundColor(palette.ink)
                        .minimumScaleFactor(0.75)
                    Text(finished ? "Tap to log your session" : state.detail)
                        .font(.system(size: 13))
                        .foregroundColor(palette.muted)
                        .minimumScaleFactor(0.85)
                }
                .lineLimit(1)
                .layoutPriority(1)
                Spacer(minLength: 6)
                VStack(alignment: .trailing, spacing: 1) {
                    if finished {
                        Text(state.phase == .done ? state.doneLabel : "Time’s up")
                            .font(.system(size: 24, weight: .semibold, design: .serif))
                            .foregroundColor(palette.ink)
                    } else {
                        TimerText(state: state)
                            .font(.system(size: TimerText.long(state) ? 30 : 36, weight: .medium).monospacedDigit())
                            .foregroundColor(state.phase == .paused ? palette.muted : palette.ink)
                            .multilineTextAlignment(.trailing)
                            // The system's timer text is as wide as it is allowed to be.
                            .frame(width: TimerText.long(state) ? 128 : 112, alignment: .trailing)
                            .minimumScaleFactor(0.8)
                        Text(TimerText.caption(state))
                            .font(.system(size: 11, weight: .semibold))
                            .tracking(0.6)
                            .foregroundColor(state.phase == .paused ? palette.accent : palette.muted)
                    }
                }
                .lineLimit(1)
            }
            // Open-ended sessions have no end to measure against (as in the app).
            if state.countsDown {
                SessionBar(state: state, stale: stale, fill: palette.accent, done: palette.success)
            }
        }
        .padding(.horizontal, 18)
        .padding(.vertical, 16)
        .activityBackgroundTint(palette.paper)
        .activitySystemActionForegroundColor(palette.ink)
    }
}

// MARK: - Pieces

/// The figure stepping onto the star, from the app icon.
private struct AppMark: View {
    let size: CGFloat
    var body: some View {
        Image("AppMark")
            .resizable()
            .interpolation(.high)
            .aspectRatio(contentMode: .fit)
            .frame(width: size, height: size)
            .clipShape(RoundedRectangle(cornerRadius: size * 0.24, style: .continuous))
            .accessibilityHidden(true)
    }
}

/// Counts down to the end, counts up for an open-ended session, and holds
/// still when paused. (Finished states show words instead; see callers.)
@available(iOS 16.1, *)
private struct TimerText: View {
    let state: StudyTimerAttributes.ContentState

    /// An hour or more can show (h:mm:ss): open-ended, or a long countdown.
    static func long(_ state: StudyTimerAttributes.ContentState) -> Bool {
        !state.countsDown || state.totalSeconds >= 3600
    }

    static func caption(_ state: StudyTimerAttributes.ContentState) -> String {
        if state.phase == .paused { return "PAUSED" }
        return state.countsDown ? "REMAINING" : "STUDIED"
    }

    var body: some View {
        if state.phase != .running {
            Text(Clock.format(state.pausedSeconds))
        } else if state.countsDown {
            if let end = state.endsAt, state.startedAt < end {
                // Drawn by the system from the dates: stops at 0:00 on its own.
                Text(timerInterval: state.startedAt...end, countsDown: true)
            } else {
                Text("0:00")
            }
        } else {
            Text(timerInterval: state.startedAt...state.startedAt.addingTimeInterval(8 * 3600), countsDown: false)
        }
    }
}

/// Elapsed share of the countdown, live while running (countdowns only).
@available(iOS 16.1, *)
private struct SessionBar: View {
    let state: StudyTimerAttributes.ContentState
    let stale: Bool
    let fill: Color
    let done: Color

    var body: some View {
        Group {
            if state.phase == .running, !stale, state.countsDown, let end = state.endsAt, state.startedAt < end, end > Date() {
                ProgressView(timerInterval: state.startedAt...end, countsDown: false, label: { EmptyView() }, currentValueLabel: { EmptyView() })
                    .progressViewStyle(.linear)
                    .tint(fill)
            } else {
                ProgressView(value: staticProgress)
                    .progressViewStyle(.linear)
                    .tint(state.phase == .done || stale ? done : fill)
            }
        }
        .accessibilityHidden(true)
    }

    private var staticProgress: Double {
        if state.phase == .done || stale { return state.countsDown ? 1 : 0 }
        guard state.countsDown, state.totalSeconds > 0 else { return 0 }
        return min(1, max(0, Double(state.totalSeconds - state.pausedSeconds) / Double(state.totalSeconds)))
    }
}

/// The smallest Dynamic Island: a ring that fills as the session goes.
@available(iOS 16.1, *)
private struct MinimalRing: View {
    let state: StudyTimerAttributes.ContentState
    let stale: Bool

    var body: some View {
        if state.phase == .running, !stale, state.countsDown, let end = state.endsAt, state.startedAt < end, end > Date() {
            ProgressView(timerInterval: state.startedAt...end, countsDown: false, label: { EmptyView() }, currentValueLabel: { EmptyView() })
                .progressViewStyle(.circular)
                .tint(Palette.islandAccent)
        } else {
            AppMark(size: 22)
        }
    }
}

private enum Clock {
    static func format(_ seconds: Int) -> String {
        let whole = max(0, seconds)
        let hours = whole / 3600, minutes = (whole % 3600) / 60, secs = whole % 60
        return hours > 0
            ? String(format: "%d:%02d:%02d", hours, minutes, secs)
            : String(format: "%d:%02d", minutes, secs)
    }
}

@available(iOS 16.1, *)
private extension ActivityViewContext {
    /// iOS 16.2 marks a countdown stale once it has ended.
    var isStaleCompat: Bool {
        if #available(iOS 16.2, *) { return isStale }
        return false
    }
}
#endif
