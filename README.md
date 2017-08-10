# Xbox-async

Controller support in python using asyncio. This script parses the output
from xboxdrv to determine joystick events.

Creates a child xboxdrv process so will require root permission or proper udev setup to run.

## Udev Setup
Here's a simple udev rule that allows users in the group `input` to access usb devices.

`/etc/udev/rules.d/99-xbox.rules`
```SUBSYSTEM=='usb',GROUP='input',MODE='0666'```

## Dependencies
* python 3.5+
* xboxdrv
