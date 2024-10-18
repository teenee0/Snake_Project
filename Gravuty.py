import tkinter as tk
import random

root = tk.Tk()
canvas_width = 600
canvas_height = 600

canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, background="black")
canvas.pack()

mass_of_balls = []

def create_ball():
    x = random.randint(0, 500)
    y = random.randint(0, 300)
    speed = 0.1
    speed1 = 0
    ball = canvas.create_oval(x, y, x + 30, y + 30, fill="white")
    mass_of_balls.append([ball, speed,speed1])
count_of_balls = 12
for i in range(count_of_balls):
    create_ball()

gravity = 0.8
prev_speed = [0.0 for _ in range(len(mass_of_balls))]
count = 0
def animate_gravity():
    global count

    for i in range(len(mass_of_balls)):
        x1, y1, x2, y2 = canvas.coords(mass_of_balls[i][0])



        if mass_of_balls[i][1] > 0:
            mass_of_balls[i][1] += gravity

        if mass_of_balls[i][1] < 0:
            mass_of_balls[i][1] += gravity*2

        if y2 >= canvas_height:

            if abs(mass_of_balls[i][1])>4.5:
                mass_of_balls[i][1] = -mass_of_balls[i][1]
            else:
                mass_of_balls[i][1] = 0

            # if mass_of_balls[i][2] == 0:
            #     mass_of_balls[i][2] = abs(mass_of_balls[i][1])
            #
            # if mass_of_balls[i][2] != 0:
            #     mass_of_balls[i][2] -= mass_of_balls[i][2] * 0.3
            #     print("*****",mass_of_balls[i][2])
            # print(speed)



            # Если шар находится на нижней границе, обнуляем его скорость
            # if y2 >= canvas_height:
            #     mass_of_balls[i][1] = 0

        ball, speed, speed2 = mass_of_balls[i]
        prev_speed[i] = speed
        print(speed)
        # f speed2 == 0 or speed2 > 1:i
        canvas.move(ball, 0, speed)

    # Проверяем, остановились ли все шары (скорость меньше определенной величины)
    # all_stopped = all(abs(speed) < 0.1 for _, speed in mass_of_balls)
    #
    # if all_stopped:
    #     return  # Останавливаем анимацию
    # print(speed, y2)
    root.after(30, animate_gravity)

animate_gravity()

root.mainloop()
