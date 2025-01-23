from ostools import *

import tkinter as tk
from tkinter import ttk

def from_rgb(r,g,b):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return f'#{r:02x}{g:02x}{b:02x}'

def emballage(func, *args, **kwargs):
    """wrapper for tkinter buttons"""
    def f():
        return func(*args, **kwargs)
    return f

def emballage_func(func, fun, i):
    def f():
        return func(fun(i))
    return f

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
        
        self.path = abs_of_path(path)
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

        tk.Button(self, command = self.test_print).grid(row = 0)


        # grid
        self.btn_toggle.grid(row = 0, column=1)
        self.btn_name.grid(row=0, column=2)

    
    def test_print(self):
        print(self.path)

    def clean_name(self) -> str:
        return clean_name_of_path(self.path)
        

    def is_disable(self) -> bool:
        return is_mod_disabled(self.path)
    
    def disable(self):
        try:
            self.path = disable_mod(self.path)
            return True
        except AssertionError:
            print("Mod already off", self.path)
        except FileNotFoundError:
            print('Mod not found', self.path)
        return False

    def able(self):
        try:
            self.path = able_mod(self.path)
            return True
        except AssertionError:
            print("Mod already ON", self.path)
            return False
        except FileNotFoundError:
            print('Mod not found', self.path)
            return False

        

    def cmd_toggle(self):
        """command to toggle mod when appropriate button is clicked"""
        if self.is_disable():
            if self.able(): self.btn_toggle.config(bg = self.theme['bg_on'])
        elif self.disable():
            self.btn_toggle.config(bg = self.theme['bg_off'])

class ScrollableFrame(tk.Frame):

    def __init__(self, root, **theme):
        self.frm = tk.Frame(root, bg = theme["bg"]) # englobe tout le bordel
        canvas = tk.Canvas(self.frm, bg = theme["bg"]) 
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(self.frm, orient=tk.VERTICAL, command=canvas.yview) 
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.configure(yscrollcommand=scrollbar.set)
        tk.Frame.__init__(self, canvas, bg = theme["bg"]) 
        self.bind( "<Configure>", lambda e: canvas.configure( scrollregion=canvas.bbox("all") ) ) 
        canvas.create_window((0, 0), window=self, anchor="nw")

        self.grid = self.frm.grid
        self.pack = self.frm.pack


class ModList(tk.Frame):
    """container for a list of mods, with a scrollbar and a title if specified"""
    def __init__(self, paths, root, cmds = None, title = None, **theme):
        tk.Frame.__init__(self, root, bg = theme['bg'])
        if title is not None:
            tk.Label(self, text = title, bg = theme["bg"], fg = theme["fg"])

        self.frm_scrollable = ScrollableFrame(root=self, **theme)
        for i, path in enumerate(paths):
            cmd = None if cmds is None else (cmds if callable(cmds) else cmds[i])
            Mod(path, root = self.frm_scrollable, cmd = cmd, **theme).grid(row = i, column=1)
        self.frm_scrollable.pack(expand = True)
    
class Tab(tk.Frame):
    """Base class for Tabs, ie what displays the mods / lists of mods"""
    def __init__(self, root, **theme):

        tk.Frame.__init__(self, root, bg = theme['bg'])
    

class TabExplorer(Tab):

    sortmode = {
        'key': lambda x: clean_name_of_name(x[-1]),
    }
    def __init__(self,path, root, **theme):
        Tab.__init__(self, root, **theme)
        self.path = abs_of_path(path)
        self.theme = theme
        self.curdir = self.path
        self.deepness = 0

        self.frm_menu = tk.Frame(
            self,
            bg = theme["bg"],   
        )

        self.btn_back = tk.Button(
            self.frm_menu, 
            bg = theme['bg'], 
            fg = theme['fg'], 
            command = self.cmd_back, 
            text='<-'
        )

        self.btn_refresh = tk.Button(
            self.frm_menu, 
            bg = theme['bg'], 
            fg = theme['fg'], 
            command = self.cmd_refresh, 
            text='refresh'
        )
        

        self.frm_current = tk.Frame(
            self, 
            bg = theme['bg'],
        )

        self.frm_menu.grid(row = 0, column=0)
        self.btn_refresh.grid(row = 0, column = 1)
        self.btn_back.grid(row = 0, column = 0)
        # self.frm_scrollable.grid(row = 2, column = 0)

        self.frm_current.grid(row = 1, column = 0)

        self.cmd_refresh()


    def cmd_refresh(self) :
        lst_mod = list(get_names(self.curdir, deepness = 1))
        lst_mod.sort(**self.sortmode)

        for children in self.frm_current.winfo_children():
            children.destroy()
        self.lst_paths = [make_path(self.curdir, *modname) for modname in lst_mod]
        ModList(
            self.lst_paths, 
            root = self.frm_current, 
            cmds = [emballage_func(self.cmd_goto, self.get_children, i) for i in range(len(self.lst_paths))],
            **self.theme
        ).pack()

    def get_children(self, i):
        return self.lst_paths[i]
    

    def cmd_back(self):
        if self.deepness > 0:
            self.curdir = partent_of_path(self.curdir)
            self.deepness -= 1

        self.cmd_refresh()

    
    def cmd_goto(self, path):
        self.curdir = path
        self.deepness += 1
        self.cmd_refresh()


class TabFullList(Tab):
    ...



class Game(tk.Frame):

    def __init__(
            self,
            folder_path,
            *,
            root,
            **theme,
        ):

        tk.Frame.__init__(self, root, bg=theme['bg'])

        self.path = folder_path

        # WIDGETS
    
        self.frm_menu = tk.Frame(
            self,
            bg = theme["bg"],   
        )

        self.btn_back = tk.Button(
            self.frm_menu, 
            bg = theme['bg'], 
            fg = theme['fg'], 
            command = self.cmd_back, 
            text='<-'
        )

        self.btn_refresh = tk.Button(
            self.frm_menu, 
            bg = theme['bg'], 
            fg = theme['fg'], 
            command = self.cmd_refresh, 
            text='refresh'
        )

        supported_displays = [
            "explorer",
        ]

        

        self.frm_scrollable = ScrollableFrame(
            self,
            **theme
        )

     
        
        # self.lbl_titre = tk.Label(
        #     self, 
        #     bg =theme['bg'] ,
        #     fg =theme["fg"] , 
        #     text=self.current_dir
        # )
        
        # self.lbl_titre.grid(row = 0, column = 1)


        self.frm_menu.grid(row = 0, column=0)
        self.btn_refresh.grid(row = 0, column = 1)
        self.btn_back.grid(row = 0, column = 0)
        self.frm_scrollable.grid(row = 2, column = 0)

    
        self.cmd_refresh()

    
    def cmd_refresh(self):
        return
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
        


    def cmd_back(self):
        return 
        if self.deep>0:
            self.deep -= 1
            self.current_dir = make_path(*self.current_dir.split("\\")[:-1])
            self.refresh()
    
    def cmd_goto(self, path):
        self.current_dir = path
        self.deep += 1
        
        self.refresh()


class App(tk.Tk):

    def __init__(self, games_folders : dict[str, str], **theme):

        tk.Tk.__init__(self, "selectr")

        notebook = ttk.Notebook(self,)
        for game, modfolder in games_folders.items():
            tab = ttk.Notebook(notebook)
            
            explo = TabExplorer(modfolder, root = tab, **theme)
            tab.add(explo, text="explo")
            notebook.add(tab, text = game)


            # tab = Game(modfolder, root = notebook, **theme)
            notebook.add(tab, text = game)
        notebook.pack(expand=True, fill = tk.BOTH)


