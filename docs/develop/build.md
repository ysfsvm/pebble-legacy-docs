# Build and emulator

Build the firmware and run it in an emulator. You do not need a watch.

Everything below was run on Linux with `podman`. `docker` takes the same
arguments.

## What you need

- `git` and `podman`
- 8 GB of free disk space
- The build container, 5 GB, pulled on first use:
  `ghcr.io/coredevices/pebbleos-docker:v13`

## Get the source

```console
$ git clone https://github.com/ysfsvm/PebbleOS-legacy.git
$ git clone https://github.com/ysfsvm/pebble-legacy-tools.git
$ cd PebbleOS-legacy
$ git submodule update --init --depth 1 --jobs 8
```

The second repository has the QEMU patches and the Bluetooth controller
stand-in used on this page. {doc}`tools` describes its tool, `plt`.

Clone `PebbleOS-legacy` with its full history. The emulator tests take the
watch's original bootloader from an old commit, and a shallow clone does
not have it.

## Start the build container

Run this in the directory that holds both clones:

```console
$ podman run --rm -it -v "$PWD":"$PWD" -w "$PWD/PebbleOS-legacy" \
    ghcr.io/coredevices/pebbleos-docker:v13 bash
# git config --system --add safe.directory '*'
# git update-index -q --refresh
# pip install -r requirements.txt
```

The rest of the page runs inside this shell.

The second line makes git look at the files again from inside the
container. Without it every build gets a version that ends in `-dirty`.

## Build a watch image

```console
# pbl configure --board snowy@dvt -DCONFIG_RELEASE=y
# pbl build
# pbl bundle
```

The result is `build/normal_snowy_dvt_<version>.pbz`. It holds the
firmware, the system resources and the emoji pack.

| Board | Watch | State |
| --- | --- | --- |
| `snowy@dvt` | Pebble Time | Runs on a watch |
| `snowy@s3` | Pebble Time Steel | Runs on a user's watch. Not tested here |
| `spalding` | Pebble Time Round | Builds. Never run on a watch |

:::{warning}
Do not build or install the recovery firmware (`--variant=prf`). The watch
keeps Pebble's own recovery firmware, and that is the only way back if a
build does not start.
:::

## Build the emulator image

```console
# pbl configure -b build-emu --board snowy@dvt -DCONFIG_SOC_STM32F4_EMULATED=y
# pbl build -b build-emu
```

`CONFIG_SOC_STM32F4_EMULATED` works around what the emulator does not
model. Never install this image on a watch.

## Build QEMU

The emulator is Core's QEMU with four patches from `pebble-legacy-tools`.
The build takes about three minutes.

```console
# cd ..
# git clone --filter=blob:none https://github.com/coredevices/qemu.git
# cd qemu
# git checkout 8a0a7c6
# git am ../pebble-legacy-tools/qemu/000*.patch
# mkdir ../qemu-build && cd ../qemu-build
# ../qemu/configure --target-list=arm-softmmu --disable-sdl --disable-tools \
    --disable-docs --disable-guest-agent --disable-werror --disable-gtk \
    --disable-curses --disable-vnc --disable-spice --disable-opengl \
    --disable-gnutls --disable-gcrypt --disable-nettle --disable-slirp \
    --disable-libusb --disable-usb-redir --disable-rust --disable-install-blobs
# ninja qemu-system-arm
# cd ../PebbleOS-legacy
```

| Patch | What it adds |
| --- | --- |
| 0001 | A serial port for the Bluetooth controller |
| 0002 | The random number generator |
| 0003 | The controller's flow control line after a reset |
| 0004 | The real sector layout of the watch's flash |

## Run the tests

The firmware expects a Bluetooth controller. The module `plt.fake_cc2564`
stands in for it. The tools package is not installed in the container;
`PYTHONPATH` makes the module runnable from the clone.

```console
# PYTHONPATH=../pebble-legacy-tools/src python3 -m plt.fake_cc2564 5556 /tmp/fake_cc2564.log &
# export PEBBLE_QEMU_BIN=$PWD/../qemu-build/qemu-system-arm
# pbl -b build-emu itest system ui notifications --bt-hci tcp:127.0.0.1:5556
```

The run takes about two minutes and ends with `14 passed, 2 deselected`.

## What the emulator does not cover

These parts of the watch have no model. A change to them has to be tried on
a watch.

- I2C, the power management chip and charging
- Accelerometer and compass
- Backlight and vibration (PWM)
- Microphone
- Deep sleep (STOP mode)
