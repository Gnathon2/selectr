"""functions that do the things in files"""
import os
from typing import Iterator


def emballage(func, *args, **kwargs):
    """wrapper for tkinter buttons"""
    def f():
        return func(*args, **kwargs)
    return f

def make_path(*elems : str):
    return os.path.sep.join(elems)

def abs_of_path(path):
    return os.path.abspath(path)


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

def get_names(rootpath, deepness = 1) -> Iterator[tuple[str]]:
    """Return tuples the length of deepness containing the relative path from rootpath to all the folders at given deepness"""
    if deepness <= 0:
        yield tuple()
    else:
        for name in os.listdir(rootpath):
            abs = make_path(rootpath, name)
            if os.path.isdir(abs): # filter the files
                for rest in get_names(abs, deepness-1):
                    yield (name,) + rest
    return




def name_of_path(path):
    return os.path.basename(os.path.abspath(path))

def partent_of_path(path):
    return os.path.dirname(os.path.abspath(path))

def clean_name_of_path(path):
    name = name_of_path(path)
    while name.lower().startswith('disabled'):
        name = name[8:]
        while name.startswith("_"):
            name = name[1:]
    return name

def is_mod_disabled(modpath):
    name = name_of_path(modpath)
    return name.lower().startswith("disabled")

def disable_mod(modpath):
    """os.rename can raise an error, the handler is in the widgets, i thought it was more appropriate"""
    old_p = abs_of_path(modpath)
    new_p = clean_path(modpath)
    os.rename(old_p, new_p)
    return new_p



def able_mod(modpath):
    old_p = abs_of_path(modpath)
    new_p = disable_path(modpath)
    os.rename(old_p, new_p)
    return new_p


def toggle_mod(modpath):
    if is_mod_disabled(modpath):
        return able_mod(modpath)
    else:
        return disable_mod(modpath)



def clean_path(path):
    path = os.path.abspath(path)
    dir = os.path.dirname(path)
    name = clean_name_of_path(path)
    return make_path(dir, name)

def disable_path(path):
    path = os.path.abspath(path)
    dir = os.path.dirname(path)
    name = clean_name_of_path(path)
    return make_path(dir, "DISABLED_" + name)


if __name__ == "__main__":
    abs = os.path.abspath(os.curdir)
    print(abs)
    print(os.path.abspath(os.pardir))
    print(os.path.sep)
    print(os.path.basename(abs))

