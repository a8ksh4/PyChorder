"""Keyboard layout for artseio using top left 4x2 keys."""

import board
import keymap_helper
# PINS = (16, 21, 19, 25,
#         20, 12, 26, 13)
# PINS = (12, 13, 14, 15,
#         19, 18, 17, 16)
BATTERY_PIN = board.GP28

# PINS = [board.GP0, board.GP1, board.GP2, board.GP3, board.GP4,
#         board.GP5, board.GP6, board.GP7, board.GP8, board.GP9,
#         board.GP10, board.GP11, board.GP12, board.GP13, board.GP14,
#         board.GP15, board.GP16, board.GP17]
PINS = [board.GP4, board.GP3, board.GP2, board.GP1, board.GP0,
        board.GP9, board.GP8, board.GP7, board.GP6, board.GP5,
        board.GP14, board.GP13, board.GP12, board.GP11, board.GP10,
        board.GP17, board.GP16, board.GP15]


ENCODER = ()

    # B0,  B1,  B2,  B3,  B4,  B5,  Eu,
    # B7,  B8,  B9,  B10, B11, B12, Ed, Eb

LAYERS = (
    # BASE
    ((1, 's'), 't', 'r', (2, 'a'), '',
     'o',      'i', 'y', (3, 'e'), '',
     '', '', '', '', '',
     '', '', ''),

    # NUMBER
    ('', '3', '2', '1', '',
     '', '6', '5', '4', '',
     '', '', '', '', '',
     '', '', ''),

    # PARENS
    ('}', '(', ')', '', '',
     '{', '[', ']', '', '',
     '', '', '', '', '',
     '', '', ''),

    # SYMBOL
    ('`', ';', '\\', '!', '',
     '=', '-', '?',  '', '',
     '', '', '', '', '',
     '', '', ''),

    # NAV
    ('_pgup', '_home', '_up',   '_end', '',
     '_pgdn', '_left', '_down', '_rght', '',
     '', '', '', '', '',
     '', '', ''),

    # MOUSE
    ('_scup', '_mbt2', '_mup',  '_mbt1', '',
     '_scdn', '_mlft', '_mdwn', '_mrgt', '',
     '', '', '', '', '',
     '', '', '')
)

CHORDS = {
    ### BASE LAYER ###
    #                       'a',
    ('o', 'e'):             'b',
    ('y', 'e'):             'c',
    ('a', 'r', 't'):        'd',
    #                       'e',
    ('a', 'r'):             'f',
    ('r', 't'):             'g',
    ('i', 'e'):             'h',
    #                       'i',
    ('s', 't'):             'j',
    ('o', 'y'):             'k',
    ('e', 'y', 'i'):        'l',
    ('o', 'i', 'y'):        'm',
    ('o', 'i'):             'n',
    #                       'o',
    ('o', 'i', 'e'):        'p',
    ('s', 't', 'a'):        'q',
    #                       'r',
    #                       's',
    #                       't',
    ('y', 'i'):             'u',
    ('s', 'r'):             'v',
    ('s', 'a'):             'w',
    ('s', 't', 'r'):        'x',
    #                       'y',
    ('s', 't', 'r', 'a'):   'z',
    #
    ('1', '2'):             '7',
    ('2', '3'):             '8',
    ('4', '5'):             '9',
    ('5', '6'):             '0',
    ('4', '2'):             '_bksp',
    ('4', '1'):             '_entr',
    ('_rght', '_end'):      '_entr',
    #
    ('o', 'i', 'y', 'e'):   ' ',
    ('y', 'a'):             '.',
    ('i', 'a'):             ',',
    ('a', 'o'):             '/',
    ('a', 'i', 'y'):        "'",
    ('t', 'i'):             '|',
    ('r', 'y'):             ':',
    ('r', 'i'):             ')',
    ('t', 'y'):             '(',
    ('r', 'i', 'y'):        '[',
    ('t', 'y', 'i'):        ']',
    # ('(', ')'):             ':',  # this is a little weird.

    ('o', 't', 'r', 'a'):   '_tab',         # Normal        *
    ('_pgdn','_home',
        '_up', '_end',):    '_tab',         # Directional
    ('_mlft', '_mbt2',
        '_mup', '_mbt1'):   '_tab',         # Mouse

    ('a', 'e'):             '_entr',        # Normal        *
    ('_end', '_rght'):      '_entr',        # Directional
    ('_mbt1', '_mrht'):     '_entr',        # Mouse

    ('s', 'e'):             '_os_ctrl',     # Normal        *
    #('_home', '_rght'):     '_os_ctrl',     # Directional
    ('_mbt2', '_mrgt'):     '_os_ctrl',     # Mouse

    # ('s', 'i'):             '_alt',
    ('s', 't', 'r', 'e'):   '_os_shft',

    ('r', 'e'):             '_bksp',        # Normal        *
    ('_up', '_rght'):       '_bksp',        # Directional
    # ('_mup', '_mrgt'):      '_bksp',        # Mouse

    ('o', 'r', 'a'):        '_esc',         # Normal        *
    ('_pgdn', '_up', '_end'): '_esc',       # Directional
    ('_mlft', '_mup', '_mbt1'): '_esc',     # Mouse

    # ('a', 'r', 'e', 'y'):   '_f11',         # Normal        *
    # ('_down', '_rght', '_up', '_end'): '_f11',  # Directional
    # ('_mdwn', '_mrgt', '_mup', '_mbt1'): '_f11', # Mouse

    # ('r', 't', 'y', 'i'):   '_alta', #set('_alt', '_tab'),
    # ('t', 's', 'i', 'o'):   '_salta', #set('_shft', '_alt', '_tab'),

    # Nav Layer:
    ('e', 'r', 'i'):            ('_set_base', 4),
    ('_left', '_up', '_rght'):  ('_set_base', 0),

    # Mouse Layer:
    ('a', 't', 'y'):            ('_set_base', 5),
    ('_mbt1', '_mdwn', '_mbt2'): ('_set_base', 0),
    ('_mup', '_mrgt'):      '_mdur', # Mouse diagonal up right
    ('_mup', '_mlft'):      '_mdul', # Mouse diagonal up left
    ('_mdwn', '_mrgt'):     '_mddr', # Mouse diagonal down right
    ('_mdwn', '_mlft'):     '_mddl', # Mouse diagonal down left
}

CHORDS = keymap_helper.prepare_chords(CHORDS)
