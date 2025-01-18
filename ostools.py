"""functions that do the things in files"""
import os



def emballage(func, *args, **kwargs):
    def f():
        return func(*args, **kwargs)
    return f

def make_path(*elems : str):
    return "\\".join(elems)


def get_chara(mod_folder, deepness = 0):

    def filtered(string):
        return string.startswith("BufferValues") or "." in string
    if deepness == 0:
        lst = [name for name in os.listdir(mod_folder) if not filtered(name)]
    else:
        lst = []
        for chara in os.listdir(mod_folder):
            if not filtered(chara):
                for name in get_chara(make_path(mod_folder, chara), deepness-1):
                    lst.append(make_path(chara, name))
    return sorted(lst)