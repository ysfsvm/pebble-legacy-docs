# FAQ

## Is it safe?

Less safe than staying on the stock firmware.

The port never writes the bootloader, the recovery firmware or the factory
data. A build that does not start falls back to Pebble's recovery firmware.
Getting out of it needs a Linux PC with Bluetooth Classic and the recovery
tool.

The port has run on one Pebble Time. The way back from the recovery
firmware was run three times with the port on PebbleOS 4.46, and not yet
on 4.47. Read {doc}`recover` before you install anything.

## Can I go back to the stock firmware?

It should be possible: the port replaces only the normal firmware, and a
stock bundle can be installed from the recovery firmware the same way as
the port. This was never run. See {doc}`recover`.

A factory reset does not bring the stock firmware back. It wipes apps and
settings and keeps the port.

## Does the old Pebble phone app work?

No. It connects over Bluetooth Classic, and PebbleOS speaks Bluetooth LE
only. Use Core's app with the changes these watches need:
[mobileapp-legacy](https://github.com/ysfsvm/mobileapp-legacy).

## Does it work with an iPhone?

Not tried. Everything on this site was checked with an Android phone.

## Do my apps and watchfaces work?

Apps see the same platform as under the stock firmware: Basalt, a
144 x 168 color display. Installing apps was checked on PebbleOS 4.46
only. There is no list of apps that were tried.

## How long does the battery last?

Not measured.

While idle the watch spends 94 to 96 % of an hour in deep sleep, on one
watch with PebbleOS 4.47. The current in deep sleep was not measured.

Charging works, with the stock charger settings.

## Why does pairing ask for a code?

The watch's Bluetooth controller is from before LE Secure Connections. The
watch shows six digits and you type them on the phone. See
{doc}`../develop/decisions`.

## Does it run on a Time Steel or a Time Round?

Both build. Neither has run on a watch.

The Time Steel is the same board with another battery. The Time Round has
its own display code, which has never run. Do not install on a watch you
cannot afford to lose.

The Pebble 2 and the original Pebble are not part of this port.

## What is broken?

See {doc}`known-issues` and {doc}`watches`.
