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

        largura = 1000
        altura = 700

        self.window.update_idletasks()

        largura_tela = self.window.winfo_screenwidth()
        altura_tela = self.window.winfo_screenheight()

        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2) - 40

        self.window.geometry(f"{largura}x{altura}+{x}+{y}")

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
            fill="both",
            padx=20,
            pady=(20, 10)
        )

        bottom = ctk.CTkFrame(
            center,
            height=90,
            fg_color="transparent"
        )

        bottom.pack(
            fill="x",
            side="bottom"
        )

        bottom.pack_propagate(False)

        navigation = ctk.CTkFrame(
            bottom,
            fg_color="transparent"
        )

        navigation.pack(
            pady=(8, 4)
        )

        self.btn_prev = ctk.CTkButton(
            navigation,
            text="❮",
            width=36,
            height=36,
            corner_radius=18,
            command=self.previous_photo
        )

        self.btn_prev.pack(
            side="left",
            padx=20
        )

        self.counter_label = ctk.CTkLabel(
            navigation,
            text="",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        self.counter_label.pack(
            side="left"
        )

        self.btn_next = ctk.CTkButton(
            navigation,
            text="❯",
            width=36,
            height=36,
            corner_radius=18,
            command=self.next_photo
        )

        self.btn_next.pack(
            side="left",
            padx=20
        )

        self.info_label = ctk.CTkLabel(
            bottom,
            text="",
            font=ctk.CTkFont(size=14)
        )

        self.info_label.pack()

                
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

        self.counter_label.configure(
            text=f"{self.current_index + 1} / {len(self.photos)}"
        )

        self.info_label.configure(
            text=nome
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