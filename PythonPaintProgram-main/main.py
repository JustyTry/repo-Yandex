from utils import *
from PIL import Image, ImageTk
from tkinter.colorchooser import askcolor
import tkinter as tk
import uuid
import os
import cv2
import numpy
import imgcompare


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel cringe")


def init_grid(rows, cols, color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(cols):
            grid[i].append(color)

    return grid


def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i *
                                          PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, BLACK, (0, i * PIXEL_SIZE),
                             (WIDTH, i * PIXEL_SIZE))

        for i in range(COLS + 1):
            pygame.draw.line(win, BLACK, (i * PIXEL_SIZE, 0),
                             (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))


def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)

    for button in buttons:
        button.draw(win)

    pygame.display.update()


def get_row_col_from_pos(pos):
    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError

    return row, col


run = True

grid = init_grid(ROWS, COLS, BG_COLOR)
drawing_color = BLACK

button_y = HEIGHT - TOOLBAR_HEIGHT/2 - 25
buttons = [
    Button(10, button_y, 60, 50, BLACK),
    Button(90, button_y, 60, 50, WHITE, "Цвет", BLACK),
    Button(160, button_y, 60, 50, WHITE, "Ласт.", BLACK),
    Button(230, button_y, 60, 50, WHITE, "Очист.", BLACK),
    Button(300, button_y, 60, 50, WHITE, "Сохр.", BLACK),
    Button(370, button_y, 60, 50, WHITE, "Выбр.", BLACK),
    Button(440, button_y, 60, 50, WHITE, "Срав.", BLACK)

]

while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            try:
                row, col = get_row_col_from_pos(pos)
                grid[row][col] = drawing_color
            except IndexError:
                for button in buttons:

                    if not button.clicked(pos):
                        continue

                    if button.text == "Очист.":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        drawing_color = BLACK
                    if button.text == "Сохр.":
                        rect = pygame.Rect(
                            0, 0, WIDTH, HEIGHT - TOOLBAR_HEIGHT)
                        sub = window.subsurface(rect)
                        unique_filename = str(uuid.uuid4())
                        pygame.image.save(
                            sub, f"./images/{unique_filename}.png")

                    if button.text == "Цвет":
                        root = tk.Tk()
                        try:
                            colors = askcolor(title="Tkinter Color Picker")
                            drawing_color = colors[0]
                            root.mainloop()
                        except:
                            drawing_color = BLACK

                    if button.text == "Выбр.":
                        root = tk.Tk()

                        def smc(name):
                            global link

                            link = f"./images/{name}"
                            print(name, link)
                            image_ = Image.open(link)
                            pic = ImageTk.PhotoImage(image_)
                            img_label = tk.Label(root, image=pic)
                            img_label.pack(side=tk.RIGHT)

                            root.mainloop()
                        try:
                            for (root_, dirs, files) in os.walk("./images"):
                                if files:
                                    for file_ in files:
                                        path = os.path.join("./images", file_)
                                        image_ = Image.open(path)
                                        n_image = image_.resize((100, 100))
                                        pic = ImageTk.PhotoImage(n_image)
                                        img_label = tk.Label(root, image=pic)

                                        Button = tk.Button(command=lambda arg=file_: smc(
                                            arg), text="Submit", image=pic, height=100, width=100, relief='flat')
                                        Button.pack(side=tk.LEFT)
                                        img_label.pic = pic

                            root.mainloop()
                        except:
                            continue

                    if button.text == "Срав.":
                        root = tk.Tk()

                        rect = pygame.Rect(
                            0, 0, WIDTH, HEIGHT - TOOLBAR_HEIGHT)
                        sub = window.subsurface(rect)
                        pygame.image.save(
                            sub, f"image.png")

                        percentage = imgcompare.image_diff_percent(
                            "./images/2f859010-eea1-4f00-bc38-c8ec56b39c6e.png", "./image.png")
                        print(percentage)
                        if percentage < 25:

                            label = tk.Label(root, text='Похожи')
                            label.pack()

                        else:
                            label = tk.Label(root, text='Не похожи')
                            label.pack()

                        def destroyer():
                            root.destroy()
                        tk.Button(root, text="Quit",
                                  command=lambda: destroyer()).pack()

                        root.mainloop()

    draw(window, grid, buttons)


pygame.quit()
