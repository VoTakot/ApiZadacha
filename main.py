import os
import sys
import requests
import arcade
from arcade.gui import UIManager, UIFlatButton
from arcade.gui.widgets.layout import UIAnchorLayout, UIBoxLayout

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "MAP"
MAP_FILE = "map.png"


class GameView(arcade.Window):
    def setup(self):
        self.theme = 'dark'
        self.z = 10
        self.ll = '73.088504,49.807760'
        self.get_image()
        self.manager = UIManager()
        self.manager.enable()

        self.anchor_layout = UIAnchorLayout()
        self.box_layout = UIBoxLayout(vertical=False, space_between=10)

        self.anchor_layout.add(self.box_layout)
        self.manager.add(self.anchor_layout)
        self.anchor_layout.center_x += self.width // 2 - 200
        self.anchor_layout.center_y += self.height // 2 - 80

        light_theme_btn = UIFlatButton(width=200,
                                      height=100,
                                      text='Светлая')
        light_theme_btn.on_click = self.set_light_theme
        self.box_layout.add(light_theme_btn)
        dark_theme_btn = UIFlatButton(width=200,
                                      height=100,
                                      text='Тёмная')
        dark_theme_btn.on_click = self.set_dark_theme
        self.box_layout.add(dark_theme_btn)

    def set_dark_theme(self, event):
        self.theme = 'dark'

    def set_light_theme(self, event):
        self.theme = 'light'

    def on_draw(self):
        self.clear()

        arcade.draw_texture_rect(
            self.background,
            arcade.LBWH(
                (self.width - self.background.width) // 2,
                (self.height - self.background.height) // 2,
                self.background.width,
                self.background.height
            ),
        )
        self.manager.draw()

    def get_image(self):
        server_address = 'https://static-maps.yandex.ru/v1?'
        api_key = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        params = {
            'll': self.ll,
            'apikey': api_key,
            'z': self.z,
            'theme': self.theme
        }

        response = requests.get(server_address, params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(response.url)
            print("Http статус:", response.status_code, "(", response.reason, ")")
            sys.exit(1)

        # Запишем полученное изображение в файл.
        with open(MAP_FILE, "wb") as file:
            file.write(response.content)

        self.background = arcade.load_texture(MAP_FILE)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.PAGEUP: # из-за того что кнопка на нумпаде не работает
            self.z = str(min(int(self.z) + 1, 21))
        elif key == arcade.key.PAGEDOWN: # из-за того что кнопка на нумпаде не работает
            self.z = str(max(int(self.z) - 1, 0))
        elif key == arcade.key.UP:
            longitude, lattitude = list(map(float, self.ll.split(',')))
            lattitude = str(min(float(lattitude) + 0.05 * (21 - int(self.z)), 90))
            self.ll = ','.join([str(longitude), str(lattitude)])
        elif key == arcade.key.DOWN:
            longitude, lattitude = list(map(float, self.ll.split(',')))
            lattitude = str(max(float(lattitude) - 0.05 * (21 - int(self.z)), -90))
            self.ll = ','.join([str(longitude), str(lattitude)])
        elif key == arcade.key.RIGHT:
            longitude, lattitude = list(map(float, self.ll.split(',')))
            longitude = str(min(float(longitude) + 0.05 * (21 - int(self.z)), 180))
            self.ll = ','.join([str(longitude), str(lattitude)])
        elif key == arcade.key.LEFT:
            longitude, lattitude = list(map(float, self.ll.split(',')))
            longitude = str(max(float(longitude) - 0.05 * (21 - int(self.z)), -180))
            self.ll = ','.join([str(longitude), str(lattitude)])

    def on_update(self, delta_time):
        self.get_image()


def main():
    gameview = GameView(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    gameview.setup()
    arcade.run()
    # Удаляем за собой файл с изображением.
    os.remove(MAP_FILE)


if __name__ == "__main__":
    main()