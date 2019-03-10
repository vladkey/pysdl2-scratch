import sys
import sdl2.ext
import sdl2.surface

def draw_rect(surface, line_color, inner_color, x, y, w, h, width=2):
    sdl2.ext.fill(surface, line_color,  (x, y, w, h))
    sdl2.ext.fill(surface, inner_color, (x+width, y+width, w-2*width, h-2*width))

BG_COLOR = sdl2.ext.Color(170, 220, 180, 127)
WHITE = sdl2.ext.Color(255, 255, 255, 0)
RED = sdl2.ext.Color(255, 0, 0, 0)

bgcolor = sdl2.ext.Color(170, 220, 180)
lncolor = sdl2.ext.Color(30, 20, 20)

def run():
    sdl2.ext.init()

    RESOURCES = sdl2.ext.Resources(__file__, "examples/resources")
    font_mgr = sdl2.ext.FontManager(RESOURCES.get_path("tuffy.ttf"))
    print("font_mgr.default: ", font_mgr.default_font)

    window = sdl2.ext.Window("VK texts", size=(1920, 960))
    window.show()

    wnd_sfc = window.get_surface()
    sdl2.ext.fill(wnd_sfc, bgcolor)

    for row in range(0, 8):
        for col in range(0, 10):
            draw_rect(wnd_sfc, lncolor, bgcolor, 64+col*180, 32+row*96, 176, 92)
            label = str(row)+"."+str(col)
            label_sfc = font_mgr.render(label, size=24, color=RED)
            dst_rect = sdl2.SDL_Rect(108+col*180, 64+row*96, 64, 64)
            sdl2.SDL_BlitSurface(label_sfc, None, wnd_sfc, dst_rect)

    processor = sdl2.ext.TestEventProcessor()
    processor.run(window)

    sdl2.ext.quit()
    return 0

if __name__ == "__main__":
    sys.exit(run())
