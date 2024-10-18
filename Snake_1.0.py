import tkinter as tk
import pygame
import random
from PIL import Image, ImageTk,ImageSequence


def load_highscore():
    """Загружает максимальный рекорд из файла 'high_score.txt' и возвращает его значение."""
    with open("high_score.txt", "r") as file:
        return int(file.read())


def save_highscore(score):
    """Сохраняет максимальный рекорд в файл 'high_score.txt'."""
    with open("high_score.txt", "w") as file:
        file.write(str(score))


root = tk.Tk()
root.title("Snake V 1.0 by Artur Otto")
pygame.init()
eat_sound = pygame.mixer.Sound('apple_eat.mp3')
respawn_sound = pygame.mixer.Sound('pl_respawn.mp3')
game_over_sound = pygame.mixer.Sound('game_over_sound.mp3')
pygame.mixer.music.load('background_music.mp3')

# Установка уровня громкости (значение от 0.0 до 1.0)
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)  # Параметр -1 указывает на циклическое воспроизведение
canvas_width = 600
canvas_height = 600

snake_body = []
direction = "Right"  # Начальное направление вправо
apple = None
snake_space = 10
flag = True
start_lenth = 2
snake_speed = 10
game_after = None
task = None
count = 0
max_score = load_highscore()
score = 0
score_text = None

def move_snake(event):
    """
        Обрабатывает события нажатия клавиш для изменения направления движения змейки.

        Args:
            event: Событие клавиши.
        """

    global direction
    if event.keysym == "Up" and direction != "Down":
        direction = "Up"
    elif event.keysym == "Down" and direction != "Up":
        direction = "Down"
    elif event.keysym == "Right" and direction != "Left":
        direction = "Right"
    elif event.keysym == "Left" and direction != "Right":
        direction = "Left"


def why_endgame():
    """Инициализирует змейку заново после завершения игры."""
    global snake_body, canvas,apple,flag,direction,start_lenth

    snake_speed = 80

    for segment in snake_body:
        canvas.delete(segment)
    snake_body.clear()
    head_x1, head_y1, head_x2, head_y2 = 20, 20, 30, 30
    for i in range(start_lenth):
        snake_body.append(canvas.create_rectangle(head_x1, head_y1 + 10, head_x2, head_y2 + 10, fill="purple"))

        # Удалить яблоко
    if apple is not None:
        canvas.delete(apple)
        apple = None

        # Вернуть флаг в начальное состояние
    flag = True

        # Установить начальное направление вправо
    direction = "Right"

# save_highscore(0)


def game():
    """Основная игровая логика змейки."""
    global snake_body, flag, apple, direction, snake_space,\
         start_lenth, snake_speed, game_after, apple_image_to_game, task, score, max_score, score_text


    if flag:
        x = round(random.randint(0, 590) / 10) * 10
        y = round(random.randint(0, 590) / 10) * 10
        apple = canvas.create_rectangle(x, y, x + 10, y + 10,fill="red")
        # apple = canvas.create_image(x, y, image=apple_image_to_game)
        flag = False
    elif not flag:

        x1, y1, x2, y2 = canvas.bbox(snake_body[-1])
        x3, y3, x4, y4 = canvas.bbox(apple)
        # print(x3,y3,x4,y4)

        if x1 >= x3 and y1 >= y3 and x2 <= x4 and y2 <= y4:
            x, y, x1, y1 = canvas.coords(snake_body[0])
            if direction == "Up":
                new_segment = canvas.create_rectangle(x, y - snake_space, x1 + snake_space, y1, fill="purple")
            elif direction == "Down":
                new_segment = canvas.create_rectangle(x, y + snake_space, x1 + snake_space, y1, fill="purple")
            elif direction == "Right":
                new_segment = canvas.create_rectangle(x + snake_space, y, x1 + snake_space, y1 + snake_space, fill="purple")
            elif direction == "Left":
                new_segment = canvas.create_rectangle(x - snake_space, y, x1, y1 + snake_space, fill="purple")
            snake_body.insert(0, new_segment)
            canvas.delete(apple)
            eat_sound.play()

            score+=10
            if score > max_score:
                save_highscore(score)
                max_score = score

            canvas.itemconfig(score_text, text = f"SCORE:{score}")

            flag = True


    head_x1, head_y1, head_x2, head_y2 = canvas.coords(snake_body[-1])
    if direction == "Up":
        new_x1, new_y1, new_x2, new_y2 = head_x1, head_y1 - snake_space, head_x2, head_y2 - snake_space
    elif direction == "Down":
        new_x1, new_y1, new_x2, new_y2 = head_x1, head_y1 + snake_space, head_x2, head_y2 + snake_space
    elif direction == "Right":
        new_x1, new_y1, new_x2, new_y2 = head_x1 + snake_space, head_y1, head_x2 + snake_space, head_y2
    elif direction == "Left":
        new_x1, new_y1, new_x2, new_y2 = head_x1 - snake_space, head_y1, head_x2 - snake_space, head_y2


    new_segment = canvas.create_rectangle(new_x1, new_y1, new_x2, new_y2, fill="purple")





    snake_body.append(new_segment)


    if len(snake_body) > 2:

        canvas.delete(snake_body.pop(0))

    task = root.after(snake_speed, game)

    if (head_x1 < 0 or head_y1 < 0 or head_x2 > canvas_width or head_y2 > canvas_height):
        root.after_cancel(task)
        game_over()

    if len(snake_body) > 2:
        for segment in snake_body[:-1]:  # Проверка на столкновение с самой собой
            if canvas.coords(segment) == canvas.coords(new_segment):
                root.after_cancel(task)
                game_over()


canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, background="white")
canvas.pack()

##################################### ФОТО PLAY ####################################################
play_image = Image.open("start.png")
play_new_width = 200
play_new_height = 75
play_image = play_image.resize((play_new_width, play_new_height))
play_image_to_game = ImageTk.PhotoImage(play_image)
##################################### ФОТО EXIT ####################################################
exit_image = Image.open("exit.png")
exit_new_width = 200
exit_new_height = 75
exit_image = exit_image.resize((exit_new_width, exit_new_height))
exit_image_to_game = ImageTk.PhotoImage(exit_image)
##################################### ФОТО BACKROUND MENU ####################################################
background_menu_image = Image.open("background_menu.jpg")
background_menu_image = background_menu_image.resize((canvas_width, canvas_height))
background_menu_photo = ImageTk.PhotoImage(background_menu_image)
##################################### ФОТО BACKROUND GAME ####################################################
background_game_image = Image.open("background_game.jpg")
background_game_image = background_game_image.resize((canvas_width, canvas_height))
background_game_photo = ImageTk.PhotoImage(background_game_image)
##################################### ФОТО APPLE ####################################################
apple_image = Image.open("apple.png")
apple_new_width = 10
apple_new_height = 10
apple_image = apple_image.resize((apple_new_width, apple_new_height))
apple_image_to_game = ImageTk.PhotoImage(apple_image)
##################################### ФОТО GAME OVER ####################################################
game_over_image = Image.open("game_over.png")
game_over_new_width = 200
game_over_new_height = 75
game_over_image = game_over_image.resize((game_over_new_width, game_over_new_height))
game_over_image_to_game = ImageTk.PhotoImage(game_over_image)
##################################### ФОТО GAME OVER NEW GAME ####################################################
new_game_image = Image.open("new_game.png")
new_game_new_width = 200
new_game_new_height = 75
new_game_image = new_game_image.resize((new_game_new_width, new_game_new_height))
new_game_image_to_game = ImageTk.PhotoImage(new_game_image)
##################################### ФОТО GAME OVER MENU ####################################################
menu_image = Image.open("menu.png")
menu_new_width = 200
menu_new_height = 75
menu_image = menu_image.resize((menu_new_width, menu_new_height))
menu_image_to_game = ImageTk.PhotoImage(menu_image)

count = 0
anim = None
def game_over():
    """Обработчик завершения игры и отображения экрана "Game Over"."""
    global game_over_image_to_game, new_game_image_to_game, menu_image_to_game,game_after
    game_over_sound.play()


    game_ov = canvas.create_image(300, 200, image=game_over_image_to_game)
    game_ov_new_game = canvas.create_image(300, 300, image=new_game_image_to_game)
    game_ov_menu = canvas.create_image(300, 400, image=menu_image_to_game)

    canvas.tag_bind(game_ov_new_game, "<Button-1>", to_game)
    canvas.tag_bind(game_ov_menu, "<Button-1>", start_menu)
    snake_speed = 0


def start_menu(event):
    """
        Запуск главного меню игры.

        Args:
            event: Событие клавиши.
            """
    global play_image_to_game, background_menu_image_photo, exit_image_to_game, canvas,max_score,score
    game_over_sound.stop()
    canvas.destroy()
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, background="white")
    background = canvas.create_image(0, 0, anchor=tk.NW, image=background_menu_photo)
    canvas.create_text(480, 20, text=f"MAX SCORE:{max_score}", fill="red", font=("Arial", 20))
    canvas.create_text(505, 50, text=f"SCORE:{score}", fill="red", font=("Arial", 20))
    canvas.pack()
    play_button = canvas.create_image(300, 250, image=play_image_to_game)
    exit_button = canvas.create_image(300, 400, image=exit_image_to_game)


    canvas.tag_bind(play_button, "<Button-1>", to_game)
    canvas.tag_bind(exit_button, "<Button-1>", exit_game)

def to_game(event):
    """
        Функция запуска игры по кнопке.

        Args:
            event: Событие клавиши.
            """
    global canvas, background_game_photo, snake_speed, max_score, score, score_text
    game_over_sound.stop()

    canvas.destroy()
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, background="white")
    background = canvas.create_image(0, 0, anchor=tk.NW, image=background_game_photo)

    canvas.pack()
    why_endgame()
    snake_speed = 80
    score = 0
    score_text = canvas.create_text(505, 20, text=f"SCORE:{score}", fill="red", font=("Arial", 20))
    respawn_sound.play()
    game()

    canvas.bind_all("<KeyPress-Up>", move_snake)
    canvas.bind_all("<KeyPress-Down>", move_snake)
    canvas.bind_all("<KeyPress-Right>", move_snake)
    canvas.bind_all("<KeyPress-Left>", move_snake)



def exit_game(event):
    """
        Закрытие игры по кнопке.

        Args:
            event: Событие клавиши."""
    root.destroy()




start_menu(1)
root.mainloop()