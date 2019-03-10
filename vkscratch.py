import sys
import sdl2.ext
# import sdl2.sdlmixer
import sdl2.audio
import ctypes

RESOURCES = sdl2.ext.Resources(__file__, "resources")
WHITE = sdl2.ext.Color(255, 255, 255, 0)
RED = sdl2.ext.Color(255, 0, 0, 0)
font_mgr = sdl2.ext.FontManager(RESOURCES.get_path("tuffy.ttf"))

def get_sprite(name, factory, scale_down=None):
    sprite_sfc = sdl2.ext.image.load_image(RESOURCES.get_path(name))
    if scale_down:
        origfmt = sprite_sfc.format.contents
        print(name, "origfmt:", origfmt.Rmask, origfmt.Gmask, origfmt.Bmask, origfmt.Amask)
        scaled_h, scaled_w, new_bpp = scale_down.x, scale_down.y, origfmt.BitsPerPixel
        scaled_sprite_sfc = sdl2.surface.SDL_CreateRGBSurface(0, scaled_h, scaled_w, new_bpp, origfmt.Rmask, origfmt.Gmask, origfmt.Bmask, origfmt.Amask)
        #    origfmt.Rmask, origfmt.Gmask, origfmt.Bmask, origfmt.Amask)
        #int SDL_BlitScaled(SDL_Surface*    src, const SDL_Rect* srcrect,
        #   SDL_Surface*    dst, SDL_Rect*       dstrect)
        new_white2 = sdl2.ext.draw.prepare_color(WHITE, scaled_sprite_sfc.contents)
        sdl2.surface.SDL_FillRect(scaled_sprite_sfc, None, new_white2)

        src_rect = sdl2.SDL_Rect(0, 0, sprite_sfc.h, sprite_sfc.w)
        dst_rect = sdl2.SDL_Rect(0, 0, scaled_h, scaled_w)
        sdl2.surface.SDL_BlitScaled(sprite_sfc, src_rect, scaled_sprite_sfc, dst_rect)

        result_sprite = factory.from_surface(scaled_sprite_sfc)
    else:
        new_white = sdl2.ext.draw.prepare_color(WHITE, sprite_sfc)
        sdl2.surface.SDL_SetColorKey(sprite_sfc, 1, new_white)
        result_sprite = factory.from_surface(sprite_sfc)

    return result_sprite

def flip_sprites(spr1, spr2):
    spr1.flip ^= sdl2.SDL_FLIP_HORIZONTAL
    spr2.flip ^= sdl2.SDL_FLIP_HORIZONTAL

_AUDIO_DEVICE_ID_ = 0

def enable_audio(driver_name):
    global _AUDIO_DEVICE_ID_
    ver = sdl2.version.SDL_version()
    sdl2.version.SDL_GetVersion(ver)
    print("SDL Version:", ver.major, ver.minor, ver.patch, " rev.", sdl2.version.SDL_GetRevision())

    sdl2.SDL_InitSubSystem(sdl2.SDL_INIT_AUDIO)
    num_aud_drivers = sdl2.audio.SDL_GetNumAudioDrivers()
    drvnames = [sdl2.audio.SDL_GetAudioDriver(i) for i in range(0, num_aud_drivers)]
    print("drvnames", drvnames)

    # Open DRIVER
    sdl2.audio.SDL_AudioInit(driver_name)
    count = sdl2.audio.SDL_GetNumAudioDevices(0)
    for i in range(0, count):
        audio_device_name = sdl2.audio.SDL_GetAudioDeviceName(i, 0)
        print("audio_device_name", audio_device_name)

    # Open DRIVER and DEVICE
    desired = sdl2.audio.SDL_AudioSpec(22050, sdl2.audio.AUDIO_U16, 1, 4096)
    actual = sdl2.audio.SDL_AudioSpec(-1, -1, -1, -1)
    _AUDIO_DEVICE_ID_ = sdl2.audio.SDL_OpenAudioDevice(None, 0, desired, actual, sdl2.audio.SDL_AUDIO_ALLOW_ANY_CHANGE)
    print("opened audio device_id", _AUDIO_DEVICE_ID_)
    print("opened audio actual", audiospec_to_str(actual))
    # print("actual: cb=", actual.callback, "userdata", actual.userdata)

def cleanup_audio():
    global _AUDIO_DEVICE_ID_
    print("Audio cleanup")
    sdl2.audio.SDL_PauseAudioDevice(_AUDIO_DEVICE_ID_, 1)
    sdl2.audio.SDL_CloseAudioDevice(_AUDIO_DEVICE_ID_)

def load_music(resource_name):
    # Load music
    b_miaw_path = sdl2.ext.compat.byteify(RESOURCES.get_path(resource_name), "utf-8")
    music_spec = sdl2.audio.SDL_AudioSpec(-1, -1, -1, -1)
    sound_buf = ctypes.POINTER(ctypes.c_uint8)()
    sound_buf_len = ctypes.c_uint()
    sdl2.audio.SDL_LoadWAV(b_miaw_path, music_spec, ctypes.byref(sound_buf), ctypes.byref(sound_buf_len))
    print("Loaded WAV: ", audiospec_to_str(music_spec))

    return sound_buf, sound_buf_len

def play_music(sound_buf, sound_buf_len):
    global _AUDIO_DEVICE_ID_
    print("Loaded WAV: sound_buf", sound_buf, "sound_buf_len=", sound_buf_len.value)
    q_retcode = sdl2.audio.SDL_QueueAudio(_AUDIO_DEVICE_ID_, sound_buf, sound_buf_len.value)
    print("q_retcode == 0?", q_retcode, "err", sdl2.SDL_GetError())
    sdl2.audio.SDL_PauseAudioDevice(_AUDIO_DEVICE_ID_, 0)

    return q_retcode

def audiospec_to_str(spec):
    t = ("freq=", spec.freq, "format=", format(spec.format, "04x"), "channels=", spec.channels, "samples=", spec.samples)
    return str(t)

WND_SIZE = sdl2.SDL_Point(1280, 850)
INITIAL_POS = sdl2.SDL_Point(588, 6) # (12, 6)
STEP = sdl2.SDL_Point(64, 42)
CAT_SIZE = sdl2.SDL_Point(40, 36)

def run():
    window = sdl2.ext.Window("Scratch cat, move with arrows", size=(WND_SIZE.x, WND_SIZE.y))
    window.show()

    renderer = sdl2.ext.Renderer(window)
    factory = sdl2.ext.SpriteFactory(sdl2.ext.TEXTURE, renderer=renderer)
    spriterenderer = factory.create_sprite_render_system(window)
    print(spriterenderer)

    #enable_audio(b'pulseaudio')
    #sound_buf, sound_buf_len = load_music("Scratch-Cat-Miaw.wav")
    #play_music(sound_buf, sound_buf_len)

    maze = "orthogonal_maze_with_20_by_20_cells.png"
    tv = "hello.bmp"
    background_sprite = factory.from_image(RESOURCES.get_path(maze))

    scratch1 = get_sprite("converted-1.png", factory, CAT_SIZE)
    scratch2 = get_sprite("converted-2.png", factory, CAT_SIZE)

    curr_pos = INITIAL_POS
    running = True
    step = 0
    looks_right = True
    while running:
        # Process input
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            elif event.type == sdl2.SDL_KEYDOWN:
                oldpos = sdl2.SDL_Point(curr_pos.x, curr_pos.y)
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False
                elif event.key.keysym.sym == sdl2.SDLK_DOWN:
                    curr_pos.y += STEP.y
                elif event.key.keysym.sym == sdl2.SDLK_UP:
                    curr_pos.y -= STEP.y
                elif event.key.keysym.sym == sdl2.SDLK_LEFT:
                    curr_pos.x -= STEP.x
                    if looks_right:
                        flip_sprites(scratch1, scratch2)
                    looks_right = False
                elif event.key.keysym.sym == sdl2.SDLK_RIGHT:
                    curr_pos.x += STEP.x
                    if not looks_right:
                        flip_sprites(scratch1, scratch2)
                    looks_right = True
                # check collision, range
                if curr_pos.x < 0 or curr_pos.x > WND_SIZE.x or curr_pos.y < 0 or curr_pos.y > WND_SIZE.y:
                    curr_pos = oldpos
        # Render
        renderer.copy(background_sprite)
        scratch = scratch1 if (step % 30) < 15 else scratch2
        scratch.position = (curr_pos.x, curr_pos.y)
        spriterenderer.render(scratch)

        text = str(curr_pos.x) + ":" + str(curr_pos.y)
        label_sfc = font_mgr.render(text, size=24, color=RED)
        label_sprite = factory.from_surface(label_sfc)
        spriterenderer.render(label_sprite, 30, 700)

        # Wait
        sdl2.SDL_Delay(10)
        step += 1

    #print("FreeWAV:", sound_buf)
    #sdl2.audio.SDL_FreeWAV(sound_buf)
    cleanup_audio()
    #sdl2.audio.SDL_AudioQuit()
    print("OK")

if __name__ == "__main__":
    sdl2.ext.init()
    run()
    sdl2.ext.quit()
    sys.exit(0)
