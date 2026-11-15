# Known issues

What is broken or rough today, on the Pebble Time with the port on
PebbleOS 4.47. What does not work at all is on {doc}`watches`.

## Recovery

- **A build that does not start leaves the watch in the recovery
  firmware.** Core's phone app cannot get it out. Have a Linux PC with
  Bluetooth Classic ready before you install anything. See {doc}`recover`.
- **Recovery was not run with the port on PebbleOS 4.47.** It was run three
  times with the port on PebbleOS 4.46. Going back to the stock firmware
  was never run.

## Bluetooth

- **iPhone was not tried.**
- **Transfers are slow.** About 13 KiB/s. A firmware update takes a few
  minutes.
- **The phone app does not offer firmware updates for the port.** A new
  build is sideloaded. See {doc}`update`.

## Display

- **Animations lose frames.** A frame of a system app takes about 35 ms to
  draw. The animations are made for 33 ms. See
  {doc}`../develop/measurements`.
- **Some emoji show as a box.** The firmware holds 136 color emoji. The
  rest come from the emoji pack, a file on the watch. A factory reset
  removes it, and the phone app installs it again after the next firmware
  update.

## Battery, sensors, storage

- **Battery life was not measured.** While idle the watch spends 94 to
  96 % of an hour in deep sleep. The current was not measured.
- **The accelerometer was not checked.** No feature that uses motion was
  tried one by one.
- **The watch holds at most 96 files.** The filesystem has 96 pages of
  128 KiB and every file takes at least one: apps, their resources and the
  system's databases. How many apps that leaves was not counted.

## Time Steel and Time Round

- **Neither has run on a watch.** The Time Round's display code has never
  run at all. Do not install on a watch you cannot afford to lose.

## For developers

- **There is little room left.** A release build for the Pebble Time fills
  91 % of the firmware's flash, 88 % of the kernel's RAM and 99 % of the
  system resources.
- **The wakeup timer breaks Bluetooth.** With
  `CONFIG_TIMER_STM32_RTC_WUT=y` Bluetooth often does not start again
  after being switched off, and Settings > Bluetooth stays on "Enabling".
  Leave the option off.
- **The clock can read one step back.** The timer driver then keeps the
  earlier value and logs a warning with the RTC's registers. The cause is
  not known.
- **Debug lines are missing from the watch's log.** The log in flash keeps
  info and above. A diagnostic build needs
  `CONFIG_LOG_BACKEND_FLASH_LEVEL_DEBUG=y`.
