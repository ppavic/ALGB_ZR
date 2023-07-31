import matplotlib.dates as mpldates
from matplotlib.dates import DateFormatter
from matplotlib.figure import Figure

# Kalsa za svaki chart na prozoru "Detalji"
class TempChart:
    def __init__(self, date_list, temperature, min_temp, max_temp):
        
        #Format datuma na dijagramu
        plot_dateformat = DateFormatter("%d/%m/%Y")
        
        # Matplotlib figure -- slika za Canvas
        self.fig = Figure(figsize=(3, 3), dpi=100, tight_layout=True)
        # Naslov
        self.fig.suptitle(
            f"""Temperatura od {min(date_list).strftime("%d/%m/%Y")} do: {max(date_list).strftime("%d/%m/%Y")}"""
        )
        # dijagram kao takav na frigure-u
        ax = self.fig.add_subplot()

        #crtanje podataka
        ax.plot(date_list, temperature, color="#ad1909", marker="o")
        ax.plot(
            [min(date_list), max(date_list)],
            [min_temp, min_temp],
            color="red",
            label="Minimum idealne temperature",
        )
        ax.plot(
            [min(date_list), max(date_list)],
            [max_temp, max_temp],
            color="blue",
            label="Maximum idealne temperature",
        )

        #Naslovi na osima
        ax.set_xlabel("Datum")
        ax.set_ylabel("Temperatura [C]")

        #Postavljanje boja
        ax.set_facecolor("#fcffed")
        # Legenda na dijagramu
        ax.legend(loc="center right", shadow=True, facecolor="#fcffed")
        # Vidljivost mreže na dijagrau
        ax.grid(visible=True)
        
        # Oznake na osima.
        ax.tick_params(axis='x', labelrotation = 45)
        ax.xaxis.set_major_locator(mpldates.DayLocator(interval=1))
        ax.xaxis.set_minor_locator(mpldates.HourLocator(interval=6))
        ax.xaxis.set_major_formatter(plot_dateformat)

    def get_fig(self):
        """Dohvatanje "slike" dijagrama

        Returns:
            Matplotlib Figure
        """        
        return self.fig
    
class HumidityChart:
    def __init__(self, date_list, humiditiy, min_hum, max_hum):
        
        plot_dateformat = DateFormatter("%d/%m/%Y")
        self.fig = Figure(figsize=(3, 3), dpi=100, tight_layout=True)
        self.fig.suptitle(
            f"""Temperatura od {min(date_list).strftime("%d/%m/%Y")} do: {max(date_list).strftime("%d/%m/%Y")}"""
        )
        
        ax = self.fig.add_subplot()

        ax.plot(date_list, humiditiy, color="#a9c6fc", marker="o")
        ax.plot(
            [min(date_list), max(date_list)],
            [min_hum, min_hum],
            color="red",
            label="Minimum idealne vlažnosti",
            linewidth=2
        )
        ax.plot(
            [min(date_list), max(date_list)],
            [max_hum, max_hum],
            color="blue",
            label="Maximum idealne vlažnosti",
            linewidth=2
        )

        ax.set_xlabel("Datum")
        ax.set_ylabel("Vlažnost tla [%]")

        ax.set_facecolor("#39383b")
        ax.legend(loc="center right", shadow=True, facecolor="#39383b",labelcolor="white")
        ax.grid(visible=True)
        ax.tick_params(axis='x', labelrotation = 45)

        ax.xaxis.set_major_locator(mpldates.DayLocator(interval=1))
        ax.xaxis.set_minor_locator(mpldates.HourLocator(interval=6))
        ax.xaxis.set_major_formatter(plot_dateformat)

    def get_fig(self):
        return self.fig


class pHChart:
    def __init__(self, date_list, ph, min_ph, max_ph):
        
        plot_dateformat = DateFormatter("%d/%m/%Y")
        self.fig = Figure(figsize=(3, 3), dpi=100, tight_layout=True)
        self.fig.suptitle(
            f"""Kiselost tla od {min(date_list).strftime("%d/%m/%Y")} do: {max(date_list).strftime("%d/%m/%Y")}"""
        )
        
        ax = self.fig.add_subplot()

        ax.plot(date_list, ph, color="#112b13", marker="o")
        ax.plot(
            [min(date_list), max(date_list)],
            [min_ph, min_ph],
            color="red",
            label="Minimum idealne kiselosti",
            linewidth=2
        )
        ax.plot(
            [min(date_list), max(date_list)],
            [max_ph, max_ph],
            color="blue",
            label="Maximum idealne kiselosti",
            linewidth=2
        )

        ax.set_xlabel("Datum")
        ax.set_ylabel("Kiselost tla [%]")

        ax.set_facecolor("#cfc493")
        ax.legend(loc="best", shadow=True, facecolor="#cfc493")
        ax.grid(visible=True)
        ax.tick_params(axis='x', labelrotation = 45)

        ax.xaxis.set_major_locator(mpldates.DayLocator(interval=1))
        ax.xaxis.set_minor_locator(mpldates.HourLocator(interval=6))
        ax.xaxis.set_major_formatter(plot_dateformat)

    def get_fig(self):
        return self.fig


class LuxChart:
    def __init__(self, date_list, lux):
        
        plot_dateformat = DateFormatter("%d/%m/%Y")
        self.fig = Figure(figsize=(3, 3), dpi=100, tight_layout=True)
        self.fig.suptitle(
            f"""Osvjetljenost od {min(date_list).strftime("%d/%m/%Y")} do: {max(date_list).strftime("%d/%m/%Y")}"""
        )
        
        ax = self.fig.add_subplot()

        ax.plot(date_list, lux, color="#faf25f", marker="o", label="Osvjetljenje [lux]")

        ax.set_xlabel("Datum")
        ax.set_ylabel("Osvjetljenots [lux]")

        ax.set_facecolor("#222b7a")
        ax.legend(loc="best", shadow=True, facecolor="#222b7a", labelcolor="white")
        ax.grid(visible=True)
        ax.tick_params(axis='x', labelrotation = 45)

        ax.xaxis.set_major_locator(mpldates.DayLocator(interval=1))
        ax.xaxis.set_minor_locator(mpldates.HourLocator(interval=6))
        ax.xaxis.set_major_formatter(plot_dateformat)

    def get_fig(self):
        return self.fig
