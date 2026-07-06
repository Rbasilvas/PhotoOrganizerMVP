import customtkinter as ctk
from PIL import Image


class Viewer:

    def __init__(self):
        self.window = None

    def open(self, image_path):

        if self.window is not None and self.window.winfo_exists():
            self.window.destroy()

        self.window = ctk.CTkToplevel()
        
        self.window.lift()
        self.window.focus_force()
        self.window.attributes("-topmost", True)
        self.window.after(300, lambda: self.window.attributes("-topmost", False))

        self.window.title("Visualizador")

        self.window.geometry("1000x700")

        image = Image.open(image_path)

        image.thumbnail((900, 650))

        photo = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=image.size
        )

        label = ctk.CTkLabel(
            self.window,
            image=photo,
            text=""
        )

        label.image = photo

        label.pack(expand=True, padx=20, pady=20)