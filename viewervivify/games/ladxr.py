from evilemu.emulator import Emulator
import os
import random
import time
from game import Game, action


class LADXR(Game):
    @staticmethod
    def is_running(emulator: Emulator):
        header = emulator.read_rom(0x134, 0x10)
        return header == b'LADXR\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80'

    def __init__(self, emulator: Emulator):
        super().__init__()
        assert self.is_running(emulator)
        self.__emulator = emulator

    @action(id="zol", name="Zol storm!", cost=500)
    def do_slime_rain(self):
        self.__emulator.write_ram8(0xDDF8 - 0xC000, 0xF0)
        self.__emulator.write_ram8(0xDDF7 - 0xC000, self.__emulator.read_ram8(0xDDF7 - 0xC000) | 0x01)

    @action(id="bomb", name="Bomb rain!", cost=300)
    def do_bomb_rain(self):
        self.__emulator.write_ram8(0xDE12 - 0xC000, 0x20)

    @action(id="cucco", name="Cucco party!", cost=200)
    def do_cucco_party(self):
        self.__emulator.write_ram8(0xDDF8 - 0xC000, 0xF1)
        self.__emulator.write_ram8(0xDDF7 - 0xC000, self.__emulator.read_ram8(0xDDF7 - 0xC000) | 0x01)

    @action(id="power", name="Piece of power", cost=50)
    def do_pop(self):
        self.__emulator.write_ram8(0xDDF8 - 0xC000, 0xF2)
        self.__emulator.write_ram8(0xDDF7 - 0xC000, self.__emulator.read_ram8(0xDDF7 - 0xC000) | 0x01)

    @action(id="tele", name="Teleport!", cost=100)
    def do_teleport(self):
        indoor = self.__emulator.read_ram8(0xDBA5 - 0xC000)
        if indoor:  # Check if we are indoor
            physics_flags = self.__emulator.read_rom(0x4000 * 7 + 0x4BD4, 0x100)
        else:
            physics_flags = self.__emulator.read_rom(0x4000 * 7 + 0x4AD4, 0x100)
        objects = self.__emulator.read_ram(0xD700 - 0xC000, 0x100)
        options = []
        for y in range(8):
            for x in range(10):
                obj = objects[x + y * 16 + 17]
                if obj != 0x00:
                    flags = physics_flags[obj]
                    if flags in {0x00, 0x02, 0x05, 0x06, 0x08, 0x0A}:
                        options.append((x, y))
        if indoor:
            # In case of indoor, try to prevent teleporting out of bounds.
            def remove(x, y):
                if (x, y) not in options:
                    return
                options.remove((x, y))
                remove(x + 1, y)
                remove(x - 1, y)
                remove(x, y + 1)
                remove(x, y - 1)
            remove(0, 0)
            remove(9, 0)
            remove(0, 7)
            remove(9, 7)
        if len(options) == 0:
            return
        x, y = random.choice(options)
        self.__emulator.write_hram(0x98 - 0x80, bytes([x * 16 + 8, y * 16 + 16]))

    @action(id="warp", name="Warp!", cost=2500)
    def do_world_warp(self):
        self.__emulator.write_ram8(0xDDF8 - 0xC000, 0xF4)
        self.__emulator.write_ram8(0xDDF7 - 0xC000, self.__emulator.read_ram8(0xDDF7 - 0xC000) | 0x01)

    @action(id="regen", name="Regenerate health", cost=100)
    def do_regen(self):
        self.__emulator.write_ram8(0xDB93 - 0xC000, 0xFF)

    @action(id="damage", name="Do 1 heart of damage", cost=100)
    def do_damage(self):
        self.__emulator.write_ram8(0xDB94 - 0xC000, 0x08)

    @action(id="addbombs", name="Give 10 bombs", cost=100)
    def do_addbombs(self):
        self.__emulator.write_ram8(0xDB4D - 0xC000, min(self.__emulator.read_ram8(0xDB4D - 0xC000) + 0x10, self.__emulator.read_ram8(0xDB77 - 0xC000)))

    @action(id="invisilink", group="gfx", name="Make link invisible", cost=500)
    def do_invisilink(self):
        self.__emulator.write_rom8(0x1D59, 0xC9)
    @do_invisilink.timeout(60)
    def undo_invisilink(self):
        self.__emulator.write_rom8(0x1D59, 0xD0)

    @action(id="gfxages", group="gfx", name="AgesGirl graphics", cost=500)
    def do_gfx_agesgirl(self):
        self.do_gfx("AgesGirl")

    @action(id="gfxbowwow", group="gfx", name="Bowwow graphics", cost=500)
    def do_gfx_bowwow(self):
        self.do_gfx("Bowwow")

    @action(id="gfxbunny", group="gfx", name="Bunny graphics", cost=500)
    def do_gfx_bunny(self):
        self.do_gfx("Bunny")

    @action(id="gfxgrandma", group="gfx", name="GrandmaUlrira graphics", cost=500)
    def do_gfx_grandmaulrira(self):
        self.do_gfx("GrandmaUlrira")

    @action(id="gfxkirby", group="gfx", name="Kirby graphics", cost=500)
    def do_gfx_kirby(self):
        self.do_gfx("Kirby")

    @action(id="gfxluigi", group="gfx", name="Luigi graphics", cost=500)
    def do_gfx_luigi(self):
        self.do_gfx("Luigi")

    @action(id="gfxmarin", group="gfx", name="Marin graphics", cost=500)
    def do_gfx_marin(self):
        self.do_gfx("Marin")

    @action(id="gfxalpha", group="gfx", name="MarinAlpha graphics", cost=500)
    def do_gfx_alpha(self):
        self.do_gfx("MarinAlpha")

    @action(id="gfxmario", group="gfx", name="Mario graphics", cost=500)
    def do_gfx_mario(self):
        self.do_gfx("Mario")

    @action(id="gfxmartha", group="gfx", name="Martha graphics", cost=500)
    def do_gfx_martha(self):
        self.do_gfx("Martha")

    @action(id="gfxmatty", group="gfx", name="Matty_LA graphics", cost=500)
    def do_gfx_matty(self):
        self.do_gfx("Matty_LA")

    @action(id="gfxmeme", group="gfx", name="Meme graphics", cost=500)
    def do_gfx_meme(self):
        self.do_gfx("Meme")

    @action(id="gfxnes", group="gfx", name="NESLink graphics", cost=500)
    def do_gfx_nes(self):
        self.do_gfx("NESLink")

    @action(id="gfxrichard", group="gfx", name="Richard graphics", cost=500)
    def do_gfx_richard(self):
        self.do_gfx("Richard")

    @action(id="gfxrooster", group="gfx", name="Rooster graphics", cost=500)
    def do_gfx_rooster(self):
        self.do_gfx("Rooster")

    @action(id="gfxrosa", group="gfx", name="Rosa graphics", cost=500)
    def do_gfx_rosa(self):
        self.do_gfx("Rosa")

    @action(id="gfxsubrosian", group="gfx", name="Subrosian graphics", cost=500)
    def do_gfx_subrosian(self):
        self.do_gfx("Subrosian")

    @action(id="gfxtarin", group="gfx", name="Tarin graphics", cost=500)
    def do_gfx_tarin(self):
        self.do_gfx("Tarin")

    @action(id="gfxrandom", group="gfx", name="Random graphics", cost=500)
    def do_gfx_random(self):
        gfx_list = [os.path.splitext(name)[0] for name in os.listdir("data/ladx") if os.path.splitext(name)[1] == ".bin"]
        self.do_gfx(random.choice(gfx_list))

    def do_gfx(self, name):
        gfx = open(f"data/ladx/{name}.bin", "rb").read()
        offset = 0x2C * 0x4000
        # Write the graphics data, but ignore some sections as they are patched differently by LADXR
        for bank, start, end in [(0x2C, 0x0900, 0x0940), (0x30, 0x3000, 0x3800)]:
            end_offset = bank * 0x4000 + start
            self.__emulator.write_rom(offset, gfx[offset-0x2C * 0x4000:end_offset-0x2C * 0x4000])
            offset = bank * 0x4000 + end
        self.__emulator.write_rom(offset, gfx[offset - 0x2C * 0x4000:])

    @action(id="disablesword", group="input", name="Disable sword (60 seconds)", cost=500)
    def do_disable_sword(self):
        self.__emulator.write_rom16(0x129E + 2, 0x12D3)
        self.__emulator.write_rom8(0x1322, 0xFF)
        self.__emulator.write_rom(0x12D3, b'\x3E\x19\xE0\xF3\xC9')
    @do_disable_sword.timeout(60)
    def do_enable_sword(self):
        self.__emulator.write_rom16(0x129E + 2, 0x1528)
        self.__emulator.write_rom8(0x1322, 0x01)

    @action(id="disablebombs", group="input", name="Disable bombs (60 seconds)", cost=500)
    def do_disable_bombs(self):
        self.__emulator.write_rom16(0x129E + 4, 0x12D3)
        self.__emulator.write_rom(0x12D3, b'\x3E\x19\xE0\xF3\xC9')
    @do_disable_bombs.timeout(60)
    def do_enable_bombs(self):
        self.__emulator.write_rom16(0x129E + 4, 0x135A)

    @action(id="disableboots", group="input", name="Disable boots (60 seconds)", cost=500)
    def do_disable_boots(self):
        self.__emulator.write_rom8(0x1705, 0xC9)
    @do_disable_boots.timeout(60)
    def do_enable_boots(self):
        self.__emulator.write_rom8(0x1705, 0xF0)

    @action(id="disablebow", group="input", name="Disable bow (60 seconds)", cost=500)
    def do_disable_bow(self):
        self.__emulator.write_rom16(0x129E + 10, 0x12D3)
        self.__emulator.write_rom(0x12D3, b'\x3E\x19\xE0\xF3\xC9')
    @do_disable_bow.timeout(60)
    def do_enable_bow(self):
        self.__emulator.write_rom16(0x129E + 10, 0x13BD)

    @action(id="disablehook", group="input", name="Disable hookshot (60 seconds)", cost=500)
    def do_disable_hook(self):
        self.__emulator.write_rom16(0x129E + 12, 0x12D3)
        self.__emulator.write_rom(0x12D3, b'\x3E\x19\xE0\xF3\xC9')
    @do_disable_hook.timeout(60)
    def do_enable_hook(self):
        self.__emulator.write_rom16(0x129E + 12, 0x1319)

    @action(id="disablerod", group="input", name="Disable magic rod (60 seconds)", cost=500)
    def do_disable_rod(self):
        self.__emulator.write_rom16(0x129E + 14, 0x12D3)
        self.__emulator.write_rom(0x12D3, b'\x3E\x19\xE0\xF3\xC9')
    @do_disable_rod.timeout(60)
    def do_enable_rod(self):
        self.__emulator.write_rom16(0x129E + 14, 0x12D8)

    @action(id="disableocarina", group="input", name="Disable ocarina (60 seconds)", cost=500)
    def do_disable_ocarina(self):
        self.__emulator.write_rom16(0x129E + 18, 0x12D3)
        self.__emulator.write_rom(0x12D3, b'\x3E\x19\xE0\xF3\xC9')
    @do_disable_ocarina.timeout(60)
    def do_enable_ocarina(self):
        self.__emulator.write_rom16(0x129E + 18, 0x41FC)

    @action(id="disablefeather", group="input", name="Disable feather (60 seconds)", cost=500)
    def do_disable_feather(self):
        self.__emulator.write_rom16(0x129E + 20, 0x12D3)
        self.__emulator.write_rom(0x12D3, b'\x3E\x19\xE0\xF3\xC9')
    @do_disable_feather.timeout(60)
    def do_enable_feather(self):
        self.__emulator.write_rom16(0x129E + 20, 0x14CB)

    @action(id="disableshovel", group="input", name="Disable shovel (60 seconds)", cost=500)
    def do_disable_shovel(self):
        self.__emulator.write_rom16(0x129E + 22, 0x12D3)
        self.__emulator.write_rom(0x12D3, b'\x3E\x19\xE0\xF3\xC9')
    @do_disable_shovel.timeout(60)
    def do_enable_shovel(self):
        self.__emulator.write_rom16(0x129E + 22, 0x12F8)

    @action(id="disablepowder", group="input", name="Disable magic powder (60 seconds)", cost=500)
    def do_disable_powder(self):
        self.__emulator.write_rom16(0x129E + 24, 0x12D3)
        self.__emulator.write_rom(0x12D3, b'\x3E\x19\xE0\xF3\xC9')
    @do_disable_powder.timeout(60)
    def do_enable_powder(self):
        self.__emulator.write_rom16(0x129E + 24, 0x148D)

    @action(id="disablerang", group="input", name="Disable boomerang (60 seconds)", cost=500)
    def do_disable_rang(self):
        self.__emulator.write_rom16(0x129E + 26, 0x12D3)
        self.__emulator.write_rom(0x12D3, b'\x3E\x19\xE0\xF3\xC9')
    @do_disable_rang.timeout(60)
    def do_enable_rang(self):
        self.__emulator.write_rom16(0x129E + 26, 0x1383)

    @action(id="disableflippers", group="input", name="Disable flippers (60 seconds)", cost=500)
    def do_disable_flippers(self):
        self.__emulator.write_rom(0x7717 + 0x4000, b'\x00\x00')
        if self.__emulator.read_ram8(0xC11C - 0xC000) == 0x01:
            self.__emulator.write_ram8(0xC11C - 0xC000, 0x00)
    @do_disable_flippers.timeout(60)
    def do_enable_flippers(self):
        self.__emulator.write_rom(0x7717 + 0x4000, b'\x20\x19')

    @action(id="invert", group="input", name="Invert buttons (60 seconds)", cost=300)
    def do_invert_dpad(self):
        self.__emulator.write_rom(0x2864, b'\xcb\x37\x2f\xe6\xf0\xb0\x47\x87\xe6\xaa\x4f\x78\x1f\xe6\x55\xb1\x00\x00\x00\x00')
    @do_invert_dpad.timeout(60)
    def do_normal_dpad(self):
        self.__emulator.write_rom(0x2864, b'\xf0\x00\xf0\x00\xf0\x00\xf0\x00\xf0\x00\xf0\x00\xf0\x00\xcb\x37\x2f\xe6\xf0\xb0')

    @action(id="runrunrun", group="input", name="Constant boots power (60 seconds)", cost=300)
    def do_runrunrun(self):
        self.__emulator.write_rom(0x11ED, b'\x00\x00')
        self.__emulator.write_rom(0x11F3, b'\x00\x00')
    @do_runrunrun.timeout(60)
    def undo_runrunrun(self):
        self.__emulator.write_rom(0x11ED, b'\x20\x0F')
        self.__emulator.write_rom(0x11F3, b'\x28\x05')

    @action(id="slow", group="input", name="Slow (30 seconds)", cost=300)
    def do_slow(self):
        self.__emulator.write_rom(0x4481 + 0x4000, b'\x3E\x01')
    @do_slow.timeout(60)
    def undo_runrunrun(self):
        self.__emulator.write_rom(0x4481 + 0x4000, b'\xF0\xB2')

    @action(id="green", group="color", name="Green link (color only)", cost=300)
    def do_color_green(self):
        self.__emulator.write_rom(0x1D8C, b'\x3E\x00\x00\x00\x00\x00\x00')
        self.__emulator.write_rom(0x1DD2, b'\x3E\x00\x00\x00\x00\x00\x00')

    @action(id="yellow", group="color", name="Yellow link (color only)", cost=300)
    def do_color_yellow(self):
        self.__emulator.write_rom(0x1D8C, b'\x3E\x01\x00\x00\x00\x00\x00')
        self.__emulator.write_rom(0x1DD2, b'\x3E\x01\x00\x00\x00\x00\x00')

    @action(id="red", group="color", name="Red link (color only)", cost=300)
    def do_color_red(self):
        self.__emulator.write_rom(0x1D8C, b'\x3E\x02\x00\x00\x00\x00\x00')
        self.__emulator.write_rom(0x1DD2, b'\x3E\x02\x00\x00\x00\x00\x00')

    @action(id="blue", group="color", name="Blue link (color only)", cost=300)
    def do_color_blue(self):
        self.__emulator.write_rom(0x1D8C, b'\x3E\x03\x00\x00\x00\x00\x00')
        self.__emulator.write_rom(0x1DD2, b'\x3E\x03\x00\x00\x00\x00\x00')

    @action(id="disco", group="color", name="Disco link (30 seconds, color only)", cost=50)
    def do_color_disco(self):
        self.__emulator.write_rom(0x1D8C, b'\x3E\x00\x00\x00\x00\x00\x00')
        self.__emulator.write_rom(0x1DD2, b'\x3E\x00\x00\x00\x00\x00\x00')
    @do_color_disco.repeat(0.1)
    def repeat_color_disco(self):
        color = random.randint(0, 7)
        self.__emulator.write_rom8(0x1D8D, color)
        self.__emulator.write_rom8(0x1DD3, color)
    @do_color_disco.timeout(30)
    def end_disco(self):
        self.__emulator.write_rom8(0x1D8D, 0)
        self.__emulator.write_rom8(0x1DD3, 0)

    @action(id="rng", name="Randomize inventory", cost=100)
    def do_randomize_inventory(self):
        items = [n for n in self.__emulator.read_ram(0xDB00 - 0xC000, 16) if n != 0]
        random.shuffle(items)
        items += [0] * (16 - len(items))
        self.__emulator.write_ram(0xDB00 - 0xC000, bytes(items))

    @action(id="swordona", name="A button = sword (30 seconds)", cost=500)
    def do_sword_on_a(self):
        self.__emulator.write_rom(0x126F, b'\x3E\x01\x00')
    @do_sword_on_a.timeout(30)
    def end_sword_on_a(self):
        self.__emulator.write_rom(0x126F, b'\xFA\x01\xDB')

    @action(id="swordonb", name="B button = sword (30 seconds)", cost=500)
    def do_sword_on_b(self):
        self.__emulator.write_rom(0x1258, b'\x3E\x01\x00')
    @do_sword_on_b.timeout(30)
    def end_sword_on_b(self):
        self.__emulator.write_rom(0x1258, b'\xFA\x00\xDB')

    @action(id="msg", name="Ingame message", cost=300)
    def do_message(self, message):
        while self.__emulator.read_ram8(0xDB95 - 0xC000) != 0x0B or self.__emulator.read_ram8(0xDB96 - 0xC000) != 0x07 or self.__emulator.read_ram8(0xC124 - 0xC000) != 0x00 or self.__emulator.read_ram8(0xC19F - 0xC000) != 0x00 or self.__emulator.read_hram8(0xA1 - 0x80) != 0x00:
            time.sleep(0.1)
        data = message.encode("ascii", "replace")[:95]
        self.__emulator.write_ram(0xC0A0 - 0xC000, data + b'\xff')
        self.__emulator.write_ram8(0xC177 - 0xC000, 0)  # wDialogAskSelectionIndex
        self.__emulator.write_ram8(0xC173 - 0xC000, 0xC9)  # wDialogIndex

        self.__emulator.write_ram8(0xC16F - 0xC000, 0)  # wDialogOpenCloseAnimationFrame
        self.__emulator.write_ram8(0xC170 - 0xC000, 0)  # wDialogCharacterIndex
        self.__emulator.write_ram8(0xC164 - 0xC000, 0)  # wDialogCharacterIndexHi
        self.__emulator.write_ram8(0xC108 - 0xC000, 0)  # wNameIndex
        self.__emulator.write_ram8(0xC112 - 0xC000, 0)  # wDialogIndexHi

        self.__emulator.write_ram8(0xC5AB - 0xC000, 0x0F)  # wDialogSFX

        if self.__emulator.read_hram8(0x99 - 0x80) < 0x48:
            self.__emulator.write_ram8(0xC19F - 0xC000, 0x81)  # wDialogState
        else:
            self.__emulator.write_ram8(0xC19F - 0xC000, 0x01)  # wDialogState
