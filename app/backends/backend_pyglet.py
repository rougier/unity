# -*- coding: utf-8 -*-
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import sys
from .. window import window
from .. import log, clock, configuration

# Backend name
__name__ = "Pyglet"

# Backend version (if available)
__version__ = ""

# Whether the framework has been initialized
__initialized__ = False

# Active windows
__windows__ = []

# Default clock
__clock__ = None

# Default configuration
__configuration__ = None


# --------------------------------------------------------------- init/exit ---
def __init__():
    global __initialized__
    __initialized__ = True

def __exit__():
    global __initialized__
    # Not an error, we cannot really terminate pyglet
    __initialized__ = True


# ------------------------------------------------------------ availability ---
try:
    import pyglet
    availability = True
    version = pyglet.version
    __init__()
except ImportError:
    availability = False
    version = None


# -------------------------------------------------------------- capability ---
capability = {
    "Window position get/set" : True,
    "Window size get/set"     : True,
    "Multiple windows"        : True,
    "Mouse scroll events"     : True,
    "Non-decorated window"    : True,
    "Non-sizeable window"     : True,
    "Fullscreen mode"         : True,
    "Unicode processing"      : True,
    "Set GL version"          : False,
    "Set GL profile"          : False,
    "Share GL context"        : True,
}




# ------------------------------------------------------- set_configuration ---
def set_configuration(config):
    """ Set gl configuration """

    global __configuration__

    __configuration__ = pyglet.gl.Config()

    __configuration__.red_size = config.red_size
    __configuration__.green_size = config.green_size
    __configuration__.blue_size = config.blue_size
    __configuration__.alpha_size = config.alpha_size

    __configuration__.accum_red_size = 0
    __configuration__.accum_green_size = 0
    __configuration__.accum_blue_size = 0
    __configuration__.accum_alpha_size = 0

    __configuration__.depth_size = config.depth_size
    __configuration__.stencil_size = config.stencil_size
    __configuration__.double_buffer = config.double_buffer
    __configuration__.stereo = config.stereo
    __configuration__.samples = config.samples




# ------------------------------------------------------------------ Window ---
class Window(window.Window):


    def __init__( self, width=256, height=256, title=None, visible=True,
                  decoration=True, fullscreen=False, config=None, context=None):

        window.Window.__init__(self, width, height, title, visible,
                               decoration, fullscreen, config, context)

        if config is None:
            config = configuration.Configuration()
        set_configuration(config)

        self._native_window = pyglet.window.Window(
            width=self._width, height=self._height, caption=title,
            vsync=False, config=__configuration__)

 	def on_mouse_drag(x, y, dx, dy, button, modifiers):
            self.dispatch_event("on_mouse_drag", x, y, dx ,dy, button)
        self._native_window.on_mouse_drag = on_mouse_drag

 	def on_mouse_enter(x, y):
            self.dispatch_event("on_enter", x, y)
        self._native_window.on_mouse_enter = on_mouse_enter

 	def on_mouse_leave(x, y):
            self.dispatch_event("on_leave", x, y)
        self._native_window.on_mouse_leave = on_mouse_leave

 	def on_mouse_motion(x, y, dx, dy):
            self.dispatch_event("on_mouse_motion", x, y, dx, dy)
        self._native_window.on_mouse_motion = on_mouse_motion

 	def on_mouse_press(x, y, button, modifiers):
            self.dispatch_event("on_mouse_press", x, y, button)
        self._native_window.on_mouse_press = on_mouse_press

 	def on_mouse_release(x, y, button, modifiers):
            self.dispatch_event("on_mouse_release", x, y, button)
        self._native_window.on_mouse_release = on_mouse_release

 	def on_mouse_scroll(x, y, scroll_x, scroll_y):
            self.dispatch_event("on_mouse_scroll", x, y, scroll_x, scroll_y)
        self._native_window.on_mouse_scroll = on_mouse_scroll

 	def on_resize(width, height):
            self.dispatch_event("on_resize", width, height)
        self._native_window.on_resize = on_resize

 	def on_show():
            self.dispatch_event("on_show")
        self._native_window.on_show = on_show

 	def on_hide():
            self.dispatch_event("on_hide")
        self._native_window.on_hide = on_hide

 	def on_close():
            self._native_window.close()
            __windows__.remove(self)
            for i in range(len(self._timer_stack)):
                handler, interval = self._timer_stack[i]
                self._clock.unschedule(handler)
            self.dispatch_event("on_close")
        self._native_window.on_close = on_close

 	def on_key_press(symbol, modifiers):
            self.dispatch_event("on_key_press", symbol, modifiers)
        self._native_window.on_key_press = on_key_press

 	def on_key_release(symbol, modifiers):
            self.dispatch_event("on_key_release", symbol, modifiers)
        self._native_window.on_key_release = on_key_release

 	def on_draw():
            self.dispatch_event("on_draw")
        self._native_window.on_draw = on_draw

        __windows__.append(self)



    def show(self):
        self._native_window.set_visible(True)

    def hide(self):
        self._native_window.set_visible(False)

    def set_fullscreen(self, state):
        self._native_window.set_fullscreen(state)

    def set_title(self, title):
        self._native_window.set_caption(title)
        self._title = title

    def get_title(self, title):
        return self._title

    def set_size(self, width, height):
        self._window.set_size(width, height)
        self._width  = self._native_window.width
        self._height = self._native_window.height

    def get_size(self):
        self._width  = self._native_window.width
        self._height = self._native_window.height
        return self._width, self._height

    def set_position(self, x, y):
        self._native_window.set_location(x,y)
        self._x, self._y = self._native_window.get_location()

    def get_position(self):
        self._x, self._y = self._native_window.get_location()
        return self._x, self._y

    def swap(self):
        self._native_window.flip()

    def activate(self):
        self._native_window.switch_to()


# ----------------------------------------------------------------- windows ---
def windows():
    return __windows__


# ----------------------------------------------------------------- process ---
def process(dt):

    for window in __windows__:

        # Activate window
        window.activate()

        # Dispatch any pending event
        window._native_window.dispatch_events()

        # Dispatch the main draw event
        window.dispatch_event('on_draw')

        # Dispatch the idle event
        window.dispatch_event('on_idle', dt)

        # Swap buffers
        window.swap()

    return len(__windows__)
