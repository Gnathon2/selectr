"""ossature mod manager

TODO : petit bug bizarre avec deepness > 0"""
import os
import tkinter as tk
from tkinter import ttk


def deprecated(f):
    def func(*args, **kwargs):
        raise DeprecationWarning
        return f(*args, **kwargs)
    return func

def make_path(*elems : str):
    return "\\".join(elems)
    
def from_rgb(r,g,b):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return f'#{r:02x}{g:02x}{b:02x}'

def emballage(func, *args, **kwargs):
    def f():
        return func(*args, **kwargs)
    return f



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



 
MODS_FOLDER = ("c:/Users/Thomas/AppData/Roaming/XXMI Launcher/GIMI/Mods")
DEEPNESS = 2 # profondeurs de categories, 0 = RaidenMod, 1 = Mods/Raiden/RaidenMod, 2 = Mods/Characters/Raiden/RaidenMod

IGNORE = [
    ".",
    "BufferValue",
]

class Mod(tk.Frame):


    
    def __init__(
            self, 
            name, 
            folder, 
            cmd_goto, 
            *args,
            bg ,
            fg, 
            nsfw = True, 
            **kwargs
        ):
        self.folder = folder
        self.name = name


        tk.Frame.__init__(self, *args, bg = bg, **kwargs)

        BG = self.cget("bg")
        FG = "white"
        BG_ON = "green"
        BG_OFF = "red"

        self.btn_toggle = tk.Button(self, bg = BG_OFF if self.is_disable() else BG_ON, fg = FG, command=self.cmd_toggle, text='   ')
        
        self.btn_name = tk.Button(self, bg = BG,fg = FG, text=self.clean_name(), command = cmd_goto)



        # grid
        self.btn_toggle.grid(row = 0, column=1)
        self.btn_name.grid(row=0, column=2)

    
    
    def path(self):
        return make_path(self.folder, self.chara, self.name)

    def clean_name(self):
        while self.is_disable():
            self.name = self.name[8:] # delete "DISABLE"
            while self.name.startswith('_'):
                self.name = self.name[1:]
        return self.name
        

    def is_disable(self) -> bool:
        return self.name.lower().startswith("disabled")
    
    def disable(self):

        try:
            old_path = self.path()
            self.name = "DISABLED_" + self.clean_name()
            os.rename(old_path, self.path())
        except FileNotFoundError:
            print("this mod wasn't found")

    def able(self):
        try:
            assert self.is_disable()
            old_path = self.path()
            self.name = self.clean_name()
            os.rename(old_path, self.path())
        except FileNotFoundError:
            print("this mod cannot be found", self.path)

        except AssertionError:
            print("This mod isn't disabled", self.path)
        

    def cmd_toggle(self):
        if self.is_disable():
            self.able()
            self.btn_toggle.config(bg = 'green')
        else:
            self.disable()
            self.btn_toggle.config(bg = "red")

    def cmd_goto(self, path):
        self.current_dir = path
        self.refresh()



@deprecated
def deballeur_mods(path, deepness):
    for ignore in IGNORE:
        if os.path.basename(path).startswith(ignore): return 
    
    if deepness == 0:
        for mod in os.listdir(path):
            yield [mod]
    else:
        for folder in os.listdir(path):
            for *lp, mod in deballeur_mods(path + "\\" + folder, deepness -  1):
                yield [folder] + lp + [mod]

    return

@deprecated
def init_mods(path):
    LIST_MODS = []
    for modpath in deballeur_mods(MODS_FOLDER, DEEPNESS):
        mod = Mod(*modpath)
        LIST_MODS.append(mod)
    return LIST_MODS

    
class Chara(tk.Frame):
    Ellipsis


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
                name = mod.name
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





class Game(tk.Frame):

    def __init__(
            self,
            mod_folder,
            *args, 
            bg = "#111111",
            fg = "#FFFFFF",
            deepness = 1,
            **kwargs,
            
        ):

        tk.Frame.__init__(self, *args, bg=bg, **kwargs)

        self.bg = bg
        self.fg = fg
    
        self.deepness = 1
        self.deep = 0
        self.current_dir = mod_folder
        self.lst_chara = get_chara(mod_folder)
        self.pack(expand=True, fill = tk.BOTH)

        self.lst_mods = []

        refresh_btn = tk.Button(self, bg = bg, fg = fg, command = self.refresh, text='refresh')
        refresh_btn.pack(anchor='n')

        goback_btn = tk.Button(self, bg = bg, fg = fg, command = self.cmd_goback, text='<-')
        goback_btn.pack(anchor = 'nw')

        self.titre = tk.Label(self, bg =bg , fg =fg , text=self.current_dir)
        self.titre.pack()



        canvas = tk.Canvas(self, bg = "black") 
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview) 
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        self.scrollable_frame = tk.Frame(canvas, bg = "black") 
        self.scrollable_frame.bind( "<Configure>", lambda e: canvas.configure( scrollregion=canvas.bbox("all") ) ) 
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

    
        self.refresh()

    
    def refresh(self):
        lst_chara = get_chara(self.current_dir, self.deepness)
        self.titre.config(text=self.current_dir)
        for mod in self.lst_mods:
            mod.destroy()

        self.lst_mods = []
        for name in lst_chara:
            mod = Mod(
                name, 
                self.current_dir, 
                emballage(self.cmd_goto, make_path(self.current_dir, name)),
                self.scrollable_frame,
                bg = self.bg,
                fg = self.fg
            )
            mod.pack()
            self.lst_mods.append(mod)
        


    def cmd_goback(self):
        if self.deep>0:
            self.deep -= 1
            self.current_dir = make_path(*self.current_dir.split("\\")[:-1])
            self.refresh()
    
    def cmd_goto(self, path):
        self.current_dir = path
        self.deep += 1
        
        self.refresh()


    def run(self):
        return self.racine.mainloop()



def main_test(
        gimi = r'C:\Users\Thomas\AppData\Roaming\XXMI Launcher\GIMI\Mods',
        zzmi = r'C:\Users\Thomas\AppData\Roaming\XXMI Launcher\ZZMI\Mods',
    ):
    racine = tk.Tk()

    notebook = ttk.Notebook(racine,)

    gimi_tab = Game(gimi, notebook, )
    zzmi_tab = Game(zzmi, notebook, )

    notebook.add(gimi_tab, text='GI')
    notebook.add(zzmi_tab, text='ZZZ')
    
    notebook.pack(expand=True, fill='both')

    



    return racine.mainloop()




if __name__=="__main__": main_test()
