import libtcodpy as libtcod

class Unit:
    def __init__(self, x, y, u_class, name, speed, attack, armor, main_map, char):
        self.x = x 
        self.y = y
        self.color = libtcod.red
        self.char = char
        self.u_class = u_class 
        self.name = name 
        self.speed = speed 
        self.attack = attack 
        self.armor = armor 
        self.move_stat = 0

        if u_class == 'infantry':
            self.path = libtcod.path_new_using_map(main_map.ground_map)

        if u_class == 'ship':
            self.path = libtcod.path_new_using_map(main_map.deepsea_map)

    def draw(self, con, cam):
        libtcod.console_set_char_foreground(con, self.x - cam.x, self.y - cam.y, self.color)
        libtcod.console_set_char(con, self.x - cam.x, self.y - cam.y, self.char)

    def path_plan(self,x,y):
        libtcod.path_compute(self.path, self.x, self.y, x, y)

    def move(self):
        if self.move_stat != 50 - self.speed:
            self.move_stat += 1 
            return
        else:
        	self.move_stat = 0

        if not libtcod.path_is_empty(self.path):
        	self.x,self.y = libtcod.path_walk(self.path, True)
