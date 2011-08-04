import libtcodpy as libtcod
import math
from unit import *

class Tile:
    def __init__(self, blocked, color, block_sight = None):
        self.blocked = blocked
        self.color = libtcod.black
        self.land_type = None
        
        if not blocked: self.color = color

        if block_sight is None: block_sight = blocked
        self.block_sight = block_sight

class Map:
    def __init__(self, width, height):
        self.size = width 
        self.width = width
        self.height = height
        self.units = []
        self.selected_unit = None

        self.world_img = libtcod.image_new(self.width, self.height)
        self.ground_map = libtcod.map_new(width, height)
        self.deepsea_map = libtcod.map_new(width, height)
        
        self.noise_zoom = 5.0
        self.noise_octaves = 8.0

        self.center = [self.width/2, self.height/2]

        self.map_list = [[Tile(True, libtcod.black) for y in range(height)] for x in range(width)]

        self.world_noise = libtcod.noise_new(2)
        self.ocean_noise = libtcod.noise_new(2)
        libtcod.noise_set_type(self.world_noise, libtcod.NOISE_PERLIN)
        self.generate_land()

    def generate_land(self):
        for x in range(self.width):
            for y in range(self.height):
            	f = [self.noise_zoom * x / self.width,
            	     self.noise_zoom * y / self.height]

                value = libtcod.noise_get_fbm(self.world_noise, f, self.noise_octaves, libtcod.NOISE_PERLIN)

                #Threshold
                c = ((value + 1.0) / 2.0)
                col = libtcod.color_lerp(libtcod.dark_green, libtcod.black, c)
                self.map_list[x][y].land_type = 'grass' 

                c = int((value + 1.0) / 2.0 * 200)
                c = c - int(self.dist(x,y))/1.5

                #This is a beach
                if c < 28:
                	col = libtcod.lightest_amber
                	self.map_list[x][y].land_type = 'beach'
                #This is water 
                if c < 20:
                    coef = self.dist(x,y) / 320
                    col = libtcod.color_lerp(libtcod.azure, libtcod.darkest_azure * (c/2), coef)
                    if c > 5:
                    	self.map_list[x][y].land_type = 'shallow_water'
                    else:
                    	self.map_list[x][y].land_type = 'deep_water'
                    	libtcod.map_set_properties(self.deepsea_map, x, y, False, True)
                
                if self.map_list[x][y].land_type == 'grass' or self.map_list[x][y].land_type == 'beach':
                    libtcod.map_set_properties(self.ground_map, x, y, False, True)

                self.map_list[x][y].color = col
                libtcod.image_put_pixel(self.world_img, x, y, self.map_list[x][y].color)
                        

    def draw(self, con, cam):
        #libtcod.image_blit_2x(self.world_img, con, 0,0, cam.x, cam.y, cam.w, cam.h)
        libtcod.image_blit_rect(self.world_img, con, 0 - cam.x, 0 - cam.y, self.width, self.height, libtcod.BKGND_SET)

    def dist(self, x, y):
        r = (self.center[0] - x)**2 + (self.center[1] - y)**2
        return math.sqrt(r)

