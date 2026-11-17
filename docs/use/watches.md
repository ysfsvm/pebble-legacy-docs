# Supported watches

| Watch | Board | State |
| --- | --- | --- |
| Pebble Time | `snowy@dvt` | Runs on one retail watch |
| Pebble Time Steel | `snowy@s3` | Runs on a user's watch. Not tested here |
| Pebble Time Round | `spalding` | Builds. Never run on a watch |

The Time Steel is the same board with another battery. The Time Round
shares the electronics but has its own display path, which has never run.

The original Pebble, the Pebble Steel and the Pebble 2 are not part of
this port. [PebbleOS-legacy-watches](https://github.com/bjsilvest/PebbleOS-legacy-watches) is a separate port for them.

## Pebble Time

Checked on one watch with the firmware on PebbleOS 4.47.

| Feature | State |
| --- | --- |
| Display, buttons | Work |
| Backlight | Works |
| Vibration | Works |
| Bluetooth LE | Works. Pairing shows a code on the watch to type on the phone |
| Notifications | Work |
| Firmware update over Bluetooth | Works. A few minutes |
| Microphone and dictation | Work |
| Compass | Works |
| Charging | Works |
| Deep sleep | 94 to 96 % of an idle hour |
| Color emoji | 136 built in. The rest need the emoji pack |
| Accelerometer | Not checked |
| Calls, music control, app install | Checked on PebbleOS 4.46 only |
| Battery life | Not measured |
| iPhone | Not tried |

## What does not work

- **Bluetooth Classic.** PebbleOS speaks Bluetooth LE only. The original
  Pebble phone app cannot connect.
- **Smartstraps.**
- **The recovery firmware from a phone.** The watch keeps Pebble's recovery
  firmware, which talks Bluetooth Classic. See {doc}`../develop/port`.

## What is slower than the stock firmware

- **Transfers.** About 13 KiB/s over Bluetooth LE.
- **Animations.** The launcher takes about 35 ms to draw a frame. The
  target is 33 ms.
