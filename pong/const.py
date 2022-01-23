import pygame as pg

WIDTH = 800
HEIGHT = 600
FPS = 60

# PS DualSense
# axis
JOY_LEFT_STICK_AXIS_X = 0
JOY_LEFT_STICK_AXIS_Y = 1
JOY_RIGHT_STICK_AXIS_X = 2
JOY_RIGHT_STICK_AXIS_Y = 3
JOY_L2_AXIS = 4
JOY_R2_AXIS = 5
# buttons
JOY_BUTTON_CROSS = 0
JOY_BUTTON_CIRCLE = 1
JOY_BUTTON_SQUARE = 2
JOY_BUTTON_TRIANGLE = 3
JOY_BUTTON_SELECT = 4
JOY_BUTTON_HOME = 5
JOY_BUTTON_START = 6
JOY_LEFT_STICK_BUTTON = 7
JOY_RIGHT_STICK_BUTTON = 8
JOY_BUTTON_L1 = 9
JOY_BUTTON_R1 = 10
JOY_DPAD_UP = 11
JOY_DPAD_DOWN = 12
JOY_DPAD_LEFT = 13
JOY_DPAD_RIGHT = 14
JOY_BUTTON_PANEL = 15

JOY_KEYS = {
    JOY_BUTTON_CROSS: 'cross',
    JOY_BUTTON_CIRCLE: 'circle',
    JOY_BUTTON_SQUARE: 'square',
    JOY_BUTTON_TRIANGLE: 'triangle',
    JOY_BUTTON_SELECT: 'select',
    JOY_BUTTON_HOME: 'home',
    JOY_BUTTON_START: 'start',
    JOY_LEFT_STICK_BUTTON: 'L3',
    JOY_RIGHT_STICK_BUTTON: 'R3',
    JOY_BUTTON_L1: 'L1',
    JOY_BUTTON_R1: 'R1',
    JOY_DPAD_UP: 'joy up',
    JOY_DPAD_DOWN: 'joy down',
    JOY_DPAD_LEFT: 'joy left',
    JOY_DPAD_RIGHT: 'joy right',
    JOY_BUTTON_PANEL: 'joy panel',
}
JOY_AXIS = {
    JOY_LEFT_STICK_AXIS_X: {-1: 'left stick left', 1: 'left stick right'},
    JOY_LEFT_STICK_AXIS_Y: {-1: 'left stick up', 1: 'left stick down'},
    JOY_RIGHT_STICK_AXIS_X: {-1: 'right stick left', 1: 'right stick right'},
    JOY_RIGHT_STICK_AXIS_Y: {-1: 'right stick up', 1: 'right stick down'},
    JOY_L2_AXIS: {1: 'L2'},
    JOY_R2_AXIS: {1: 'R2'},
}

DEFAULT_ACCEPT_KEYS = dict(event_key=(pg.K_SPACE, pg.K_RETURN), event_joy_key=(JOY_BUTTON_CROSS, JOY_BUTTON_START))
