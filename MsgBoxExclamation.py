from PIL import Image, ImageTk
import customtkinter
import time
import tkinter

""" Moj custom Message box. najbolje se vidi na "dark windows temi"""
class MsgBoxExclamation:
    def __init__(self, title="Obavijest", msg=""):

        # Ikona
        self.img_path = "./resources/" + "Alert_ex.png"

        self.image = None
        self.msg = msg
        # Kontrolna varijabla stanja klase, dali se "vrti# ili ne
        self.running = False

        # TopLevele setup - geometrija itd..
        self.top = customtkinter.CTkToplevel()
        self.top.geometry("400x115")  # dimenzija
        self.top.minsize(
            400, 115
        )  # min i max size ne dozvolkjavaju povećavanje prozora
        self.top.maxsize(400, 115)
        self.top.title(title)  # naslov
        self.top.lift()  # podiže dialog iznad onog koji je pokrenut
        self.top.focus_force()  # input fokus na ovaj dialog
        self.top.grab_set()  # svi eventi su na ovom widgetu pozadinski je disablean

        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.top.after(10, self.create_widgets)
        self.top.bind("<Escape>", self.on_closing)  # izlazak tipkom escape

    def create_widgets(self):

        # slika Ikone
        self.image = ImageTk.PhotoImage(Image.open(self.img_path).resize((50, 50)))

        # Header frame naslov
        self.frame_header = customtkinter.CTkFrame(
            master=self.top, corner_radius=5, width=335, height=50
        )
        self.frame_header.place(x=60, y=5, anchor=tkinter.NW)

        # Widget lable na headeru
        self.label_header = customtkinter.CTkLabel(
            master=self.frame_header,
            corner_radius=5,
            text=self.msg,
            text_font=("Consolas", -14),
            width=325,
            height=40,
            justify=tkinter.LEFT,
            wraplength=315,
        )
        self.label_header.place(x=5, y=5, anchor=tkinter.NW)

        self.frame_buttons = customtkinter.CTkFrame(
            master=self.top, corner_radius=5, width=390, height=50
        )
        self.frame_buttons.place(x=5, y=60, anchor=tkinter.NW)

        # Widget button
        self.buton_OK = customtkinter.CTkButton(
            master=self.frame_buttons,
            corner_radius=5,
            width=100,
            height=20,
            text="OK",
            command=self.on_OK,
        )
        self.buton_OK.place(x=195, y=15, anchor=tkinter.N)

        self.img_label = customtkinter.CTkLabel(
            master=self.top, image=self.image, width=50, height=50
        )
        self.img_label.place(x=5, y=5, anchor=tkinter.NW)

        self.top.bind("<Escape>", self.on_OK)

    def on_closing(self, event=None):
        self.running = False

    def on_OK(self, event=None):
        self.running = False

    # Pozivanje prozora i njegova glavna petlja
    def show(self):
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
        return 0
