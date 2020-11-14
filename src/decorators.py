from src.utils import color


def header(function):
    def formatting(*args, **kwargs):

        line_size = kwargs.get('size', 70)
        fmt = kwargs.get('format', False)
        head = kwargs.get('head', True)

        if fmt is True:

            if head is True:
                print('\n' + '#' * line_size + '\n')
                print(color(**kwargs).center(line_size))
                function(*args, **kwargs)
                print('\n' + '#' * line_size + '\n')

            else:
                print('\n' + '#' * line_size + '\n')

        else:
            return function(*args, **kwargs)

    return formatting
