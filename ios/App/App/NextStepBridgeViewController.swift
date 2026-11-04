//
//  NextStepBridgeViewController.swift
//
//  The app's Capacitor view controller (Main.storyboard points at it). Capacitor
//  only auto-registers the plugins `cap sync` lists from node_modules
//  (capacitor.config.json packageClassList), so plugins that live in this
//  target are registered here, before the web app loads.
//
//  SPDX-License-Identifier: Apache-2.0
//

import UIKit
import WebKit
import Capacitor

class NextStepBridgeViewController: CAPBridgeViewController {

    override func capacitorDidLoad() {
        super.capacitorDidLoad()
        bridge?.registerPluginInstance(StudyLiveActivityPlugin())
        #if DEBUG
        installStudyTimerDemo()
        #endif
    }

    #if DEBUG
    /// Simulator check without signing in (Debug builds only; compiled out of
    /// Release). Launch with
    ///   -NSUStudyTimerDemo '{"notifyIn":45,"remaining":1110,"mode":"running"}'
    /// and the web app (services/studyTimerDemo.ts, which also only runs in a
    /// Debug native build) schedules a sample "Time's up" notification and
    /// starts a sample Live Activity through the same code students use.
    private func installStudyTimerDemo() {
        // Read the raw argument: UserDefaults would parse "{...}" as a plist.
        let arguments = ProcessInfo.processInfo.arguments
        guard let flag = arguments.firstIndex(of: "-NSUStudyTimerDemo"), flag + 1 < arguments.count,
              let data = arguments[flag + 1].data(using: .utf8),
              let object = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let json = try? JSONSerialization.data(withJSONObject: object),
              let source = String(data: json, encoding: .utf8) else { return }
        let script = WKUserScript(source: "window.__NSU_STUDY_TIMER_DEMO__ = \(source);",
                                  injectionTime: .atDocumentStart,
                                  forMainFrameOnly: true)
        webView?.configuration.userContentController.addUserScript(script)
    }
    #endif
}
