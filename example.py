#!/usr/bin/env python3
# Example usage of xbox-async library
import xbox_async
from xbox_async import Button
import asyncio
import sys
import signal

def trigger_l_handle(val):
    if val is 255:
        print("LTrigger maxed!")

def trigger_r_handle(val):
    if val is 255:
        print("RTrigger maxed!")

def stick_l_handle(x, y):
    print("Left stick: (%f, %f)" % (x, y))

def stick_r_handle(x, y):
    print("Right stick: (%f, %f)" % (x, y))

def quit():
    sys.exit(0)

async def example():
    joy = await xbox_async.Joystick.create()
    joy.on_button(Button.A, lambda: print('A'))
    joy.on_button(Button.B, lambda: print('B'))
    joy.on_button(Button.X, lambda: print('X'))
    joy.on_button(Button.Y, lambda: print('Y'))
    joy.on_button(Button.L3, lambda: print('L3'))
    joy.on_button(Button.R3, lambda: print('R3'))
    joy.on_button(Button.LB, lambda: print('LB'))
    joy.on_button(Button.RB, lambda: print('RB'))
    joy.on_button(Button.DpadU, lambda: print('DpadU'))
    joy.on_button(Button.DpadD, lambda: print('DpadD'))
    joy.on_button(Button.DpadL, lambda: print('DpadL'))
    joy.on_button(Button.DpadR, lambda: print('DpadR'))
    joy.on_button(Button.Back, lambda: print('Back'))
    joy.on_button(Button.Start, lambda: print('Start'))
    joy.on_button(Button.Guide, lambda: print('Guide'))
    joy.on_button(Button.LTrigger, trigger_l_handle)
    joy.on_button(Button.RTrigger, trigger_r_handle)
    joy.on_button(Button.LStick, stick_l_handle)
    joy.on_button(Button.RStick, stick_r_handle)

    while True:
        joy = await joy.read()

    joy.close()

if __name__ == "__main__":
    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, quit)
    loop.run_until_complete(example())
