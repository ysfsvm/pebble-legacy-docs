# Testing

What a build goes through before it is installed on a watch.

A Pebble Time cannot be opened to rescue it. So every build runs in the
emulator first, and what the emulator cannot run is known before the
install.

The commands are those of `plt`, see {doc}`tools`.

## Before a build goes on a watch

1. A release build from a clean checkout of one commit: `plt build`.
2. Two emulator builds of the same commit: one with timer events from
   SysTick, one with the RTC wakeup timer (`CONFIG_TIMER_STM32_RTC_WUT=y`).
3. Core's integration tests on both emulator builds.
4. The update test.
5. After a move to a new PebbleOS release: the update test in both
   directions.
6. The comparison of Core's boards: `plt gate --objects`.

`plt emu test` runs steps 2 to 4 and records the results with the image.
`plt watch flash` refuses an image without them.

## Integration tests

The parts `system`, `ui` and `notifications` of Core's test suite, run as
on {doc}`build`. The firmware starts behind Pebble's own bootloader, as on
a watch. A stand-in plays the Bluetooth controller.

Pass: `14 passed` on each emulator build.

```console
$ plt emu test <image>
$ plt emu try [--wut]
```

`plt emu test` builds the image's commit for the emulator, both ways, and
runs the tests on each. `plt emu try` runs them on the checkout as it is,
uncommitted changes included, and records nothing.

## Update test

The test starts an emulator build and sends it a bundle the way the phone
app does: firmware and system resources. The firmware restarts and the
bootloader installs the update.

`plt emu test` ends with this test, on the wakeup timer build, with the
build's own bundle. To repeat only this test:

```console
$ plt emu test <image> --update-only
```

An update between two versions has no `plt` command. The
[tools manual](https://github.com/ysfsvm/pebble-legacy-tools#plt-emu-test)
shows how to run it by hand.

Pass: after the restart the firmware reports the version of the bundle.
A transfer that finished is not a pass.

Run in the emulator so far: PebbleOS 4.47 to itself, 4.46 to 4.47, and
4.47 back to 4.46.

## Core's boards

The port must not change the firmware of Core's own watches. Three of
Core's boards are built twice, from Core's release and from the port, and
compared object by object.

```console
$ plt gate --objects
```

It needs an unchanged checkout of Core's release, by default `base` next to
the port's checkout (`PLT_BASE_WORKTREE`). It takes about 10 minutes.
Pass: `0 differing objects` for each board.

Objects are compared without debug information. Line numbers in log and
assert calls and the version string are masked, so a line that only moved
does not count. `version.c` is skipped.

`plt gate` without `--objects` is the quick check before that. It lists the
source files the port changes that still differ for a Core board once the
`CONFIG_` conditions are resolved. It reads the board configurations that
`--objects` leaves behind; before the first such run it only counts the
changed files.

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
