import customtkinter as ctk
from PIL import Image, ImageTk
import os
import json
from tkinter import filedialog

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")


class PhotoOrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.albums_file = "albums.json"
        self.title("Photo Organizer MVP")
        self.geometry("1100x700")
        self.minsize(1000, 650)

        # Top bar
        top = ctk.CTkFrame(self, height=70, corner_radius=0)
        top.pack(fill="x", side="top")
        self.logo = ctk.CTkLabel(top, text="📸 Photo Organizer", font=ctk.CTkFont(size=22, weight="bold"))
        self.logo.pack(side="left", padx=20)
        self.search = ctk.CTkEntry(top, width=360, placeholder_text="Pesquisar álbuns, pessoas ou tags...")
        self.search.pack(side="right", padx=20, pady=14)

        # --- Theme toggle and header extras ---
        self.theme_var = ctk.StringVar(value="dark-blue")

        def toggle_theme():
            current = ctk.get_appearance_mode()
            ctk.set_appearance_mode("light" if current == "dark" else "dark")
            self.set_status("Tema alternado")

        self.btn_theme = ctk.CTkButton(top, text="🌗", width=40, command=toggle_theme)
        self.btn_theme.pack(side="right", padx=(0, 8), pady=12)

        # --- Load small icons (PNG) if exist in assets/ ---
        def load_icon(name, size=(20, 20)):
            p = os.path.join(os.path.dirname(__file__), "assets", name)
            if os.path.exists(p):
                img = Image.open(p).resize(size)
                return ImageTk.PhotoImage(img)
            return None

        # Main area
        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True, padx=18, pady=12)

        # Sidebar
        sidebar = ctk.CTkFrame(container, width=240, corner_radius=8)
        sidebar.pack(side="left", fill="y", padx=(0, 12), pady=6)
        sidebar.pack_propagate(False)
        self.btn_manage = ctk.CTkButton(sidebar, text="  Gerenciamento de Pastas", anchor="w", command=self.show_manage)
        self.btn_recog = ctk.CTkButton(sidebar, text="  Reconhecimento de Fotos", anchor="w", command=self.show_recog)
        self.btn_cloud = ctk.CTkButton(sidebar, text="  Integração com Nuvem", anchor="w", command=self.show_cloud)
        self.btn_manage.pack(fill="x", padx=12, pady=(20, 8))
        self.btn_recog.pack(fill="x", padx=12, pady=8)
        self.btn_cloud.pack(fill="x", padx=12, pady=8)
        ctk.CTkLabel(sidebar, text="Álbuns recentes", font=ctk.CTkFont(size=12, weight="bold")).pack(padx=12, pady=(18, 6), anchor="w")
        self.recent_list = ctk.CTkTextbox(sidebar, width=200, height=180)
        self.recent_list.pack(padx=12, pady=(0, 12))

        # Content area
        self.content = ctk.CTkFrame(container, corner_radius=8)
        self.content.pack(side="left", fill="both", expand=True)

        # Status bar
        self.status = ctk.CTkLabel(self, text="Pronto", anchor="w")
        self.status.pack(fill="x", side="bottom")

        # Pages
        self.page_manage = ctk.CTkFrame(self.content)
        self.page_recog = ctk.CTkFrame(self.content)
        self.page_cloud = ctk.CTkFrame(self.content)

        # Manage page: cards layout
        header = ctk.CTkLabel(self.page_manage, text="Gerenciamento de Pastas", font=ctk.CTkFont(size=18, weight="bold"))
        header.pack(anchor="nw", padx=16, pady=(12, 6))
        cards = ctk.CTkFrame(self.page_manage)
        cards.pack(fill="x", padx=16)
        card1 = ctk.CTkFrame(cards, width=320, height=140, corner_radius=8)
        card1.pack(side="left", padx=8, pady=8)
        ctk.CTkLabel(card1, text="Criar novo álbum", font=ctk.CTkFont(size=14, weight="bold")).pack(padx=12, pady=(12, 6), anchor="w")
        self.entry_album = ctk.CTkEntry(card1, placeholder_text="Nome do álbum")
        self.entry_album.pack(padx=12, pady=6, fill="x")
        ctk.CTkButton(card1, text="Criar", command=self.create_album).pack(padx=12, pady=(6, 12), anchor="e")

        card2 = ctk.CTkFrame(cards, width=320, height=140, corner_radius=8)
        card2.pack(side="left", padx=8, pady=8)
        ctk.CTkLabel(card2, text="Importar fotos", font=ctk.CTkFont(size=14, weight="bold")).pack(padx=12, pady=(12, 6), anchor="w")
        ctk.CTkButton(card2, text="Selecionar Pasta", command=self.select_folder).pack(padx=12, pady=12, anchor="w")

        # Album viewer area
        self.album_view = ctk.CTkFrame(self.page_manage)
        self.album_view.pack(fill="both", expand=True, padx=16, pady=12)
        self.album_text = ctk.CTkTextbox(self.album_view)
        self.album_text.pack(fill="both", expand=True, padx=8, pady=8)

        # Recognition page
        header2 = ctk.CTkLabel(self.page_recog, text="Reconhecimento de Fotos", font=ctk.CTkFont(size=18, weight="bold"))
        header2.pack(anchor="nw", padx=16, pady=(12, 6))
        recog_area = ctk.CTkFrame(self.page_recog)
        recog_area.pack(fill="both", expand=True, padx=16, pady=12)
        left = ctk.CTkFrame(recog_area, width=420)
        left.pack(side="left", fill="y", padx=(0, 12))
        self.preview_label = ctk.CTkLabel(left, text="Preview", width=420, height=320, fg_color="#1f1f1f", corner_radius=8)
        self.preview_label.pack(padx=8, pady=8)
        ctk.CTkButton(left, text="Anexar foto (simulação)", command=self.simulate_attach).pack(padx=8, pady=6)
        right = ctk.CTkFrame(recog_area)
        right.pack(side="left", fill="both", expand=True)
        ctk.CTkLabel(right, text="Perfis detectados", font=ctk.CTkFont(size=14, weight="bold")).pack(anchor="nw", padx=8, pady=(8, 4))
        self.detected = ctk.CTkTextbox(right, height=12)
        self.detected.pack(fill="both", expand=True, padx=8, pady=8)

        # Cloud page
        header3 = ctk.CTkLabel(self.page_cloud, text="Integração com Nuvem", font=ctk.CTkFont(size=18, weight="bold"))
        header3.pack(anchor="nw", padx=16, pady=(12, 6))
        ctk.CTkLabel(self.page_cloud, text="Conectores disponíveis (simulação):").pack(anchor="nw", padx=16, pady=6)
        ctk.CTkButton(self.page_cloud, text="Configurar Google Drive", command=lambda: self.not_implemented("Google Drive")).pack(padx=16, pady=6, anchor="nw")
        ctk.CTkButton(self.page_cloud, text="Configurar OneDrive", command=lambda: self.not_implemented("OneDrive")).pack(padx=16, pady=6, anchor="nw")

        # load icons after buttons exist
        self.icon_manage = load_icon("folder.png")
        self.icon_recog = load_icon("face.png")
        self.icon_cloud = load_icon("cloud.png")

        if self.icon_manage:
            self.btn_manage.configure(image=self.icon_manage, compound="left")
        if self.icon_recog:
            self.btn_recog.configure(image=self.icon_recog, compound="left")
        if self.icon_cloud:
            self.btn_cloud.configure(image=self.icon_cloud, compound="left")

        # start
        self.load_recent_albums()
        self.show_manage()

    def set_status(self, text):
        self.status.configure(text=text)

    def load_albums(self):
        if not os.path.exists(self.albums_file):
            return []

        try:
            with open(self.albums_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("albums", [])
        except:
            return [] 
         
    def save_albums(self, albums):
        with open(self.albums_file, "w", encoding="utf-8") as f:
            json.dump({"albums": albums}, f, ensure_ascii=False, indent=4)

    def load_recent_albums(self):
        albums = self.load_albums()

        self.recent_list.delete("0.0", "end")

        for album in albums:
            self.recent_list.insert("end", f"{album}\n")      

    def _hide_all(self):
        for p in (self.page_manage, self.page_recog, self.page_cloud):
            p.pack_forget()

    def show_manage(self):
        self._hide_all()
        self.page_manage.pack(fill="both", expand=True)
        self.set_status("Visualizando Gerenciamento de Pastas")

    def show_recog(self):
        self._hide_all()
        self.page_recog.pack(fill="both", expand=True)
        self.set_status("Visualizando Reconhecimento de Fotos")

    def show_cloud(self):
        self._hide_all()
        self.page_cloud.pack(fill="both", expand=True)
        self.set_status("Visualizando Integração com Nuvem")

    def select_folder(self):
        folder = filedialog.askdirectory()

        if not folder:
            return

        extensoes = (".jpg", ".jpeg", ".png", ".bmp", ".gif")

        fotos = [
            f for f in os.listdir(folder)
            if f.lower().endswith(extensoes)
        ]

        total = len(fotos)

        self.album_text.delete("0.0", "end")
        self.album_text.insert(
            "0.0",
            f"Pasta selecionada:\n{folder}\n\nFotos encontradas: {total}"
        )

        self.set_status(f"{total} foto(s) encontradas")    

    def create_album(self):
        name = self.entry_album.get().strip()
        if not name:
            self.album_text.insert("0.0", "Digite um nome de álbum antes.\n")
            return
        base = os.path.join(os.path.expanduser("~"), "Pictures", "PhotoOrganizerAlbums")
        os.makedirs(base, exist_ok=True)
        path = os.path.join(base, name)
        try:
            os.makedirs(path, exist_ok=True)
            albums = self.load_albums()

            if name not in albums:
                albums.append(name)
                self.save_albums(albums)

            self.album_text.insert("0.0", f"Álbum criado: {path}\n")

            self.load_recent_albums()

            self.set_status(f"Álbum '{name}' criado")
        except Exception as e:
            self.album_text.insert("0.0", f"Erro ao criar álbum: {e}\n")
            self.set_status("Erro ao criar álbum")

    
    def simulate_attach(self):
        sample = os.path.join(os.path.dirname(__file__), "sample.jpg")
        if os.path.exists(sample):
            try:
                img = Image.open(sample).resize((420, 320))
                self.tkimg = ImageTk.PhotoImage(img)
                self.preview_label.configure(image=self.tkimg, text="")
                self.detected.delete("0.0", "end")
                self.detected.insert("0.0", "Pessoa A: 98%\nPessoa B: 87%\nTag: praia, família")
                self.set_status("Imagem carregada (simulação)")
            except Exception as e:
                self.preview_label.configure(text=f"Erro ao abrir imagem: {e}")
                self.set_status("Erro ao carregar imagem")
        else:
            self.preview_label.configure(text="Nenhuma sample.jpg encontrada\n(coloque sample.jpg na pasta do projeto)")
            self.set_status("Nenhuma imagem sample.jpg")

    def not_implemented(self, name):
        self.set_status(f"Integração com {name} não configurada")
        self.preview_label.configure(text=f"Integração com {name} não configurada", image="")


if __name__ == "__main__":
    app = PhotoOrganizerApp()
    app.mainloop()
