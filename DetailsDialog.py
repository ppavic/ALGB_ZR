from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import ttk
from customtkinter import *
import tkinter as tk
from tkinter import ttk
import time
from datetime import datetime, timedelta
from SqlLiteUtils import SQLManager
from Charting import TempChart, HumidityChart, pHChart, LuxChart


class DetailsDialog:
    def __init__(self, user_name, plant_id) -> None:

        self.is_running = False

        self.user_name = user_name
        self.plant_id = plant_id

        # TopLevele setup - geometrija itd..
        self.top = CTkToplevel()
        self.top.geometry("1024x768")  # dimenzija
        self.top.title("Detalji o senzorima.")  # naslov

        # min i max size ne dozvoljavaju povećavanje i smanjivanje prozora do određenih dimenzija
        # self.top.minsize(1024, 768)
        # self.top.maxsize(1024, 768)
        self.top.lift()  # podiže dialog iznad onog koji je pokrenut
        self.top.focus_force()  # input fokus na ovaj dialog
        self.top.grab_set()  # svi eventi su na ovom widgetu pozadinski je disablean

        # za Windows display scaling and 4K monitore
        # self.top.tk.call("tk", "scaling", 1.25)

        # podaci iz baze za biljku
        self.temp_data = []
        self.hum_data = []
        self.ph_data = []
        self.lux_data = []
        self.date_data = []

        # podaci o uvjetima za biljku
        self.temp_min = None
        self.temp_max = None
        self.hum_min = None
        self.hum_max = None
        self.ph_min = None
        self.ph_max = None

        # stringovi datuma
        self.start_date = (datetime.now() - timedelta(days=14)).strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        self.stop_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # figure za canvas
        self.fig_temp = None
        self.fig_hum = None
        self.fig_ph = None
        self.fig_lux = None
        
        # Što se događa na klok X glavnog prozora
        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)

        #Izradi Widgete (50 ms odmora kako bi se izbjegao " flickering" kažu na netu ali tako ne izgleda)
        self.top.after(50, self.create_widgets)
        
        # Što ako stisnemo Esc gumbić 
        self.top.bind("<Escape>", self.on_closing)  # izlazak tipkom escape

        
        self.prepare_figures(start_date=self.start_date, stop_date=self.stop_date)
        
        self.top.bind("Configure>", self.on_resize)
        
        # Charts - Dijagrami
        self.fig_temp = TempChart(
            date_list=self.date_data,
            temperature=self.temp_data,
            min_temp=self.temp_min,
            max_temp=self.temp_max,
        )

        self.fig_hum = HumidityChart(
            date_list=self.date_data,
            humiditiy=self.hum_data,
            min_hum=self.hum_min,
            max_hum=self.hum_max,
        )

        self.fig_ph = pHChart(
            date_list=self.date_data,
            ph=self.ph_data,
            min_ph=self.ph_min,
            max_ph=self.ph_max,
        )

        self.fig_lux = LuxChart(date_list=self.date_data, lux=self.lux_data)

    def create_widgets(self):

        # Style za tabove
        s = ttk.Style()

        # Provjera dali je Tema već "instancirana, ako je da se ne instancira ponovno"
        theme_exists = False
        for t in s.theme_names():
            if t == "MyStyle":
                theme_exists = True

        if not theme_exists:
            s.theme_create(
                "MyStyle",
                parent="alt",
                settings={
                    "TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0]}},
                    "TNotebook.Tab": {
                        "configure": {
                            "padding": [30, 15],
                            "font": ("Consolas", "12", "bold", "underline"),
                        },
                    },
                },
            )
            s.theme_use("MyStyle")

        # Glavni frame
        self.frame_main = tk.Frame(master=self.top, bg="#433f4f")
        self.frame_main.grid(row=2, column=1, sticky=tk.NSEW, padx=5, pady=5)

        self.top.grid_columnconfigure(1, weight=1)
        self.top.grid_rowconfigure(2, weight=1)

        self.frame_main.grid_columnconfigure(1, weight=1)
        self.frame_main.grid_rowconfigure(1, weight=1)

        # Prozor s Tabovima aka Notebook iz ttk (themed Tkinter)
        self.tabWidget = ttk.Notebook(self.frame_main, padding=[10, 10, 10, 10])
        self.tabWidget.grid(row=1, column=1, padx=5, pady=5, sticky=tk.NSEW)

        #Frameovi za svaki radni list
        self.frame_Temperature = tk.Frame(self.tabWidget, bg="#9c3e0b")
        self.frame_Humidity = tk.Frame(self.tabWidget, bg="#354159")
        self.frame_Acidity = tk.Frame(self.tabWidget, bg="#8cf52a")
        self.frame_Luminosity = tk.Frame(self.tabWidget, bg="#f0eadf")
        # konfiguracija grid managera
        self.frame_Temperature.grid_columnconfigure(1, weight=1)
        self.frame_Temperature.grid_rowconfigure(1, weight=1)
        self.frame_Humidity.grid_columnconfigure(1, weight=1)
        self.frame_Humidity.grid_rowconfigure(1, weight=1)
        self.frame_Acidity.grid_columnconfigure(1, weight=1)
        self.frame_Acidity.grid_rowconfigure(1, weight=1)
        self.frame_Luminosity.grid_columnconfigure(1, weight=1)
        self.frame_Luminosity.grid_rowconfigure(1, weight=1)
        # Naslovi
        self.tabWidget.add(self.frame_Temperature, text="Temperatura")
        self.tabWidget.add(self.frame_Humidity, text="Vlažnost zemje")
        self.tabWidget.add(self.frame_Acidity, text="Kiselost zemlje")
        self.tabWidget.add(self.frame_Luminosity, text="Količina svjetla")

        # koji je radni list inicijalno označen
        self.tabWidget.select(0)

        # Canvas za svaki radni list
        self.canvas_temperature = FigureCanvasTkAgg(
            self.fig_temp.get_fig(), master=self.frame_Temperature
        )
        self.canvas_temperature.draw()
        self.canvas_temperature.get_tk_widget().grid(
            row=1,
            column=1,
            sticky=tk.NSEW,
            padx=5,
            pady=5,
        )

        self.canvas_hum = FigureCanvasTkAgg(
            self.fig_hum.get_fig(), master=self.frame_Humidity
        )
        self.canvas_hum.draw()
        self.canvas_hum.get_tk_widget().grid(
            row=1, column=1, sticky=tk.NSEW, padx=5, pady=5
        )

        self.canvas_ph = FigureCanvasTkAgg(
            self.fig_ph.get_fig(), master=self.frame_Acidity
        )
        self.canvas_ph.draw()
        self.canvas_ph.get_tk_widget().grid(
            row=1, column=1, sticky=tk.NSEW, padx=5, pady=5
        )

        self.canvas_lux = FigureCanvasTkAgg(
            self.fig_lux.get_fig(), master=self.frame_Luminosity
        )
        self.canvas_lux.draw()
        self.canvas_lux.get_tk_widget().grid(
            row=1, column=1, padx=5, pady=5, sticky=tk.NSEW
        )

    # Query iz baze za podatke sa senzora i biljaka
    def prepare_figures(self, start_date: str, stop_date: str) -> None:

        sql_str = f"""SELECT U.NAME,
                             U.SURNAME,
                             P.ID AS PLANT_ID,
                             P.RND_TEMP,
                             P.RND_HUM, 
                             P.RND_PH,
                             P.RND_LUM,
                             P.MIN_TEMP,
                             P.MAX_TEMP,
                             P.MIN_HUM,
                             P.MAX_HUM,
                             P.MIN_PH,
                             P.MAX_PH
                             FROM PLANTS AS P INNER JOIN USERS AS U ON U.ID = P.fk_USER_ID
                             WHERE P.ID = {self.plant_id} AND U.LOGIN= \'{self.user_name}\'"""

        plant_data, headers = SQLManager.execute_string(
            database="DB.sqlite", sql_str=sql_str, headers=True
        )

        "Ubacivanje u rječnik kako bi bilo laše odabirati vrijednosti iz baze o senzorima"
        dict_plant_data = {}

        for i in range(len(headers)):
            # print(headers[i], " : ", plant_data[0][i])
            dict_plant_data[headers[i]] = plant_data[0][i]

        sql_str = f"""SELECT S.DATE_TIME,
                             S.SENSOR1_TEMP,
                             S.SENSOR2_HUM,
                             S.SENSOR3_PH,
                             S.SENSOR4_LUM
                             FROM SENSORS AS S WHERE S.DATE_TIME > \'{start_date}\' AND S.DATE_TIME < \'{stop_date}\'
                             ORDER BY S.DATE_TIME"""

        sensor_data = SQLManager.execute_string("DB.sqlite", sql_str=sql_str)

        self.temp_min = dict_plant_data["MIN_TEMP"]
        self.temp_max = dict_plant_data["MAX_TEMP"]
        self.hum_min = dict_plant_data["MIN_HUM"]
        self.hum_max = dict_plant_data["MAX_HUM"]
        self.ph_min = dict_plant_data["MIN_PH"]
        self.ph_max = dict_plant_data["MAX_PH"]

        # random senzora za svaku biljku.
        for n in range(len(sensor_data)):
            self.date_data.append(
                datetime.strptime(sensor_data[n][0], "%Y-%m-%d %H:%M:%S")
            )
            self.temp_data.append(sensor_data[n][1] * dict_plant_data["RND_TEMP"])
            self.hum_data.append(sensor_data[n][2] * dict_plant_data["RND_HUM"])
            self.ph_data.append(sensor_data[n][3] * dict_plant_data["RND_PH"])
            self.lux_data.append(sensor_data[n][4] * dict_plant_data["RND_LUM"])

    #zatvaranje prozora
    def on_closing(self, event=None):
        self.is_running = False
    # ako zatreba, što se događa kod "resize-a"
    def on_resize(self, event=None):
        pass
    # Glaavna Petlja ovog Widgeta
    def show(self):
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

        return 0
