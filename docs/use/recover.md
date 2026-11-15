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
- Python 3.11 or newer
- `plt` with its `watch` extra, see {doc}`../develop/tools`
- a bundle (`.pbz`) of the port with firmware and resources

1. Put the watch on the charger.
2. Switch Bluetooth off on the phone, so that it does not connect to the
   watch instead.
3. Find the watch's Bluetooth address:

   ```console
   $ bluetoothctl --timeout 10 scan bredr
   $ bluetoothctl devices
   ```

4. Start the install:

   ```console
   $ python -m plt.recover install <address> <bundle.pbz>
   ```

   It pairs with the watch, opens a serial connection, writes the
   firmware and then the resources, and tells the watch that the update is
   complete. With the port on PebbleOS 4.46 the transfer took about a
   minute and a half.

5. Wait for `DONE`. The watch restarts, the bootloader copies the firmware
   into place and starts it.
6. Switch Bluetooth on again on the phone.

The recovery firmware keeps no pairing and cannot continue a transfer.
When the connection drops, the command removes the pairing, pairs again and
starts over, up to 40 times (`--windows N` changes that). Each time it
first asks the watch how much of the update it holds, and continues from
there if the watch answers. `GAVE UP` means none of them got through. Check that the watch
is on and shows the recovery screen, then run the command again. Do not
hold buttons to help it along.

### With the image registry

If you build with `plt`, `plt watch recover` does the same install with
the image marked as the recovery image, or a named one:

```console
$ plt images role <image> recovery
$ PLT_WATCH_BT=<address> plt watch recover [<image>]
```

It tries up to 30 times within 15 minutes, saves the full output in the
logs directory and prints the last lines. After `DONE` it marks the image
as the one the watch runs, but does not check the version the watch then
reports. Check it with `plt watch status` once the phone is connected
again.

## Other commands

They talk to the recovery firmware the same way, and take the same
address.

| Command | What it does |
| --- | --- |
| `python -m plt.recover alive <address> [--minutes M]` | Asks for the version every 10 seconds and logs how long the connection lasts. Default 5 minutes |
| `python -m plt.recover log <address> <prefix>` | Saves the logs of the last three starts as `<prefix>-gen0.bin` to `<prefix>-gen2.bin` |
| `python -m plt.recover coredump <address> <file> [--windows N]` | Saves the core dump the watch holds |
| `python -m plt.coredump <file>` | Lists the threads, registers and stacks of a core dump |

## Back to the stock firmware

The port replaces only the normal firmware. A stock bundle for the Pebble
Time, installed from the recovery firmware, should bring the stock firmware
back. This was never run.
