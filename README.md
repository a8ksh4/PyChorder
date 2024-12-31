# PyChorder
This is simple chording keyboard firmware written in circuitpython.  I adapted it from my other gpio keyboard firmware and have removed some of the features to keep things simple for now.

It support lots of features:
* Typing
* Chords - press 'a' and 'r' to type 'f'.
* Momentary layer changes - hold a key to active a layer for a moment
* Default layer changes - set the base layer
* Oneshot Shift, Ctrl, Alt.
* Arrow keys, home, end, pgup, pgdn navigation.
* Reporting battery voltage on the serial device from an analog pin.
* Generating key combinations as a single action.  E.g. '_alta' will generate an alt+tab key press.
* Game mode for a specific layer with chording disabled to reduce keypress latency.

To be added shortly or if needed:
* System command execution triggered from keypress (via the service)
* one-shot layer changes.
* Mouse cursor movement.
* Mouse wheel
* Encoder wheel
* Adjusting audio levels, display brightness
* Pin matrix scanning (currently it's one key per pin)
* Keypress Sequences from a single key
* Support setting the voltage pin to None if it isn't needed.

Known Issues
* Alt wasn't working?

## Changing the Keymap
When you create a new keymap file, update the import statement at the top of code.py to reference it:
* from keymap_artsey_left import BATTERY_PIN, PINS, LAYERS, CHORDS

The keymap file is written in python (and looks a lot like json probably).
* PINS and LAYERS are the expected keyboard layout stuff.
* CHORDS lists the combinations of keys that produce other effects.

### Supported Keys and Special Keys/Effects
* Most keys are given as thenir character in quotes.  E.g. 'a' will type an 'a'.
  * 'a' - 'z'
  * 'A' - 'Z'
  * '0' - '9'
  * '!', '@', ... '|', '<', ... all of the symbols
* Layer changes are given as a tuple with the layer number and optionaly a character to be typed if the key is tapped rather than held.
  * (1, 'a') will change to layer 1 when held or type an 'a' if tapped.
* And behaviors without a symbol use a special word:
  * Functional stuff: '_esc', '_tab', '_entr', ' ' (space)
  * Navigation: '_left', '_rght', '_up', '_down', '_pgup', '_pgdn', '_home', '_end'
  * Mouse Diagonals: '_mdur' (up right), '_mdul', '_mddr" (down right), '_mddl'
  * One-Shot Operations: '_os_shift', '_os_ctrl', '_os_alt'

### Keymap_translate file
The primary functionality here is to translate the content in our keymap to the codes that circuitpython sends to the computer.  E.g. 'A' is a Keycode.SHIFT and a Keycode.A.

Scroll down to the bottom and you can define keys like the following that will generate key combinations:
* '_alta': (Keycode.LEFT_ALT, Keycode.TAB),
* '_salta': (Keycode.LEFT_ALT, Keycode.LEFT_SHIFT, Keycode.TAB),

And at the bottom you can map aliases  to commands to be exesuted by the service on keypres.  Give the account and command as key value pair.  For example:
* '_sys_shdn': {'root': 'shutdown now'},
* '_sys_touch': {'dan': 'touch /tmp/touched'},

## Configuring the service for battery reporting
* Edit the battery.service with the paths appropriate for your system:
  * StandardOutput=file:/home/dan/git/PyChorder/battery.log
  * StandardError=file:/home/dan/git/PyChorder/battery.log
  * WorkingDirectory=/home/dan/git/PyChorder
  * ExecStart=/home/dan/git/PyChorder/keyboard_service.py
* Edit the output file and serial port in keyboard_service.py to reference the serial port that shows up on your system when you plug in the keyboard with circuitpython on it into your computer.
  * BATTERY_FILE = '/home/dan/.battery'
  * SERIAL_PORT = '/dev/ttyACM0'
  
## Globals in the code.py
You may want to adjust HOLD_TIME to adjust how much time it takes for a combinatino of keys being pressed to be tested as a chord.  Longer means you have a little more time to plop down your fingers to generate a chord.  Other implications:
* ...
* BATTERY_REPORT_INTERVAL = 15000  # in ms
  * Battery voltage report is via serial device, e.g. /dev/ttyACM0
* POLL_FREQUENCY = 200.0  # in Hz
* HOLDTIME = 200  # in ms
  * How long you have to press all keys to form a chord.
* ONESHOT_TIMEOUT = 500
  * Not implemented
* BASE_LAYER = 0
  * The default base layer.  This will be updated by _set_base key bindings.
