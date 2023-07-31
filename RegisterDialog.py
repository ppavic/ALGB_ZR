import customtkinter
import time
import tkinter as tk
from MsgBoxExclamation import MsgBoxExclamation

" Dialog za dodavanje novog korisnika odnosno registraciju"
class RegistrateDialog:
    def __init__(self, master=None, title="Registracija novog korisnika"):

        self.master = master

        self.name = None
        self.surname = None
        self.login = None
        self.password_1 = None
        self.password_2 = None

        self.is_running = False

        # TopLevele setup - geometrija itd..
        self.top = customtkinter.CTkToplevel()
        self.top.geometry("500x300")  # dimenzija
        # min i max size ne dozvolkjavaju povećavanje prozora
        self.top.minsize(500, 300)
        self.top.maxsize(500, 300)
        self.top.title(title)  # naslov
        self.top.lift()  # podiže dialog iznad onog koji je pokrenut
        self.top.focus_force()  # input fokus na ovaj dialog
        self.top.grab_set()  # svi eventi su na ovom widgetu pozadinski je disablean

        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.top.after(10, self.create_widgets)
        self.top.bind("<Escape>", self.on_closing)  # izlazak tipkom escape

    def create_widgets(self):
        # Setup frameova

        # Header frame naslov
        self.frame_header = customtkinter.CTkFrame(
            master=self.top, corner_radius=5, width=480, height=50
        )
        self.frame_header.place(x=250, y=5, anchor=tk.N)
        # Widget lable na headeru
        self.label_header = customtkinter.CTkLabel(
            master=self.frame_header,
            corner_radius=5,
            text="Unesite podatke potrebne za registraciju:",
            text_font=("Arial", -16),
            width=300,
            height=20,
        )
        self.label_header.place(x=240, y=15, anchor=tk.N)

        # Header frame Input
        self.frame_input = customtkinter.CTkFrame(
            master=self.top, corner_radius=5, width=480, height=180
        )
        self.frame_input.place(x=250, y=60, anchor=tk.N)

        # Widgeti za input dva labela i dva entrija
        # name entry
        self.entry_name = customtkinter.CTkEntry(
            master=self.frame_input, corner_radius=0, width=350, height=30
        )
        self.entry_name.place(x=295, y=5, anchor=tk.N)
        # name label
        self.label_name = customtkinter.CTkLabel(
            master=self.frame_input, width=100, height=30, text="Ime:"
        )
        self.label_name.place(x=60, y=5, anchor=tk.N)

        # prezime entry
        self.entry_surname = customtkinter.CTkEntry(
            master=self.frame_input,
            corner_radius=0,
            width=350,
            height=30,
        )
        self.entry_surname.place(x=295, y=40, anchor=tk.N)
        # prezime label
        self.label_surname = customtkinter.CTkLabel(
            master=self.frame_input, width=100, height=30, text="Prezime:"
        )
        self.label_surname.place(x=60, y=40, anchor=tk.N)
        # username
        self.entry_username = customtkinter.CTkEntry(
            master=self.frame_input, corner_radius=0, width=350, height=30
        )
        self.entry_username.place(x=295, y=75, anchor=tk.N)

        # prezime label
        self.label_surname = customtkinter.CTkLabel(
            master=self.frame_input, width=100, height=30, text="Korisničko ime:"
        )
        self.label_surname.place(x=60, y=75, anchor=tk.N)
        # Password - prvi put
        self.entry_password_1 = customtkinter.CTkEntry(
            master=self.frame_input, corner_radius=0, width=350, height=30, show="*"
        )
        self.entry_password_1.place(x=295, y=110, anchor=tk.N)

        self.label_password_1 = customtkinter.CTkLabel(
            master=self.frame_input, width=100, height=30, text="Lozinka:"
        )
        self.label_password_1.place(x=60, y=110, anchor=tk.N)

        # Password - drugi put
        self.entry_password_2 = customtkinter.CTkEntry(
            master=self.frame_input, corner_radius=0, width=350, height=30, show="*"
        )
        self.entry_password_2.place(x=295, y=145, anchor=tk.N)

        self.label_password_2 = customtkinter.CTkLabel(
            master=self.frame_input, width=100, height=30, text="Ponovi lozinku:"
        )
        self.label_password_2.place(x=60, y=145, anchor=tk.N)

        # Header frame gumbi
        self.frame_buttons = customtkinter.CTkFrame(
            master=self.top, corner_radius=5, width=480, height=50
        )
        self.frame_buttons.place(x=250, y=245, anchor=tk.N)

        # Widgeti gumbiju na frame_buttons
        self.buton_OK = customtkinter.CTkButton(
            master=self.frame_buttons,
            corner_radius=5,
            width=100,
            height=20,
            text="OK",
            command=self.on_OK,
        )
        self.buton_OK.place(x=60, y=15, anchor=tk.N)

        self.buton_Cancel = customtkinter.CTkButton(
            master=self.frame_buttons,
            corner_radius=5,
            width=100,
            height=20,
            text="Cancel",
            command=self.on_closing,
        )
        self.buton_Cancel.place(x=420, y=15, anchor=tk.N)

    # Event Kod zatvaranja dialoga
    def on_closing(self, event=None):
        self.is_running = False
        self.login = None
        self.password = None

    #Evevnt kod pritiska na gumb OK i validacija unosa prije dodavanja u bazu
    def on_OK(self, event=None):
        if self.entry_username.get() != "":
            self.login = self.entry_username.get()
        if self.entry_name.get() != "":
            self.name = self.entry_name.get()
        if self.entry_surname.get() != "":
            self.surname = self.entry_surname.get()
        if self.entry_password_1.get() != "":
            self.password_1 = self.entry_password_1.get()
        if self.entry_password_2.get() != "":
            self.password_2 = self.entry_password_2.get()

        if self.validate_input() != -1:
            if self.validate_input() == 0:
                # missing name
                MsgBoxExclamation(msg="Nedostaje ime!").show()
                self.set_focus_on_top()

            if self.validate_input() == 1:
                # missing surname
                MsgBoxExclamation(master=self, msg="Nedostaje prezime!").show()
                self.set_focus_on_top()

            if self.validate_input() == 2:
                # missing username
                MsgBoxExclamation(master=self, msg="Nedostaje korisničko ime!").show()
                self.set_focus_on_top()

            if self.validate_input() == 3:
                # missing pass 1
                MsgBoxExclamation(master=self, msg="Nedostaje unos za lozinku!").show()
                self.set_focus_on_top()

            if self.validate_input() == 4:
                # missing pass 2
                MsgBoxExclamation(
                    master=self, msg="Nedostaje unos za ponovljenu lozinku!"
                ).show()
                self.set_focus_on_top()

            if self.validate_input() == 5:
                # passwds not equal
                MsgBoxExclamation(
                    master=self, msg="Lozinka i ponovljena lozinak nisu iste!"
                ).show()
                self.set_focus_on_top()

        if self.validate_input() == -1:
            self.is_running = False

    # ukoliko dialog izgubi fokus
    def set_focus_on_top(self):
        if self.top.grab_status() == None or self.top.grab_status() == "global":
            self.top.grab_set()
            self.top.lift()

    # Metoda koja vraća login, imeprezime i lozinku, ujedno pokreće prozor i njegova glavna petlja
    def get_input(self):
        """
        returns:\n
        login, name, surname, password
        """
        self.is_running = True

        while self.is_running:
            try:
                self.top.update()
            except Exception:
                return 0
            finally:
                time.sleep(0.01)

        time.sleep(0.05)
        self.top.destroy()
        return self.login, self.name, self.surname, self.password_1

    # Validacija unosa
    def validate_input(self):
        if self.entry_name.get() == None:
            return 0
        if self.entry_name.get().strip() == "":
            return 0
        if self.entry_surname.get() == None:
            return 1
        if self.entry_surname.get().strip() == "":
            return 1
        if self.entry_username.get() == None:
            return 2
        if self.entry_username.get().strip() == "":
            return 2
        if self.entry_password_1.get() == None:
            return 3
        if self.entry_password_1.get().strip() == "":
            return 3
        if self.entry_password_2.get() == None:
            return 4
        if self.entry_password_2.get().strip() == "":
            return 4
        if self.entry_password_1.get() != None and self.entry_password_2.get() != None:
            if (
                self.entry_password_1.get().strip()
                != self.entry_password_2.get().strip()
            ):
                return 5
        return -1
