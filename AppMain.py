import customtkinter
import time
import tkinter as tk
from PIL import Image, ImageTk
from LoginDialog import LoginDialog
from SqlLiteUtils import SQLManager
from MsgBoxExclamation import MsgBoxExclamation
from RegisterDialog import RegistrateDialog
from CanvasContainer import CanvasContainer
from PlantWidget import PlantWidget
from datetime import datetime, timedelta


class AppMainWindow(customtkinter.CTk):
    # customtkinter
    customtkinter.set_appearance_mode("Light")  # Tema
    # prikaz elemanata prozora - zelena boja
    customtkinter.set_default_color_theme("green")

    # inicijalna veličina glavnog prozora
    WIDTH = 1024
    HEIGHT = 768
    WINDOW_TITLE = "Moje biljke. :)"

    def __init__(self):
        # konstruktor klase od koje se nasljeđuje
        super().__init__()

        # setup glavnog prozora
        self.title(AppMainWindow.WINDOW_TITLE)

        # Geometrija glavnog prozora
        self.geometry(f"{AppMainWindow.WIDTH}x{AppMainWindow.HEIGHT}")
        self.minsize(AppMainWindow.WIDTH, AppMainWindow.HEIGHT)
        self.propagate(True)

        # event kada se pritisne gumbić "X"
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # varijable o korisniku
        self.login = None
        self.name = None
        self.surname = None
        self.password = None
        self.database = "DB.sqlite"
        self.itemlist = []

        # date time varijable za sync i slično
        self.start_time = datetime.now()
        self.sync_hours = 3
        self.next_sync_time = self.start_time + timedelta(hours=self.sync_hours)
        
        # automatski sync
        # print("Start time: ", self.start_time)
        # print("Next sync time: ", self.next_sync_time)

        # info o glavnom propzoru
        self.is_loggedIn = False
        self.is_rebuilding = False
        self.is_running = False

        self.sensor_temp = None
        self.sensor_hum = None
        self.sensor_acid = None
        self.sensor_lum = None

        self.label_info_strvar = customtkinter.StringVar(
            value="Dobrodošli, prijavite se za nastavak."
        )

        # direktorij za resurse tipa ikone i sl...
        self.resources_path = "./resources/"

        # dodavanje widgeta na glavni prozor
        self.after(5, self.create_widgets)
        # pokretnje loop-a
        self.after(5, self.check_loop)
        self.bind("<Configure>", self.on_resize)


    def create_widgets(self):
        # Putanje Ikona
        self.img_user_reg_path = self.resources_path + "user_reg.png"
        self.img_user_logout_path = self.resources_path + "user_logout.png"
        self.img_user_login_path = self.resources_path + "user_login.png"
        self.img_exit_path = self.resources_path + "x_square.png"

        # konfiguracija grida glwanog prozora
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)

        # prvi horizontalni frame
        self.frame_top = customtkinter.CTkFrame(master=self, height=50, corner_radius=5)
        self.frame_top.grid(row=0, column=0, padx=5, pady=5, sticky=tk.EW)

        # srednji frame
        self.frame_middle = customtkinter.CTkFrame(
            master=self, corner_radius=0, bg_color="black"
        )
        self.frame_middle.grid(row=1, column=0, padx=5, pady=5, sticky=tk.NSEW)

        self.frame_middle.grid_columnconfigure(0, weight=0)
        self.frame_middle.grid_columnconfigure(1, weight=1)
        self.frame_middle.grid_rowconfigure(1, weight=1)

        # canvas na srednjem frameu kao "Container sa scrollbar-om"
        self.container = CanvasContainer(self.frame_middle)
        self.container.grid(row=1, column=1, padx=5, pady=0, sticky=tk.NSEW)

        # zadnji horizontalni frame
        self.frame_bottom = customtkinter.CTkFrame(
            master=self, height=50, corner_radius=5
        )
        self.frame_bottom.grid(row=2, column=0, padx=5, pady=5, sticky=tk.EW)
        self.frame_bottom.columnconfigure(3, weight=1)

        # button Izlaz (dolje desno)
        self.btn_exit_img = ImageTk.PhotoImage(
            Image.open(self.img_exit_path).resize((16, 16))
        )
        self.btn_exit = customtkinter.CTkButton(
            master=self.frame_bottom,
            corner_radius=5,
            text="Izlaz",
            command=self.on_closing,
            compound="right",
            image=self.btn_exit_img,
        )
        self.btn_exit.grid(row=0, column=4, padx=5, pady=5, sticky=tk.E)

        # Btn prijava
        self.btn_user_login = ImageTk.PhotoImage(
            Image.open(self.img_user_login_path).resize((16, 16))
        )
        self.btn_login = customtkinter.CTkButton(
            master=self.frame_top,
            text="Prijava",
            corner_radius=5,
            command=self.on_button_login,
            image=self.btn_user_login,
            compound="left",
        )
        self.btn_login.grid(row=0, column=0, padx=5, pady=5)

        # Btn Izradi korisnika
        self.btn_user_reg = ImageTk.PhotoImage(
            Image.open(self.img_user_reg_path).resize((16, 16))
        )
        self.btn_register = customtkinter.CTkButton(
            master=self.frame_top,
            text="Novi korisnik",
            corner_radius=5,
            command=self.on_button_register,
            compound="right",
            image=self.btn_user_reg,
        )
        self.btn_register.grid(row=0, column=1, padx=5, pady=5)
        # Btn Odjava Korisnika
        self.btn_user_logut = ImageTk.PhotoImage(
            Image.open(self.img_user_logout_path).resize((16, 16))
        )
        self.btn_logout = customtkinter.CTkButton(
            master=self.frame_top,
            text="Odjava",
            corner_radius=5,
            image=self.btn_user_logut,
            compound="right",
            command=self.on_button_logout,
        )
        self.btn_logout.grid(row=0, column=5, padx=5, pady=5, sticky=tk.E)
        # label info.
        self.label_info = customtkinter.CTkLabel(
            master=self.frame_bottom,
            text_font=("Consolas", -12),
            textvariable=self.label_info_strvar,
            anchor=tk.E,
        )
        self.label_info.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    def on_closing(self, event=None):
        self.is_running = False

    def on_resize(self, event):
        if len(self.itemlist):
            for i in range(len(self.itemlist)):
                self.itemlist[i].update_width(self.container.winfo_width() - 30)

    # loop koji se stalno ponavlja dok aplikacija radi
    def check_loop(self, event=None):
        self.is_running = True

        while self.is_running:
            try:
                self.update()
                self.check_sync()
                if self.is_rebuilding:
                    ## rebuild
                    self.itemlist.clear()
                    self.container.clear_widgets()
                    self.populate_itemlist()
                    self.is_rebuilding = False
            except Exception as e:
                raise e
            finally:
                time.sleep(0.05)

            time.sleep(0.1)
        self.destroy()
        return 0
    
    # Kilk na gumb login
    def on_button_login(self):
        
        # prozor za login
        login_dialog = LoginDialog(parent_window=self)
        
        # rezultati nakon pritiska "Enter ili gumba OK"
        self.login, self.password = login_dialog.show()
        
        # provjera podataka u bazi
        login_check = SQLManager.login_check(self.database, self.login, self.password)

        # provjera dali je login uspio
        if login_check == 0:
            MsgBoxExclamation(
                msg="Login ili password nisu uredu, ili nisu uneseni!"
            ).show()
            self.login = None
            self.password = None
        # ako je uspio
        if login_check:
            self.is_loggedIn = True
            self.name, self.surname = SQLManager.get_user_info(
                self.database, self.login
            )
            self.label_info_strvar.set(f"Dobrodošli {self.name} {self.surname}")
            # napuni listu Itemima iz DB-a
            self.populate_itemlist()

    def populate_itemlist(self):
        if self.login and not len(self.itemlist):
            self.get_sensors_from_DB()
            # traži Iteme iz baze
            result = SQLManager.get_user_items(self.login, "DB.sqlite")
            r = 0
            if result:
                for n in result:
                    plant = PlantWidget(
                        self.container.frame_scrollable, owner=self.login
                    )
                    plant.grid(row=r, column=0, padx=5, pady=5)
                    plant.fill_plant_data(
                        n[0], n[1], n[2], n[3], n[4], n[5], n[6], n[7], self.login, n[8]
                    )
                    plant.refresh_senzor_data(
                        self.sensor_temp,
                        self.sensor_hum,
                        self.sensor_acid,
                        self.sensor_lum,
                    )
                    plant.mark_sensor_values()
                    # dodaj u listu
                    self.itemlist.append(plant)
                    r += 1

                blank = PlantWidget(
                    self.container.frame_scrollable, blank=True, owner=self.login
                )
                blank.grid(row=r, column=0, padx=5, pady=5)
                self.itemlist.append(blank)

            if not result:
                blank = PlantWidget(
                    self.container.frame_scrollable, blank=True, owner=self.login
                )
                blank.grid(row=1, column=0, padx=5, pady=5)
                self.itemlist.append(blank)
    # odlogiravanje na gumb "Odjava"
    def on_button_logout(self):
        self.reset_login_data()
        self.itemlist.clear()
        self.container.clear_widgets()
        pass
    # Registriranje na gumb Registracija
    def on_button_register(self):
        (
            new_usr_login,
            new_usr_name,
            new_usr_surname,
            new_usr_pass,
        ) = RegistrateDialog().get_input()

        result = 0

        if new_usr_login != None and new_usr_surname != None and new_usr_pass != None:
            result = SQLManager.add_new_user(
                self.database,
                new_usr_name,
                new_usr_surname,
                new_usr_login,
                new_usr_pass,
            )
        else:
            MsgBoxExclamation(msg=f"Nije dodan novi korisnik.").show()
            return

        if result == 1:
            MsgBoxExclamation(
                msg=f"Novi korisnik je uspješno dodan. Login: {new_usr_login}"
            ).show()

        if result == 0:
            MsgBoxExclamation(
                msg=f"Novog korisnika nije moguće dodati, probajte drugo korisničko ime!"
            ).show()
    # resetiranje podataka nakon odjave ili po potrebi
    def reset_login_data(self):
        self.login = None
        self.name = None
        self.surname = None
        self.password = None
        self.is_loggedIn = False
        self.label_info_strvar.set("Dobrodošli, prijavite se za nastavak.")

    def check_sync(self):
        """Ako je prošlo vrijeme za sync ponovno pročitaj senzore i iizgradi sučelje
        """        
        if self.next_sync_time < datetime.now():
            self.is_rebuilding = True
            # print("Synchronizing sensors...")
            self.next_sync_time = datetime.now() + timedelta(hours=self.sync_hours)

    def get_sensors_from_DB(self):
        """Dohvati senzore iz DB-a
        """        
        result = SQLManager.get_sensors_now(
            "DB.sqlite",
            date_time_now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        self.sensor_temp = result[1]
        self.sensor_hum = result[2]
        self.sensor_acid = result[3]
        self.sensor_lum = result[4]