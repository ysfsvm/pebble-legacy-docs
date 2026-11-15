# Recover

What to do when the watch shows Pebble's recovery screen, or does not
start.

The recovery firmware is Pebble's own, from 2015. It talks Bluetooth
Classic, and Core's phone app cannot drive it. Getting out of it means
installing a firmware from a Linux PC.

:::{warning}
Entering the recovery firmware erases the normal firmware. Do not enter it
to look at it. The only way out is a new install.
:::

## What was run

| Path | State |
| --- | --- |
| Port to recovery firmware and back, from a PC | Run three times on one Pebble Time, with the port on PebbleOS 4.46 |
| The same with the port on PebbleOS 4.47 | Not run |
| Recovery firmware to a stock firmware | Never run |
| Any of this on a Time Steel or Time Round | Never run |

## How the watch gets there

The bootloader starts the recovery firmware instead of the normal one
when:

- the firmware crashed, or was reset by the watchdog, three starts in a
  row. A firmware that has run for 15 minutes counts as stable, and the
  count starts again.
- Back, Select and Up were held for 5 seconds.
- a phone or PC asked for it over Bluetooth.
- there is no firmware in the internal flash.

Each time, the bootloader copies the recovery firmware over the normal
firmware. The filesystem with your apps and settings stays.

## Buttons

| Where | Hold | Effect |
| --- | --- | --- |
| Normal firmware | Back + Select, 5 s | Restart. Nothing is erased |
| Normal firmware | Back + Select + Up, 5 s | Recovery firmware. **Erases the firmware** |
| While the watch starts | Up + Back, 5 s | Recovery firmware, by the bootloader's source. **Erases the firmware.** Not confirmed on a watch |
| Recovery firmware | Down, 5 s | Factory reset. **Erases the filesystem** |
| Recovery firmware | Up + Select, 5 s | Manufacturing mode. Do not |
| Anywhere | Back, 8 to 11 s | The power chip switches the watch off |

The two rows for the recovery firmware are from Pebble's source release,
which is newer than the recovery firmware on the watch.

## What each action keeps

| Action | Firmware | Apps and settings |
| --- | --- | --- |
| Restart | Kept | Kept |
| Factory reset in Settings | Kept | Erased |
| Entering the recovery firmware | Erased | Kept |
| Down for 5 s in the recovery firmware | Already gone | Erased |
| Install from a PC | Written | Kept |

## The watch shows an error code

The bootloader stops on a screen with a code when it cannot go on.
Pressing Back, Up or Down restarts the watch.

| Code | Meaning |
| --- | --- |
| `fe504501` | A button is stuck |
| `fe504502` | The external flash does not answer |
| `fe504503` | The recovery firmware could not be loaded, or did not start |
| `fe504504` | The firmware did not finish starting seven times in a row |

## Install a firmware from a PC

You need:

- a Linux PC with a Bluetooth adapter that does Bluetooth Classic
- BlueZ (`bluetoothctl`)
- Python 3 with `libpebble2`
- the tools repository, see {doc}`../develop/build`
- a bundle (`.pbz`) of the port with firmware and resources

:::{note}
The scripts are being repackaged into one tool. The steps stay; the command
lines below will change.
:::

1. Put the watch on the charger.
2. Switch Bluetooth off on the phone, so that it does not connect to the
   watch instead.
3. Find the watch's Bluetooth address:

   ```console
   $ bluetoothctl --timeout 10 scan bredr
   $ bluetoothctl devices
   ```

4. Start the install from the tools repository:

   ```console
   $ python3 tools/recovery/classic_resume_install.py <address> <bundle.pbz>
   ```

   The script pairs with the watch, opens a serial connection, writes the
   firmware and then the resources, and tells the watch that the update is
   complete. With the port on PebbleOS 4.46 the transfer took about a
   minute and a half.

5. Wait for `DONE`. The watch restarts, the bootloader copies the firmware
   into place and starts it.
6. Switch Bluetooth on again on the phone.

The recovery firmware keeps no pairing and cannot continue a transfer.
When the connection drops, the script removes the pairing, pairs again and
starts over, up to 40 times. `GAVE UP` means none of them got through.
Check that the watch is on and shows the recovery screen, then run the
script again. Do not hold buttons to help it along.

## Other scripts

All in `tools/recovery`. They talk to the recovery firmware the same way.

| Script | What it does |
| --- | --- |
| `classic_prf_alive.py` | Asks for the version every 10 seconds and logs how long the connection lasts |
| `classic_prf_log.py` | Saves the recovery firmware's log of its last three starts |
| `classic_get_coredump.py` | Saves the core dump the watch holds |
| `coredump_parse.py` | Lists the tasks, registers and stacks of a core dump |

## Back to the stock firmware

The port replaces only the normal firmware. A stock bundle for the Pebble
Time, installed from the recovery firmware, should bring the stock firmware
back. This was never run.
