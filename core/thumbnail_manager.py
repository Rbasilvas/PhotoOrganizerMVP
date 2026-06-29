from PIL import Image
import customtkinter as ctk


class ThumbnailManager:

    def create_thumbnail(self, image_path, size=(120, 120)):

        image = Image.open(image_path)

        image.thumbnail(size)

        return ctk.CTkImage(
            light_image=image,
            dark_image=image,
            size=image.size
        )