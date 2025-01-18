from ostools import *

import tkinter as tk
from tkinter import ttk

def from_rgb(r,g,b):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return f'#{r:02x}{g:02x}{b:02x}'

class Mod(tk.Frame):
    """One mod is displayed including:
    - preview if preview.png in the folder
    - name which is clickable
    - rename button
    - toggle button (whick also displays the current status)
    - open folder button

    path: absolute path of the mod
    cmd: what it does to click on the name """
    def __init__(self, path, cmd,*, root, **theme):
        
        self.path = os.path.abspath(path)
        self.theme = theme

        tk.Frame.__init__(self, root, bg = theme["bg"])

        self.btn_toggle = tk.Button(
            self, 
            bg = theme['bg_off'] if self.is_disable() else theme['bg_on'], 
            fg = theme["fg"], 
            command = self.cmd_toggle, 
            text = '   ',
        )
        
        self.btn_name = tk.Button(
            self, 
            bg = theme["bg"],
            fg = theme["fg"], 
            text=self.clean_name(),
            command = cmd,
        )



        # grid
        self.btn_toggle.grid(row = 0, column=1)
        self.btn_name.grid(row=0, column=2)

    


    def clean_name(self):
        return clean_name_of_path(self.path)
        

    # def is_disable(self) -> bool:
    #     return is_mod_disabled(self.path)
    
    def disable(self):
        new_p = disable_mod(self.path)
        if new_p is None:
            print("mod not found", self.path)
        else:
            self.path = new_p
        return
        try:
            old_p = self.path
            new_p = clean_path(self.path)
            os.rename(old_p, new_p)
            self.path = new_p
        except FileNotFoundError:
            print("this mod wasn't found", self.path)

    def able(self):
        try:
            self.path = able_mod(self.path)
        except AssertionError:
            print("Mod already ON", self.path)
        except FileNotFoundError:
            print('Mod not found', self.path)
        return

        if new_p is None:
            print("mod not found", self.path)
        else:
            self.path = new_p
        return 
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

    def clean_name(self):
        return clean_name_of_path(self.path)



class Game(tk.Frame):

    def __init__(
            self,
            mod_folder,
            *args, 
            bg = "#111111",
            fg = "#FFFFFF",
            deepness = 0,
            **kwargs,
            
        ):

        tk.Frame.__init__(self, *args, bg=bg, **kwargs)

        self.bg = bg
        self.fg = fg
    
        self.deepness = deepness
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