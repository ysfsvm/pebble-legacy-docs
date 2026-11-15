# Phone app

The watch needs a phone app that speaks Bluetooth LE to PebbleOS. This
project uses [Core Devices' app](https://github.com/coredevices/mobileapp)
with a few changes, in
[mobileapp-legacy](https://github.com/ysfsvm/mobileapp-legacy).

Only the Android app was built and used.

## What the changes do

| Change | Why |
| --- | --- |
| A legacy watch running PebbleOS is treated as a PebbleOS watch | Core's app takes every Pebble Time for a watch on the stock firmware |
| Watch settings follow the hardware | No backlight color or touch settings on a watch without them |
| A local Battery Life page | Core's page is drawn by Core's server |
| A bundle's files are installed after an update | The emoji pack, see {doc}`update` |

## Get it

Download the APK of a release, see {doc}`download`. Or build it:

```console
$ git clone --recurse-submodules https://github.com/ysfsvm/mobileapp-legacy.git
$ cd mobileapp-legacy
$ cp androidApp/src/google-services-dummy.json androidApp/src/google-services.json
$ ./gradlew :androidApp:assembleDebug
```

The APK is `androidApp/build/outputs/apk/debug/androidApp-debug.apk`.

Every push to the `legacy` branch is also built by GitHub Actions. The APK
is an artifact of the run.

:::{note}
The app has the same package name as Core's app from the store. Android
does not install one over the other. Remove Core's app first.
:::

## What does not work

A self-built app has no sign-in. Everything that needs Core's servers is
off, among them the account and the hosted Battery Life page.

## Settings worth knowing

| Setting | Effect |
| --- | --- |
| **Show legacy watches in BLE scan** | Lists Pebble Time family watches in the Bluetooth LE scan. Turn it on if the watch does not show up when pairing |
| **Always send notifications** | Off: a notification is not sent while the phone's screen is on |
| **Show debug options** | Shows the **Debug** entry in a watch's menu |

## Battery Life

The watch sends a record every hour: battery level and voltage, time spent
asleep, backlight time, Bluetooth connection time. The app keeps the
records on the phone and draws them.

The first record comes one hour after the watch starts. An estimate of
days per charge needs a day of records.

The battery level comes from the battery voltage. It is noisy from hour to
hour.
