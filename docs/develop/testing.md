# Testing

What a build goes through before it is installed on a watch.

A Pebble Time cannot be opened to rescue it. So every build runs in the
emulator first, and what the emulator cannot run is known before the
install.

:::{note}
The scripts named here are in the tools repository, see {doc}`build`. They
are being repackaged into one tool. The checks stay; the command lines will
change.
:::

## Before a build goes on a watch

1. A release build from a clean checkout of one commit.
2. Two emulator builds of the same commit: one with timer events from
   SysTick, one with the RTC wakeup timer (`CONFIG_TIMER_STM32_RTC_WUT=y`).
3. Core's integration tests on both emulator builds.
4. The update test.
5. After a move to a new PebbleOS release: the update test in both
   directions.
6. The comparison of Core's boards.

## Integration tests

The parts `system`, `ui` and `notifications` of Core's test suite, run as
on {doc}`build`. The firmware starts behind Pebble's own bootloader, as on
a watch. A stand-in plays the Bluetooth controller.

Pass: `14 passed` on each emulator build.

`tools/emu/itest.sh` starts the stand-in and the tests in one go.

## Update test

`tools/emu/emu_fw_update.py` starts an emulator build and sends it a
bundle the way the phone app does: firmware and system resources. The
firmware restarts and the bootloader installs the update.

```console
# python3 emu_fw_update.py <build dir> <qemu> <bundle.pbz> <output dir>
```

Run it in the firmware tree, inside the build container.

Pass: after the restart the firmware reports the version of the bundle.
A transfer that finished is not a pass.

Run in the emulator so far: PebbleOS 4.47 to itself, 4.46 to 4.47, and
4.47 back to 4.46.

## Core's boards

The port must not change the firmware of Core's own watches. Three of
Core's boards are built twice, from Core's release and from the port, and
compared object by object.

```console
# bash core_compare.sh <Core tree> <port tree> <output dir> \
    asterix obelix@pvt getafix@dvt2
```

Run it inside the build container. Pass: no object is added, removed or
changed for any board.

Objects are compared without debug information. Line numbers in log and
assert calls and the version string are masked, so a line that only moved
does not count. `version.c` is skipped.

`tools/gate/gate_check.py` is the quick check before that. It lists the
source files the port changes that still differ for a Core board once the
`CONFIG_` conditions are resolved.

## What the emulator covers

| Area | Covered |
| --- | --- |
| Start through Pebble's bootloader | Yes |
| Display and buttons | Yes |
| Bluetooth start-up, advertising, a connection | With the controller stand-in |
| Firmware update, installed by the bootloader | Yes |

## What only a watch runs

| Code | Why |
| --- | --- |
| Timer events from the RTC alarm | The emulator build takes them from SysTick or the wakeup timer |
| Deep sleep (STOP mode) | The emulator build only waits for interrupts |
| The display driver's wait for the FPGA | The emulated FPGA is ready at once |
| Power chip, charging, accelerometer, compass The emulator has no model of these chips |
| Microphone | No model |
| The recovery firmware | Does not run in the emulator |

A change to one of these has to be tried on a watch.

## On the watch

After an install, check the version the watch reports. It must be the
bundle's.

The measurements on {doc}`measurements` are a separate build and are not
part of these checks.
