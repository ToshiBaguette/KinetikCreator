from itertools import chain


# PARTIE TEXTE
def truncline(text, font, maxwidth):
    """Fonction coupant le texte en deux pour tenir sur plusieurs lignes à longueur fixe"""
    real = len(text)
    stext = text
    l = font.size(text)[0]
    cut = 0
    a = 0
    done = 1
    while l > maxwidth:
        a = a + 1
        n = text.rsplit(None, a)[0]
        if stext == n:
            cut += 1
            stext = n[:-cut]
        else:
            stext = n
        l = font.size(stext)[0]
        real = len(stext)
        done = 0
    return real, done, stext


def wrapline(text, font, maxwidth):
    """
    Fonction à appeler lorsqu'on veut couper un string en plusieurs lignes (sans prendre les \n en compte)
    :param text: Texte à couper
    :param font: Police de caractère
    :param maxwidth: Taille de la ligne en pixels
    :return: Liste de lignes
    """
    done = 0
    wrapped = []

    while not done:
        nl, done, stext = truncline(text, font, maxwidth)
        wrapped.append(stext.strip())
        text = text[nl:]
    return wrapped


def wrap_multi_line(text, font, maxwidth):
    """
    Fonction à appeler lorsqu'on veut couper un string en plusieurs lignes (prenant en compte les \n)
    :param text: Texte à couper
    :param font: Police de caractères
    :param maxwidth: Taille de la ligne en pixels
    :return: Liste de lignes
    """
    lines = chain(*(wrapline(line, font, maxwidth) for line in text.splitlines()))
    return list(lines)

def get_cursor_pos(cursor, lines):
    x, y = 0, 0
    remaining = cursor
    for line in lines:
        for letter in line:
            if remaining > 0:
                x += 1
                remaining -= 1
        if remaining > 0:
            x = 0
            y += 1

    return x, y
