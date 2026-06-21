//
//  SignInWithApplePlugin.swift
//
//  A minimal Capacitor plugin wrapping Apple's system AuthenticationServices
//  framework (ASAuthorizationAppleIDProvider) — NO third-party SDK, so nothing
//  extra is bundled into the IPA and nothing extra to declare in App Privacy.
//  This is deliberate: community social-login plugins drag in the Facebook /
//  Google SDKs, which is unacceptable for an app used by minors.
//
//  JS side: utils/signInWithApple.ts (registerPlugin('SignInWithApple')).
//  The returned identityToken + raw nonce are exchanged for a Firebase session
//  by the web layer (OAuthProvider('apple.com') + signInWithCredential).
//
//  SPDX-License-Identifier: Apache-2.0
//

import Foundation
import Capacitor
import AuthenticationServices

@objc(SignInWithApplePlugin)
public class SignInWithApplePlugin: CAPPlugin, CAPBridgedPlugin,
    ASAuthorizationControllerDelegate, ASAuthorizationControllerPresentationContextProviding {

    public let identifier = "SignInWithApplePlugin"
    public let jsName = "SignInWithApple"
    public let pluginMethods: [CAPPluginMethod] = [
        CAPPluginMethod(name: "authorize", returnType: CAPPluginReturnPromise),
    ]

    private var savedCall: CAPPluginCall?

    @objc func authorize(_ call: CAPPluginCall) {
        savedCall = call
        let request = ASAuthorizationAppleIDProvider().createRequest()
        request.requestedScopes = [.fullName, .email]
        // Apple receives the SHA-256 hash of the nonce; Firebase verifies it
        // against the raw nonce on the JS side.
        if let nonce = call.getString("nonce") {
            request.nonce = nonce
        }
        DispatchQueue.main.async {
            let controller = ASAuthorizationController(authorizationRequests: [request])
            controller.delegate = self
            controller.presentationContextProvider = self
            controller.performRequests()
        }
    }

    public func authorizationController(controller: ASAuthorizationController,
                                        didCompleteWithAuthorization authorization: ASAuthorization) {
        guard let credential = authorization.credential as? ASAuthorizationAppleIDCredential,
              let tokenData = credential.identityToken,
              let identityToken = String(data: tokenData, encoding: .utf8) else {
            savedCall?.reject("No identity token returned by Apple")
            savedCall = nil
            return
        }
        savedCall?.resolve([
            "identityToken": identityToken,
            "givenName": credential.fullName?.givenName ?? "",
            "familyName": credential.fullName?.familyName ?? "",
            "email": credential.email ?? "",
            "user": credential.user,
        ])
        savedCall = nil
    }

    public func authorizationController(controller: ASAuthorizationController,
                                        didCompleteWithError error: Error) {
        let nsError = error as NSError
        if nsError.code == ASAuthorizationError.canceled.rawValue {
            savedCall?.reject("USER_CANCELLED", "canceled")
        } else {
            savedCall?.reject(error.localizedDescription)
        }
        savedCall = nil
    }

    public func presentationAnchor(for controller: ASAuthorizationController) -> ASPresentationAnchor {
        return self.bridge?.viewController?.view.window ?? UIWindow()
    }
}
