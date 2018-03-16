def cycle(p):
    try:
        len(p)
    except TypeError:
        # len() is not defined for this type. Assume it is
        # a finite iterable so we must cache the elements.
        cache = []
        for i in p:
            yield i
            cache.append(i)
        p = cache
    while p:
        yield from p


RED = 0xFF0000
ORANGE = 0xFF8000
YELLOW = 0xFFFF00
CYAN = 0x00FFFF
BLUE = 0x0000FF
PINK = 0xFF00FF
WHITE = 0x808080


color = cycle([CYAN, PINK, YELLOW])
