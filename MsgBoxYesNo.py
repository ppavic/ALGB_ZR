from PIL import Image, ImageTk
import customtkinter
import time
import tkinter

""" Moj custom Message box. najbolje se vidi na "dark windows temi"""
class MsgBoxYesNo:
    def __init__(self, master=None, title="?", msg=""):
        """
        title -> Title of message box\n
        msg -> Message to display
        """

        # cijela putanja ikone
        self.IMG_FILE_PATH = "./resources/" + "Question.png"

        self.image = None
        self.msg = msg
        self.master = master
        self.running = False
        self.return_val = None

        # TopLevele setup - geometrija itd..
        self.top = customtkinter.CTkToplevel()
        self.top.geometry("300x115")  # dimenzija
        # min i max size ne dozvoljavaju povećavanje prozora
        self.top.minsize(300, 115)
        self.top.maxsize(300, 115)
        self.top.title(title)  # naslov
        self.top.lift()  # podiže dialog iznad onog koji je pokrenut
        self.top.focus_force()  # input fokus na ovaj dialog
        self.top.grab_set()  # svi eventi su na ovom widgetu pozadinski je disablean

        self.top.protocol("WM_DELETE_WINDOW", self.on_closing) # Što kada se stisne X na glavnom prozoru

        self.top.after(10, self.create_widgets)
        self.top.bind("<Escape>", self.on_closing)  # izlazak tipkom escape

    def create_widgets(self):

        self.image = ImageTk.PhotoImage(Image.open(self.IMG_FILE_PATH).resize((50, 50)))

        # Header frame naslov
        self.frame_header = customtkinter.CTkFrame(
            master=self.top, corner_radius=5, width=235, height=50
        )
        self.frame_header.place(x=60, y=5, anchor=tkinter.NW)

        # Widget lable na headeru
        self.label_header = customtkinter.CTkLabel(
            master=self.frame_header,
            corner_radius=5,
            text=self.msg,
            text_font=("Consolas", -14),
            width=225,
            height=40,
            justify=tkinter.LEFT,
            wraplength=200,
        )

        self.label_header.place(x=5, y=5, anchor=tkinter.NW)

        self.frame_buttons = customtkinter.CTkFrame(
            master=self.top, corner_radius=5, width=290, height=50
        )
        self.frame_buttons.place(x=5, y=60, anchor=tkinter.NW)

        # Widget button
        self.buton_Yes = customtkinter.CTkButton(
            master=self.frame_buttons,
            corner_radius=5,
            width=100,
            height=20,
            text="Yes",
            command=self.on_Yes,
        )

        self.buton_Yes.place(x=25, y=25, anchor=tkinter.W)

        self.button_No = customtkinter.CTkButton(
            master=self.frame_buttons,
            corner_radius=5,
            width=100,
            height=20,
            text="No",
            command=self.on_No,
        )

        self.button_No.place(anchor=tkinter.W, x=165, y=25)

        self.img_label = customtkinter.CTkLabel(
            master=self.top, image=self.image, width=50, height=50
        )
        self.img_label.place(x=5, y=5, anchor=tkinter.NW)

    def on_closing(self, event=None):
        self.running = False
        self.return_val = 0

    def on_Yes(self, event=None):
        self.running = False
        self.return_val = 1
        return 1

    def on_No(self, event=None):
        self.running = False
        self.return_val = 0
        return 0

    def show_self(self):
        self.running = True

        while self.running:
            try:
                self.top.update()
            except Exception:
                self.return_val = 0
                return self.return_val
            finally:
                time.sleep(0.01)

        time.sleep(0.05)
        self.top.destroy()
        return self.return_val


# Za testiranje
# root = tkinter.Tk()

# def run_mb():
#     mb = MsgBoxYesNo(master=root, title="Title", msg="Message")
#     a = mb.show_self()
#     print(a)

# btn = tkinter.Button(master=root, text="Run MB", command=run_mb)
# btn.grid(row=0, column=0, padx=30, pady=30)

# root.mainloop()
