# Design decisions

What the port does differently from Pebble's stock firmware, and why.

## Pebble's bootloader and recovery firmware stay

The watch's debug pads are inside the sealed case. Without opening it, the
recovery firmware is the only way back when a build does not start.

Cost: the recovery firmware is from 2015 and talks Bluetooth Classic.
Core's phone app cannot drive it. Installing from it needs a PC.

The port never builds a recovery firmware of its own.

## Bluetooth LE only

PebbleOS has one Bluetooth stack, NimBLE, and it is LE only. The watch's
controller, a TI CC2564B, does both. The port uses its LE side.

Cost:

- The original Pebble app cannot connect.
- Transfers are slower: about 13 KiB/s.
- Pairing uses a code. The controller is from before LE Secure
  Connections, so the watch shows six digits to type on the phone.

## One watch for the phone, in both firmwares

The watch keeps its public Bluetooth address and advertises as a Pebble
Technology device, as it did under the stock firmware. At first start the
port imports the pairing the stock firmware stored.

A phone paired under the stock firmware sees the same watch.

Cost: no LE privacy. The address on the air is the real one.

## The clock keeps the stock set-up

The recovery firmware reads the watch's clock (RTC) and expects the stock
configuration: 256 steps a second. With another configuration it resets in
a loop, and the watch is left without a working recovery.

So the port's timer has 256 steps a second, 3.9 ms each.

Cost: a 1 ms sleep takes 12 to 16 ms.

## Timer events come from the RTC alarm

The port can wake the processor with the RTC alarm or with the RTC wakeup
timer. It uses the alarm.

With the wakeup timer the kernel locked interrupts for 60 µs on most ticks.
The Bluetooth controller's replies lost bytes and Bluetooth did not come
back after being switched off.

## Full emoji from a pack file

The system resources fill their flash region. Only 136 color emoji fit.

The rest are in a pack file of 360 KB on the watch's filesystem. The
Pebble Time and Time Steel bundles carry the pack, and the phone app installs it after an
update. Without the pack the watch draws the 136.

## Factory reset keeps the firmware

In PebbleOS a factory reset ends in the recovery firmware. On these watches
that is Pebble's, and it would install the stock firmware again.

The port wipes the filesystem and keeps the firmware.

## The Bluetooth controller is off while Bluetooth is off

In airplane mode, and while the watch lies still, the controller is held in
shutdown. It should draw about 1 µA there instead of tens. This was not
measured on a watch.

Cost: Bluetooth takes about a second to come back.

## Smaller choices

| Choice | Reason |
| --- | --- |
| Backlight capped at 80 % | A margin. The current at full duty was not measured |
| Compass calibration survives a restart | It is kept in the RTC backup registers, as stock did |
| Stock language packs load | The community packs were built for the stock layout |
| Certification screen shows Pebble's IDs | The stock values, plus ratings from the FCC filing |
| Charger settings are the stock ones | 4.30 V, automatic stop and restart |
