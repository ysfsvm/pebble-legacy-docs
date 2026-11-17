# Update

Install a new build on a watch that already runs this firmware.

## From the app

The app of this project, from version legacy-2, looks for new releases on
GitHub. When one is newer than the watch's build, the watch's card shows
**Update PebbleOS to** the new version, with the release notes.

- It looks at the **Background Refresh Interval** (Settings > General) and
  when the watch connects.
- **Check for Updates** in the watch's **⋮** menu looks right away.
- **Look for Port Builds Automatically** (Settings > General) off: it only
  looks on **Check for Updates**.

The card also shows the build the watch runs, with links to the release
notes and to this site.

## Sideload a bundle

You need:

- the phone app of this project, see {doc}`app`
- a bundle (`.pbz`) for your watch on the phone, see {doc}`download`

1. In the app, open **Settings** and turn on **Show debug options**.
2. Open **Watches**. The watch must be connected.
3. Tap the watch's **⋮** menu, then **Debug**, then **Firmware Update
   Debug**.
4. Tap **Sideload FW** and pick the `.pbz`.
5. Leave the app open. The watch shows the update screen, then restarts.
6. After it reconnects, the app installs the emoji pack that came in the
   bundle. The watch's card shows its progress.

Check the version on the watch in **Settings > System > Information**.

## How long it takes

Measured once, on a Pebble Time with an Android phone.

| Step | Time |
| --- | --- |
| Firmware and resources | 2 min 30 s |
| Restart and reconnect | 55 s |
| Emoji pack | 40 s |

## The emoji pack

The firmware has 136 color emoji built in. The pack has the rest.

```{image} ../_static/images/emoji-notification.png
:alt: A notification with emoji on the watch
:width: 144px
```

If the transfer of the pack is cut off, the app sends it again the next
time the watch connects. It gives up after three tries and shows an error.
Until then the watch draws the built-in emoji only.

The **Emoji pack** section of **Firmware Update Debug**, on the same screen
as **Sideload FW**, shows what happened to the pack after the last update
and installs it by hand: from the release the watch runs, downloaded from
GitHub, or from a picked file.

## If the watch does not come back

A build that does not start three times in a row makes the watch fall back
to the recovery firmware. See {doc}`recover`.
