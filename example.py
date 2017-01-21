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
    print("Stick at (%f, %f)" % (x, y))

def quit():
    sys.exit(0)

async def example():
    joy = await xbox_async.Joystick.create()
    joy.on_button(Button.A, lambda: print('A pressed'))
    joy.on_button(Button.LTrigger, triggerHandle)
    joy.on_button(Button.LStick, stickHandle)
    while True:
        joy = await joy.read()
        print("Hi")

    joy.close()

if __name__ == "__main__":
    if sys.platform == "win32":
        loop = asyncio.ProactorEventLoop()
        asyncio.set_event_loop(loop)
    else:
        loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, quit)
    loop.run_until_complete(example())
