import os.path
from PIL import Image, ImageDraw
from io import BytesIO


class MonKeyTextureGenerator:
    def __init__(self):
        self.texture_image = self.open_image('Texture.png')
        # Texture image skin coloring positions
        self.texture_skin_positions = self.create_texture_skin_position_list()
        self.texture_eye_position = self.create_texture_eye_position()

    def create_texture_skin_position_list(self):
        width, height = self.texture_image.size
        width = int(width)
        height = int(height)

        middle = (int(0.5 * width), int(0.5 * height))
        middle_top = (int(0.35 * width), int(0.1 * height))
        right_top = (int(0.8 * width), int(0.05 * height))
        down_left = (int(0.1 * width), int(0.85 * height))
        down_middle = (int(0.4 * width), int(0.9 * height))
        small_middle_part = (int(0.33 * width), int(0.31 * height))
        small_right_part = (int(0.96 * width), int(0.31 * height))
        return [middle, middle_top, right_top, down_left, down_middle, small_middle_part, small_right_part]

    def create_texture_eye_position(self):
        width, height = self.texture_image.size
        eye_position = (int(0.88 * width), int(0.88 * height))
        return eye_position

    def open_image(self, image_name):
        directory = os.path.dirname(__file__)
        input_img = os.path.join(directory, image_name)
        return Image.open(input_img)

    def save_colored_image_as_bytes(self, image):
        output = BytesIO()
        image.save(output,format="PNG")
        contents = output.getvalue()
        output.close()
        return contents

    def generate_unity_texture(self, monKey_data):
        unity_texture_copy = self.texture_image.copy()
        for position in self.texture_skin_positions:
            ImageDraw.floodfill(unity_texture_copy, xy=position, value=monKey_data['fur_color'])
        ImageDraw.floodfill(unity_texture_copy, xy=self.texture_eye_position, value=monKey_data['eye_color'])
        return self.save_colored_image_as_bytes(unity_texture_copy)
