import Foundation
import Darwin
import FamilyControls
import ManagedSettings
import DeviceActivity

@available(iOS 16.0, *)
struct StudyFocusLease: Codable {
    let activity: String
    let deadline: Date
}

@available(iOS 16.0, *)
struct StudyFocusModel: Codable {
    var owner: String? = nil
    var enabled = false
    // Expand categories into the specific applications chosen in Apple's picker.
    var selection = FamilyActivitySelection(includeEntireCategory: true)
    var lease: StudyFocusLease? = nil
}

@available(iOS 16.0, *)
enum StudyFocusStore {
    static let group = "group.com.nextstepuni.app.studyfocus"
    static let settings = ManagedSettingsStore(named: ManagedSettingsStore.Name("nextstepuni.study"))
    static let center = DeviceActivityCenter()
    static var available: Bool { FileManager.default.containerURL(forSecurityApplicationGroupIdentifier: group) != nil }

    enum Failure: Error { case unavailable, locked, wrongOwner, noSelection, unauthorized }

    private static func persist(_ model: StudyFocusModel) throws {
        guard let directory = FileManager.default.containerURL(forSecurityApplicationGroupIdentifier: group) else { throw Failure.unavailable }
        var file = directory.appendingPathComponent("focus.json")
        try JSONEncoder().encode(model).write(to: file, options: [.atomic, .completeFileProtectionUntilFirstUserAuthentication])
        var values = URLResourceValues()
        values.isExcludedFromBackup = true
        try file.setResourceValues(values)
    }

    /// App and extension share one short file lock. An old interval callback
    /// cannot clear a newer session between checking its generation and writing.
    static func transaction<T>(_ body: (inout StudyFocusModel) throws -> T) throws -> T {
        guard let directory = FileManager.default.containerURL(forSecurityApplicationGroupIdentifier: group) else {
            settings.clearAllSettings()
            throw Failure.unavailable
        }
        let lock = open(directory.appendingPathComponent("focus.lock").path, O_CREAT | O_RDWR, S_IRUSR | S_IWUSR)
        guard lock >= 0 else { settings.clearAllSettings(); throw Failure.locked }
        defer { close(lock) }
        guard flock(lock, LOCK_EX) == 0 else { settings.clearAllSettings(); throw Failure.locked }
        defer { flock(lock, LOCK_UN) }
        let file = directory.appendingPathComponent("focus.json")
        var model: StudyFocusModel
        if FileManager.default.fileExists(atPath: file.path) {
            do { model = try JSONDecoder().decode(StudyFocusModel.self, from: Data(contentsOf: file)) }
            catch {
                settings.clearAllSettings()
                stopOwnedMonitoring()
                model = StudyFocusModel()
            }
        } else { model = StudyFocusModel() }
        do {
            let result = try body(&model)
            try persist(model)
            return result
        } catch Failure.wrongOwner {
            // A late request from another signed-in scope must not disturb the
            // current student's lease. Ownership checks happen before mutations.
            throw Failure.wrongOwner
        } catch {
            // A failure must not leave a shield without a durable release lease.
            settings.clearAllSettings()
            stopOwnedMonitoring()
            model.enabled = false
            model.lease = nil
            try? persist(model)
            throw error
        }
    }

    static func stopOwnedMonitoring() {
        let names = center.activities.filter { $0.rawValue.hasPrefix(StudyFocusPolicy.activityPrefix) }
        if !names.isEmpty { center.stopMonitoring(names) }
    }

    static func release(_ model: inout StudyFocusModel) {
        settings.clearAllSettings()
        model.lease = nil
        stopOwnedMonitoring()
    }

    static func reconcile(_ model: inout StudyFocusModel, now: Date = Date()) {
        guard AuthorizationCenter.shared.authorizationStatus == .approved else {
            release(&model)
            model.enabled = false
            model.selection = FamilyActivitySelection(includeEntireCategory: true)
            return
        }
        if !model.enabled || model.lease.map({ $0.deadline <= now }) == true { release(&model) }
    }

    static func selectionCount(_ model: StudyFocusModel) -> Int {
        model.selection.applicationTokens.count + model.selection.webDomainTokens.count
    }

    static func status(_ model: StudyFocusModel) -> [String: Any] {
        ["available": available, "authorized": AuthorizationCenter.shared.authorizationStatus == .approved,
         "enabled": model.enabled, "active": model.lease != nil, "selectionCount": selectionCount(model)]
    }

    static func sync(owner: String?, deadline: Date?) throws -> [String: Any] {
        try transaction { model in
            if model.owner != owner {
                release(&model)
                model = StudyFocusModel()
                model.owner = owner
            }
            reconcile(&model)
            guard owner != nil, model.enabled, selectionCount(model) > 0,
                  let end = StudyFocusPolicy.validDeadline(deadline, now: Date()) else {
                release(&model)
                return status(model)
            }
            if let lease = model.lease, lease.deadline == end,
               center.activities.contains(DeviceActivityName(lease.activity)) { return status(model) }
            release(&model)
            let name = DeviceActivityName(StudyFocusPolicy.activityPrefix + UUID().uuidString)
            let window = StudyFocusPolicy.monitoringWindow(deadline: end, now: Date())
            var calendar = Calendar(identifier: .gregorian)
            calendar.timeZone = TimeZone(secondsFromGMT: 0)!
            let units: Set<Calendar.Component> = [.year, .month, .day, .hour, .minute, .second]
            var start = calendar.dateComponents(units, from: window.start)
            var finish = calendar.dateComponents(units, from: window.end)
            start.calendar = calendar; start.timeZone = calendar.timeZone
            finish.calendar = calendar; finish.timeZone = calendar.timeZone
            // Register cleanup successfully BEFORE applying any restriction.
            try center.startMonitoring(name, during: DeviceActivitySchedule(intervalStart: start, intervalEnd: finish, repeats: false))
            model.lease = StudyFocusLease(activity: name.rawValue, deadline: end)
            // A process kill after shielding must still leave a readable release
            // lease for the extension. Persist under the lock BEFORE shielding.
            try persist(model)
            settings.shield.applications = model.selection.applicationTokens.isEmpty ? nil : model.selection.applicationTokens
            settings.shield.webDomains = model.selection.webDomainTokens.isEmpty ? nil : model.selection.webDomainTokens
            // Never shield an entire category, which could also include study tools.
            settings.shield.applicationCategories = nil
            settings.shield.webDomainCategories = nil
            return status(model)
        }
    }

    static func intervalEnded(_ name: DeviceActivityName) {
        _ = try? transaction { model in
            if StudyFocusPolicy.shouldRelease(activity: name.rawValue, currentActivity: model.lease?.activity,
                                               deadline: model.lease?.deadline, now: Date()) {
                release(&model)
            }
        }
    }
}
