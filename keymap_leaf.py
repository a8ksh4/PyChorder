'''Custom experimental keymap for the Leaf cyberdeck.'''

import board
import keymap_helper
# PINS = (16, 21, 19, 25,
#         20, 12, 26, 13)
# PINS = (12, 13, 14, 15,
#         19, 18, 17, 16)
BATTERY_PIN = board.GP28
REVERSE_DIODES = False

ROWS = None
COLS = None
PINS = [board.GP4, board.GP3, board.GP2, board.GP1, board.GP0,
        board.GP9, board.GP8, board.GP7, board.GP6, board.GP5,
        board.GP14, board.GP13, board.GP12, board.GP11, board.GP10,
        board.GP17, board.GP16, board.GP15]

# uses the addresses of above pins in list, not gp addrs.
SHUTDOWN_COMBO = (0, 1, 2, 3, 5, 6, 7, 8)
ENCODER = ()

    # B0,  B1,  B2,  B3,  B4,  B5,  Eu,
    # B7,  B8,  B9,  B10, B11, B12, Ed, Eb

GAME_MODE_LAYER = 5
LAYERS = (
    # BASE - 0
    ('s',     't',       'r',        'a',      '-',
     'o',     'i',       'y',        'e',   '_os_shft',
     '',       '_os_alt', '_os_ctrl', '_os_shft',  '_entr',
                (1, '_esc'), (2, ' '), (3, '_tab')),

    # NUMBER - 1
    ('[', '7', '8', '9', ']',
     ';', '4', '5', '6', '=',
     '`', '1', '2', '3', '\\',
                '', '', ''),

    # SYM - 2
    ('{', '&', '*', '(', '}',
     ':', '$', '%', '^', '+',
     '~', '!', '@', '#', '|',
                '', '', ''),

    # NAV - 3
    ('_pgup', '_home', '_up',   '_end', '_mup',
     '_pgdn', '_left', '_down', '_rght', '_mdwn',
     '', '', '', '', '',
     '', '', ''),

    # MOUSE - 4
    ('_scup', '_mbt2', '_mup',  '_mbt1', '',
     '_scdn', '_mlft', '_mdwn', '_mrgt', '',
     '', '', '', '', '',
     '_mbt1', '_mbt2', '_mbt3'),

    # GAME - 5
    ('_set_base_0', '', '_up', '', 'c',
     '', '_left', '_down', '_rght', 'x',
     '1', '2', '3', '4', 'z',
     '_esc', '_entr', '_tab'),
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
    ('2', '3'):             '0',

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

    # Base layer toggle from BASE to GAME
    ('s', 't', 'r', 'a', '-'):   ('_set_base', 5),
    # ('_esc', '_entr', '_tab'):  ('_set_base', 0),
    ('_mup', '_mlft', '_mrgt'):  ('_set_base', 0),
    ('i', 'e', 'r'):  ('_set_base', 4),

    # Symbol layer addons
    ('(', '}'):             ')',
    ('_esc', ' '):          3,
    ('_tab', ' '):          '_shft',

    # shutdown system syscall
    ('a', 'r', 't', 's', 'e', 'y', 'i', 'o'): '_sys_shdn',

    ('o', 't', 'r', 'a'):   '_tab',         # Normal        *
    # ('_pgdn','_home',
    #     '_up', '_end',):    '_tab',         # Directional
    # ('_mlft', '_mbt2',
    #     '_mup', '_mbt1'):   '_tab',         # Mouse

    ('a', 'e'):             '_entr',        # Normal        *
    # ('_end', '_rght'):      '_entr',        # Directional
    # ('_mbt1', '_mrht'):     '_entr',        # Mouse

    # ('s', 'e'):             '_os_ctrl',     # Normal        *
    # #('_home', '_rght'):     '_os_ctrl',     # Directional
    # ('_mbt2', '_mrgt'):     '_os_ctrl',     # Mouse

    # # ('s', 'i'):             '_alt',
    # ('s', 't', 'r', 'e'):   '_os_shft',

    ('r', 'e'):             '_bksp',        # Normal        *
    ('8', '6'):             '_bksp',        # Number
    ('*', '^'):             '_bksp',        # Symbol
    # ('_up', '_rght'):       '_bksp',        # Directional
    # ('_mup', '_mrgt'):      '_bksp',        # Mouse

    # ('o', 'r', 'a'):        '_esc',         # Normal        *
    # ('_pgdn', '_up', '_end'): '_esc',       # Directional
    # ('_mlft', '_mup', '_mbt1'): '_esc',     # Mouse

    ('a', 'r', 'e', 'y'):   '_f11',         # Normal        *
    ('_down', '_rght', '_up', '_end'): '_f11',  # Directional
    ('_mdwn', '_mrgt', '_mup', '_mbt1'): '_f11', # Mouse

    # ('r', 't', 'y', 'i'):   '_alta', #set('_alt', '_tab'),
    # ('t', 's', 'i', 'o'):   '_salta', #set('_shft', '_alt', '_tab'),

    # Nav Layer:
    # ('e', 'r', 'i'):            ('_set_base', 4),
    # ('_left', '_up', '_rght'):  ('_set_base', 0),

    # Mouse Layer:
    # ('a', 't', 'y'):            ('_set_base', 5),
    # ('_mbt1', '_mdwn', '_mbt2'): ('_set_base', 0),
    ('_mup', '_mrgt'):      '_mdur', # Mouse diagonal up right
    ('_mup', '_mlft'):      '_mdul', # Mouse diagonal up left
    ('_mdwn', '_mrgt'):     '_mddr', # Mouse diagonal down right
    ('_mdwn', '_mlft'):     '_mddl', # Mouse diagonal down left
}

CHORDS = keymap_helper.prepare_chords(CHORDS)
