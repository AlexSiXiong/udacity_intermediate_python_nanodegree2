"""The implementation of the meme engine."""
import random
import os
from PIL import Image, ImageFont, ImageDraw

from helper import dir_walk, generate_color
from .MemeEngineInterface import MemeEngineInterface
from helper import warp_long_text


class MemeEngine(MemeEngineInterface):
    """Meme Engine accepts the image loaded and it processes all the image processing works."""

    @staticmethod
    def load_img(path):
        """Load the image from the path."""
        return Image.open(path)

    @staticmethod
    def resize_img(img, width=800):
        """Note img = img.resize(300, 300) => img = img.resize((300,300))."""
        w, h = img.size
        ratio = width / w
        return img.resize((int(width), int(h * ratio)), Image.NEAREST)

    @staticmethod
    def assign_font():
        """Load and assign a font randomly to the quote."""
        font_dir = './fonts'
        font_path = random.choice(dir_walk(font_dir))
        return ImageFont.truetype(font_path, size=30, encoding='utf-8')

    def synthesis_new_img(self, image, text, author):
        """Add the text on the image."""
        draw = ImageDraw.Draw(image)
        w, h = image.size
        color = generate_color()

        sentence = warp_long_text(text + ' - ' + author)
        font = self.assign_font()

        draw.text(
            (w / 16, h / random.uniform(1.3, 1.5)),
            sentence,
            fill=color,
            font=font,
            stroke_width=1
        )

        return image

    def save_file(self, image):
        """Save the processed image to the target place."""
        image_output_name = f"meme_{random.randint(0, 100)}.jpg"
        output_path = os.path.join(self.output_dir, image_output_name)
        image.save(output_path)
        print(f'image saved in {output_path}')
        return output_path

    def make_meme(self, img_path: str, text: str, author: str, width=500):
        """Create a meme."""
        try:
            self.can_ingest(img_path)
            img = self.load_img(img_path)
            img = self.resize_img(img)
            new_img = self.synthesis_new_img(img, text, author)
            return self.save_file(new_img)
        except Exception as e:
            print('make_meme error.')
            print(e)
