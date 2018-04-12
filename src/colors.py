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


RED = 0xCC0000
ORANGE = 0xCC8000
CYAN = 0x00CCCC
YELLOW = 0xCCCC00
BLUE = 0x00CCCC
GREEN = 0x00CC00
PINK = 0xCC00CC
WHITE = 0x808080


color = cycle([CYAN, PINK, YELLOW])
