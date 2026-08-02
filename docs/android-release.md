# Android release — building the bundle Google Play accepts

Play only accepts a **signed Android App Bundle** (`.aab`). Not an APK, and not an
unsigned or debug-signed build. This is the whole path from a clean checkout to a
file you can upload.

## 1. Create the upload key (once, and only once)

This is yours. It never enters the repository — `android/keystore.properties`,
`*.jks` and `*.keystore` are gitignored, and the build reads the passwords from
that file at build time.

Run from the repo root, and answer the prompts (name, organisation, country —
"NEXTSTEPUNI LIMITED" / "IE" is fine; the values are not shown to users):

Use the JDK that Android Studio bundles. macOS ships a `/usr/bin/keytool` stub
that only tells you to install Java, so the full path matters:

```bash
"/Applications/Android Studio.app/Contents/jbr/Contents/Home/bin/keytool" \
  -genkeypair -v \
  -keystore ~/nextstepuni-upload-key.jks \
  -alias nextstepuni-upload \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -storetype PKCS12
```

PKCS12 keystores use one password for both the store and the key, so the
`storePassword` and `keyPassword` below are the same value.

Keep `~/nextstepuni-upload-key.jks` and its password somewhere durable — a
password manager, not just this Mac. If the machine dies with the only copy, you
can still recover: Play App Signing holds the real app signing key, and Google
can reset a lost *upload* key on request. Losing it is an inconvenience; leaking
it is not recoverable, which is why it stays out of git.

## 2. Point the build at it

Create `android/keystore.properties` (gitignored) with the values you just used:

```properties
storeFile=/Users/<you>/nextstepuni-upload-key.jks
storePassword=<the store password>
keyAlias=nextstepuni-upload
keyPassword=<the key password>
```

`storeFile` must be an absolute path. If this file is missing the build still
works for debug, but the release bundle will be unsigned and Play will reject it.

## 3. Build the bundle

```bash
npm run build                    # compile the web app into dist/
npx cap sync android             # copy dist/ into the Android project
cd android && JAVA_HOME="$HOME/.jdks/jdk-21.0.12+8/Contents/Home" ./gradlew bundleRelease
```

**JAVA_HOME is not optional.** Android Studio Quail 3 bundles Java 25, and this
project's Gradle 8.14.3 supports Java 24 at most — building with the bundled JDK
fails with `Unsupported class file major version 69`. Bumping Gradle to 9.x is
the obvious-looking fix, but AGP 8.13.0 expects Gradle 8.x, so it trades one
incompatibility for a worse one. A Temurin JDK 21 (the version AGP 8.x targets)
lives in `~/.jdks/` — self-contained, no system install, and it leaves both the
system Java and Android Studio's own JDK alone.

## ⚠️ The bundle is far too large to publish

A clean build currently produces a **569 MB** `.aab`, which Google Play will
reject outright. The cause is not the app: `dist/exam-figures` is 539 MB across
3,114 PNGs, and Capacitor copies the whole of `dist/` into the native shell.

This is not Android-specific — the iOS app ships the same payload
(`ios/App/App/public` is 608 MB).

The fix is to serve `/exam-figures/**` from Firebase Hosting on native rather
than bundling it, which the app is already positioned for: the files are hosted
today, and the app needs the network for Firebase regardless. That takes the
download from roughly 600 MB to roughly 70 MB. Until that lands, no Android
release can be published.

The bundle lands at:

```
android/app/build/outputs/bundle/release/app-release.aab
```

That is the file you upload to Play Console.

## 4. Version numbers

`android/app/build.gradle` holds them:

- `versionCode` — an integer Play uses to order releases. **Must increase with
  every upload.** Play rejects a bundle whose versionCode it has already seen.
- `versionName` — the human-readable string ("1.0"), shown on the listing.

These are separate from the iOS `MARKETING_VERSION` / `CURRENT_PROJECT_VERSION`
and are not kept in sync automatically.

## Known gaps in the Android build

- **No Google Sign-In.** `signInWithPopup` has no popup to open inside the
  Capacitor webview. Adding it needs a native Google plugin *and* the release
  signing SHA-1 registered in the Firebase console, so v1 ships with email and
  password only. Sign in with Apple is iOS-only by design.
- **The Android shell has had none of the polish iOS got.** Icons, splash screen
  and store assets were produced for the App Store; check them on a real device
  before shipping.
