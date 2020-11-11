def _get_attr_dict(**kwargs):

    dict_colors = {
        'white': ';30',
        'red': ';31',
        'green': ';32',
        'yellow': ';33',
        'blue': ';34',
        'purple': ';35',
        'lblue': ';36',
        'grey': ';37',
    }

    dict_effects = {
        'none': '0',
        'bold': '1',
        'underline': '4',
        'negative': '7',
    }

    dict_backgrounds = {
        'white': ';40',
        'red': ';41',
        'green': ';42',
        'yellow': ';43',
        'blue': ';44',
        'purple': ';45',
        'lblue': ';46',
        'grey': ';47',
    }

    cor = kwargs.get('cor')
    effect = kwargs.get('effect')
    background = kwargs.get('background')

    color_number = dict_colors.get(cor, '')
    effect_number = dict_effects.get(effect, '')
    background_number = dict_backgrounds.get(background, '')

    return color_number, effect_number, background_number


def _color(**kwargs):

    cor, effect, background = _get_attr_dict(**kwargs)
    text = kwargs.get('text', '')

    return f'\033[{effect}{cor}{background}m{text}\033[m'


def header(function):
    def formatting(*args, **kwargs):
        line_size = kwargs.get('size', 70)
        format = kwargs.get('format', False)

        if format is True:
            print('\n' + '#' * line_size + '\n')
            print(_color(**kwargs).center(line_size))
            function(*args, **kwargs)
            print('\n' + '#' * line_size + '\n')

        else:
            return function(*args, **kwargs)

    return formatting
