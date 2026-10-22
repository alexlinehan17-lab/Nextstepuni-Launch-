//
//  StudyTimerWidgetBundle.swift
//
//  The StudyTimerWidget extension: the study timer's Live Activity, and
//  nothing else (no Home Screen widgets). Live Activities need iOS 16.1; on
//  older systems the bundle is empty and the app works as before.
//
//  SPDX-License-Identifier: Apache-2.0
//

import SwiftUI
import WidgetKit

@main
struct StudyTimerWidgetBundle: WidgetBundle {
    var body: some Widget {
        if #available(iOS 16.1, *) {
            StudyTimerLiveActivity()
        }
    }
}
