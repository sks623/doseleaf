# Doseleaf — Android prescription companion

An installable Android prototype (Android 8.0+, API 26). It is **not a hosted website**: the APK bundles a React interface and uses native Java for the camera, Android file picker, SQLite, private image files, Gemini HTTPS calls, notifications and alarms. It works without a web server. Gemini extraction requires internet and your own API access for this prototype.

## Try the APK

1. Install `Doseleaf-Android-Preview.apk` on an Android phone. This is a debug-signed prototype, not a Play Store release.
2. Open **Add prescription**. Choose **Take photo** for your camera, or **Upload prescription** for an image from your phone/gallery/files.
3. Tap **Gemini** and supply an API key from Google AI Studio. The key remains in memory for this app session. No key is built into the APK or saved in prescriptions.
4. Tap **Read with Gemini**. The selected photo goes directly from the phone to Google's Gemini API. The default is configurable `gemini-3.8-flash`, which was listed in Google's model catalog on 20 September 2026. The requested name “Gemini 3.58 Plus” could not be verified.
5. Review the source transcription and clarification questions. Confirm unclear medical details with a prescriber/pharmacist; fill those answers and correct the matching medicine fields. Set start/end dates and actual clock times yourself. The app never chooses a dose or invents timing from “morning”, “BD” or “1-0-1”.
6. Confirm and save. Records are stored in the phone's private app storage, with a date-wise archive and taken/undo tracking.
7. Open **Today → Notification settings**, allow notifications, and allow precise alarms when Android requests it. Android reminders can fire while the app is closed. Without precise alarm permission Android may delay them. Force-stop, notification denial, battery restrictions and turning off the phone can prevent or delay them.

**No cloud backup is implemented. Uninstalling or clearing app data deletes prescriptions.** Keep your original prescription. Selected photos are normalized for orientation and size before extraction/storage. The prototype accepts images, not multipage PDFs. Non-daily, tapering or as-needed medicines can be archived without daily reminders. It does not interpret those instructions into a schedule.

## Features implemented

- Native camera capture and system image picker; no broad gallery/storage permission.
- Handwriting and printed-text extraction with a Gemini image request and structured JSON.
- Source excerpts; name, strength, dose, route, food instructions, frequency and duration fields.
- Uncertainty/missing-field clarification questions and mandatory human review.
- Local SQLite prescription history and dose marks; private photo files.
- Native AlarmManager reminders, notification channel, Android 13 notification permission, precise-alarm setting, restart/timezone rescheduling.
- Calendar `.ics` export through Android's share menu.
- Clearly labeled fictional example mode, separated from saved records and real reminders.

## Build

Java 17 and the Android SDK are needed. Install `platforms;android-35` and `build-tools;35.0.0` through Android SDK Manager. The checked-in assets allow an APK build without Node:

```sh
python3 build_apk.py --sdk "$ANDROID_HOME"
```

The result is `build/Doseleaf-Android-Preview.apk`. The script generates a local debug key unless `--keystore` supplies an existing debug keystore. Retain the same signing key for updates; never commit private release keys. A fresh debug key cannot update an installation signed with another key.

Alternatively, open this project in Android Studio. Gradle files target Android Gradle Plugin 8.7.3 / Gradle 8.9 / Java 17. No Gradle wrapper is included; Android Studio or a locally installed compatible Gradle can build it. The included GitHub Actions workflow builds the APK with the official SDK command-line tools and uploads an artifact.

To edit/rebuild the interface:

```sh
cd ui
npm install
npm run build
cd ..
python3 sync_prompts.py
python3 build_apk.py --sdk "$ANDROID_HOME"
```

## Structure

- `ui/src/App.tsx`: screens and review flow.
- `ui/src/native.ts`: typed request bridge to Android, no remote website dependency.
- `ui/src/lib/model.ts`: validation and calendar export.
- `app/src/main/java/com/doseleaf/app/MainActivity.java`: restricted local WebView, capture/import, Gemini client, Android settings.
- `Database.java`: SQLite and native save validation.
- `Scheduler.java`, `ReminderReceiver.java`, `BootReceiver.java`: Android reminders.
- `PhotoProvider.java`: narrowly scoped camera/share content provider.
- `prompts/`: extraction instructions and exact JSON response schema.

The interface is loaded only from bundled assets at a synthetic local HTTPS origin. Remote navigation is blocked or opened in the system browser for the documented Google setup links. The JavaScript bridge is never attached to arbitrary web content. Cloud backups are disabled; no analytics are installed. Notifications use generic text to avoid exposing medicine names on the lock screen. App-private storage relies on Android's device/app protections; no separate vault encryption is claimed.

## Prototype boundaries / validation

Validated here: Java compilation, UI build, TypeScript checking, Android manifest, APK v2/v3 signature, review/clarification/date/time validation, and calendar recurrence bounds. Real camera/file-picker behavior, background alarm timing, handset compatibility and live Gemini reading still need device/API-key testing. No diagnostic or prescribing claims are made. Review safeguards reduce risk but do not make model output medically reliable. Do not use the prototype as the sole reminder for critical medication.

For distribution to other users, add managed authentication and a server-side Gemini credential or suitable short-lived token architecture; do not embed a shared unrestricted API key in an APK. Add backup/restore, record editing and lifecycle controls, accessibility/device testing and a stable release signing process before a production launch.

## Official references

- [Gemini models](https://ai.google.dev/gemini-api/docs/models)
- [Gemini generateContent API](https://ai.google.dev/api/generate-content)
- [Android alarms](https://developer.android.com/develop/background-work/services/alarms)
- [Android notification permission](https://developer.android.com/develop/ui/compose/notifications/notification-permission)
