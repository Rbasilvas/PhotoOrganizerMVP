import os

import customtkinter as ctk
from PIL import Image


class Viewer:

    def __init__(self):

        self.window = None
        self.photos = []
        self.current_index = 0

        self.image_label = None
        self.info_label = None

    def open(self, photos, current_index):

        self.photos = photos
        self.current_index = current_index

        if self.window is not None and self.window.winfo_exists():
            self.window.destroy()

        self.window = ctk.CTkToplevel()

        self.window.title("Visualizador")

        self.window.geometry("1000x700")

        self.window.lift()
        self.window.focus_force()
        self.window.attributes("-topmost", True)
        self.window.after(
            300,
            lambda: self.window.attributes("-topmost", False)
        )

        # Navegação pelo teclado
        self.window.bind("<Left>", lambda e: self.previous_photo())
        self.window.bind("<Right>", lambda e: self.next_photo())
        self.window.bind("<Escape>", lambda e: self.window.destroy())

        main = ctk.CTkFrame(self.window)
        main.pack(fill="both", expand=True)

        # Botão esquerda
        self.left_button = ctk.CTkButton(
            main,
            text="◀",
            width=60,
            command=self.previous_photo
        )

        self.left_button.pack(
            side="left",
            padx=15
        )

        # Área central
        center = ctk.CTkFrame(main)

        center.pack(
            side="left",
            expand=True,
            fill="both"
        )

        self.image_label = ctk.CTkLabel(
            center,
            text=""
        )

        self.image_label.pack(
            expand=True,
            pady=(15, 5)
        )

        self.info_label = ctk.CTkLabel(
            center,
            text=""
        )

        self.info_label.pack(
            pady=(0, 15)
        )

        # Botão direita
        self.right_button = ctk.CTkButton(
            main,
            text="▶",
            width=60,
            command=self.next_photo
        )

        self.right_button.pack(
            side="right",
            padx=15
        )

        self.show_photo()

    def show_photo(self):

        image_path = self.photos[self.current_index]

        image = Image.open(image_path)

        image.thumbnail((850, 600))

        photo = ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=image.size
        )

        self.image_label.configure(
            image=photo,
            text=""
        )

        self.image_label.image = photo

        nome = os.path.basename(image_path)

        self.info_label.configure(
            text=(
                f"Foto {self.current_index + 1} de {len(self.photos)}\n"
                f"{nome}"
            )
        )

    def next_photo(self):

        if not self.photos:
            return

        self.current_index += 1

        if self.current_index >= len(self.photos):
            self.current_index = 0

        self.show_photo()

    def previous_photo(self):

        if not self.photos:
            return

        self.current_index -= 1

        if self.current_index < 0:
            self.current_index = len(self.photos) - 1

        self.show_photo()