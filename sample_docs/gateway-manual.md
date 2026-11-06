# Larkfield LF-200 Home Gateway: User Manual

The Larkfield LF-200 is a fictional home gateway used as sample content for this project. It combines a fibre modem, a dual-band wireless router and a four-port network switch in one unit.

## What's in the box

The box contains the LF-200 gateway, a 12 V power adapter, a two-metre Ethernet cable, a fibre patch lead and a printed quick-start card. Contact your supplier if anything is missing. Keep the original packaging for the length of the warranty, because returns must be shipped in it.

## Front panel lights

The Power light is solid white when the unit is running and flashes amber during a firmware update. The Link light is solid green when the fibre connection is established and flashes green while it is negotiating. The Wireless light is solid blue when at least one wireless band is enabled. A solid red Link light means no signal is reaching the unit from the wall socket.

## First-time setup

Connect the fibre patch lead between the wall socket and the port marked FIBRE, then connect the power adapter and press the power button. Wait about three minutes for the Link light to turn solid green. Connect a computer to any LAN port, or join the wireless network printed on the label underneath the unit, then open http://192.168.50.1 in a browser. Sign in with the admin password printed on the same label. You will be asked to choose a new admin password before you can change any settings.

## Wireless network settings

The LF-200 broadcasts on both 2.4 GHz and 5 GHz under a single network name by default, and steers each device to the better band automatically. To give each band its own name, open Wireless, then Advanced, and turn off Band Steering. The 2.4 GHz band reaches further through walls, while the 5 GHz band is faster at short range. Security defaults to WPA3 with WPA2 fallback for older devices.

## Guest network

The guest network gives visitors internet access while keeping them away from your own computers, printers and storage. Open Wireless, then Guest, turn on Enable Guest Network and choose a password. You can set it to switch off automatically after 4, 12 or 24 hours. Devices on the guest network cannot see each other or anything on the main network.

## Parental schedules

Family Time lets you pause internet access for chosen devices at set times. Open Family, then Schedules, select a device or a group of devices, and mark the hours when access should be paused. A typical use is blocking tablets and game consoles overnight or during homework. Schedules follow the clock set under System, so check the time zone there first. Devices stay connected to the local network during a pause, but they cannot reach the internet.

## Port forwarding

Port forwarding sends traffic arriving from the internet to one device on your network, which is needed for game servers and some security cameras. Open Network, then Port Forwarding, and enter the external port, internal port, protocol and the device's address. Give the device a reserved address under Network, then DHCP Reservations, so that the rule keeps working after a restart. The gateway accepts up to 32 forwarding rules.

## Scheduled maintenance

The gateway checks for firmware updates every night and restarts itself at 03:00 local time if one has been installed. Internet access drops for about four minutes during this restart, and every connected device has to rejoin. To move or disable this window, open System, then Maintenance, and change Update Window. Disabling automatic updates is not recommended, because security fixes are delivered this way.

## Backing up and restoring settings

Open System, then Backup, and select Download Settings to save a file named lf200-settings.bak. Keep this file private, because it contains your wireless passwords. To restore it, use Upload Settings on the same page. A settings file can only be restored on firmware of the same major version or newer.

## Factory reset

Press and hold the recessed RESET button on the rear panel for 15 seconds, until the Power light flashes amber. Release the button and wait about five minutes for the unit to restart. A factory reset erases every setting, including your wireless network name, guest network, schedules and forwarding rules, and restores the admin password printed on the label. A reset does not remove installed firmware updates.

## Technical specifications

| Item | Value |
| --- | --- |
| Model | LF-200 |
| Fibre interface | GPON SC/APC, 2.5 Gbit/s downstream |
| LAN ports | 4 x 1 Gbit/s Ethernet |
| Wireless standard | Wi-Fi 6 (802.11ax), 2.4 GHz and 5 GHz |
| Power | 12 V DC, 2 A, 24 W maximum |
| Operating temperature | 0 to 40 degrees Celsius |
| Dimensions | 210 x 150 x 40 mm |
| Weight | 480 g |
