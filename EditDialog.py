import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
import time
from SqlLiteUtils import SQLManager
from datetime import datetime
from PIL import Image, ImageTk
from os import path, remove


class EditDialog(tk.Frame):
    def __init__(self, master) -> None:
        super().__init__(master=master, bg="gray")

        self.is_running = True

        self.top = ctk.CTkToplevel()
        self.top.geometry("1024x600")  # dimenzija
        # min i max size ne dozvoljavaju povećavanje prozora
        self.top.minsize(1024, 600)
        self.top.maxsize(1024, 600)
        self.top.title("Uredi podatke o biljci")  # naslov
        self.top.lift()  # podiže dialog iznad onog koji je pokrenut
        self.top.focus_force()  # input fokus na ovaj dialog
        self.top.grab_set()  # svi eventi su na ovom widgetu pozadinski je disablean

        self.top.protocol("WM_DELETE_WINDOW", self.on_cancel)

        self.top.grid_columnconfigure((1, 2, 3, 4), weight=1)
        self.top.grid_rowconfigure(
            (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17), weight=1
        )
        self.top.grid_rowconfigure((11), weight=2)

        # StrVar za labele kraj slidera
        self.strvar_max_temp = tk.StringVar(
            master=self.top, value="Maksimalna temperatura [C]:"
        )
        self.strvar_min_temp = tk.StringVar(
            master=self.top, value="Minimalna temperatura [C]:"
        )
        self.strvar_max_hum = tk.StringVar(
            master=self.top, value="Maksimalna vlažnost [%]:"
        )
        self.strvar_min_hum = tk.StringVar(
            master=self.top, value="Minimalna vlažnost [%]:"
        )
        self.strvar_max_ph = tk.StringVar(master=self.top, value="Maksimalni pH:")
        self.strvar_min_ph = tk.StringVar(master=self.top, value="Minimalni pH:")
        self.check_box_new_name = tk.StringVar(master=self.top, value="off")
        self.strvar_image_path = tk.StringVar(
            master=self.top, value="./Old image path/"
        )
        self.strvar_old_plant_name = tk.StringVar(master=self, value="Naziv: ")

        self.strvar_sensor_temp = tk.StringVar(master=self, value="Temperatura [C]: ")
        self.strvar_sensor_hum = tk.StringVar(
            master=self, value="Vlažnost zemlje [%]: "
        )
        self.strvar_sensor_ph = tk.StringVar(
            master=self, value="Kiselost zemlje [pH]: "
        )
        self.strvar_sensor_lux = tk.StringVar(master=self, value="Osvjetljenje [lux] ")

        self.strvar_entry_plant_name = tk.StringVar(master=self, value="")

        self.plant_image = None
        self.plant_image_path = None
        self.plant_new_image_filename = None
        self.plant_owner = None
        self.plant_name = None
        self.plant_new_image_path = None
        self.plant_image_is_changed = False
        self.plant_ID = None

        self.plant_old_tmb = None
        self.plant_old_image = None

        self.is_updated = False

        # init widgets
        self.create_widgets()
        self.set_def_values_from_scale()
        self.update()
        self.update_idletasks()
        self.after(20, self.create_canvas)

    def create_widgets(self):

        # Canvas za sliku
        self.canvas_image = tk.Canvas(
            master=self.top,
            bg=self.master.cget("bg"),
            borderwidth=0,
            highlightthickness=0,
            width=400,
            height=400,
        )
        self.label_image_path = ctk.CTkLabel(
            master=self.top,
            anchor=tk.W,
            textvariable=self.strvar_image_path,
            height=3,
            width=300,
            wraplength=600,
            justify=tk.LEFT,
        )
        self.label_old_plant_name = ctk.CTkLabel(
            master=self.top, anchor=tk.W, textvariable=self.strvar_old_plant_name
        )
        self.lable_sensor_title = ctk.CTkLabel(
            master=self.top, anchor=tk.W, text="Očitanje senzora:"
        )
        self.label_sensor_temp = ctk.CTkLabel(
            master=self.top, anchor=tk.W, text="Temperatura [C]:"
        )
        self.label_sensor_hum = ctk.CTkLabel(
            master=self.top, anchor=tk.W, text="Vlažnost zemlje: [%]:"
        )
        self.label_sensor_ph = ctk.CTkLabel(
            master=self.top, anchor=tk.W, text="Kiselost zemlje: [pH]:"
        )
        self.label_sensor_lux = ctk.CTkLabel(
            master=self.top, anchor=tk.W, text="Osvjetljenje: [lux]:"
        )

        self.label_conditions = ctk.CTkLabel(
            master=self.top, anchor=tk.CENTER, text="Najbolji uvjeti za biljku:"
        )

        self.label_MinMax_temp = ctk.CTkLabel(
            master=self.top, anchor=tk.CENTER, text="Temperatura: [C]:"
        )

        self.label_min_temp = ctk.CTkLabel(
            master=self.top, anchor=tk.E, width=25, textvariable=self.strvar_min_temp
        )
        self.scale_min_temp = ctk.CTkSlider(
            master=self.top,
            from_=-35,
            to=45,
            orient="horizontal",
            height=22,
            command=self.on_scale_temp_change,
            number_of_steps=1000,
        )

        self.label_max_temp = ctk.CTkLabel(
            master=self.top, anchor=tk.E, width=25, textvariable=self.strvar_max_temp
        )
        self.scale_max_temp = ctk.CTkSlider(
            master=self.top,
            from_=-35,
            to=45,
            orient="horizontal",
            height=22,
            command=self.on_scale_temp_change,
            number_of_steps=1000,
        )

        self.label_MinMax_hum = ctk.CTkLabel(
            master=self.top, anchor=tk.CENTER, text="Vlažnost: [%]:"
        )

        self.label_min_hum = ctk.CTkLabel(
            master=self.top, anchor=tk.E, width=25, textvariable=self.strvar_min_hum
        )
        self.scale_min_hum = ctk.CTkSlider(
            master=self.top,
            from_=0,
            to=100,
            orient="horizontal",
            height=25,
            command=self.on_scale_hum_change,
            number_of_steps=1000,
        )

        self.label_max_hum = ctk.CTkLabel(
            master=self.top, anchor=tk.E, width=25, textvariable=self.strvar_max_hum
        )
        self.scale_max_hum = ctk.CTkSlider(
            master=self.top,
            from_=0,
            to=100,
            orient="horizontal",
            height=25,
            command=self.on_scale_hum_change,
            number_of_steps=1000,
        )

        self.label_MinMax_pH = ctk.CTkLabel(
            master=self.top, anchor=tk.CENTER, text="Kiselost zemlje:"
        )

        self.label_min_ph = ctk.CTkLabel(
            master=self.top, anchor=tk.E, width=25, textvariable=self.strvar_min_ph
        )
        self.scale_min_ph = ctk.CTkSlider(
            master=self.top,
            from_=3,
            to=8,
            orient="horizontal",
            height=25,
            command=self.on_scale_ph_change,
            number_of_steps=1000,
        )

        self.label_max_ph = ctk.CTkLabel(
            master=self.top, anchor=tk.E, width=25, textvariable=self.strvar_max_ph
        )
        self.scale_max_ph = ctk.CTkSlider(
            master=self.top,
            from_=3,
            to=8,
            orient="horizontal",
            height=25,
            command=self.on_scale_ph_change,
            number_of_steps=1000,
        )

        self.btn_change_image = ctk.CTkButton(
            master=self.top,
            text="Promijeni sliku...",
            command=self.on_button_change_image,
        )

        self.chbox_new_name = ctk.CTkCheckBox(
            master=self.top,
            text="Promijeni ime?",
            variable=self.check_box_new_name,
            onvalue="on",
            offvalue="off",
            command=self.chk_box_state,
        )
        self.entry_new_plant_name = ctk.CTkEntry(
            master=self.top, state="disabled", textvariable=self.strvar_entry_plant_name
        )

        self.label_sensors_current = ctk.CTkLabel(
            master=self.top, anchor=tk.W, text="Trenutno očitanje senzora:"
        )

        self.label_temp = ctk.CTkLabel(
            master=self.top, anchor=tk.W, textvariable=self.strvar_sensor_temp
        )
        self.label_hum = ctk.CTkLabel(
            master=self.top, anchor=tk.W, textvariable=self.strvar_sensor_hum
        )
        self.label_ph = ctk.CTkLabel(
            master=self.top, anchor=tk.W, textvariable=self.strvar_sensor_ph
        )
        self.label_lux = ctk.CTkLabel(
            master=self.top, anchor=tk.W, textvariable=self.strvar_sensor_lux
        )

        self.button_apply = ctk.CTkButton(
            master=self.top, text="Apply", command=self.on_apply
        )
        self.button_cancel = ctk.CTkButton(
            master=self.top, text="Cancel", command=self.on_cancel
        )

        # postavljanje na frame - grid manager
        self.canvas_image.grid(row=1, column=1, rowspan=10)
        self.label_image_path.grid(row=11, column=1, sticky=tk.NSEW)
        self.label_old_plant_name.grid(row=12, column=1, sticky=tk.NSEW)
        self.lable_sensor_title.grid(row=13, column=1, sticky=tk.NSEW)
        self.label_sensor_temp.grid(row=14, column=1, sticky=tk.NSEW)
        self.label_sensor_hum.grid(row=15, column=1, sticky=tk.NSEW)
        self.label_sensor_ph.grid(row=16, column=1, sticky=tk.NSEW)
        self.label_sensor_lux.grid(row=17, column=1, sticky=tk.NSEW)

        self.label_conditions.grid(row=1, column=2, columnspan=3, sticky=tk.NSEW)
        self.label_MinMax_temp.grid(row=2, column=2, columnspan=3, sticky=tk.NSEW)

        self.label_min_temp.grid(row=3, column=2, sticky=tk.NSEW)
        self.scale_min_temp.grid(row=3, column=3, sticky=tk.EW, columnspan=2)
        self.label_max_temp.grid(row=4, column=2, sticky=tk.NSEW)
        self.scale_max_temp.grid(row=4, column=3, sticky=tk.EW, columnspan=2)

        self.label_MinMax_hum.grid(row=5, column=2, columnspan=3, sticky=tk.NSEW)

        self.label_min_hum.grid(row=6, column=2, sticky=tk.NSEW)
        self.scale_min_hum.grid(row=6, column=3, sticky=tk.EW, columnspan=2)

        self.label_max_hum.grid(row=7, column=2, sticky=tk.NSEW)
        self.scale_max_hum.grid(row=7, column=3, sticky=tk.EW, columnspan=2)

        self.label_MinMax_pH.grid(row=8, column=2, columnspan=3, sticky=tk.NSEW)

        self.label_min_ph.grid(row=9, column=2, sticky=tk.NSEW)
        self.scale_min_ph.grid(row=9, column=3, sticky=tk.EW, columnspan=2)

        self.label_max_ph.grid(row=10, column=2, sticky=tk.NSEW)
        self.scale_max_ph.grid(row=10, column=3, sticky=tk.EW, columnspan=2)

        self.btn_change_image.grid(row=11, column=2, sticky=tk.NSEW)

        self.chbox_new_name.grid(row=12, column=2, sticky=tk.NSEW)
        self.entry_new_plant_name.grid(row=12, column=3, sticky=tk.NSEW, columnspan=2)

        self.label_sensors_current.grid(row=13, column=1, sticky=tk.NSEW)

        self.label_temp.grid(row=14, column=1, sticky=tk.NSEW)
        self.label_hum.grid(row=15, column=1, sticky=tk.NSEW)
        self.label_ph.grid(row=16, column=1, sticky=tk.NSEW)
        self.label_lux.grid(row=17, column=1, sticky=tk.NSEW)

        self.button_apply.grid(row=17, column=3, sticky=tk.NSEW)
        self.button_cancel.grid(row=17, column=4, sticky=tk.NSEW)

        self.pad_widgets()
        self.set_def_slider_value()

        # Da se ne piše padding za svaki widget :)

    def pad_widgets(self):
        for widget in self.top.winfo_children():
            # print(widget.winfo_name())
            widget.grid_configure(padx=5, pady=5)

    # postavljanje "default" vrijhednosti za svaki "slider"
    def set_def_slider_value(self):
        self.scale_max_temp.set(35)
        self.scale_min_temp.set(-10)
        self.scale_max_hum.set(85)
        self.scale_min_hum.set(10)
        self.scale_max_ph.set(7)
        self.scale_min_ph.set(4)

    def set_def_values_from_scale(self):
        self.strvar_min_temp.set(
            "Minimalna temperatura [C]: " + str(self.scale_min_temp.get())
        )
        self.strvar_max_temp.set(
            "Maksimalna temperatura [C]: " + str(self.scale_max_temp.get())
        )
        self.strvar_min_hum.set(
            "Minimalna vlažnost [%]: " + str(self.scale_min_hum.get())
        )
        self.strvar_max_hum.set(
            "Maksimalna vlažnost [%]: " + str(self.scale_max_hum.get())
        )
        self.strvar_min_ph.set("Minimalni pH: " + str(self.scale_min_ph.get()))
        self.strvar_max_ph.set("Maksimalni pH: " + str(self.scale_max_ph.get()))
    
    # Za svaki slider ,test za njegov min i Max da  se nebi dogodilo da min veći od max
    # U svakom slučaju zgodnije nego tražiti direktan upis korisnika u Entry pa zatim raditi sve provjere.
    def on_scale_temp_change(self, event):
        if self.scale_min_temp.get() > self.scale_max_temp.get():
            self.scale_max_temp.set(self.scale_min_temp.get())
            self.strvar_min_temp.set(
                "Minimalna temperatura [C]: " + str(round(self.scale_min_temp.get(), 1))
            )
            self.strvar_max_temp.set(
                "Maksimalna temperatura [C]: "
                + str(round(self.scale_max_temp.get(), 1))
            )
        else:
            self.strvar_min_temp.set(
                "Minimalna temperatura [C]: " + str(round(self.scale_min_temp.get(), 1))
            )
            self.strvar_max_temp.set(
                "Maksimalna temperatura [C]: "
                + str(round(self.scale_max_temp.get(), 1))
            )

    def on_scale_hum_change(self, event):
        if self.scale_min_hum.get() > self.scale_max_hum.get():
            self.scale_max_hum.set(self.scale_min_hum.get())
            self.strvar_min_hum.set(
                "Minimalna vlažnost [%]: " + str(round(self.scale_min_hum.get(), 1))
            )
            self.strvar_max_hum.set(
                "Maksimalna vlažnost [%]: " + str(round(self.scale_max_hum.get(), 1))
            )
        else:
            self.strvar_min_hum.set(
                "Minimalna vlažnost [%]: " + str(round(self.scale_min_hum.get(), 1))
            )
            self.strvar_max_hum.set(
                "Maksimalna vlažnost [%]: " + str(round(self.scale_max_hum.get(), 1))
            )

    def on_scale_ph_change(self, event):
        if self.scale_min_ph.get() > self.scale_max_ph.get():
            self.scale_max_ph.set(self.scale_min_ph.get())
            self.strvar_min_ph.set(
                "Minimalni pH: " + str(round(self.scale_min_ph.get(), 1))
            )
            self.strvar_max_ph.set(
                "Maksimalni pH: " + str(round(self.scale_max_ph.get(), 1))
            )
        else:
            self.strvar_min_ph.set(
                "Minimalni pH: " + str(round(self.scale_min_ph.get(), 1))
            )
            self.strvar_max_ph.set(
                "Maksimalni pH: " + str(round(self.scale_max_ph.get(), 1))
            )

    # Checkbox za promjenu naziva
    def chk_box_state(self):
        if self.chbox_new_name.get() == "on":
            self.entry_new_plant_name.configure(state="normal")
            self.strvar_entry_plant_name.set(
                self.strvar_old_plant_name.get().replace("Naziv: ", "").strip()
            )
        if self.chbox_new_name.get() == "off":
            self.entry_new_plant_name.configure(state="disabled")
            self.strvar_entry_plant_name.set("")

    # Even Nakon klika gumbića apply - izmjena podataka u DB , zatvaranje prozora i rebild glavnog
    def on_apply(self):
        min_temp = self.scale_min_temp.get()
        max_temp = self.scale_max_temp.get()
        min_hum = self.scale_min_hum.get()
        max_hum = self.scale_max_hum.get()
        min_ph = self.scale_min_ph.get()
        max_ph = self.scale_max_ph.get()
        plant_ID = self.plant_ID

        if self.plant_image_is_changed:
            plant_image = self.plant_new_image_filename
            plant_thmb_image = "tmb_" + self.plant_new_image_filename

        if (
            self.check_box_new_name.get() == "on"
            and self.entry_new_plant_name.get() != None
            and self.entry_new_plant_name.get().strip() != ""
        ):
            plant_new_name = self.entry_new_plant_name.get()

            if self.plant_image_is_changed:
                sql_string = f"""UPDATE PLANTS
                                SET
                                PLANT_NAME = \'{plant_new_name}\',
                                MIN_TEMP = {min_temp},
                                MAX_TEMP = {max_temp},
                                MIN_HUM = {min_hum},
                                MAX_HUM = {max_hum},
                                MIN_PH = {min_ph},
                                MAX_PH = {max_ph},
                                IMAGE_NAME = \'{plant_image}\',
                                THUMB_NAME = \'{plant_thmb_image}\'
                                WHERE ID = {plant_ID}"""
            else:
                sql_string = f"""UPDATE PLANTS
                                SET
                                PLANT_NAME = \'{plant_new_name}\',
                                MIN_TEMP = {min_temp},
                                MAX_TEMP = {max_temp},
                                MIN_HUM = {min_hum},
                                MAX_HUM = {max_hum},
                                MIN_PH = {min_ph},
                                MAX_PH = {max_ph}
                                WHERE ID = {plant_ID}"""

        else:
            if self.plant_image_is_changed:
                sql_string = f"""UPDATE PLANTS
                                SET
                                MIN_TEMP = {min_temp},
                                MAX_TEMP = {max_temp},
                                MIN_HUM = {min_hum},
                                MAX_HUM = {max_hum},
                                MIN_PH = {min_ph},
                                MAX_PH = {max_ph},
                                IMAGE_NAME = \'{plant_image}\',
                                THUMB_NAME = \'{plant_thmb_image}\'
                                WHERE ID = {plant_ID}"""
            else:
                sql_string = f"""UPDATE PLANTS
                                SET
                                MIN_TEMP = {min_temp},
                                MAX_TEMP = {max_temp},
                                MIN_HUM = {min_hum},
                                MAX_HUM = {max_hum},
                                MIN_PH = {min_ph},
                                MAX_PH = {max_ph}
                                WHERE ID = {plant_ID}"""

        SQLManager.execute_edit(database="DB.sqlite", sql_str=sql_string)

        if self.plant_image_is_changed:
            # save image in both folders
            imgtmp = Image.open(self.plant_new_image_path.name)

            if path.exists("./resources/FULL_IMAGE/" + self.plant_new_image_filename):
                self.plant_new_image_filename = "Copy-" + self.plant_new_image_filename
            try:
                imgtmp.save("./resources/FULL_IMAGE/" + self.plant_new_image_filename)
            except Exception as e:
                raise e

            try:
                tmb_tempimage = imgtmp.resize((200, 200))
            except Exception as e:
                raise e

            if path.exists("./resources/TMB_IMAGE/" + plant_thmb_image):
                plant_thmb_image = "Copy-" + plant_thmb_image
            try:
                tmb_tempimage.save("./resources/TMB_IMAGE/" + plant_thmb_image)
            except Exception as e:
                raise e

            # Brisanje stare slike ako je došlo do zamjene slike
            try:
                remove("./resources/FULL_IMAGE/" + self.plant_old_image)
            except Exception as e:
                raise e

            try:
                remove("./resources/TMB_IMAGE/" + self.plant_old_tmb)
            except Exception as e:
                raise e

        # izgleda čudno, moglo je i drugaćije ali radi
        self.master.master.master.master.master.is_rebuilding = True
        self.is_running = False
    
    # Gašenje prozora
    def on_cancel(self):
        self.is_running = False

    # Open File dialog za sliku
    def on_button_change_image(self):

        file_types = [("JPEG", "*.jpg"), ("PNG", "*.png")]
        self.plant_new_image_path = filedialog.askopenfile(
            title="Odaberite sliku biljke", filetypes=file_types
        )

        self.change_image(self.plant_new_image_path.name)

        # ako je stisnut cancel na file dialogu...
        if self.plant_new_image_path == None:
            return

        if self.plant_new_image_path != None:
            self.strvar_image_path.set(self.plant_new_image_path.name)
            self.plant_new_image_filename = path.basename(
                self.plant_new_image_path.name
            )
            # Ako smo zamjenili sliku, stanje "kontrolne" varijable se promjenilo
            self.plant_image_is_changed = True

    # Na početku otvaranja prozora, punjenje forme vrijednostima iz baze
    def fill_form(self):

        # podaci iz baze:f
        sql_str = f"""SELECT p.ID AS PLANT_ID,
                             u.ID AS USER_ID,
                             u.NAME  AS USER_NAME,
                             u.SURNAME AS USER_SURNAME,
                             u.LOGIN AS USER_LOGIN,
                             p.fk_USER_ID,
                             p.PLANT_NAME,
                             p.DATE,
                             p.IMAGE_NAME,
                             p.THUMB_NAME,
                             p.RND_TEMP, 
                             p.RND_HUM,
                             p.RND_LUM,
                             p.RND_PH,
                             p.MIN_TEMP,
                             p.MAX_TEMP,
                             p.MIN_HUM,
                             p.MAX_HUM,
                             p.MIN_PH,
                             p.MAX_PH
                             FROM PLANTS AS p 
                             INNER JOIN USERS AS u ON p.fk_USER_ID = u.ID WHERE u.LOGIN = \'{self.plant_owner}\' AND p.ID = {self.plant_ID}"""

        result, headers = SQLManager.execute_string(
            "DB.sqlite", sql_str=sql_str, headers=True
        )

        dict_results = {}

        for i in range(len(headers)):
            # print(headers[i]," : ", result[0][i])
            dict_results[headers[i]] = result[0][i]

        # print(dict_results)

        self.strvar_old_plant_name.set(
            self.strvar_old_plant_name.get() + dict_results["PLANT_NAME"]
        )
        self.strvar_image_path.set(
            "./resources/FULL_IMAGE/" + dict_results["IMAGE_NAME"]
        )

        self.strvar_min_temp.set(
            "Minimalna temperatura [C]: " + str(round(dict_results["MIN_TEMP"], 1))
        )
        self.strvar_max_temp.set(
            "Maksimalna temperatura [C]: " + str(round(dict_results["MAX_TEMP"], 1))
        )
        self.strvar_min_hum.set(
            "Minimalna vlažnost [%]: " + str(round(dict_results["MIN_HUM"], 1))
        )
        self.strvar_max_hum.set(
            "Maksimalna vlažnost [%]: " + str(round(dict_results["MAX_HUM"], 1))
        )
        self.strvar_min_ph.set("Minimalni pH: " + str(round(dict_results["MIN_PH"], 1)))
        self.strvar_max_ph.set(
            "Maksimalni pH: " + str(round(dict_results["MAX_PH"], 1))
        )

        self.scale_max_temp.set(dict_results["MAX_TEMP"])
        self.scale_min_temp.set(dict_results["MIN_TEMP"])
        self.scale_max_hum.set(dict_results["MAX_HUM"])
        self.scale_min_hum.set(dict_results["MIN_HUM"])
        self.scale_max_ph.set(dict_results["MAX_PH"])
        self.scale_min_ph.set(dict_results["MIN_PH"])

        self.plant_ID = dict_results["PLANT_ID"]
        self.plant_old_tmb = dict_results["THUMB_NAME"]
        self.plant_old_image = dict_results["IMAGE_NAME"]

        sensors = SQLManager.get_sensors_now(
            "DB.sqlite", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        # print(sensors)
        self.strvar_sensor_temp.set(
            self.strvar_sensor_temp.get()
            + str(round(dict_results["RND_TEMP"] * sensors[1], 1))
        )
        self.strvar_sensor_hum.set(
            self.strvar_sensor_hum.get()
            + str(round(dict_results["RND_HUM"] * sensors[2], 1))
        )
        self.strvar_sensor_ph.set(
            self.strvar_sensor_ph.get()
            + str(round(dict_results["RND_PH"] * sensors[3], 1))
        )
        self.strvar_sensor_lux.set(
            self.strvar_sensor_lux.get()
            + str(round(dict_results["RND_LUM"] * sensors[4], 1))
        )

        if (dict_results["RND_TEMP"] * sensors[1] > dict_results["MAX_TEMP"]) or (
            dict_results["RND_TEMP"] * sensors[1] < dict_results["MIN_TEMP"]
        ):
            self.label_temp.configure(text_color="red")

        if (dict_results["RND_HUM"] * sensors[2] > dict_results["MAX_HUM"]) or (
            dict_results["RND_HUM"] * sensors[2] < dict_results["MIN_HUM"]
        ):
            self.label_hum.configure(text_color="red")

        if (dict_results["RND_PH"] * sensors[3] > dict_results["MAX_PH"]) or (
            dict_results["RND_PH"] * sensors[3] < dict_results["MIN_PH"]
        ):
            self.label_ph.configure(text_color="red")

        self.plant_image_path = "./resources/FULL_IMAGE/" + dict_results["IMAGE_NAME"]
    # Canvas za sliku
    def create_canvas(self):
        height = self.canvas_image.winfo_height()
        width = self.canvas_image.winfo_width()
        self.plant_image = ImageTk.PhotoImage(
            Image.open(self.plant_image_path).resize(
                (int(width * 0.95), int(height * 0.95))
            )
        )
        self.canvas_image.create_image(
            width / 2, height / 2, anchor=tk.CENTER, image=self.plant_image
        )
    # Zamjena slike
    def change_image(self, img_path):
        height = self.canvas_image.winfo_height()
        width = self.canvas_image.winfo_width()
        self.plant_image = ImageTk.PhotoImage(
            Image.open(img_path).resize((int(width * 0.95), int(height * 0.95)))
        )
        self.canvas_image.create_image(
            width / 2, height / 2, anchor=tk.CENTER, image=self.plant_image
        )
    # metoda kojom pokrećemo ovu formu i njena glavna petlja
    def show(self, plant_owner, plant_name, plant_ID):
        self.plant_ID = plant_ID
        self.is_running = True
        self.plant_owner = plant_owner
        self.plant_name = plant_name
        self.fill_form()
        self.canvas_image.image = self.plant_image

        while self.is_running:
            try:
                self.top.update()
            except Exception as a:
                raise a
            finally:
                time.sleep(0.01)

        time.sleep(0.05)
        self.top.destroy()
        return 1


# U nastavku za testiranje samo ove forme bez pokretanja cijele aplikacije

# root = ctk.CTk()

# root.geometry("1024x600")
# root.minsize(width=1024, height=600)
# root.maxsize(width=1024, height=600)

# root.grid_columnconfigure(1, weight=1)
# root.grid_rowconfigure(1, weight=1)


# new_ = EditDialog(root)
# new_.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

# root.mainloop()
