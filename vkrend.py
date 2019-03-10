import sys
import sdl2.ext

RESOURCES = sdl2.ext.Resources(__file__, "resources")
# font_surface = sdl2.ext.image.load_image(RESOURCES.get_path("font.bmp"), "SDL")
BG_COLOR = sdl2.ext.Color(170, 220, 180, 127)
WHITE = sdl2.ext.Color(255, 255, 255, 0)

font_surface = sdl2.ext.image.load_image(RESOURCES.get_path("font.bmp"), "SDL")
new_white = sdl2.ext.draw.prepare_color(WHITE, font_surface)
print("WHITE: ", int(WHITE), "new_white: ", new_white)
retcode = sdl2.surface.SDL_SetColorKey(font_surface, 1, new_white)
print("SDL_SetColorKey: retcode=", retcode)
# SDL_SetSurfaceColorMod

def run():
    window = sdl2.ext.Window("Hello World!", size=(592, 460))
    window.show()

    renderer = sdl2.ext.Renderer(window)
    renderer.color = BG_COLOR
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    spriterenderer = factory.create_sprite_render_system(window)

    renderer.clear()
    letters = factory.from_surface(font_surface)
    spriterenderer.render(letters, 100, 64)

    sdl2.ext.TestEventProcessor().run(window)

if __name__ == "__main__":
    sdl2.ext.init()
    run()
    sdl2.ext.quit()
