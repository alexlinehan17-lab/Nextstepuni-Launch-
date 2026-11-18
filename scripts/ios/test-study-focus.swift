// Run with the real policy source, no Screen Time mocks:
// swiftc ios/App/Shared/StudyFocusPolicy.swift scripts/ios/test-study-focus.swift -o /tmp/nsu-focus-policy && /tmp/nsu-focus-policy
import Foundation

@main struct StudyFocusPolicyChecks {
    static func main() {
        let now = Date(timeIntervalSince1970: 1_794_312_000)
        for seconds in [1, 5 * 60, 10 * 60, 15 * 60, 25 * 60, 4 * 3600] {
            let deadline = now.addingTimeInterval(Double(seconds))
            let window = StudyFocusPolicy.monitoringWindow(deadline: deadline, now: now)
            precondition(window.duration >= 15 * 60)
            precondition(window.start <= now)
            precondition(window.end == deadline, "Short monitoring windows must not extend study time")
            precondition(StudyFocusPolicy.validDeadline(deadline, now: now) == deadline)
        }
        precondition(StudyFocusPolicy.validDeadline(nil, now: now) == nil)
        precondition(StudyFocusPolicy.validDeadline(now, now: now) == nil)
        precondition(StudyFocusPolicy.validDeadline(now.addingTimeInterval(-1), now: now) == nil)
        precondition(StudyFocusPolicy.validDeadline(now.addingTimeInterval(14401), now: now) == nil)
        precondition(!StudyFocusPolicy.shouldRelease(activity: "old", currentActivity: "new", deadline: now, now: now))
        precondition(!StudyFocusPolicy.shouldRelease(activity: "new", currentActivity: "new", deadline: now.addingTimeInterval(1), now: now))
        precondition(StudyFocusPolicy.shouldRelease(activity: "new", currentActivity: "new", deadline: now, now: now))
        precondition(StudyFocusPolicy.shouldRelease(activity: "new", currentActivity: "new", deadline: now, now: now.addingTimeInterval(7200)))
        precondition(!StudyFocusPolicy.shouldRelease(activity: "new", currentActivity: nil, deadline: nil, now: now))
        print("Study focus: 33 native deadline and stale-callback assertions passed")
    }
}
