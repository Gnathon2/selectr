"""ossature mod manager

TODO : petit bug bizarre avec deepness > 0"""

from widgets import *


def deprecated(f):
    def func(*args, **kwargs):
        raise DeprecationWarning
        return f(*args, **kwargs)
    return func


@deprecated
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
