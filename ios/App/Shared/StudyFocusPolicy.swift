import Foundation

/// Foundation-only rules, also exercised by scripts/ios/test-study-focus.swift.
enum StudyFocusPolicy {
    static let activityPrefix = "nextstepuni.study."
    static let maximumRemaining: TimeInterval = 4 * 60 * 60

    static func validDeadline(_ deadline: Date?, now: Date) -> Date? {
        guard let deadline, deadline > now,
              deadline.timeIntervalSince(now) <= maximumRemaining else { return nil }
        return deadline
    }

    /// DeviceActivity requires a >=15 minute interval, and supports starting an
    /// already-ongoing interval. Short sessions keep their real end time; only
    /// the monitoring window begins earlier. No usage events are collected.
    static func monitoringWindow(deadline: Date, now: Date) -> DateInterval {
        let end = Date(timeIntervalSince1970: ceil(deadline.timeIntervalSince1970))
        let start = min(now, end.addingTimeInterval(-16 * 60))
        return DateInterval(start: start, end: end)
    }

    static func shouldRelease(activity: String, currentActivity: String?, deadline: Date?, now: Date) -> Bool {
        guard activity == currentActivity, let deadline else { return false }
        return now >= deadline
    }
}
