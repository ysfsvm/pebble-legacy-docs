# Update

Install a new build on a watch that already runs this firmware.

You need:

- the phone app of this project, see {doc}`app`
- a bundle (`.pbz`) for your watch on the phone

## Steps

1. In the app, open **Settings** and turn on **Show debug options**.
2. Open **Watches**. The watch must be connected.
3. Tap the watch's **⋮** menu, then **Debug**, then **Firmware Update
   Debug**.
4. Tap **Sideload FW** and pick the `.pbz`.
5. Leave the app open. The watch shows the update screen, then restarts.
6. After it reconnects, the app installs the emoji pack that came in the
   bundle. Nothing to do.

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

To install the pack by hand, use **Install watch files** on the same
screen as **Sideload FW**.

## If the watch does not come back

A build that does not start three times in a row makes the watch fall back
to the recovery firmware. See {doc}`recover`.
