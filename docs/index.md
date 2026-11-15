# PebbleOS for legacy watches

[PebbleOS](https://github.com/coredevices/PebbleOS) is the open firmware of
today's Pebble watches. This project runs it on the Pebble Time from 2015,
which Core Devices' firmware does not support.

:::{important}
This is a community port. Core Devices, Google and Pebble Technology did
not make it and do not support it.
:::

## State

| Watch | State |
| --- | --- |
| Pebble Time | Runs on a watch |
| Pebble Time Steel | Builds. Never run on a watch |
| Pebble Time Round | Builds. Never run on a watch |

{doc}`use/watches` has the details.

## Where to go

::::{grid} 1 1 2 2
:gutter: 3

:::{grid-item-card} What works
:link: use/watches
:link-type: doc

Each feature of the watch, and whether it was checked on one.
:::

:::{grid-item-card} Build and emulator
:link: develop/build
:link-type: doc

Build the firmware and test it without a watch.
:::

:::{grid-item-card} How the port works
:link: develop/port
:link-type: doc

What the port replaces, what it leaves alone, and where the code is.
:::

:::{grid-item-card} Design decisions
:link: develop/decisions
:link-type: doc

What differs from the stock firmware, and why.
:::
::::

## Before you install anything

A Pebble Time is sealed. It has no debug port to rescue it with.

The port replaces only the watch's normal firmware. The bootloader, the
recovery firmware and the factory data stay Pebble's. If a build does not
start, the watch falls back to the recovery firmware, and getting out of it
needs a Linux PC with Bluetooth Classic. A phone cannot do it.

There is no install guide yet.

## Source

| Repository | Content |
| --- | --- |
| [PebbleOS-legacy](https://github.com/ysfsvm/PebbleOS-legacy) | The firmware |
| [mobileapp-legacy](https://github.com/ysfsvm/mobileapp-legacy) | Core's phone app, with the changes these watches need |
| [PebbleOS-legacy-firmware](https://github.com/ysfsvm/PebbleOS-legacy-firmware) | Tools for building, testing and measuring |

The port started from Brian Silvestri's
[PebbleOS-legacy-watches](https://github.com/bjsilvest/PebbleOS-legacy-watches).
Most of the driver code is his.

```{toctree}
:caption: Use
:maxdepth: 1
:hidden:

use/watches
```

```{toctree}
:caption: Develop
:maxdepth: 1
:hidden:

develop/build
develop/port
develop/decisions
```
