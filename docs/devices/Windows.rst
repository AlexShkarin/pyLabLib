.. _generic_windows_devices:

Generic Windows devices
==============================

There is some support for generic Windows drivers for some devices.

Joysticks
------------------------------

Basic support for Windows-compatible joysticks / gamepads using WinMM. Since the driver only supports polling, the events (button/axis presses) are emulated using a separate polling loop. The main device class is :class:`pylablib.devices.Windows.Joystick<.joystick.Joystick>`. Since this library is a standard part of Windows, no additional software is required, apart from potential joystick drivers.

The code supports polling the joystick state (button and axes) as well as querying events::

    >> from pylablib.devices import Windows
    >> Windows.list_joysticks()
    {0: TDeviceInfo(name='Microsoft PC-joystick driver', id=(121, 17), nbuttons=10, naxes=2)}
    >> j=Windows.Joystick()
    >> j.get_buttons()
    [False, False, False, False, False, False, False, False, False, False]
    >> j.start()  # start polling loop in a separate thread
    >> j.get_events()  # get the recent events (since the last get_events call)
    TJoystickEvent(kind='axis', index=0, old=0, new=-1, timestamp=1000000000.000),
    TJoystickEvent(kind='axis', index=0, old=-1, new=0, timestamp=1000000001.000)]
    >> j.stop()  # stop the polling loop when done