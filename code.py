
import time
import board
import gc
import digitalio
import analogio
import usb_hid
from keymap_artsey_left import BATTERY_PIN, PINS, LAYERS, CHORDS
from keymap_translate import KEYMAP_TRANSLATE
from keys import SHIFTED
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

POLL_FREQUENCY = 200.0
HOLDTIME = 250
# ONESHOT_TIMEOUT = 500
BASE_LAYER = 0
TICKER = 0
EVENTS = []
PENDING_BUTTONS = set()
OS_SHIFT_PENDING = False
OS_CTRL_PENDING = False
OS_ALT_PENDING = False
LK_SHIFT_ACTIVE = False
TIMER = None
DEBUG = False

def to_volts(reading):
    '''Converts analog reading to volts'''
    return reading * 2 * 3.3 / 65536


def time_ms():
    '''simple ns to ms'''
    return int(time.monotonic_ns() / 1000000)


def get_output_key(buttons, layer, tap):
    '''takes the current layer and pressed buttons and figures out 
    what output key should be sent.  If a new layer should be set.'''

    #print('buttons:', buttons, 'layer:', layer, 'tap:', tap)
    
    # mapped_buttons are the keys on the current layer corresponding
    # to the pressed buttons.
    mapped_buttons = [LAYERS[layer][b] for b in buttons]
    
    # If it was a tap, we ignore any hold-for-layer keys and get the tap behavior.
    if len(mapped_buttons) > 1 or tap:
        # convert any hold-tap layer keys to just the (tap) key
        mapped_buttons = [b if isinstance(b, str) else b[1] 
                            for b in mapped_buttons]
        mapped_buttons = tuple(sorted(mapped_buttons))
        
        # Multuple buttons pressed, translate chord to output key
        if len(mapped_buttons) > 1:
            result = CHORDS.get(mapped_buttons, (None, None))
            assert isinstance(result, tuple)
            
        else:
            # Not a chord
            result = mapped_buttons[0], None

    else:
        if isinstance(mapped_buttons[0], str):
            result = mapped_buttons[0], None
        else:
            result = None, mapped_buttons[0][0]

    #print(f'get output key: {buttons}, {layer}, {tap}, {result}')
    return result


def activate_keys(buttons_pressed, device):
    '''preserves history of buttons already pressed.
    '''
    global TICKER  
    global BASE_LAYER
    global EVENTS
    global OS_SHIFT_PENDING
    global OS_CTRL_PENDING
    global OS_ALT_PENDING

    clock = time_ms()

    current_layer = [BASE_LAYER,] + [e['layer'] for e in EVENTS if e['layer']]
    current_layer = current_layer[-1]

    # Remove events whos buttons are no longer pressed.
    for event in EVENTS:
        still_pressed = [b for b in event['buttons'] if b in buttons_pressed]
        if not still_pressed:
            event['status'] = 'released'

    # Remove buttons from buttons_pressed if associated with an event
    all_event_butons = sum([e['buttons'] for e in EVENTS], [])
    #print('all event buttons:', all_event_butons)
    buttons_pressed = [b for b in buttons_pressed if b not in all_event_butons]

    # Move buttons_pressed to pending - pending buttons is buttons
    # that have been pressed but are not associated with an event.
    PENDING_BUTTONS.update(buttons_pressed)

    if PENDING_BUTTONS:
        if not TICKER:
            TICKER = clock

        # DO WE MEET THE CONDITIONS TO START A NEW EVENT?
        if ( len(PENDING_BUTTONS) > len(buttons_pressed)  # one or more keys released
                or clock - TICKER > HOLDTIME ):           # hold time exceeded

            tap =  clock - TICKER < HOLDTIME

            # print(f'{(len(PENDING_BUTTONS), len(buttons_pressed), clock, TICKER, clock-TICKER)}')
            output_key, new_layer = get_output_key(PENDING_BUTTONS, current_layer, tap)
            # print(f'output_key: {output_key}, new_layer: {new_layer}')

            if output_key == '_set_base':
                BASE_LAYER = new_layer
                output_key, new_layer = None, None

            if output_key == '_os_shft':
                OS_SHIFT_PENDING = True
                output_key = None

            if output_key == '_os_ctrl':
                OS_CTRL_PENDING = True
                output_key = None

            if output_key == '_os_alt':
                OS_ALT_PENDING = True
                output_key = None

            if output_key is not None and OS_SHIFT_PENDING:
                if output_key in SHIFTED:
                    output_key = SHIFTED[output_key]
                OS_SHIFT_PENDING = False

            if output_key is not None and OS_CTRL_PENDING:
                output_key = ('_ctrl', output_key)
                OS_CTRL_PENDING = False

            if output_key is not None and OS_ALT_PENDING:
                output_key = ('_alt', output_key)
                OS_ALT_PENDING = False

            # align on tuple output_key
            if not isinstance(output_key, tuple):
                output_key = (output_key,)

            new_event = {'buttons': list(PENDING_BUTTONS),
                            'output_keys': output_key,
                            'layer': new_layer,
                            'status': 'new',
                            'uinput_codes': []
                        }

            # print(f'New event: {new_event}')
            EVENTS.append(new_event)
            PENDING_BUTTONS.clear()
            TICKER = 0

    # Relase keys for ended events
    for event in EVENTS:
        if event['status'] != 'released':
            continue

        for uinput_code in event['uinput_codes'][::-1]:
            print('    device release', uinput_code)
            device.release(uinput_code)
        event['status'] = 'delete'
        # print(event)

    # Delete done events
    EVENTS = [e for e in EVENTS if e['status'] != 'delete']

    # Check for ctrl alt shift state
    alt_pressed = [e for e in EVENTS if '_alt' in e['output_keys'] and e['status'] == 'active']
    shift_pressed = [e for e in EVENTS if '_shift' in e['output_keys'] and e['status'] == 'active']
    ctrl_pressed = [e for e in EVENTS if '_ctrl' in e['output_keys'] and e['status'] == 'active']

    # Generate key press based on top active event.
    if EVENTS and EVENTS[-1]['status'] == 'new':
        last_event = EVENTS[-1]
        last_event['status'] = 'active'
        effective_keys = [k for k in last_event['output_keys'] if
                            not (k == '_alt' and alt_pressed) and
                            not (k == '_shift' and shift_pressed) and
                            not (k == '_ctrl' and ctrl_pressed)]

        uinput_codes = [KEYMAP_TRANSLATE[k] for k in effective_keys
                            if k and k is not None]
        # print('effective_keys:', effective_keys)
        # print('uinput_codes:', uinput_codes)
        unpress_later = []
        for uinput_code in uinput_codes:
            # if isinstance(uinput_code[0], tuple):
            if isinstance(uinput_code, tuple):
                temp_codes = uinput_code[:-1]
                keep = uinput_code[-1]
            else:
                temp_codes = []
                keep = uinput_code
            unpress_later.append(keep)

            for temp_code in temp_codes:
                print('    device press', temp_code)
                device.press(temp_code)
                time.sleep(0.01)

            print('    device press', keep)
            device.press(keep)
            time.sleep(0.01)
            for temp_code in temp_codes:
                print('    device release', temp_code)
                device.release(temp_code)
                time.sleep(0.01)
        last_event['uinput_codes'] = unpress_later


##############################################################################
# Main loop
##############################################################################
time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems

keyboard = Keyboard(usb_hid.devices)
keyboard_layout = KeyboardLayoutUS(keyboard)

# Initialize the key pins and analog battery pin
key_pins = []
for pin in PINS:
    key_pin = digitalio.DigitalInOut(pin)
    key_pin.direction = digitalio.Direction.INPUT
    key_pin.pull = digitalio.Pull.UP
    key_pins.append(key_pin)

battery_pin = analogio.AnalogIn(BATTERY_PIN)

# Event tracking variables for in loop
last_voltage_report_time = 0
previously_pressed = None
pressed_time = None
pressed_toggle = False
counter = 0

while True: 
    counter += 1
    current_time = time.monotonic()
    
    # Check each pin
    pressed = [n for n, key_pin in enumerate(key_pins)
                    if not key_pin.value]

    # Report battery voltage every 15 seconds and check for gc
    if current_time - last_voltage_report_time > 15:
        print('voltage:', to_volts(battery_pin.value))
        last_voltage_report_time = current_time
        
        # gc now if nothing is happening
        if not ( pressed
                 or previously_pressed
                 or pressed_toggle):
            gc.collect()
        
    if pressed != previously_pressed:
        print('pressed:', pressed, counter, current_time)
        previously_pressed = pressed
        pressed_time = current_time
        pressed_toggle = True
        activate_keys(pressed, keyboard)

    elif pressed_toggle \
            and (current_time - pressed_time)*1000 > HOLDTIME:
        print('pressed toggle:', pressed, counter, current_time)
        # pressed_toggle makes sure activate_keys gets called after 
        # the defined hold time so keys that are layer changes when held
        # get activated before any subsequent key presses that depend 
        # on the layer change. 
        activate_keys(pressed, keyboard)
        pressed_toggle = False

    time.sleep(1/POLL_FREQUENCY)
