import DeviceActivity

/// Runs outside the web view, including while NextStepUni is suspended.
/// iOS delivers interval callbacks when the device is in use.
final class StudyFocusMonitor: DeviceActivityMonitor {
    override func intervalDidEnd(for activity: DeviceActivityName) {
        super.intervalDidEnd(for: activity)
        StudyFocusStore.intervalEnded(activity)
    }

    override func intervalDidStart(for activity: DeviceActivityName) {
        super.intervalDidStart(for: activity)
        // A delayed start callback must never reapply a shield after the deadline.
        StudyFocusStore.intervalEnded(activity)
    }
}
