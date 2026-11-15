# Tools

`plt` builds, tests, installs and measures the port. It keeps a registry of
built images and installs on a watch only an image whose emulator tests are
on record. The source and the full manual are in
[pebble-legacy-tools](https://github.com/ysfsvm/pebble-legacy-tools).

## Install

You need Linux and Python 3.11 or newer. The builds and tests run in Core's
build container with `podman`, see {doc}`build`.

```console
$ git clone https://github.com/ysfsvm/pebble-legacy-tools.git
$ cd pebble-legacy-tools
$ pip install '.[watch]'
$ plt --help
```

The `watch` extra installs what talks to a watch: `libpebble2`, `pypng`
and `websocket-client`. Every command has `--help`.

## Settings

Each setting is read from the environment, then from the file `plt.conf`
in `$XDG_CONFIG_HOME` or `~/.config` (`PLT_CONFIG` names another), then
takes its default. The file holds `KEY=VALUE` lines.

| Setting | Default | Meaning |
| --- | --- | --- |
| `PLT_HOME` | `~/pebble-legacy` | Data directory |
| `PLT_IMAGES` | `<home>/images` | Built images and `registry.json` |
| `PLT_LOGS` | `<home>/logs` | Logs of builds, emulator runs and the watch |
| `PLT_BENCH` | `<home>/bench` | Measurement results and reference screens |
| `PLT_WORKTREE` | the current directory | Firmware checkout, when `--wt` is not given |
| `PLT_BASE_WORKTREE` | `base` next to the worktree | Unchanged checkout of Core's release, for `plt gate --objects` |
| `PLT_QEMU` | `qemu-system-arm` | The patched QEMU. Give an absolute path |
| `PLT_CONTAINER` | `ghcr.io/coredevices/pebbleos-docker:v10` | Build container, when the firmware's CI files name none that is present |
| `PLT_WATCH_BT` | none | The watch's Bluetooth Classic address, for `plt watch recover` |
| `PLT_PYTHON` | the Python that runs `plt` | Python with the `watch` packages |

The manual lists three more, for the container runs. `plt` never pulls a
container: pull it with `podman pull` first.

## images

```console
$ plt images
$ plt images add NAME BUNDLE.pbz LOG.DICT.JSON [ELF]
$ plt images role NAME current|recovery
```

Without arguments: every image with its version, checksum, options and
recorded tests. `add` registers a bundle built outside `plt`; it has no
commit, so `plt emu test` cannot test it. `role` marks the image the watch
runs, or the one `plt watch recover` installs.

## build

```console
$ plt build NAME [-D OPTION=VALUE ...] [--wt PATH]
```

Builds the checkout's commit for `snowy@dvt` with the release options from
an empty build directory, and registers the bundle, its log dictionary and
its ELF under NAME. It refuses uncommitted changes, a name that exists, and
a bundle that calls itself `-dirty` or names another commit.

## emu

```console
$ plt emu test NAME [--update-only] [--wt PATH]
$ plt emu try [--wut] [--perf f0|f2] [--hw] [-D OPTION=VALUE ...] [--wt PATH]
```

`emu test` runs the checks of {doc}`testing` on a built image and records
them: two emulator builds, the integration tests on each, then the update
test. The checkout must be at the image's commit. `--update-only` repeats
the update test.

`emu try` builds the checkout as it is, uncommitted changes included, and
runs the integration tests. Nothing is recorded. `--wut` takes timer events
from the RTC wakeup timer, `--perf` plays the measurement keys instead, and
`--hw` only compiles the watch build.

## watch

```console
$ plt watch status
$ plt watch log [GEN]
$ plt watch shot [OUT.png]
$ plt watch flash NAME [--force WHY]
$ plt watch recover [NAME]
```

These go through Core's phone app on an Android phone over `adb`, with the
app's developer connection on. `status` prints the firmware the watch
reports. `log` saves and decodes the flash log of one start (0 is the
current one). `shot` saves the screen. `flash` installs an image, see
below. `recover` installs from the PC over Bluetooth Classic, without the
phone, see {doc}`../use/recover`.

## bench

```console
$ plt bench run NAME [--log DUMP.bin]
$ plt bench report NAME...
$ plt bench reference NAME
```

`run` starts a measurement on the watch, waits about 5 minutes, then pulls
and checks the log. The image must be a measurement image and the one the
watch runs. `report` prints the tables of {doc}`measurements`. `reference`
stores the screens of a run as the ones later runs must show.

## gate

```console
$ plt gate [--objects] [--wt PATH]
```

Lists the source files the port changes that may still change Core's own
boards (`asterix`, `obelix@pvt`, `getafix@dvt2`). `--objects` builds the
three boards from Core's release and from the port and compares every
object. It takes about 10 minutes and decides.

## recover

```console
$ python -m plt.recover install ADDRESS BUNDLE.pbz [--windows N]
$ python -m plt.recover log ADDRESS PREFIX
$ python -m plt.recover alive ADDRESS [--minutes M]
$ python -m plt.recover coredump ADDRESS OUT [--windows N]
$ python -m plt.coredump DUMP
```

These reach a watch from the PC without the phone or the registry.
{doc}`../use/recover` has the steps.

## What the tool refuses

`plt watch flash`:

- refuses an image whose emulator tests and update test are not recorded
  as passed, and refuses while no recovery image is set. `--force WHY`
  overrides both and records the reason.
- refuses an image file whose SHA-256 differs from the registered one, and
  a watch that does not answer. These cannot be overridden.
- saves the watch's flash log before it installs. If that fails, it
  prints `log backup: FAILED` and goes on.
- after the restart, asks the watch for its version up to twelve times,
  20 s apart. Only the image's version counts as an install; anything else
  is recorded as failed.

No command builds or writes a recovery firmware, a bootloader or factory
data.
