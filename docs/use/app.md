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
| A bundle's files are installed after an update, with progress on the watch's card | The emoji pack, see {doc}`update` |
| New releases of the port are offered as updates, and the watch's card shows the build it runs | Core's app knows only Pebble's and Core's firmware |

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
| **Look for Port Builds Automatically** | Off: the app looks for new releases only on **Check for Updates** |

## Battery Life

The watch sends a record every hour: battery level and voltage, backlight,
vibration, notifications, calls, buttons, display updates, CPU, Bluetooth
connection, the watchface and some settings. The app keeps the records on
the phone for 180 days.

The page shows the level and the voltage over up to seven days, the
watchface each hour with the store's battery impact, tags that mark busy
hours, hourly activity, totals, and the full record of any hour. Touch a
chart and drag sideways to read an hour. It shows only what the watch
measured; there is no estimate of days per charge.

The first record comes one hour after the watch starts.

The battery level comes from the battery voltage. It is noisy from hour to
hour.
