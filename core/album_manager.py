import os
import json


class AlbumManager:

    def __init__(self, albums_file="data/albums.json"):

        self.albums_file = albums_file

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.albums_file):

            with open(self.albums_file, "w", encoding="utf-8") as f:

                json.dump(
                    {"albums": []},
                    f,
                    ensure_ascii=False,
                    indent=4
                )

    def load_albums(self):

        with open(self.albums_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        print("ARQUIVO:", self.albums_file)
        print("DADOS:", data)
        print("TOTAL:", len(data["albums"]))

        return data["albums"]

    def save_albums(self, albums):

        with open(self.albums_file, "w", encoding="utf-8") as f:

            json.dump(
                {"albums": albums},
                f,
                ensure_ascii=False,
                indent=4
            )

    def create_album(self, name):

        base = os.path.join(
            os.path.expanduser("~"),
            "Pictures",
            "PhotoOrganizerAlbums"
        )

        os.makedirs(base, exist_ok=True)

        path = os.path.join(base, name)

        os.makedirs(path, exist_ok=True)

        albums = self.load_albums()

        if name not in albums:

            albums.append(name)

            self.save_albums(albums)

        return path
    
    def get_photo_count(self, album):

        pasta = os.path.join(
            os.path.expanduser("~"),
            "Pictures",
            "PhotoOrganizerAlbums",
            album
        )

        if not os.path.exists(pasta):
            return 0

        extensoes = (
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".gif"
        )

        return sum(
            1
            for arquivo in os.listdir(pasta)
            if arquivo.lower().endswith(extensoes)
        )