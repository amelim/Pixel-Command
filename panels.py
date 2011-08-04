import libtcodpy as libtcod

class Unit_Panel():
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.console = libtcod.console_new(width, height)
        self.unit_image = libtcod.image_new(self.width - 4, self.width - 4)

    def draw(self, main_map):
        #Settings
        libtcod.console_set_default_background(self.console, libtcod.black)
        libtcod.console_set_alignment(self.console, libtcod.CENTER)

        if main_map.selected_unit:
            start = (self.width - 4)/2
            #Draw all units in the unit image
            for x in range(self.width - 4):
                for y in range(self.width - 4):
                    libtcod.image_put_pixel(self.unit_image, x, y, main_map.map_list[main_map.selected_unit.x + x - start][main_map.selected_unit.y + y - start].color)
                    for u in main_map.units:
                        if u.x == (main_map.selected_unit.x + x - start) and u.y == (main_map.selected_unit.y + y - start):
                            libtcod.console_set_char_foreground(self.console, x + 2, y + 4, u.color)
                            libtcod.console_set_char(self.console, x + 2, y + 4, u.char)

            libtcod.console_print_frame(self.console, 0, 0, self.width, self.height, False, libtcod.BKGND_NONE, main_map.selected_unit.name)
            libtcod.console_rect(self.console, 0,0, 20, 1, False)
            libtcod.image_blit_rect(self.unit_image, self.console, 2, 4, self.width - 4, self.width - 4, libtcod.BKGND_SET)

            libtcod.console_set_alignment(self.console, libtcod.LEFT)
            #Unit stats
            statx = self.width + 1
            libtcod.console_print(self.console, 2, statx, 'Speed')
            libtcod.console_print(self.console, 2, statx + 1, 'Attack')
            libtcod.console_print(self.console, 2, statx + 2, 'Armor')

            libtcod.console_set_alignment(self.console, libtcod.RIGHT)
            libtcod.console_print(self.console, self.width - 2, statx, str(main_map.selected_unit.speed))
            libtcod.console_print(self.console, self.width - 2, statx + 1, str(main_map.selected_unit.attack))
            libtcod.console_print(self.console, self.width - 2, statx + 2, str(main_map.selected_unit.armor))

            libtcod.console_blit(self.console, 0, 0, self.width, self.height, 0, 1, 60 - self.height/2, 1, 0.75)
