# Contributing

What a change to the firmware must satisfy to be accepted.

The port follows
[PebbleOS' contribution guidelines](https://github.com/ysfsvm/PebbleOS-legacy/blob/main/docs/community/contributing.md).
This page lists what matters most and what the port adds.

## Commits

- One topic per commit. The tree builds after every commit.
- The title is `area: short description`. The body says what was wrong and
  what changed.
- Every commit is signed off with your own name and the email address you
  commit with: `git commit -s`. The sign-off certifies the
  [Developer Certificate of Origin](https://developercertificate.org/).
- A commit made with the help of an LLM tool carries the trailer
  `Assisted-by: LLM`. Do not name the tool, the model or the vendor, and
  remove any `Co-Authored-By` line the tool adds. A tool never signs off.
- `gitlint` passes.

```text
area: short description

What was wrong. What changed.

Assisted-by: LLM
Signed-off-by: Your Name <you@example.com>
```

Files that came from Brian Silvestri's port keep his copyright line.

## Shared code stays Core's

Core's own boards must build to the same objects with and without the
port.

- A change to code that Core's boards also build goes behind an option in
  `Kconfig.legacy`. The options there are open only to boards that select
  `LEGACY_WATCH`.
- A new driver or board file needs no option. Core's boards do not build
  it.
- Before a change is merged, three of Core's boards are built with and
  without it and compared object by object. No object may differ. See
  {doc}`testing`.

## Pebble's parts stay Pebble's

- Nothing writes the bootloader, the recovery firmware or the factory
  data.
- No recovery firmware build (`--variant=prf`).
- The clock set-up, the RTC backup registers, the flash layout and the
  power chip settings keep the stock layout. A change to one of them is
  accepted only after every piece of stock code that reads it was read.
  The list is on {doc}`port`.

## Tests

Before a change is sent:

1. The release build of `snowy@dvt` builds.
2. The emulator build passes the integration tests: `14 passed`.
3. The update test passes.
4. A change to the timer also passes with the wakeup timer build
   (`CONFIG_TIMER_STM32_RTC_WUT=y`).

{doc}`testing` has the commands.

A change to code that the emulator cannot run needs a run on a watch.
PebbleOS asks for proof from real hardware for drivers and connectivity:
logs, measurements or captures. Say in the pull request where the change
ran: on a watch, in the emulator, or built only.

New behaviour comes with a test where that is feasible.

## Code

- `clang-format` for C, `ruff` for Python.
- Comments are short. The long explanation goes in the commit message.
- No issue numbers in the code. They go in the commit message.
- Routine log lines use `PBL_LOG_DBG`. `PBL_LOG_INFO` is for events worth
  seeing in a default log, and never for something that repeats in normal
  use.

## Pull requests

- Keep them small. A big pull request made with an LLM tool is not
  reviewed unless it was agreed first.
- Text is in English.
- A change to what the user sees comes with a picture or a video.
