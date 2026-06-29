import os
import shutil


class PhotoManager:

    def import_photos(self, photos, album_name):

        album_path = os.path.join(
            os.path.expanduser("~"),
            "Pictures",
            "PhotoOrganizerAlbums",
            album_name
        )

        os.makedirs(album_path, exist_ok=True)

        imported = []

        for photo in photos:

            destination = os.path.join(
                album_path,
                os.path.basename(photo)
            )

            shutil.copy2(photo, destination)

            imported.append(destination)

        return imported