from os import path
import string
import customtkinter
import time
from datetime import datetime
import tkcalendar
from tkinter import StringVar, filedialog
import tkinter
from PIL import Image
from MsgBoxExclamation import MsgBoxExclamation

"""Dialog za unos osnovnih podataka za novu biljku"""


class NewItemDialog:
    def __init__(self, master=None, title="Unesite podatke za novu biljku."):

        self.running = False

        # TopLevele setup - geometrija itd..
        self.top = customtkinter.CTkToplevel()
        self.top.geometry("800x450")  # dimenzija
        self.top.title(title)  # naslov

        # min i max size ne dozvoljavaju povećavanje i smanjivanje prozora do određenih dimenzija
        self.top.minsize(550, 240)
        self.top.maxsize(1000, 600)
        self.top.lift()  # podiže dialog iznad onog koji je pokrenut
        self.top.focus_force()  # input fokus na ovaj dialog
        self.top.grab_set()  # svi eventi su na ovom widgetu pozadinski je disablean

        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.top.after(10, self.create_widgets)
        self.top.bind("<Escape>", self.on_closing)  # izlazak tipkom escape

        # varijable Naziv, datum ...
        self.image_path: string = None
        self.plant_name: string = None
        self.date_of_planting: datetime = None
        self.image_full_path: string = None
        self.image_name: string = None
        self.image_thumb_name: string = None

        self.result = ()

        # stringvar za entry_foto...
        self.entry_foto_strVar = StringVar(self.top)

    def create_widgets(self):
        # grid manager
        self.top.grid_columnconfigure(0, weight=0)
        self.top.grid_columnconfigure(1, weight=1)
        self.top.grid_columnconfigure(2, weight=0)
        self.top.grid_rowconfigure(0, weight=0)
        self.top.grid_rowconfigure(1, weight=1)
        self.top.grid_rowconfigure(2, weight=0)

        # Frameovi i widgeti
        self.buttons_frame = customtkinter.CTkFrame(
            master=self.top, corner_radius=5, height=55
        )

        self.buttons_frame.grid(row=2, column=1, sticky=tkinter.NSEW, padx=5, pady=5)

        self.buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.button_OK = customtkinter.CTkButton(
            self.buttons_frame, text="OK", width=120, height=25, command=self.on_OK
        )

        self.button_OK.grid(row=0, column=3, padx=5, pady=5, sticky=tkinter.E)

        self.button_cancel = customtkinter.CTkButton(
            self.buttons_frame,
            text="Cancel",
            width=120,
            height=25,
            command=self.on_closing,
        )

        self.button_cancel.grid(row=0, column=4, padx=5, pady=5, sticky=tkinter.E)

        self.widgets_frame = customtkinter.CTkFrame(
            master=self.top, corner_radius=5, height=380
        )

        self.widgets_frame.grid(row=1, column=1, sticky=tkinter.NSEW, padx=5, pady=5)

        self.widgets_frame.grid_columnconfigure((0, 4), weight=1)

        self.widgets_frame.grid_rowconfigure((2, 6), weight=1)

        self.label_title = customtkinter.CTkLabel(
            master=self.widgets_frame,
            text="Unesite podatke za novu biljku!\n Sva polja su obavezna.",
            text_font=("Consolas", -14),
        )

        self.label_title.grid(
            row=1, column=1, columnspan=3, padx=5, pady=5, sticky=tkinter.EW
        )

        self.label_naziv_biljke = customtkinter.CTkLabel(
            master=self.widgets_frame,
            text="Naziv biljke: ",
            text_font=("Consolas", -14),
            anchor=tkinter.E,
        )

        self.label_naziv_biljke.grid(row=3, column=1, padx=5, pady=5, sticky=tkinter.EW)

        self.label_foto = customtkinter.CTkLabel(
            master=self.widgets_frame,
            text="Fotografija biljke: ",
            text_font=("Consolas", -14),
            anchor=tkinter.E,
        )

        self.label_foto.grid(row=4, column=1, pady=5, padx=5, sticky=tkinter.EW)

        self.label_date = customtkinter.CTkLabel(
            master=self.widgets_frame,
            text="Datum sadnje biljke: ",
            text_font=("Consolas", -14),
            anchor=tkinter.E,
        )

        self.label_date.grid(row=5, column=1, pady=5, padx=5, sticky=tkinter.EW)

        self.entry_naziv = customtkinter.CTkEntry(self.widgets_frame, width=300)

        self.entry_naziv.grid(row=3, column=2, pady=5, padx=5, sticky=tkinter.EW)

        self.entry_foto = customtkinter.CTkEntry(
            self.widgets_frame,
            width=300,
            textvariable=self.entry_foto_strVar,
            state=tkinter.DISABLED,
        )

        self.entry_foto.grid(row=4, column=2, pady=5, padx=5, sticky=tkinter.EW)

        self.button_file_open = customtkinter.CTkButton(
            self.widgets_frame, text="...", width=30, command=self.on_file_dialog
        )

        self.button_file_open.grid(row=4, column=3, padx=5, pady=5, sticky=tkinter.E)

        self.date_entry = tkcalendar.DateEntry(
            master=self.widgets_frame, date_pattern="dd/mm/y"
        )

        self.date_entry.set_date(datetime.today().strftime("%d/%m/%Y"))
        self.date_entry.grid(row=5, column=2, padx=5, pady=5, sticky=tkinter.EW)

    # OpenFile dialog za odabir slike
    def on_file_dialog(self, event=None):
        file_types = [("PNG", "*.png"), ("JPEG", "*.jpg")]
        self.image_path = filedialog.askopenfile(
            title="Odaberite sliku biljke", filetypes=file_types
        )

        # ako je stisnut cancel na file dialogu...
        if self.image_path != None:
            self.entry_foto_strVar.set(self.image_path.name)
            self.image_full_path = self.image_path.name
            self.image_name = path.basename(self.image_full_path)

    # Event  koji se podiže stiskanjem gumbića OK
    # Tu se obavi validacija unosa i dodavanje u bazu
    def on_OK(self, event=None):

        if self.validate() == 0:
            MsgBoxExclamation(self, msg="Niste unjeli naziv biljke").show()
            self.set_focus_on_top()

        if self.validate() == 1:
            MsgBoxExclamation(self, msg="Niste odabrali sliku biljke").show()
            self.set_focus_on_top()

        if self.validate() == -1:
            self.plant_name = self.entry_naziv.get()
            self.date_of_planting = self.date_entry.get_date()
            self.image_name = self.image_name
            self.image_thumb_name = "tmb_" + self.image_name

            # save image in folders
            imgtmp = Image.open(self.image_full_path)

            if path.exists("./resources/FULL_IMAGE/" + self.image_name):
                self.image_name = "Copy-" + self.image_name
            try:
                imgtmp.save("./resources/FULL_IMAGE/" + self.image_name)
            except Exception as e:
                raise e

            try:
                tmb_tempimage = imgtmp.resize((200, 200))
            except Exception as e:
                raise e

            if path.exists("./resources/TMB_IMAGE/" + self.image_thumb_name):
                self.image_thumb_name = "Copy-" + self.image_thumb_name
            try:
                tmb_tempimage.save("./resources/TMB_IMAGE/" + self.image_thumb_name)
            except Exception as e:
                raise e

            self.result = (
                self.plant_name,
                self.date_of_planting,
                self.image_name,
                self.image_thumb_name,
            )

            self.running = False

    # Validacija unosa
    def validate(self):
        if self.entry_naziv.get() == None:
            return 0
        if self.entry_naziv.get().strip() == "":
            return 0
        if self.entry_foto.get() == None:
            return 1
        if self.entry_foto.get().strip() == "":
            return 1
        return -1

    # ukoliko dialog izgubi fokus
    def set_focus_on_top(self):
        if self.top.grab_status() == None or self.top.grab_status() == "global":
            self.top.grab_set()
            self.top.lift()

    # event kod zatvaranja dialoga
    def on_closing(self, event=None):
        self.running = False

    # glavna petlja dialoga
    def show_self(self):
        self.running = True

        while self.running:
            try:
                self.top.update()
            except Exception:
                return 0
            finally:
                time.sleep(0.01)

        time.sleep(0.05)
        self.top.destroy()
        return self.result


# #Za testiranje
# root = tkinter.Tk()

# def run_mb():
#     nid = NewItemDialog(master=root)
#     nid.show_self()

# btn = tkinter.Button(master=root, text="Run MB", command=run_mb)
# btn.grid(row=0, column=0, padx=30, pady=30)

# root.mainloop()
