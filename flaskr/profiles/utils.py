import os
from secrets import token_hex

from flaskr import app
from PIL import Image


class _Image(Image.Image):

    def crop_to_aspect(self, aspect, divisor=1, alignx=0.5, aligny=0.5):
        # https://stackoverflow.com/questions/43734194/pillow-create-thumbnail-by-cropping-instead-of-preserving-aspect-ratio/43738947
        """Crops an image to a given aspect ratio.
        Args:
            aspect (float): The desired aspect ratio.
            divisor (float): Optional divisor. Allows passing in (w, h) pair as the first two arguments.
            alignx (float): Horizontal crop alignment from 0 (left) to 1 (right)
            aligny (float): Vertical crop alignment from 0 (left) to 1 (right)
        Returns:
            Image: The cropped Image object.
        """
        if self.width / self.height > aspect / divisor:
            newwidth = int(self.height * (aspect / divisor))
            newheight = self.height
        else:
            newwidth = self.width
            newheight = int(self.width / (aspect / divisor))
        img = self.crop((alignx * (self.width - newwidth),
                         aligny * (self.height - newheight),
                         alignx * (self.width - newwidth) + newwidth,
                         aligny * (self.height - newheight) + newheight))
        return img


Image.Image.crop_to_aspect = _Image.crop_to_aspect


def save_photos(photo, id: int, folder_name: str, width: int, height: int):
    random_hex = token_hex(8)
    _, file_ext = os.path.splitext(photo.filename)
    photo_filename = random_hex + str(id) + file_ext
    photo_path = os.path.join(app.root_path,
                              f"static/images/uploads/{folder_name}/" + photo_filename)

    image = Image.open(photo)

    cropped = image.crop_to_aspect(width, height)
    cropped.thumbnail((width, height), Image.ANTIALIAS)

    cropped.save(photo_path)
    return photo_filename


def remove_photo(file_path):
    try:
        full_path = os.path.join(app.root_path, "static" + file_path)
        os.unlink(full_path)
    except:
        return None
