import tkinter as tk
import random

root = tk.Tk()
canvas_width = 600
canvas_height = 600

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, background="black")
canvas.pack()

mass_of_balls = []
mass_of_balls2 = []
initial_coords = {}

def create_ball():
    """Создает мячи на холсте и сохраняет их идентификаторы и начальные координаты."""
    x = random.randint(0, 500)
    y = random.randint(0, 300)
    speed = 0.1
    speed1 = 0
    ball_id = canvas.create_oval(x, y, x + 30, y + 30, fill="white")
    mass_of_balls.append([ball_id, speed, speed1])
    mass_of_balls2.append(ball_id)
    x1, y1, x2, y2 = canvas.coords(ball_id)
    initial_coords[ball_id] = (x1, y1, x2, y2)
    return ball_id

count_of_balls = 12
for i in range(count_of_balls):
    ball_id = create_ball()

def on_click(event):
    """Обработчик события щелчка мыши для начала перетаскивания мяча."""
    x, y = event.x, event.y
    for ball_id in mass_of_balls2:
        x0, y0, x1, y1 = initial_coords[ball_id]
        if x0 < x < x1 and y0 < y < y1:
            canvas.tag_bind(ball_id, "<B1-Motion>", lambda e, id=ball_id: on_drag(e, id))
            canvas.tag_unbind(ball_id, "<Button-1")

def on_drag(event, ball_id):
    """Обработчик события перетаскивания мяча мышью."""
    x0, y0, x1, y1 = initial_coords[ball_id]
    dx, dy = event.x - x0, event.y - y0
    x0, y0, x1, y1 = x0 + dx, y0 + dy, x1 + dx, y1 + dy
    canvas.coords(ball_id, x0, y0, x1, y1)
    initial_coords[ball_id] = (x0, y0, x1, y1)


gravity = 0.8


def animate_gravity():
    """Функция, имитирующая гравитацию для мячей на холсте."""
    global count
    for i in range(len(mass_of_balls)):

        x1, y1, x2, y2 = canvas.coords(mass_of_balls[i][0])

        initial_coords[mass_of_balls[i][0]] = (x1, y1, x2, y2)

        # print(initial_coords)

        if mass_of_balls[i][1] > 0:
            mass_of_balls[i][1] += gravity
            # mass_of_balls[i][1] = gravity

        if mass_of_balls[i][1] < 0:
            mass_of_balls[i][1] += gravity * 2
            # mass_of_balls[i][1] += gravity

        if y2 >= canvas_height:
            if abs(mass_of_balls[i][1]) > 4.5:
                mass_of_balls[i][1] = -mass_of_balls[i][1]
            else:
                mass_of_balls[i][1] = 0
        if y2 < canvas_height - canvas_height*0.01 and mass_of_balls[i][1] == 0:
            mass_of_balls[i][1] = 1

        ball, speed, speed2 = mass_of_balls[i]

        canvas.move(ball, 0, speed)
    root.after(30, animate_gravity)

animate_gravity()
canvas.tag_bind("all", "<Button-1>", on_click)
root.mainloop()
