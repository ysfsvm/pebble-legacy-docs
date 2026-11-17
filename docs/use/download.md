# Download

Each repository publishes its own releases.

| What | Where | File |
| --- | --- | --- |
| Firmware | [PebbleOS-legacy releases](https://github.com/ysfsvm/PebbleOS-legacy/releases) | `normal_<board>_<version>.pbz` |
| Phone app | [mobileapp-legacy releases](https://github.com/ysfsvm/mobileapp-legacy/releases) | `pebble-legacy-app-<tag>.apk` |

Every release has a `SHA256SUMS` file. Check a download with it:

```console
$ sha256sum -c SHA256SUMS_snowy_dvt.txt --ignore-missing
```

## Which firmware file

| Watch | File | State |
| --- | --- | --- |
| Pebble Time | `normal_snowy_dvt_<version>.pbz` | Runs on a watch |
| Pebble Time Steel | `normal_snowy_s3_<version>.pbz` | Runs on a user's watch. Not tested here |
| Pebble Time Round | `normal_spalding_<version>.pbz` | Builds. Never run on a watch |

The Pebble Time and Time Steel files carry the emoji pack. The Time Round
file does not.

The other files of a firmware release are for developers: the `.elf` has
the symbols, and the `loghash_dict.json` decodes the watch's log.

## The phone app

The APK is a debug build. It has the same package name as Core's app from
the store, so remove that one first. See {doc}`app`.

## Next

- The watch already runs this firmware: {doc}`update`.
- The watch runs Pebble's stock firmware: there is no guide for the first
  install yet.
