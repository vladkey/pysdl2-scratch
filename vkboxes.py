import sys
import sdl2.ext
import sdl2.surface

def draw_rect(surface, line_color, inner_color, x, y, w, h, width=2):
    sdl2.ext.fill(surface, line_color,  (x, y, w, h))
    sdl2.ext.fill(surface, inner_color, (x+width, y+width, w-2*width, h-2*width))

BG_COLOR = sdl2.ext.Color(170, 220, 180, 127)
WHITE = sdl2.ext.Color(255, 255, 255, 0)

bgcolor = sdl2.ext.Color(170, 220, 180)
lncolor = sdl2.ext.Color(30, 20, 20)

def run():
    sdl2.ext.init()

    RESOURCES = sdl2.ext.Resources(__file__, "resources")
    font_surface = sdl2.ext.image.load_image(RESOURCES.get_path("font.bmp"), "SDL")
    print("font_surface: ", font_surface)
    new_white = sdl2.ext.draw.prepare_color(WHITE, font_surface)
    # print("new_white: ", new_white)
    rc = sdl2.surface.SDL_SetColorKey(font_surface, 1, new_white)

    # _font_sprite = sdl2.ext.SoftwareSprite(font_surface, True)
    # print("font_sprite: ", _font_sprite)
    font = sdl2.ext.BitmapFont(font_surface, (32, 32))
    print("font: ", font)

    test_sprite = font.render("7.7")
    print("test_sprite: ", test_sprite)
    
    window = sdl2.ext.Window("VK boxes", size=(1920, 960))
    window.show()

    wnd_sfc = window.get_surface()
    sdl2.ext.fill(wnd_sfc, bgcolor)

    for row in range(0, 8):
        for col in range(0, 10):
            draw_rect(wnd_sfc, lncolor, bgcolor, 64+col*180, 32+row*96, 176, 92)
            label = str(row)+"."+str(col)
            font.render_on(wnd_sfc, label, offset=(108+col*180, 64+row*96))

    processor = sdl2.ext.TestEventProcessor()
    processor.run(window)

    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
