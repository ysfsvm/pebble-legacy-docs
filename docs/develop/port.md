# How the port works

The port adds the Pebble Time as boards to PebbleOS. It is a series of
commits on top of a Core Devices release tag. Core's own boards build to
the same objects with and without it.

## What it replaces

Only the normal firmware. Three things on the watch stay Pebble's and are
never written:

- the bootloader
- the recovery firmware (PRF)
- the factory data

## How the watch starts

1. Pebble's bootloader runs. It sits in the first 16 KiB of the internal
   flash.
2. It starts the firmware at `0x08004000`.
3. If the firmware fails to start three times, the bootloader starts the
   recovery firmware instead and erases the normal firmware.

Holding Back, Select and Up for 5 seconds does the same as step 3.

A firmware update is staged in the external flash. The bootloader copies it
into place at the next start.

## Flash layout

The external flash is 16 MiB. The layout is the stock one.

| Range | Content | Owner |
| --- | --- | --- |
| `0x000000` | Flash logs, pairing storage, time zones | Port |
| `0x0c0000` | Pairing storage of the stock firmware | Pebble, read only |
| `0x0e0000` | Factory data | Pebble, read only |
| `0x100000` | Staged firmware update | Shared with the bootloader |
| `0x200000` | Recovery firmware | Pebble, read only |
| `0x300000` | System resources, two banks | Port |
| `0x400000` | Filesystem | Port |

The firmware asserts before it writes a read-only range. The flash driver
also locks the recovery firmware's range in the chip at every start.

## State shared with Pebble's firmware

The bootloader and the recovery firmware read state the port leaves
behind. The port keeps each item as the stock firmware had it.

| State | Why it matters |
| --- | --- |
| Clock (RTC) set-up | The recovery firmware resets in a loop with another set-up |
| RTC backup registers | Boot flags, reboot reason, stuck buttons, time zone, compass calibration |
| Flash erase marker | An erase cut off by a reset is finished at the next start |
| Power chip settings | Charger voltage and limits |
| Firmware checksum | The bootloader checks a staged update with it |

Change one of these only after reading every piece of stock code that uses
it.

## Hardware and drivers

| Part | Chip | Driver |
| --- | --- | --- |
| Processor | ST STM32F439 | `soc/stm32` |
| Flash | Spansion S29VS, 16 MiB | `drivers/flash/s29vs.c` |
| Display | Lattice iCE40LP FPGA in front of the panel | `drivers/display/ice40lp` |
| Bluetooth | TI CC2564B | `drivers/bluetooth/cc2564.c` |
| Accelerometer | Bosch BMI160 | `drivers/imu/bmi160` |
| Compass | NXP MAG3110 | `drivers/imu/mag3110` |
| Power and charger | Maxim MAX14690 | `drivers/pmic/max14690.c` |
| Microphone | PDM on the I2S interface | `drivers/audio` |

The board files are in `boards/snowy` and `boards/spalding`. The
[board page](https://github.com/ysfsvm/PebbleOS-legacy/blob/main/docs/boards/snowy/index.md)
lists every pin.

## Changes to shared code

Some of PebbleOS' shared code needs to behave differently on these watches.
Each such change is behind an option in `Kconfig.legacy`. The option is off
for Core's boards.

Every change is checked by building three of Core's boards with and without
the port and comparing the objects. They must be identical.

## What is not done yet

The port is not in the shape PebbleOS wants for its own boards.

| Today | Where it has to go |
| --- | --- |
| The devices are described in C tables in the board files. Only the flash partitions are in the devicetree | Every device in the devicetree, with bindings that follow Linux's for the STM32F4 |
| The drivers call ST's Standard Peripheral Library | No vendor library. Drivers write the registers themselves |
| Some drivers reach into each other | Each driver implements one of PebbleOS' driver classes |

Until then the port lives in this fork.
