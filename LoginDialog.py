import customtkinter
import time
import tkinter as tk


class LoginDialog:
    def __init__(self, parent_window):

        self.parent_window = parent_window
        self.is_running = False

        self.login = None
        self.password = None

        """Top window -> "treba se "disableati" prozor ispod"""

        # TopLevele setup - geometrija itd..
        self.top = customtkinter.CTkToplevel()
        self.top.geometry("500x300")  # dimenzija
        self.top.minsize(
            500, 300
        )  # min i max size ne dozvolkjavaju povećavanje prozora
        self.top.maxsize(500, 300)
        self.top.title("Prijava")  # naslov
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
            text="Unesite podatke za prijavu:",
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
        self.entry_username = customtkinter.CTkEntry(
            master=self.frame_input,
            corner_radius=0,
            width=350,
            height=30,
        )
        self.entry_username.place(x=295, y=50, anchor=tk.N)

        self.label_username = customtkinter.CTkLabel(
            master=self.frame_input, width=100, height=30, text="Korisničko ime:"
        )
        self.label_username.place(x=60, y=50, anchor=tk.N)

        self.entry_password = customtkinter.CTkEntry(
            master=self.frame_input, corner_radius=0, width=350, height=30, show="*"
        )
        self.entry_password.place(x=295, y=100, anchor=tk.N)
        
        self.entry_password.bind(
            "<Return>", self.on_button_OK
        )  # nakon pritiska enter nakon lozinke isto kao da smo stisnuli gumb OK

        self.label_password = customtkinter.CTkLabel(
            master=self.frame_input, width=100, height=30, text="Lozinka:"
        )
        
        self.label_password.place(x=60, y=100, anchor=tk.N)

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
            command=self.on_button_OK,
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

    def on_closing(self):
        self.is_running = False

    def on_button_OK(self, events=None):
        if self.entry_username.get() != "" and self.entry_username.get() != None:
            self.login = self.entry_username.get()
        if self.entry_password.get() != "" and self.entry_password.get() != None:
            self.password = self.entry_password.get()
        self.is_running = False

    def check_loop(self):
        self.is_running = True

        while self.is_running:
            try:
                self.top.update()
            except Exception as e:
                raise e
            finally:
                time.sleep(0.01)

        time.sleep(0.05)
        self.top.destroy()
        return 0

    def show(self):
        self.check_loop()
        return self.login, self.password
