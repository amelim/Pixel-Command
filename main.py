import libtcodpy as libtcod
from gamestate import *
from unit import *
from panels import *
from camera import *

#In number of tiles to display at a time
SCREEN_WIDTH = 120
SCREEN_HEIGHT = 120
PANEL_WIDTH = 20
PANEL_HEIGHT = 40
LIMIT_FPS = 20
FONT = "fonts/arial8x8.png"
main_map = Map(400, 400)
unit_panel = Unit_Panel(PANEL_WIDTH, PANEL_HEIGHT)
cam = Camera(0,0,SCREEN_WIDTH, SCREEN_HEIGHT)

def handle_keys(mouse):
    key = libtcod.console_check_for_keypress() 
    if libtcod.console_is_key_pressed(libtcod.KEY_UP) and cam.y > 0:
    	cam.y -= 1
    if libtcod.console_is_key_pressed(libtcod.KEY_DOWN) and cam.y < main_map.width - cam.w:
    	cam.y += 1
    if libtcod.console_is_key_pressed(libtcod.KEY_LEFT) and cam.x > 0:
    	cam.x -= 1
    if libtcod.console_is_key_pressed(libtcod.KEY_RIGHT) and cam.x < main_map.height - cam.h:
    	cam.x += 1

    if mouse.lbutton_pressed:
    	main_map.selected_unit = None
        for u in main_map.units:
            if u.x == mouse.cx + cam.x and u.y == mouse.cy + cam.y:
            	main_map.selected_unit = u

    if mouse.rbutton_pressed:
        if main_map.selected_unit != None:
        	main_map.selected_unit.path_plan(mouse.cx + cam.x, mouse.cy + cam.y)


def render(mouse):
    libtcod.console_clear(0)
    libtcod.console_clear(unit_panel.console)
    main_map.draw(0, cam)
    
    #unit_panel rendering

    #unit rendering
    libtcod.console_set_alignment(0, libtcod.CENTER)
    libtcod.console_set_default_background(0, libtcod.black)

    for u in main_map.units:
    	u.draw(0,cam)
        #Draw name function
        if (u.x == mouse.cx + cam.x and u.y == mouse.cy + cam.y) or u == main_map.selected_unit:
            libtcod.console_print(0, u.x - cam.x, u.y - cam.y -1, u.name)
            #Draw the destination if moving
            x,y = libtcod.path_get_destination(u.path)
            if not libtcod.path_is_empty(u.path):
        	    libtcod.console_set_char(0, x - cam.x, y - cam.y, libtcod.CHAR_ARROW_S)
    
    unit_panel.draw(main_map)


def update():
    for u in main_map.units:
    	u.move()

def main():

    libtcod.console_set_custom_font(FONT, libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    libtcod.sys_set_fps(20)
    libtcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, 'Junta!', False)
    main_map.units.append(Unit(60,60, 'ship', 'Destroyer A-2', 1, 20, 5, main_map, libtcod.CHAR_ARROW2_N))
    main_map.units.append(Unit(169,150, 'infantry', 'Recon Platoon', 10, 4, 2, main_map, libtcod.CHAR_DARROW_V))
    main_map.units.append(Unit(173, 151, 'infantry', 'Weapons Team', 10, 3, 2, main_map, libtcod.CHAR_DARROW_V))


    while not libtcod.console_is_window_closed():
    	mouse = libtcod.mouse_get_status()
    	#print main_map.map_list[mouse.cx + cam.x][mouse.cy + cam.y].land_type
    	handle_keys(mouse)
    	update()
    	render(mouse)
    	libtcod.console_flush()

if __name__ == '__main__':
	main()
