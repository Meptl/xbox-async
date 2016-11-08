#!/usr/bin/env python3
# Example usage of xbox-async library
import xbox_async
from xbox_async import Button
import asyncio
import sys
import signal

def triggerHandle(val):
    if val is 255:
        print('Left trigger maxed!')

def stickHandle(x, y):
    deadzone = 4000
    if abs(x) > deadzone or abs(y) > deadzone:
        print("Stick at (%d, %d)" % (x, y))

def quit():
    sys.exit(0)

async def example():
    joy = await xbox_async.Joystick.create()
    joy.onButton(Button.A, lambda: print('A pressed'))
    joy.onButton(Button.LTrigger, triggerHandle)
    joy.onButton(Button.LStick, stickHandle)
    joy = await joy.init()
    joy.close()

if __name__ == "__main__":
    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, quit)
    loop.run_until_complete(example())
