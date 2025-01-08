"""ossature mod manager"""
import os
import tkinter as tk
from tkinter import ttk


MODS_FOLDER = ("c:/Users/Thomas/AppData/Roaming/XXMI Launcher/GIMI/Mods")
DEEPNESS = 2 # profondeurs de categories, 0 = RaidenMod, 1 = Mods/Raiden/RaidenMod, 2 = Mods/Characters/Raiden/RaidenMod

IGNORE = [
    ".",
    "BufferValue",
]

class Mod:
    def __init__(self, *modpath):
        self.modpath = modpath[:-1]
        self.name = modpath[-1]
    


    def is_disable(self) -> bool:
        return self.name.lower().startswith("disabled")
    
    def relative_path(self):
        return "/".join(self.modpath) + '/' + self.name
    
    def absolute_path(self):
        return MODS_FOLDER + "/" + self.relative_path()

    
    def disable(self):

        try:
            old_path = self.absolute_path()
            self.name = "DISABLED_" + self.name
            os.rename(old_path, self.absolute_path())
        except FileNotFoundError:
            print("this mod wasn't found")

    def clean_name(self):
        if self.is_disable():
            name = self.name[8:]
            while name.startswith('_'):
                name = name[1:]
            return name
        else:
            return self.name

    def able(self):
        try:
            assert self.is_disable()
            old_path = self.absolute_path()
            self.name = self.clean_name()
            os.rename(old_path, self.absolute_path())
        except FileNotFoundError:
            print("this mod cannot be found", self.path)

        except AssertionError:
            print("This mod isn't disabled", self.path)
        

    def toggle(self):
        if self.is_disable():
            self.able()
            self.bouton.config(bg = 'green')
        else:
            self.disable()
            self.bouton.config(bg = "red")



def deballeur_mods(path, deepness):
    for ignore in IGNORE:
        if os.path.basename(path).startswith(ignore): return 
    
    if deepness == 0:
        for mod in os.listdir(path):
            yield [mod]
    else:
        for folder in os.listdir(path):
            for *lp, mod in deballeur_mods(path + "/" + folder, deepness -  1):
                yield [folder] + lp + [mod]

    return


def init_mods(path):
    LIST_MODS = []
    for modpath in deballeur_mods(MODS_FOLDER, DEEPNESS):
        mod = Mod(*modpath)
        LIST_MODS.append(mod)
    return LIST_MODS


def main():
# Création de la fenêtre principale

    
    LIST_FRAMES = {}
    LIST_MODS = init_mods(MODS_FOLDER)
    def init_frame(name: str):
        frame = tk.Frame(scrollable_frame, bg = "black")
        LIST_FRAMES[name] = frame
        tk.Label(frame, text = name, bg = "black", fg= "white").pack(anchor = "n")
        frame.pack(anchor = "w")

    def buttonize():
        for mod in LIST_MODS:
            if DEEPNESS:
                name = mod.modpath[-1]
                if name not in LIST_FRAMES:
                    init_frame(name)
                mod.bouton = tk.Button(LIST_FRAMES[name], text = mod.clean_name(), command=mod.toggle)
                mod.bouton.config(bg = "red" if mod.is_disable() else "green")
                mod.bouton.pack(anchor = "w")
            else:
                mod.bouton = tk.Button(scrollable_frame, text = mod.clean_name(), command=mod.toggle)
                mod.bouton.config(bg = "red" if mod.is_disable() else "green")
                mod.bouton.pack()

    def refresh():
        while LIST_MODS:
            mod = LIST_MODS.pop()
            mod.bouton.destroy()
        for mod in init_mods(MODS_FOLDER):
            LIST_MODS.append(mod)

        
        buttonize()



    racine = tk.Tk()
    racine.title("Mon Application Tkinter")
    racine.config(bg = "black")

    tk.Button(racine, text = "refresh", command = refresh).pack(anchor="nw")

    frame = tk.Frame(racine, bg = 'black')
    frame.pack(fill = tk.BOTH, expand = True)
    canvas = tk.Canvas(frame, bg = "black") 
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=canvas.yview) 
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = tk.Frame(canvas, bg = "black") 
    scrollable_frame.bind( "<Configure>", lambda e: canvas.configure( scrollregion=canvas.bbox("all") ) ) 
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    
    buttonize()

    # Lancement de la boucle principale de l'application
    racine.mainloop()



if __name__=="__main__":
    # for modpath in deballeur_mods(MODS_FOLDER, 1):
    #     mod = Mod(*modpath)
    #     print(mod.name)
    #     print(mod.relative_path())

    main()