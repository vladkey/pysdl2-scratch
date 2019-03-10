Overview
========

I am looking at "multimedia"/game programming with Linux. What options besides C/C++ and OpenGL and shaders I have?  
That was a journey into ctypes, wrappers and C libraries.


Prerequisites
-------------

The first answer: let's try py-sdl2 (https://github.com/marcusva/py-sdl2 and https://pysdl2.readthedocs.io/)

```bash
OPTIONAL=libsdl2-gfx-1.0-0 libsdl2-ttf-2.0-0
sudo apt install libsdl2-2.0-0 $OPTIONAL
```

Examples
--------

PySDL2 already has its examples. My examples started from them.

vkrend.py: Draws a bitmap with letters (font.bmp) on a window using white color as transparent.

vkboxes.py: Draws boxes and labels in it. "Font" is created from font.bmp.
Needs patch in sdl2/ext/font.py:

```python
-        imgsurface = SoftwareSprite(sf, False)
+        imgsurface = SoftwareSprite(sf.contents, False)
```

vktxtbox.py: Draws same boxes and labels in it; but "font" is created from tuffy.ttf using libsdl2-ttf-2.0-0

vkscratch.py: A cat named Scratch in a maze. Use arrows to walk, Esc to exit.

Running
-------

```bash
export PYTHONPATH=/path/to/py-sdl2
python3 vkscratch.py
```
