# Hardware reference

Which chip is where on the Pebble Time, and what the port does with it.
The pins are from `boards/snowy/snowy.c`, `boards/snowy/snowy.h` and the
drivers.

The Time Steel is the same board. The Time Round differs in the
[last section](#time-round).

## Watches

| | Pebble Time | Time Steel | Time Round |
| --- | --- | --- | --- |
| Board | `snowy@dvt` | `snowy@s3` | `spalding` |
| Platform | Basalt | Basalt | Chalk |
| Display | 144 x 168 | 144 x 168 | 180 x 180, round |
| Battery model | 144 h | 204 h | 44 h |
| Low-power mode at | 3 % | 2 % | 7 % |
| Emulator machine | `pebble-snowy-bb` | `pebble-snowy-bb` | `pebble-s4-bb` |

## Chips and pins

| Part | Chip | Bus | Pins |
| --- | --- | --- | --- |
| Processor | ST STM32F439, 1 MiB flash, 192 KiB RAM, 64 KiB CCM | | |
| Flash | Spansion S29VS, 16 MiB parallel NOR | FMC bank 1 at `0x60000000` | Ports D and E, PB7; reset PD2 |
| Display | Lattice iCE40LP FPGA in front of the panel | SPI6, DMA2 stream 5 | SCK PG13, MOSI PG14, CS PG8, CRESET PG15, CDONE PG9, BUSY PG10 |
| Display rails | | GPIO | 6.6 V PF3, 4.5 V PF2 |
| Bluetooth | TI CC2564B | USART1, 921600 baud, flow control | TX PA9, RX PA10, CTS PA11, RTS PA12, shutdown PB12 |
| Accelerometer | Bosch BMI160 | SPI1, 3 MHz | SCK PA5, MISO PA6, MOSI PA7, CS PA4, interrupts PG5 and PG6 |
| Compass | NXP MAG3110 | I2C1 at `0x0e` | Data ready PF14 |
| Power and charger | Maxim MAX14690 | I2C1 at `0x28` | Interrupt PG7, battery voltage on ADC channel 1 (PA1) |
| I2C1 | | 400 kHz | SCL PB6, SDA PB9 |
| Light sensor | Phototransistor | ADC channel 2 | Input PA2, supply PA3 |
| Backlight | LED | TIM12 channel 1, 256 Hz | PB14 |
| Vibration | Motor on an H-bridge | TIM10 channel 1, 22 kHz | PWM PB8, enable PF4 |
| Microphone | PDM | SPI2 as I2S, DMA1 stream 3 | Clock PB10, data PB15 |
| Buttons | | GPIO, active low | Back PG4, Up PG3, Select PG1, Down PG2 |
| Debug console | | USART3, 115200 baud | TX PC10, RX PC11 |
| 32.768 kHz output | | MCO1 | PA8, to the Bluetooth controller and the FPGA |

The debug console cannot be reached on a sealed watch.

The display SPI is set up for 16 MHz while the FPGA is programmed and
32 MHz for frames. From the 48 MHz bus clock that comes out as 12 and
24 MHz.

## Clocks

| Clock | Value |
| --- | --- |
| System | 96 MHz, from the 16 MHz internal oscillator through the PLL (M 16, N 192, P 2) |
| Buses | AHB 96 MHz, APB1 24 MHz, APB2 48 MHz |
| Internal flash | 4 wait states, prefetch off |
| Microphone | 51.2 MHz from the I2S PLL, 1.024 MHz PDM clock, 16 kHz after the filter. On only while recording |
| RTC | 32.768 kHz from outside (LSE in bypass mode), prescalers 127 and 255: 256 steps a second |

## Power

The MAX14690 feeds the watch and charges the battery. The port writes the
stock settings at every start and every time the charger is plugged in.

| Setting | Value |
| --- | --- |
| Charge voltage | 4.30 V |
| Stop and restart | Automatic. Restart 70 mV below the charge voltage |
| Precharge | Below 3.00 V, at a tenth of the charge current |
| Charge done | At a tenth of the charge current |
| Timers | Fast charge 300 min, precharge 30 min, maintain 15 min |
| Interrupt | Charger plugged or unplugged, debounced for 1 s |
| LDO2 | Display FPGA. On from the start |
| LDO3 | Microphone. On only while recording |
| Power off | `0xb2` to register `0x1f` |

## RTC backup registers

The stock layout. The bootloader and the recovery firmware read some of
them.

| Register | Content |
| --- | --- |
| DR0 | Boot bits |
| DR1 | Stuck buttons |
| DR2 | Bootloader version |
| DR3, DR4 | Time and interval |
| DR5 to DR8 | Reboot reason |
| DR10 | Factory reset under way. Added by the port |
| DR11 | Flash erase under way |
| DR12 to DR16 | Time zone |
| DR17, DR18 | Compass calibration |
| DR19 | Last app |

The flash layout is on {doc}`port`.

## On the board, not used

Pins from Pebble's board file. The port does not set them up.

| Part | Pins |
| --- | --- |
| Smartstrap connector | Data PE1 (UART8), supply enable PF13, sense PE0 |
| Apple authentication chip | I2C2: SDA PF0, SCL PF1 |
| Debug console wake-up | PC12 |

## Time Round

Same pins and chips. These values differ:

| Item | Pebble Time, Time Steel | Time Round |
| --- | --- | --- |
| Framebuffer | Rectangular | Round, with a mask per row |
| FPGA image | `snowy_framebuffer.fpga` | `spalding_framebuffer.fpga` |
| 6.6 V display rail | Open drain | Push-pull |
| Accelerometer axes | X and Y swapped | Not swapped, Y inverted |
| Compass axes | X and Y swapped, both inverted | Not swapped, Y inverted |
| Light sensor table | Measured on a Pebble Time | Measured on a Time Round |
| Battery warnings | PebbleOS defaults | At 34 % and 20 % |
