import tkinter as tk

"""Canva uz Textbox je jedan od tzv. "Scrollable Widget" pa se zato u ovom 
   slučaju koristi da bi se omogućilo skrolanje nakon dodavanja  više biljaka na zaslon"""


class CanvasContainer(tk.Frame):
    def __init__(self, parent, **kwargs) -> None:
        tk.Frame.__init__(self, master=parent, **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # scrollbar
        self.vertical_scrollbar = tk.Scrollbar(self, orient="vertical")
        self.vertical_scrollbar.grid(row=0, column=1, sticky=tk.NS)

        # canvas - on "nosi" "widgete"
        self.canva_container = tk.Canvas(
            self, bg=parent.cget("bg"), borderwidth=0, highlightthickness=0
        )
        self.canva_container.grid(row=0, column=0, sticky=tk.NSEW)

        # povezianje scrollbar-a i canvasa
        self.canva_container.configure(yscrollcommand=self.vertical_scrollbar.set)
        self.vertical_scrollbar.configure(command=self.canva_container.yview)

        # frame koji će se scrollati
        # svi widgeti idu na ovaj frame.
        self.frame_scrollable = tk.Frame(master=self, bg="#0e2e2c")

        # Apstraktno za objasniti, predstavlja prozor na Canvasu u koji se stavlja Widget
        self.canva_container.create_window(
            (0, 0), window=self.frame_scrollable, anchor=tk.NW
        )
        # povezivanje "Evenata"
        self.canva_container.bind("<Configure>", self.on_configure)
        self.frame_scrollable.bind("<Configure>", self.reset_scroll_region)
        self.canva_container.bind_all("<MouseWheel>", self.on_Mousewheel_Turn)
    #resetiranje regije za "scroll"
    def reset_scroll_region(self, event):
        self.canva_container.configure(scrollregion=self.canva_container.bbox("all"))

    """Event "configrue" """
    def on_configure(self, event):
        self.canva_container.configure(scrollregion=self.canva_container.bbox("all"))

    # Micanje svih Widgeta s Canvasa
    def clear_widgets(self):
        for w in self.frame_scrollable.winfo_children():
            w.destroy()
        self.frame_scrollable.configure(width=1, height=1)
        self.canva_container.configure(scrollregion=self.canva_container.bbox("all"))
    # Event scrolanja miša na Canvasu
    def on_Mousewheel_Turn(self, event):
        self.canva_container.yview_scroll(int(-1 * (event.delta / 120)), "units")
