import os
import tkinter as tk
import customtkinter
from PIL import Image, ImageTk
from MsgBoxYesNo import MsgBoxYesNo
from SqlLiteUtils import SQLManager
from InfoDialog import InfoDialog
from NewItemDialog import NewItemDialog
from EditDialog import EditDialog
from datetime import datetime

""" Custom Widget za svaku biljku koji se pojavljuje na Canvasu glavnog prozora i dinamički se multiplicira ovisno o broju biljaka
    Puuuno muke zbog 4 K monitora i windows scaleing-a """
class PlantWidget(tk.Frame):
    def __init__(self, parent, blank=False, owner=None, *args, **kwargs):
        super().__init__(*args, master=parent, **kwargs)

        self.master = parent
        self.is_blank = blank

        self.configure(bg="#1a4744")

        ## Plant data
        self.plant_name = None
        self.plant_dop = None
        self.plant_image = None
        self.plant_tmb_image = None
        self.plant_rnd_tmp = None
        self.plant_rnd_hum = None
        self.plant_rnd_pH = None
        self.plant_rnd_lum = None
        self.plant_owner = owner
        self.plant_ID = None

        # plant senzor data
        self.sensor_temp = None
        self.sensor_hum = None
        self.sensor_ph = None
        self.sensor_lum = None

        # IKONE
        self.plus_image_path = "./resources/" + "Add.png"
        self.edit_image_path = "./resources/" + "pen_grey.png"
        self.info_image_path = "./resources/" + "Info.png"
        self.delete_image_path = "./resources/" + "Delete.png"

        self.image_canvas = None

        # PhotoImage za elemmetnr
        self.img_plus = ImageTk.PhotoImage(
            Image.open(self.plus_image_path).resize((50, 50))
        )
        self.img_edit = ImageTk.PhotoImage(
            Image.open(self.edit_image_path).resize((30, 30))
        )
        self.img_info = ImageTk.PhotoImage(
            Image.open(self.info_image_path).resize((30, 30))
        )
        self.img_delete = ImageTk.PhotoImage(
            Image.open(self.delete_image_path).resize((30, 30))
        )

        self.create_widgets_all()
        # Možda može i bez ovoga
        self.update()
        self.update_idletasks()

    def create_widgets_all(self):
        # gumb dodaj biljku
        self.button_plant_image = customtkinter.CTkButton(
            master=self,
            corner_radius=0,
            width=250,
            height=250,
            image=self.img_plus,
            compound="top",
            text="Dodaj biljku",
            command=self.on_btn_add_plant
        )
        self.button_plant_image.place(anchor=tk.NW, x=5, y=5, width=250, height=250)

        ### label frame u koji idu svi labeli
        self.label_frame = tk.LabelFrame(
            master=self, borderwidth=0, bg=self.cget("bg"), height=250, width=600
        )
        self.label_frame.place(anchor=tk.NW, x=260, y=5)

        # #### LABEL_S_TEXTOM
        self.label_name = customtkinter.CTkLabel(
            master=self.label_frame,
            text="Naziv biljke:",
            anchor=tk.E,
            height=1,
            width=200,
            text_color="white"
        )
        self.label_name.place(anchor=tk.W, x=5, rely=0.1)

        # # dop - date of planting
        self.label_dop = customtkinter.CTkLabel(
            master=self.label_frame,
            text="Datum sadnje biljke:",
            anchor=tk.E,
            height=1,
            width=200,
            text_color="white"
        )
        self.label_dop.place(anchor=tk.W, x=5, rely=0.26)

        self.label_temp = customtkinter.CTkLabel(
            master=self.label_frame,
            text="Senzor temperature [C]:",
            anchor=tk.E,
            height=1,
            width=200,
            text_color="white"
        )
        self.label_temp.place(anchor=tk.W, x=5, rely=0.42)

        self.label_humid = customtkinter.CTkLabel(
            master=self.label_frame,
            text="Senzor vlage zemlje [%]:",
            anchor=tk.E,
            height=1,
            width=200,
            text_color="white"
        )
        self.label_humid.place(anchor=tk.W, x=5, rely=0.58)

        self.label_acid = customtkinter.CTkLabel(
            master=self.label_frame,
            text="Kiselost zemlje [pH]:",
            anchor=tk.E,
            height=1,
            width=200,
            text_color="white"
        )
        self.label_acid.place(anchor=tk.W, x=5, rely=0.74)

        self.label_lux = customtkinter.CTkLabel(
            master=self.label_frame,
            text="Količina svjetlosti [lux]:",
            anchor=tk.E,
            height=1,
            width=200,
            text_color="white"
        )
        self.label_lux.place(anchor=tk.W, x=5, rely=0.9)

        # LABEL PRAZAN
        self.label_name_txt = customtkinter.CTkLabel(
            master=self.label_frame, text="", anchor=tk.W, height=1, width=100, text_color="white"
        )
        self.label_name_txt.place(anchor=tk.W, x=220, rely=0.1)

        # dop - date of planting
        self.label_dop_txt = customtkinter.CTkLabel(
            master=self.label_frame, text="", anchor=tk.W, height=1, width=100, text_color="white"
        )
        self.label_dop_txt.place(anchor=tk.W, x=220, rely=0.26)

        self.label_temp_txt = customtkinter.CTkLabel(
            master=self.label_frame, text="", anchor=tk.W, height=1, width=100, text_color="white"
        )
        self.label_temp_txt.place(anchor=tk.W, x=220, rely=0.42)

        self.label_humid_txt = customtkinter.CTkLabel(
            master=self.label_frame, text="", anchor=tk.W, height=1, width=100, text_color="white"
        )
        self.label_humid_txt.place(anchor=tk.W, x=220, rely=0.58)

        self.label_acid_txt = customtkinter.CTkLabel(
            master=self.label_frame, text="", anchor=tk.W, height=1, width=100, text_color="white"
        )
        self.label_acid_txt.place(anchor=tk.W, x=220, rely=0.74)

        self.label_lux_txt = customtkinter.CTkLabel(
            master=self.label_frame, text="", anchor=tk.W, height=1, width=100, text_color="white"
        )
        self.label_lux_txt.place(anchor=tk.W, x=220, rely=0.9)

        # gumbi na desnoj strani
        ## label frame u koji idu svi gumbi desno
        self.button_frame = tk.LabelFrame(
            master=self, borderwidth=0, bg=self.cget("bg"), height=250, width=200
        )
        self.button_frame.place(anchor=tk.NW, x=865, y=5)

        self.button_info = customtkinter.CTkButton(
            master=self.button_frame,
            text="Info",
            compound="right",
            image=self.img_info,
            width=100,
            height=50,
            command=self.on_btn_info,
        )
        self.button_info.place(anchor=tk.CENTER, relx=0.5, rely=0.15)

        self.button_edit = customtkinter.CTkButton(
            master=self.button_frame,
            text="Uredi",
            compound="right",
            image=self.img_edit,
            width=100,
            height=50,
            command=self.on_btn_edit,
        )
        self.button_edit.place(anchor=tk.CENTER, relx=0.5, rely=0.50)

        self.button_delete = customtkinter.CTkButton(
            master=self.button_frame,
            text="Izbriši",
            compound="right",
            image=self.img_delete,
            width=100,
            height=50,
            command=self.on_btn_delete,
        )
        self.button_delete.place(anchor=tk.CENTER, relx=0.5, rely=0.85)

        if self.is_blank:
            self.button_delete.state = "disabled"
            self.button_edit.state = "disabled"
            self.button_info.state = "disabled"
    # Update širine ovog widgeta kod promjene glavnog prozora i Canvasa
    def update_width(self, window_width):
        # print("W: ", window_width)

        self.configure(width=window_width, height=260)
        self.button_frame.place(x=window_width - 200 - 5)
        self.label_frame.configure(width=window_width - 300 - 313 - 10)
    # 
    def fill_plant_data(
        self,
        plant_name: str,
        plant_dop: str,
        img_name: str,
        thumb_name: str,
        rnd_tmp: float,
        rnd_hum: float,
        rnd_ph: float,
        rnd_lum: float,
        owner: str,
        ID: int,
    ) -> None:
        """Dadavanje podataka o biljci u PlantWidget

        Args:
            plant_name (str): Ime biljke
            plant_dop (str): Datum sadnje
            img_name (str): Ime Slike
            thumb_name (str): Ime male slike
            rnd_tmp (float): random temperatura
            rnd_hum (float): random vlažnost
            rnd_ph (float): random pH tla
            rnd_lum (float): random izvor svjetla
            owner (str): login korisnika
        """
        self.plant_name = plant_name
        self.plant_dop = plant_dop
        self.plant_image = img_name
        self.plant_tmb_image = thumb_name
        self.plant_rnd_tmp = rnd_tmp
        self.plant_rnd_hum = rnd_hum
        self.plant_rnd_pH = rnd_ph
        self.plant_rnd_lum = rnd_lum
        self.plant_owner = owner
        self.plant_ID = ID

        # gumb postaje canvas za sliku biljke
        self.button_plant_image.destroy()

        image_path = "./resources/TMB_IMAGE/" + self.plant_tmb_image
        img = Image.open(image_path)
        img = img.resize((250, 250))
        self.image_canvas = ImageTk.PhotoImage(img)
        self.canvas_image = tk.Canvas(
            self, width=250, height=250, highlightthickness=0, bg=self.cget("bg")
        )
        self.canvas_image.place(anchor=tk.NW, x=5, y=5, width=250, height=250)
        self.canvas_image.create_image(0, 0, image=self.image_canvas, anchor=tk.NW)
        self.label_name_txt.configure(text=self.plant_name)
        datum = self.plant_dop.split("-")
        self.label_dop_txt.configure(text=datum[2] + "/" + datum[1] + "/" + datum[0])
    # podaci senzora 
    def refresh_senzor_data(
        self, temperature: float, humidity: float, ph: float, lux: float
    ) -> None:
        self.sensor_temp = temperature * self.plant_rnd_tmp
        self.sensor_hum = humidity * self.plant_rnd_hum
        self.sensor_ph = ph * self.plant_rnd_pH
        self.sensor_lum = lux * self.plant_rnd_lum
        self.label_acid_txt.configure(text=str(round(self.sensor_ph, 3)))
        self.label_temp_txt.configure(text=str(round(self.sensor_temp, 3)))
        self.label_humid_txt.configure(text=str(round(self.sensor_hum, 3)))
        self.label_lux_txt.configure(text=str(round(self.sensor_lum, 3)))
        
        # # Da vidim što se događa s vrijednostima
        # print("Temp: ", self.sensor_temp, " Temp_: ", temperature," Rand: ", self.plant_rnd_tmp)
        # print("Hum: ", self.sensor_hum, " Hum_: ", humidity," Rand: ", self.plant_rnd_hum)
        # print("pH: ", self.sensor_ph, " Temp_: ", ph," Rand: ", self.plant_rnd_pH)

    def mark_sensor_values(self):
        """Ukoliko je vrijednost senzora van željenih granica označi vrijednost crvenom bojom.
        """        

        if self.plant_ID != None and self.plant_owner != None:
            sql_str = f"""SELECT p.ID AS PLANT_ID,
                             u.ID AS USER_ID,
                             u.NAME  AS USER_NAME,
                             p.MIN_TEMP,
                             p.MAX_TEMP,
                             p.MIN_HUM,
                             p.MAX_HUM,
                             p.MIN_PH,
                             p.MAX_PH,
                             p.RND_TEMP,
                             p.RND_HUM,
                             p.RND_PH
                             FROM PLANTS AS p 
                             INNER JOIN USERS AS u ON p.fk_USER_ID = u.ID WHERE u.LOGIN = \'{self.plant_owner}\' AND p.ID = {self.plant_ID}"""

            result, headers = SQLManager.execute_string(
                "DB.sqlite", sql_str=sql_str, headers=True
            )

            sensors = SQLManager.get_sensors_now(
                "DB.sqlite", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        else:
            return

        # Što ako u bazi nema niti jedna biljka...
        if not result:
            return

        dict_results = {}

        for i in range(len(headers)):
            dict_results[headers[i]] = result[0][i]

        if (dict_results["RND_TEMP"] * sensors[1] > dict_results["MAX_TEMP"]) or (
            dict_results["RND_TEMP"] * sensors[1] < dict_results["MIN_TEMP"]
        ):
            self.label_temp_txt.configure(text_color="red")

        if (dict_results["RND_HUM"] * sensors[2] > dict_results["MAX_HUM"]) or (
            dict_results["RND_HUM"] * sensors[2] < dict_results["MIN_HUM"]
        ):
            self.label_humid_txt.configure(text_color="red")

        if (dict_results["RND_PH"] * sensors[3] > dict_results["MAX_PH"]) or (
            dict_results["RND_PH"] * sensors[3] < dict_results["MIN_PH"]
        ):
            self.label_acid_txt.configure(text_color="red")
    # Što se dešava nakon stiskanja gumbića Delete
    def on_btn_delete(self):
        result = MsgBoxYesNo(
            self, "Brisanje biljke", f"Dali želite obrisati biljku: {self.plant_name}?"
        ).show_self()

        if result:
            SQLManager.delete_item(
                self.plant_owner, self.plant_name, "DB.sqlite"
            )
            # App Main
            self.master.master.master.master.is_rebuilding = True

        try:
            os.remove("./resources/FULL_IMAGE/" + self.plant_image)
        except Exception as e:
            raise e

        try:
            os.remove("./resources/TMB_IMAGE/" + self.plant_tmb_image)
        except Exception as e:
            raise e

    def on_btn_info(self):
        """Pozovi prozor "Info"
        """        
        InfoDialog(master=self, image_name=self.plant_image).show_self()

    def on_btn_add_plant(self):
        """Dodaj novu biljku
        """        
        result = NewItemDialog(master=self).show_self()
        # print(result)
        if result:
            dateTime = result[1].strftime("%Y-%m-%d")
            SQLManager.add_new_item(
                self.plant_owner,
                result[0],
                dateTime,
                result[2],
                result[3],
                database="DB.sqlite",
            )
            self.master.master.master.master.is_rebuilding = True

    def on_btn_edit(self):
        """Uredi postojeću biljku
        """        
        EditDialog(self).show(self.plant_owner, self.plant_name, self.plant_ID)
