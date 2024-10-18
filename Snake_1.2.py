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
root.title("Snake V 1.2 by Artur Otto and Arseniy Akimov")
pygame.init()
eat_sound = pygame.mixer.Sound('apple_eat.mp3')
respawn_sound = pygame.mixer.Sound('pl_respawn.mp3')
game_over_sound = pygame.mixer.Sound('game_over_sound.mp3')
hard_game_sound = pygame.mixer.Sound('hard_button_sound.mp3')
pygame.mixer.music.load('background_music.mp3')

# Установка уровня громкости (значение от 0.0 до 1.0)
pygame.mixer.music.set_volume(0)
pygame.mixer.music.play(-1)  # Параметр -1 указывает на циклическое воспроизведение
canvas_width = 900
canvas_height = 600

snake_body = []
direction = "Right"  # Начальное направление вправо
apple = None
snake_space = 10
flag = True
start_length = 2
snake_speed = 80
game_after = None
task = None
count = 0
max_score = load_highscore()
score = 0
score_text = None
hard_game_mode_mass = []
hard_game_mode_flag = False
generate_flag = False


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
    global snake_body, canvas,apple,flag,direction,start_length, generate_flag, hard_game_mode_mass

    snake_speed = 80
    generate_flag = False
    if len(hard_game_mode_mass)>0:
        for el in hard_game_mode_mass:
            canvas.delete(el)



    hard_game_mode_mass.clear()

    for segment in snake_body:
        canvas.delete(segment)

    snake_body.clear()
    head_x1, head_y1, head_x2, head_y2 = 20, 20, 30, 30
    for i in range(start_length):
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
         start_length, snake_speed, game_after, apple_image_to_game,\
        task, score, max_score, score_text, hard_game_mode_flag, generate_flag, canvas_width,canvas_height



    if hard_game_mode_flag == True and generate_flag == False:
        for i in range(20):
            x = random.randint(0, canvas_width)
            y = random.randint(0, canvas_height)
            length = random.randint(10, 30)
            raindrop = canvas.create_rectangle(x, y, x + length, y + length, fill="grey")

            hard_game_mode_mass.append((raindrop, length))
        generate_flag = True


    if flag:
        x = round(random.randint(0, 590) / 10) * 10
        y = round(random.randint(0, 590) / 10) * 10
        # apple = canvas.create_rectangle(x, y, x + 10, y + 10,fill="red")
        apple = canvas.create_image(x, y, image=apple_image_to_game)
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

    if hard_game_mode_flag == True:

        for raindrop, lena in hard_game_mode_mass:
            speed = lena / 11
            canvas.move(raindrop, 0, 10)
            x1, y1, x2, y2 = canvas.coords(raindrop)
            if y2 > canvas_height:
                canvas.coords(raindrop, x1, -20, x2, -20 + lena)









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

    if hard_game_mode_flag: # Проверка на столкновение с камнем
        for segment in snake_body:
            segment_coords = canvas.coords(segment)

            for raindrop, length in hard_game_mode_mass:
                square_coords = canvas.coords(raindrop)


                if (square_coords[0] <= segment_coords[0] <= square_coords[2] and
                        square_coords[1] <= segment_coords[1] <= square_coords[3]):
                    root.after_cancel(task)
                    game_over()



canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()



##################################### ФОТО PLAY ####################################################
play_image = Image.open("start-button-1.png")
play_image_act = Image.open("start-button-10.png")
play_new_width = 230
play_new_height = 86
play_image = play_image.resize((play_new_width, play_new_height))
play_image_to_game = ImageTk.PhotoImage(play_image)
play_image_act = play_image_act.resize((play_new_width, play_new_height))
play_image_act_to_game = ImageTk.PhotoImage(play_image_act)
##################################### ФОТО EXIT ####################################################
exit_image = Image.open("exit-button-1.png")
exit_image_act = Image.open("exit-button-10.png")
exit_new_width = 230
exit_new_height = 86
exit_image = exit_image.resize((exit_new_width, exit_new_height))
exit_image_to_game = ImageTk.PhotoImage(exit_image)
exit_image_act = exit_image_act.resize((exit_new_width, exit_new_height))
exit_image_act_to_game = ImageTk.PhotoImage(exit_image_act)
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
apple_new_width = 50
apple_new_height = 25
apple_image = apple_image.resize((apple_new_width, apple_new_height))
apple_image_to_game = ImageTk.PhotoImage(apple_image)
##################################### ФОТО GAME OVER ####################################################
game_over_image = Image.open("game_over.png")
game_over_new_width = 200
game_over_new_height = 75
game_over_image = game_over_image.resize((game_over_new_width, game_over_new_height))
game_over_image_to_game = ImageTk.PhotoImage(game_over_image)
##################################### ФОТО GAME OVER NEW GAME ####################################################
new_game_image = Image.open("restart-button-1.png")
new_game_new_width = 200
new_game_new_height = 57
new_game_image = new_game_image.resize((new_game_new_width, new_game_new_height))
new_game_image_to_game = ImageTk.PhotoImage(new_game_image)
##################################### ФОТО GAME OVER MENU ####################################################
menu_image = Image.open("menu-button-1.png")
menu_new_width = 200
menu_new_height = 57
menu_image = menu_image.resize((menu_new_width, menu_new_height))
menu_image_to_game = ImageTk.PhotoImage(menu_image)
##################################### ФОТО HARD GAME MODE ####################################################
hard_game_mode_image = Image.open("icons8-череп-1000.png")
hard_game_mode_new_width = 50
hard_game_mode_new_height = 58
hard_game_mode_image = hard_game_mode_image.resize((hard_game_mode_new_width, hard_game_mode_new_height))
hard_game_mode_image_to_game = ImageTk.PhotoImage(hard_game_mode_image)
##################################### ФОТО CANCEL HARD GAME MODE ####################################################
cancel_hard_game_mode_image = Image.open("cancel_hard_game.png")
cancel_hard_game_mode_new_width = 50
cancel_hard_game_mode_new_height = 50
cancel_hard_game_mode_image = cancel_hard_game_mode_image.resize((cancel_hard_game_mode_new_width, cancel_hard_game_mode_new_height))
cancel_hard_game_mode_image_to_game = ImageTk.PhotoImage(cancel_hard_game_mode_image)


count = 0
anim = None
def game_over():
    """Обработчик завершения игры и отображения экрана "Game Over"."""
    global game_over_image_to_game, new_game_image_to_game, menu_image_to_game,game_after
    game_over_sound.play()


    game_ov = canvas.create_image(canvas_width/2, canvas_height/2-100, image=game_over_image_to_game)
    game_ov_new_game = canvas.create_image(canvas_width/2, canvas_height/2, image=new_game_image_to_game)
    game_ov_menu = canvas.create_image(canvas_width/2, canvas_height/2+100, image=menu_image_to_game)

    canvas.tag_bind(game_ov_new_game, "<Button-1>", to_game)
    canvas.tag_bind(game_ov_menu, "<Button-1>", start_menu)
    snake_speed = 0


def start_menu(event):
    """
        Запуск главного меню игры.

        Args:
            event: Событие клавиши.
            """
    global play_image_to_game, background_menu_image_photo, exit_image_to_game,\
        canvas,max_score,score, hard_game_mode_image_to_game, cancel_hard_game_mode_image_to_game, hard_game_mode_flag, hard_game_mode_button

    game_over_sound.stop()
    canvas.destroy()
    canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, background="white")
    background = canvas.create_image(0, 0, anchor=tk.NW, image=background_menu_photo)
    canvas.create_text(canvas_width-120, 20, text=f"MAX SCORE:{max_score}", fill="red", font=("Arial", 20))
    canvas.create_text(canvas_width-95, 50, text=f"SCORE:{score}", fill="red", font=("Arial", 20))
    canvas.pack()
    play_button = canvas.create_image(canvas_width/2, canvas_height/2-20, image=play_image_to_game, activeimage=play_image_act_to_game)
    exit_button = canvas.create_image(canvas_width/2, canvas_height/2+100, image=exit_image_to_game, activeimage=exit_image_act_to_game)
    hard_game_mode_button = canvas.create_image(canvas_width-50, canvas_height-50, image=hard_game_mode_image_to_game)

    if hard_game_mode_flag:
        canvas.itemconfig(hard_game_mode_button, image=cancel_hard_game_mode_image_to_game)
    else:
        canvas.itemconfig(hard_game_mode_button, image=hard_game_mode_image_to_game)


    canvas.tag_bind(play_button, "<Button-1>", to_game)
    canvas.tag_bind(exit_button, "<Button-1>", exit_game)
    canvas.tag_bind(hard_game_mode_button, "<Button-1>", hard_mode_edit)


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
    score_text = canvas.create_text(canvas_width-95, 20, text=f"SCORE:{score}", fill="red", font=("Arial", 20))
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


def hard_mode_edit(event):
    global hard_game_mode_flag, hard_game_mode_button

    hard_game_mode_flag = not hard_game_mode_flag

    if hard_game_mode_flag:  # Если флаг установлен в True, меняем изображение на cancel_hard_game_mode_image_to_game
        canvas.itemconfig(hard_game_mode_button, image=cancel_hard_game_mode_image_to_game)
        hard_game_sound.play()
    else:  # Если флаг установлен в False, меняем изображение на hard_game_mode_image_to_game
        canvas.itemconfig(hard_game_mode_button, image=hard_game_mode_image_to_game)





start_menu(1)
root.mainloop()