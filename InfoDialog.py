import customtkinter
import time
from datetime import datetime
import tkinter
from PIL import Image, ImageTk
from SqlLiteUtils import SQLManager
from DetailsDialog import DetailsDialog

""" Dialog za prikaz podataka o biljci"""
class InfoDialog:
    def __init__(self, image_name: str, master, title: str = "Informacije o biljci:"):

        self.master = master
        self.image_name = image_name

        self.running = False

        # cijela putanja ikone
        self.IMG_FILE_PATH = "./resources/" + "chart.png"

        # Putanja slike biljke
        self.img_canvas_path = "./resources/FULL_IMAGE/" + self.image_name

        # TopLevele setup - geometrija itd..
        self.top = customtkinter.CTkToplevel()
        self.top.geometry("560x900")  # dimenzija
        self.top.title(title)  # naslov

        # min i max size ne dozvoljavaju povećavanje i smanjivanje prozora do određenih dimenzija
        self.top.minsize(560, 870)
        self.top.maxsize(560, 870)
        self.top.lift()  # podiže dialog iznad onog koji je pokrenut
        self.top.focus_force()  # input fokus na ovaj dialog
        self.top.grab_set()  # svi eventi su na ovom widgetu pozadinski je disablean

        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.top.after(10, self.create_widgets)
        self.top.after(20, self.mark_sensor_values)

        self.top.bind("<Escape>", self.on_closing)  # izlazak tipkom escape

        # grid prozora
        self.top.grid_columnconfigure(0, weight=1)
        self.top.grid_rowconfigure(0, weight=1)

        # varijable update datuma i vremena
        self.stringvar_date = tkinter.StringVar()
        self.stringvar_time = tkinter.StringVar()

    def create_widgets(self):

        # glavni frame
        self.frame_widgets = customtkinter.CTkFrame(self.top, corner_radius=10)
        self.frame_widgets.grid(row=0, column=0, padx=5, pady=5, sticky=tkinter.NSEW)

        # grid glavnog framea
        self.frame_widgets.grid_columnconfigure((1, 2, 3), weight=1)
        self.frame_widgets.grid_rowconfigure((2, 3), weight=1)

        self.label_datetime_time = customtkinter.CTkLabel(
            self.frame_widgets,
            textvariable=self.stringvar_time,
            justify=tkinter.CENTER,
        )
        self.label_datetime_date = customtkinter.CTkLabel(
            self.frame_widgets,
            textvariable=self.stringvar_date,
            justify=tkinter.CENTER,
        )

        # ikona
        self.img_details = ImageTk.PhotoImage(
            Image.open(self.IMG_FILE_PATH).resize((12, 12))
        )

        # Slika
        self.canvas = customtkinter.CTkCanvas(
            master=self.frame_widgets,
            bg="#000000",
            width=350,
            height=350,
            highlightthickness=0,
        )
        # tekstbox u kojem će pisati najbolji uvjeti za biljku
        self.text_conditions = customtkinter.CTkTextbox(
            self.frame_widgets, text_font=(("Consolas", -14))
        )
        # Naziv biljke
        self.label_plant_name = customtkinter.CTkLabel(
            master=self.frame_widgets,
            text="Naziv biljke:\n" + str(self.master.plant_name),
        )
        # Senzor 1 Temperatura
        self.label_sensor1 = customtkinter.CTkLabel(
            master=self.frame_widgets,
            width=450,
            text="Senzor temperature [C]: " + str(round(self.master.sensor_temp, 2)),
            anchor=tkinter.W,
        )

        # Naslov
        self.label_sensor_title = customtkinter.CTkLabel(
            master=self.frame_widgets,
            text="Trenutno očitanje senzora:",
            anchor=tkinter.W,
        )

        # Senzor 2 Vlažnost
        self.label_sensor2 = customtkinter.CTkLabel(
            master=self.frame_widgets,
            width=450,
            text="Senzor vlažnosti zemlje [%]: "
            + str(round(self.master.sensor_hum, 2)),
            anchor=tkinter.W,
        )
        # Senzor 3 PH
        self.label_sensor3 = customtkinter.CTkLabel(
            master=self.frame_widgets,
            width=450,
            text="Senzor kiselosti zemlje [pH]: "
            + str(round(self.master.sensor_ph, 2)),
            anchor=tkinter.W,
        )
        # Senzor 4
        self.label_sensor4 = customtkinter.CTkLabel(
            master=self.frame_widgets,
            width=450,
            text="Senzor svjetlosti [lux]: " + str(round(self.master.sensor_lum, 2)),
            anchor=tkinter.W,
        )
        # Gumb za prikaz dijagrama
        self.button_charts = customtkinter.CTkButton(
            master=self.frame_widgets,
            text="Detalji",
            corner_radius=5,
            compound="left",
            image=self.img_details,
            command=self.on_btn_details
        )
        # Gumb za zatvaranje
        self.button_ok = customtkinter.CTkButton(
            master=self.frame_widgets,
            text="OK",
            corner_radius=5,
            command=self.on_OK,
        )
        # PIL PhotoImage biljke za Canvas
        self.image_plant = ImageTk.PhotoImage(
            Image.open(self.img_canvas_path).resize((350, 350))
        )
        self.canvas_image_id = self.canvas.create_image(
            0, 0, image=self.image_plant, anchor=tkinter.NW
        )

        # postavljanje u grid datuma, vremena ITD...
        self.label_datetime_time.grid(
            row=1, column=1, padx=5, pady=5, sticky=tkinter.NSEW
        )
        
        self.label_datetime_date.grid(
            row=1, column=2, padx=5, pady=5, sticky=tkinter.NSEW
        )

        self.canvas.grid(row=2, column=1, padx=5, pady=5, columnspan=2)

        self.text_conditions.grid(
            row=3, column=1, columnspan=3, padx=5, pady=5, sticky=tkinter.EW
        )

        self.label_sensor_title.grid(
            row=4, column=1, columnspan=2, padx=5, pady=5, sticky=tkinter.EW
        )

        self.label_plant_name.grid(row=2, column=3, padx=5, pady=5, sticky=tkinter.NSEW)

        self.label_sensor1.grid(
            row=5, column=1, columnspan=2, padx=5, pady=5, sticky=tkinter.EW
        )

        self.label_sensor2.grid(
            row=6, column=1, columnspan=2, padx=5, pady=5, sticky=tkinter.EW
        )

        self.label_sensor3.grid(
            row=7, column=1, columnspan=2, padx=5, pady=5, sticky=tkinter.EW
        )

        self.label_sensor4.grid(
            row=8, column=1, columnspan=2, padx=5, pady=5, sticky=tkinter.EW
        )

        self.button_ok.grid(row=8, column=3, padx=5, pady=5, sticky=tkinter.W)

        self.button_charts.grid(row=7, column=3, padx=5, pady=5, sticky=tkinter.W)

    #Označi crvenom bojom vrijednosti senzora van zadani "Idealnih" uvjeta
    def mark_sensor_values(self):

        # Dohvaćanje ostalih podataka
        sql_str = f"SELECT * FROM PLANTS INNER JOIN USERS ON PLANTS.fk_USER_ID = USERS.ID WHERE USERS.LOGIN = '{self.master.plant_owner}' AND PLANTS.ID = {self.master.plant_ID}"
        result, headers = SQLManager.execute_string(
            "DB.sqlite", sql_str=sql_str, headers=True
        )

        # postavljanje rezultata u rječnik
        dict_results = {}
        for i in range(len(headers)):
            dict_results[headers[i]] = result[0][i]

        txt = f"""Poštovana/i {dict_results['NAME']},\nNajbolji uvjeti za rast biljke su:\n\nTemperatura od: {round(dict_results['MIN_TEMP'],0)} do: {round(dict_results['MAX_TEMP'], 0)} stupnjeva C,\nVlažnost zemlje od: {round(dict_results['MIN_HUM'])} do: {round(dict_results['MAX_HUM'], 0)} %,\nKiselost zemlje od: {round(dict_results['MIN_PH'], 1)} do: {round(dict_results['MAX_PH'], 1)}.\n\nSve vrijednosti ukoliko izlaze van zadanih okvira\noznačene su crvenom bojom!"""
        # print(txt)
        self.text_conditions.insert(tkinter.INSERT, txt)

        # ukoliko su uvjeti van idealnih granica --- ofarbaj text u crveno
        if (self.master.sensor_temp > dict_results["MAX_TEMP"]) or (
            self.master.sensor_temp < dict_results["MIN_TEMP"]
        ):
            self.label_sensor1.configure(text_color="red")
        if (self.master.sensor_hum > dict_results["MAX_HUM"]) or (
            self.master.sensor_hum < dict_results["MIN_HUM"]
        ):
            self.label_sensor2.configure(text_color="red")
        if (self.master.sensor_ph > dict_results["MAX_PH"]) or (
            self.master.sensor_ph < dict_results["MIN_PH"]
        ):
            self.label_sensor3.configure(text_color="red")
    
    # Otvaranje dialoga s dijagramima
    def on_btn_details(self, event=None):
        details = DetailsDialog(user_name=self.master.plant_owner, plant_id= self.master.plant_ID)
        details.show()

    # Event na kolik OK
    def on_OK(self, event=None):
        # print("Width: ", self.frame_widgets.winfo_width())
        # print("Height: ", self.frame_widgets.winfo_height())
        self.running = False

    # Event na kolik esc ili X na prozoru
    def on_closing(self, event=None):
        self.running = False

    # petlja za update
    def show_self(self):
        self.running = True

        while self.running:
            try:
                self.top.update()
                self.stringvar_date.set(
                    f"Datum: {datetime.today().strftime('%d-%m-%Y')}"
                )
                self.stringvar_time.set(
                    f"Vrijeme: {datetime.now().strftime('%H:%M:%S')}"
                )
                if self.top.grab_status() == None:
                    self.top.grab_set()
                    # print(self.top.grab_status())
            except Exception:
                return 0
            finally:
                time.sleep(0.01)

        time.sleep(0.05)
        self.top.destroy()
        return 0


# Za testiranje van main app-a
# root = tkinter.Tk()


# def run_mb():
#     info = InfoDialog(image_name="Filodendron.jpg", master=root)
#     info.show_self()


# btn = tkinter.Button(master=root, text="Run MB", command=run_mb)
# btn.grid(row=0, column=0, padx=30, pady=30)

# root.mainloop()
