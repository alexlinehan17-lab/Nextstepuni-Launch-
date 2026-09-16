# Header directions · 16 September 2026

Open `index.html` through the project’s Vite development server.

Four interactive visual directions for the existing training-progress and notification controls:

1. **Your little orbit:** selected Star Crew character within a progress ring; circular post button.
2. **The paper trail:** numbered rank ticket with a segmented progress line; folded-note notification.
3. **A note for you:** Stargazer companion beside the progress line; a miniature post pocket.
4. **Quiet confidence:** restrained type and an orange underline; an Updates label and ink count.

The preview includes a desktop/phone toggle, four personal characters, sample unread/read notifications, message details, progress details, an earned-points interaction and a rank-up animation. All preview interaction stays in React memory; it sends nothing and changes no account data.

Uses approved Star Crew artwork and the app’s actual rank thresholds. Sample lifetime points are 6,200 (Driven, 69% towards Elite); the separately labelled spendable Journey Points balance is 5,065. This is a design exploration, including a proposed phone treatment; the current app hides this desktop control on mobile.

## Selected pairing

The default preview combines the Star Crew progress ring from direction 01 with the folded-note notification button from direction 02. The unread badge clears when all sample notes are read. The four original directions remain available for comparison.

The selected pairing is implemented in `TrainingPulse` and `NotificationBell`, using the student's actual avatar, earned rank, streak, spendable balance and notifications. The notification panel includes full-message reading and the Listener companion. Production keeps the existing milestones action and desktop-only header placement.
