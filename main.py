import arcade
import random

# устанавливаем константы
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Star Wars"


# класс с игрой
class MyGame(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.background = arcade.load_texture("images/space_background.png")
        self.Our_Ship = War_Ship("images/x-wing.png", 0.5)
        self.set_mouse_visible(False)
        self.sprite_list = arcade.SpriteList()
        self.Enemies = arcade.SpriteList()

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        bullet = Bullet()
        bullet.center_x = x
        bullet.bottom = self.Our_Ship.top
        arcade.play_sound(bullet.sound)
        self.sprite_list.append(bullet)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        self.Our_Ship.center_x = x
        self.Our_Ship.center_y = y


    # начальные значения
    def setup(self):
        self.Our_Ship.center_x = SCREEN_WIDTH / 2
        self.Our_Ship.center_y = SCREEN_HEIGHT / 2
        for i in range(50):
            enemy = Enemy()
            enemy.center_x = random.randint(20, SCREEN_WIDTH - 20)
            enemy.center_y = 50 * i + SCREEN_HEIGHT
            enemy.texture = enemy.textures[0]
            self.Enemies.append(enemy)

    # отрисовка
    def on_draw(self):
        arcade.start_render()
        arcade.set_background_color(arcade.color.AMAZON)
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.Our_Ship.draw()
        self.sprite_list.draw()
        self.Enemies.draw()

    # игровая логика
    def update(self, delta_time):
        self.Our_Ship.update()
        self.sprite_list.update()
        self.Enemies.update()
        self.Enemies.update_animation()
        for bullet in self.sprite_list:
            for enemy in self.Enemies:
                if arcade.check_for_collision(bullet, enemy):
                    enemy.kill()
                    bullet.kill()
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.kill()

class War_Ship(arcade.Sprite):
    def update(self):
        if self.top >= SCREEN_HEIGHT:
            self.top = SCREEN_HEIGHT
        elif self.bottom <= 0:
            self.bottom = 0
        if self.right >= SCREEN_WIDTH:
            self.right = SCREEN_WIDTH
        elif self.left <= 0:
            self.left = 0

class Bullet(arcade.Sprite):
    def __init__(self):
        super(Bullet, self).__init__("images/laser.png", 0.8)
        self.sound = arcade.load_sound("sounds/laser.wav")
        self.change_y = 5

    def update(self):
        self.center_y += self.change_y

class Enemy(arcade.AnimatedTimeSprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.textures.append(arcade.load_texture("images/tie_fighter1.png"))
        self.textures.append(arcade.load_texture("images/tie_fighter2.png"))
        self.change_y = 1

    def update(self):
        self.center_y -= self.change_y


window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
window.setup()
arcade.run()
