//
//  StudyLiveActivityPlugin.swift
//
//  Puts the running study timer on the Lock Screen and in the Dynamic Island
//  (ActivityKit, iOS 16.1+). A student asked for it: the timer is pointless if
//  they have to unlock the iPad to check it. Local plugin, registered by
//  NextStepBridgeViewController; the drawing is in the StudyTimerWidget
//  extension, and the shared type is Shared/StudyTimerAttributes.swift.
//
//  JS side: services/studyLiveActivity.ts. It calls sync() with the whole state
//  whenever the session changes (start, pause, resume, keep going, finish), or
//  with null to end it (saved, discarded, signed out, or nothing to restore).
//  The countdown itself runs on the device (Text(timerInterval:)), so nothing
//  needs updating while the app is in the background.
//
//  SPDX-License-Identifier: Apache-2.0
//

import Foundation
import Capacitor
#if canImport(ActivityKit)
import ActivityKit
#endif

@objc(StudyLiveActivityPlugin)
public class StudyLiveActivityPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "StudyLiveActivityPlugin"
    public let jsName = "StudyLiveActivity"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "isAvailable", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "sync", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "endAll", returnType: CAPPluginReturnPromise),
    ]

    /// Tapping the Live Activity opens nextstepuni://study (widgetURL).
    private static let studyRoomURL = URL(string: "nextstepuni://study")

    override public func load() {
        NotificationCenter.default.addObserver(self, selector: #selector(handleOpenURL(_:)),
                                               name: .capacitorOpenURL, object: nil)
        // A tap that launched the app arrived before this plugin was loaded.
        if let url = ApplicationDelegateProxy.shared.lastURL { open(url) }
    }

    @objc private func handleOpenURL(_ notification: Notification) {
        guard let object = notification.object as? [String: Any], let url = object["url"] as? URL else { return }
        open(url)
    }

    private func open(_ url: URL) {
        guard url.scheme == Self.studyRoomURL?.scheme, url.host == Self.studyRoomURL?.host else { return }
        // Held until the web app listens (services/studyLiveActivity.ts).
        notifyListeners("open", data: ["route": "study-session"], retainUntilConsumed: true)
    }

    @objc func isAvailable(_ call: CAPPluginCall) {
        #if canImport(ActivityKit)
        if #available(iOS 16.1, *) {
            call.resolve(["available": ActivityAuthorizationInfo().areActivitiesEnabled])
            return
        }
        #endif
        call.resolve(["available": false])
    }

    @objc func sync(_ call: CAPPluginCall) {
        #if canImport(ActivityKit)
        if #available(iOS 16.1, *) {
            let state = call.getObject("state").flatMap(Self.contentState(from:))
            Task {
                do {
                    let active = try await StudyActivityController.sync(state)
                    call.resolve(["active": active])
                } catch {
                    call.reject("Could not show the study timer on the Lock Screen", nil, error)
                }
            }
            return
        }
        #endif
        call.resolve(["active": false])
    }

    @objc func endAll(_ call: CAPPluginCall) {
        #if canImport(ActivityKit)
        if #available(iOS 16.1, *) {
            Task {
                _ = try? await StudyActivityController.sync(nil)
                call.resolve()
            }
            return
        }
        #endif
        call.resolve()
    }

    #if canImport(ActivityKit)
    /// The JS state (milliseconds since 1970 for dates) as the activity's state.
    @available(iOS 16.1, *)
    static func contentState(from object: JSObject) -> StudyTimerAttributes.ContentState? {
        guard let subject = object["subject"] as? String,
              let phaseName = object["phase"] as? String,
              let phase = StudyTimerAttributes.Phase(rawValue: phaseName),
              let startedAt = (object["startedAt"] as? NSNumber)?.doubleValue else { return nil }
        let endsAt = (object["endsAt"] as? NSNumber)?.doubleValue
        return StudyTimerAttributes.ContentState(
            subject: subject,
            detail: object["detail"] as? String ?? "",
            phase: phase,
            countsDown: object["countsDown"] as? Bool ?? true,
            startedAt: Date(timeIntervalSince1970: startedAt / 1000),
            endsAt: endsAt.map { Date(timeIntervalSince1970: $0 / 1000) },
            pausedSeconds: (object["pausedSeconds"] as? NSNumber)?.intValue ?? 0,
            totalSeconds: (object["totalSeconds"] as? NSNumber)?.intValue ?? 0,
            doneLabel: object["doneLabel"] as? String ?? "Time’s up"
        )
    }
    #endif
}

#if canImport(ActivityKit)
/// One study timer activity at a time: update it in place, start it if there is
/// none, end every one of them when there is no session.
@available(iOS 16.1, *)
enum StudyActivityController {
    @discardableResult
    static func sync(_ state: StudyTimerAttributes.ContentState?) async throws -> Bool {
        let activities = Activity<StudyTimerAttributes>.activities
        guard let state = state else {
            for activity in activities { await end(activity) }
            return false
        }
        if let current = activities.first {
            for extra in activities.dropFirst() { await end(extra) }
            await update(current, to: state)
            return true
        }
        // The student can turn Live Activities off for the app in Settings.
        guard ActivityAuthorizationInfo().areActivitiesEnabled else { return false }
        try request(state)
        return true
    }

    /// A running countdown goes stale when it ends, so the Lock Screen can say
    /// "Time's up" even if the app is not running to tell it.
    private static func staleDate(for state: StudyTimerAttributes.ContentState) -> Date? {
        state.phase == .running && state.countsDown ? state.endsAt : nil
    }

    private static func request(_ state: StudyTimerAttributes.ContentState) throws {
        if #available(iOS 16.2, *) {
            _ = try Activity.request(attributes: StudyTimerAttributes(),
                                     content: ActivityContent(state: state, staleDate: staleDate(for: state)),
                                     pushType: nil)
        } else {
            _ = try Activity.request(attributes: StudyTimerAttributes(), contentState: state, pushType: nil)
        }
    }

    private static func update(_ activity: Activity<StudyTimerAttributes>, to state: StudyTimerAttributes.ContentState) async {
        if #available(iOS 16.2, *) {
            await activity.update(ActivityContent(state: state, staleDate: staleDate(for: state)))
        } else {
            await activity.update(using: state)
        }
    }

    private static func end(_ activity: Activity<StudyTimerAttributes>) async {
        if #available(iOS 16.2, *) {
            await activity.end(nil, dismissalPolicy: .immediate)
        } else {
            await activity.end(using: nil, dismissalPolicy: .immediate)
        }
    }
}
#endif
