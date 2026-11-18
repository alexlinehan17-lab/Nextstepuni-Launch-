import Foundation
import UIKit
import SwiftUI
import Combine
import Capacitor
import FamilyControls
import ManagedSettings

@objc(StudyFocusPlugin)
public class StudyFocusPlugin: CAPPlugin, CAPBridgedPlugin {
    public let identifier = "StudyFocusPlugin"
    public let jsName = "StudyFocus"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "sync", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "configure", returnType: CAPPluginReturnPromise),
        CAPPluginMethod(name: "setEnabled", returnType: CAPPluginReturnPromise),
    ]
    private var expiry: Timer?
    private var permission: AnyCancellable?
    private var picker: UIViewController?
    private var pickerCall: CAPPluginCall?
    private var owner: String?
    private var generation = UUID()
    private static let unavailable: [String: Any] = ["available": false, "authorized": false, "enabled": false, "active": false, "selectionCount": 0]

    override public func load() {
        guard #available(iOS 16.0, *) else { return }
        NotificationCenter.default.addObserver(self, selector: #selector(reconcile), name: UIApplication.didBecomeActiveNotification, object: nil)
        permission = AuthorizationCenter.shared.$authorizationStatus.dropFirst().receive(on: DispatchQueue.main).sink { [weak self] _ in self?.reconcile() }
        DispatchQueue.main.async { [weak self] in self?.reconcile() }
    }

    @objc private func reconcile() {
        guard #available(iOS 16.0, *), StudyFocusStore.available else { return }
        _ = try? StudyFocusStore.transaction { model in StudyFocusStore.reconcile(&model) }
        armExpiry()
    }

    @available(iOS 16.0, *)
    private func armExpiry() {
        expiry?.invalidate()
        expiry = nil
        let end = try? StudyFocusStore.transaction { $0.lease?.deadline }
        if let end {
            expiry = Timer.scheduledTimer(withTimeInterval: max(0.1, end.timeIntervalSinceNow), repeats: false) { [weak self] _ in self?.reconcile() }
        }
    }

    @objc func sync(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            guard #available(iOS 16.0, *), StudyFocusStore.available else { call.resolve(Self.unavailable); return }
            let nextOwner = call.getString("owner")
            if self.owner != nextOwner {
                self.owner = nextOwner
                self.generation = UUID()
                self.picker?.dismiss(animated: false)
                self.picker = nil
                self.pickerCall?.reject("The signed-in student changed.")
                self.pickerCall = nil
            }
            do {
                let deadline = call.getDouble("deadline").map { Date(timeIntervalSince1970: $0 / 1000) }
                call.resolve(try StudyFocusStore.sync(owner: nextOwner, deadline: deadline))
                self.armExpiry()
            } catch { call.reject("App blocking could not start. Restrictions have been cleared.", nil, error) }
        }
    }

    @objc func setEnabled(_ call: CAPPluginCall) {
        DispatchQueue.main.async {
            guard #available(iOS 16.0, *), StudyFocusStore.available else { call.resolve(Self.unavailable); return }
            do {
                let result = try StudyFocusStore.transaction { model in
                    guard let owner = call.getString("owner"), owner == model.owner else { throw StudyFocusStore.Failure.wrongOwner }
                    let enabled = call.getBool("enabled") ?? false
                    if enabled {
                        guard AuthorizationCenter.shared.authorizationStatus == .approved else { throw StudyFocusStore.Failure.unauthorized }
                        guard StudyFocusStore.selectionCount(model) > 0 else { throw StudyFocusStore.Failure.noSelection }
                    } else { StudyFocusStore.release(&model) }
                    model.enabled = enabled
                    return StudyFocusStore.status(model)
                }
                call.resolve(result)
                self.armExpiry()
            } catch { call.reject("Could not change app blocking.", nil, error) }
        }
    }

    @objc func configure(_ call: CAPPluginCall) {
        Task { @MainActor in
            guard #available(iOS 16.0, *), StudyFocusStore.available else { call.resolve(Self.unavailable); return }
            guard let requestedOwner = call.getString("owner"), requestedOwner == self.owner,
                  self.pickerCall == nil else { call.reject("App selection is unavailable."); return }
            let requestedGeneration = self.generation
            do {
                // Only a student's explicit tap reaches this request.
                if AuthorizationCenter.shared.authorizationStatus != .approved {
                    try await AuthorizationCenter.shared.requestAuthorization(for: .individual)
                }
                guard self.owner == requestedOwner, self.generation == requestedGeneration else {
                    call.reject("The signed-in student changed."); return
                }
                let selection = try StudyFocusStore.transaction { model in model.selection }
                let view = StudyFocusPicker(selection: selection) { [weak self] chosen in
                    guard let self else { return }
                    self.picker?.dismiss(animated: true)
                    self.picker = nil
                    self.pickerCall = nil
                    guard self.owner == requestedOwner, self.generation == requestedGeneration else { call.reject("The signed-in student changed."); return }
                    do {
                        let result = try StudyFocusStore.transaction { model in
                            guard model.owner == requestedOwner else { throw StudyFocusStore.Failure.wrongOwner }
                            if let chosen {
                                // Materialise expanded category choices as explicit
                                // tokens before dropping the category selection.
                                var explicit = FamilyActivitySelection(includeEntireCategory: true)
                                explicit.applicationTokens = chosen.applicationTokens
                                explicit.webDomainTokens = chosen.webDomainTokens
                                // Exclude our own app when the system exposes its token.
                                // The remaining opaque tokens stay on this device.
                                if let token = Application(bundleIdentifier: "com.nextstepuni.app").token { explicit.applicationTokens.remove(token) }
                                StudyFocusStore.release(&model)
                                model.selection = explicit
                                model.enabled = StudyFocusStore.selectionCount(model) > 0
                            }
                            return StudyFocusStore.status(model)
                        }
                        call.resolve(result)
                        self.armExpiry()
                    } catch { call.reject("Could not save the selected apps.", nil, error) }
                }
                guard let presenter = self.bridge?.viewController, presenter.presentedViewController == nil else {
                    call.reject("Close the current dialog before choosing apps."); return
                }
                let hosting = UIHostingController(rootView: view)
                hosting.isModalInPresentation = true
                self.picker = hosting
                self.pickerCall = call
                presenter.present(hosting, animated: true)
            } catch { call.reject("Screen Time access was not granted.", nil, error) }
        }
    }

    deinit {
        expiry?.invalidate()
        NotificationCenter.default.removeObserver(self)
    }
}

@available(iOS 16.0, *)
private struct StudyFocusPicker: View {
    @State var selection: FamilyActivitySelection
    @State private var overLimit = false
    let finish: (FamilyActivitySelection?) -> Void
    var body: some View {
        NavigationStack {
            FamilyActivityPicker(selection: $selection)
                .navigationTitle("Distracting apps")
                .navigationBarTitleDisplayMode(.inline)
                .toolbar {
                    ToolbarItem(placement: .cancellationAction) { Button("Cancel") { finish(nil) } }
                    ToolbarItem(placement: .confirmationAction) {
                        Button("Done") {
                            if selection.applicationTokens.count > 50 || selection.webDomainTokens.count > 50 { overLimit = true }
                            else { finish(selection) }
                        }
                    }
                }
                .alert("Choose fewer apps", isPresented: $overLimit) {
                    Button("OK", role: .cancel) {}
                } message: {
                    Text("Choose up to 50 apps and 50 websites. Expand a category to choose individual apps and keep your study tools available.")
                }
        }
    }
}
