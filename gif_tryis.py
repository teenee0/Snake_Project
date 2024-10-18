import tkinter as tk
from PIL import Image, ImageTk, ImageSequence

def update_image(item):
    global num_frames
    canvas.itemconfig(item, image=frames[num_frames])  # Обновляем изображение на холсте
    num_frames = (num_frames + 1) % len(frames)  # Переходим к следующему кадру
    root.after(speed, update_image, item)  # Запускаем обновление с заданной скоростью

root = tk.Tk()
canvas = tk.Canvas(root, width=600, height=600)
canvas.pack()

gif = Image.open("duck.gif")
frames = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(gif)]
num_frames = 0
speed = 50

# Создаем изображение на холсте
itemm = canvas.create_image(300, 300, image=frames[0])

# Запускаем обновление изображения
update_image(itemm)





def move_snake(event):
    """
        Обрабатывает события нажатия клавиш для изменения направления движения змейки.

        Args:
            event: Событие клавиши.
        """
    print(event.keysym)

    if event.keysym == "Up" :
        canvas.move(itemm, 0,-40)
    elif event.keysym == "Down" :
        canvas.move(itemm, 0,40)
    elif event.keysym == "Right" :
        canvas.move(itemm, 40,0)
    elif event.keysym == "Left" :
        canvas.move(itemm, -40,0)

canvas.bind_all("<KeyPress-Up>", move_snake)
canvas.bind_all("<KeyPress-Down>", move_snake)
canvas.bind_all("<KeyPress-Right>", move_snake)
canvas.bind_all("<KeyPress-Left>", move_snake)
root.mainloop()