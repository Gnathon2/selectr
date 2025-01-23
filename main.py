"""ossature mod manager

TODO : petit bug bizarre avec deepness > 0"""

from widgets import *



    


def main_test(
        games_modfolders : dict,
        **theme
    ):
    racine = tk.Tk()

    notebook = ttk.Notebook(racine,)

    for game, modfolder in games_modfolders.items():
        tab = Game(modfolder, root = notebook, **theme)
        notebook.add(tab, text = game)
    
    notebook.pack(expand=True, fill='both')

    return racine.mainloop()




if __name__=="__main__": 
    App(
        games_folders={ 
            "GIMI": r'C:\Users\Thomas\AppData\Roaming\XXMI Launcher\GIMI\Mods',
            "ZZMI": r'C:\Users\Thomas\AppData\Roaming\XXMI Launcher\ZZMI\Mods',
        },
        bg = "#001111",
        fg = "#FFFFEE",
        bg_on = "#AAFFAA",
        bg_off = "#FFAAAA",
    ).mainloop()
