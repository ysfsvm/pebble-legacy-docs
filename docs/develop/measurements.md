# Measurements

How the speed of the user interface is measured, and what the numbers are.

Every number here is from one Pebble Time with the port on PebbleOS 4.47.
The stock firmware was never measured, so there is nothing to compare
with.

## How it is measured

The measurement build is the branch `probe/v4.47` of the firmware,
configured with `CONFIG_LEGACY_PERF_PROBE=y`. It is not for daily use.

1. The PC sends the watch a trigger.
2. The watch waits 5 seconds, enters airplane mode and waits 20 seconds.
3. The watch presses a fixed sequence of 41 keys by itself, three times,
   15 seconds apart.
4. The watch leaves airplane mode. The PC pulls the watch's log and reads
   the counters, the time of each frame and a sampling profile from it.

The key sequence:

| Keys | Screen |
| --- | --- |
| Back, 3 times | Watch face |
| Select | Launcher |
| Down 6 times, Up 6 times, 400 ms apart | Launcher, scrolling |
| Down 10 times, Up 10 times, 120 ms apart | Launcher, scrolling fast |
| Select, then 4 s | The first app |
| Back, 2 times | Watch face |
| Down | Timeline |
| Back | Watch face |

Time is measured in steps of 4 ms.

With `plt`, see {doc}`tools`:

```console
$ plt build <image> -D CONFIG_LEGACY_PERF_PROBE=y
$ plt watch flash <image>
$ plt bench run <image>
$ plt bench report <image>
```

`plt bench run` sends the trigger, waits for the watch to come back and
checks each run. `plt bench report` prints one line per run and the mean
of the runs that counted.

## When a run counts

Before the runs:

- The watch is off the charger, at 40 to 90 % charge, lying on a table.
- The watch face, the backlight setting and the app list are the same as
  for the run it is compared with.
- The watch was left alone for 2 minutes after the install.

A run counts when:

- every key landed on the expected screen. The watch logs the name of the
  screen after each key, and the names are compared with a reference run.
- there are 41 keys, no restart, and the log's time does not jump.
- no notification or call arrived.

A run that fails one of these is dropped. Two builds are compared only
when one change separates them.

## A frame today

Mean per frame over three runs that counted, on the measurement build
with both display options below on.

| Part | Time |
| --- | --- |
| The app on screen draws its window | 34.7 ms |
| The compositor | 1.6 ms |
| Transfer to the display | 23.9 ms |
| of it, waiting for the FPGA between lines | 13.2 ms |
| Waiting for the display before the frame | 0.9 ms |

The animations are made for 33 ms a frame. Drawing alone takes longer.

5.0 % of the profile's samples are in interrupt handlers.

## Where the drawing time goes

From a profile of the drawing alone. Its runs did not count, because one
key landed on another screen, so only the shares are used.

| Code | Share of the drawing |
| --- | --- |
| 64-bit divisions in `integer_sqrt`, used for stroked lines and their round caps | About 8 % |
| Heap allocation (`pbl_heap_alloc`) | About 8 % |

Both are PebbleOS code that Core's watches run too.

## Two display options

Each was measured against the build without it, three runs each.

| Option | Effect |
| --- | --- |
| `CONFIG_DISPLAY_ICE40LP_STM32_FAST_LINE` | Samples in interrupt handlers fall from 5.4 to 5.0 %. Drawing time does not change beyond the spread between runs |
| `CONFIG_DISPLAY_ICE40LP_STM32_BUSY_EDGE` | The wait before a frame falls from 2.1 to 0.9 ms, drawing from 36.6 to 34.7 ms |

Both are on for all three watches.

## Not measured

- The stock firmware on the same watch
- Battery life and the current in deep sleep
- Anything while a phone is connected
- The real clock frequency of the processor
