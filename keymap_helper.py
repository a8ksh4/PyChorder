"""This code has been migrated out of the keymap file so that it can be
updated in one place and used in all of the keymap files."""

def prepare_chords(chords):
    '''The output from the chords dict needs to be a tuple, so we convert the 
    human friendly format to this.'''
    tmp = []
    for k, v in chords.items():
        assert isinstance(k, tuple)
        assert isinstance(v, (str, tuple, int))
        if isinstance(v, tuple):
            # hold-tap instance of key layer change
            assert len(v) == 2
            assert isinstance(v[0], str)
            assert isinstance(v[1], int)

        elif isinstance(v, str):
            # plain key instance
            v = (v, None)

        elif isinstance(v, int):
            # plain layer change
            v = (None, v)

        tmp.append((tuple(sorted(k)), v))
    return dict(tmp)
