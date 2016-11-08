# Controller support using asyncio.

import asyncio
from enum import Enum

# Enum for controller events. Values are arbitrary but unique.
class Button(Enum):
    A, B, X, Y = range(0, 4)
    LStick, RStick, LTrigger, RTrigger = range(4, 8)
    L3, R3, LB, RB = range(8, 12)
    DpadU, DpadD, DpadL, DpadR = range(12, 16)
    Back = 16
    Start = 17
    Guide = 18   # This is the Xbox button on the Xbox controller

class Joystick:
    @classmethod
    async def create(cls):
        joy = await Joystick.create("--no-uinput", "--detach-kernel-driver")
        return joy

    # Spawns xboxdrv using the given arguments. This is useful for telling xboxdrv to work with
    # a second controller, or a specific device
    @classmethod
    async def create(cls, *args):
        self = Joystick()
        self.proc = await asyncio.create_subprocess_exec("xboxdrv",
                                                 *args,
                                                 stdout=asyncio.subprocess.PIPE)

        # Init callback dict
        self.handlers = {}
        for b in Button:
            self.handlers[b] = []

        # Evaluate xboxdrv preample.
        # This could likely use some improvement
        while True:
            line = await self.proc.stdout.readline()
            if line:
                if b'Press Ctrl-C' in line:
                    break
                if b'ERROR' in line:
                    print(await self.proc.stdout.readline()) # Next line is error message
                    raise OSError('Error running xboxdrv')
            else:
                raise RuntimeError('Failed to read xboxdrv')

        return self


    async def init(self):
        while True:
            line = await self.proc.stdout.readline()
            if line:
                self.call_handlers(line)
            else:
                break

        return self

    def onButton(self, button, callback):
        self.handlers[button].append(callback)

    # Each handler will parse its portion of the input line
    def call_handlers(self, line):
        self.handleLStick(line)
        self.handleRStick(line)
        self.handleDpad(line)
        self.handleSpecial(line)
        self.handleActionButtons(line)
        self.handleBumpers(line)
        self.handleTriggers(line)

    # Returns a value from (-32768 to +32767)
    def handleLStick(self, line):
        if self.handlers[Button.LStick]:
            leftX = int(line[3:9])
            leftY = int(line[13:19])
            for cb in self.handlers[Button.LStick]:
                cb(leftX, leftY)

        # "Clicking" the left analog stick
        if self.handlers[Button.L3] and int(line[90:91]):
            for cb in self.handlers[Button.L3]:
                cb()

    def handleRStick(self, line):
        if self.handlers[Button.RStick]:
            rightX = self.axisScale(int(line[24:30]))
            rightY = self.axisScale(int(line[34:40]))
            for cb in self.handlers[Button.LStick]:
                cb(leftX, leftY)

        # "Clicking" the left analog stick
        if self.handlers[Button.R3] and int(line[95:96]):
            for cb in self.handlers[Button.R3]:
                cb()

    def handleDpad(self, line):
        if self.handlers[Button.DpadU] and int(line[45:46]):
            for cb in self.handlers[Button.DpadU]:
                cb()

        if self.handlers[Button.DpadD] and int(line[50:51]):
            for cb in self.handlers[Button.DpadD]:
                cb()

        if self.handlers[Button.DpadL] and int(line[55:56]):
            for cb in self.handlers[Button.DpadL]:
                cb()

        if self.handlers[Button.DpadR] and int(line[60:61]):
            for cb in self.handlers[Button.DpadR]:
                cb()

    def handleSpecial(self, line):
        if self.handlers[Button.Back] and int(line[68:69]):
            for cb in self.handlers[Button.Back]:
                cb()

        if self.handlers[Button.Guide] and int(line[76:77]):
            for cb in self.handlers[Button.Guide]:
                cb()

        if self.handlers[Button.Start] and int(line[84:85]):
            for cb in self.handlers[Button.Start]:
                cb()

    def handleActionButtons(self, line):
        if self.handlers[Button.A] and int(line[100:101]):
            for cb in self.handlers[Button.A]:
                cb()

        if self.handlers[Button.B] and int(line[104:105]):
            for cb in self.handlers[Button.B]:
                cb()
        if self.handlers[Button.X] and int(line[108:109]):
            for cb in self.handlers[Button.X]:
                cb()
        if self.handlers[Button.Y] and int(line[112:113]):
            for cb in self.handlers[Button.Y]:
                cb()

    def handleBumpers(self, line):
        if self.handlers[Button.LB] and int(line[118:119]):
            for cb in self.handlers[Button.LB]:
                cb()

        if self.handlers[Button.RB] and int(line[123:124]):
            for cb in self.handlers[Button.RB]:
                cb()

    # Returns a value from 0 - 255
    def handleTriggers(self, line):
        if self.handlers[Button.LTrigger]:
            for cb in self.handlers[Button.LTrigger]:
                cb(int(line[129:132]))

        if self.handlers[Button.RTrigger]:
            for cb in self.handlers[Button.RTrigger]:
                cb(int(line[136:139]))

    def close(self):
        self.proc.kill()
