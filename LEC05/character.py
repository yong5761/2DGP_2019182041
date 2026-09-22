from pico2d import *


open_canvas(800, 600)

# 여기를 채우시오.
character = load_image('character.png')
cx, cy = 400, 300
radius = 200
angle = 0
start = True

while start:
    rad = math.radians(angle)
    x = cx + radius * math.cos(rad)
    y = cy + radius * math.sin(rad)

    clear_canvas()
    character.draw(x, y)
    update_canvas()
    
    angle = (angle + 1) % 360
    delay(0.01)

close_canvas()

