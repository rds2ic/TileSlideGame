import pygame
from random import randint
from PIL import Image
import tkinter as tk
from tkinter.simpledialog import askstring

# Initiating pygame
pygame.init()
WIDTH = HEIGHT = 900
FPS = 240
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Class that holds grid of individual slots


class TileGrid:
    def __init__(self, rows: int, image_path):
        self.rows = rows
        self.image_path = image_path
        nums = [n for n in range(self.rows * self.rows)]
        num_len = len(nums)
        self.num_len = num_len
        self.refresh()

    def __len__(self):
        return self.num_len

    def make_image_list(self):
        # makes the list of images to assign to tiles
        images = []
        image = Image.open(self.image_path)
        self.image = pygame.image.fromstring(image.resize(
            (WIDTH, WIDTH)).tobytes(), image.resize((WIDTH, WIDTH)).size, "RGB")  # type: ignore
        for i in range(self.rows*self.rows-1):
            # left, upper, right, lower
            new_image = image.resize((WIDTH, WIDTH)).crop(
                ((i % self.rows)*WIDTH//self.rows, (i//self.rows)*WIDTH//self.rows, ((i % self.rows)*WIDTH//self.rows)+WIDTH//self.rows, ((i//self.rows)
                                                                                                                                          * WIDTH//self.rows)+WIDTH//self.rows))
            image_data = new_image.tobytes()
            image_dimensions = new_image.size
            IMG = pygame.image.fromstring(
                image_data, image_dimensions, "RGB")  # type: ignore
            images.append(IMG)
        return images

    def show_image(self, s):
        # function to show the original image when a key is pressed
        s.blit(self.image, (0, 0))
        # type: ignore
        pygame.draw.rect(s, (0, 0, 0), (WIDTH-WIDTH//self.rows, WIDTH -
                                        WIDTH//self.rows, WIDTH//self.rows, WIDTH//self.rows))
        pygame.display.update()

    def return_values(self):
        # returns an array of the values of each tile
        self.arr_values = [[] for _ in range(self.rows)]
        for i, v in enumerate(self.arr):
            for j in v:
                self.arr_values[i].append(j.return_value()[0])
        return self.arr_values

    def swap(self, i1: int, j1: int):
        # swaps two tiles and updates the position of the empty tile
        i2, j2 = self.empty_pos
        v1 = self.arr[i1][j1].return_value()[0]
        v2 = self.arr[i2][j2].return_value()[0]
        self.empty_pos = (i1, j1)
        self.arr[i1][j1].update_val(v2)
        self.arr[i2][j2].update_val(v1)

    def get_neighbours(self, i: int, j: int):
        # creates a list which contains all the neighbouring tiles
        neighbours = []
        if i == 0:
            neighbours.append(self.arr[i+1][j])
        elif i == self.rows - 1:
            neighbours.append(self.arr[i-1][j])
        else:
            neighbours.append(self.arr[i+1][j])
            neighbours.append(self.arr[i-1][j])
        if j == 0:
            neighbours.append(self.arr[i][j+1])
        elif j == self.rows - 1:
            neighbours.append(self.arr[i][j-1])
        else:
            neighbours.append(self.arr[i][j+1])
            neighbours.append(self.arr[i][j-1])
        return neighbours

    def refresh(self, rows=-1):
        # randomises the puzzle with an option to change the number of rows
        if rows != -1:
            self.rows = rows
        # Setting up the grid by making two 2D arrays
        # self.arr stores the tile objects
        # self.arr_values stores the tile position value in relation to which part of the image it is
        nums = [n for n in range(self.rows * self.rows)]
        num_len = len(nums)
        self.num_len = num_len
        self.arr = [[] for _ in range(self.rows)]
        self.arr_values = [[] for _ in range(self.rows)]
        self.images = self.make_image_list()
        for i in range(num_len):
            # picking a random number to index from the image list
            rand = randint(0, num_len-1-i)
            self.arr[i//self.rows].append(Tile(nums[rand], (i % self.rows)*WIDTH//self.rows,
                                               (i // self.rows)*WIDTH//self.rows, self.rows, self.images))
            self.arr_values[i//self.rows].append(nums[rand])
            # storing the position of the empty tile
            if nums[rand] == (self.rows*self.rows)-1:
                self.empty_pos = (i//self.rows, i % self.rows)
            nums.pop(rand)

    def draw(self, s):
        # loops through all the tiles and calls each of their draw functions
        for i in self.arr:
            for j in i:
                j.draw(s)

    def check_game_over(self):
        # checks if each tiles value is greater than the one before it and if so the game is over
        holder = -1
        for i, v in enumerate(self.return_values()):
            for j, b in enumerate(v):
                if b > holder:
                    holder = b
                else:
                    return False
        return True

# class of the individual tile


class Tile:
    def __init__(self, val: int, x: int, y: int, rows: int, images):
        # val stores the positional value of the tile
        self.val = val
        self.x, self.y = x, y
        self.rows = rows
        self.images = images
        if self.val != (self.rows*self.rows)-1:
            self.image = self.images[self.val]
        self.rect = pygame.Rect(self.x, self.y, WIDTH //
                                self.rows, WIDTH//self.rows)
        self.colour = (0, 0, 0)

    def update_val(self, val: int):
        # updates the positional value of the tile and the pygame rect that is drawn
        self.val = val
        self.rect = pygame.Rect(self.x, self.y, WIDTH //
                                self.rows, WIDTH//self.rows)
        try:
            self.image = self.images[self.val]
        except:
            pass
        self.colour = (0, 0, 0)

    def __str__(self):
        return str(self.val)

    def return_value(self):
        return self.val, self.x, self.y

    def draw(self, s):
        # checks if the value corresponds to the empty tile
        if self.val != (self.rows*self.rows)-1:
            s.blit(self.image, (self.x, self.y))
        else:
            pygame.draw.rect(s, self.colour, self.rect)


def update_display(s, t, rows):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    s.fill((255, 255, 255))
    # drawing all the tiles
    t.draw(s)
    # drawing grid lines
    for i in range(1, rows):
        pygame.draw.line(s, (128, 128, 128), (i * WIDTH //
                                              rows, 0), (i * WIDTH//rows, WIDTH))
        pygame.draw.line(s, (128, 128, 128), (0, i * WIDTH //
                                              rows), (WIDTH, i * WIDTH//rows))
    clock.tick(FPS)
    pygame.display.update()


def main():
    running = True
    rows = 3
    # the image used can be changed here
    t = TileGrid(rows, 'rf.jpg')
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # checks if the close button is pressed
                running = False
                pygame.quit()
            if pygame.mouse.get_pressed()[0]:
                # calculates position of tile clicked
                # x and y are the pixel coordinates of the mouse
                x, y = pygame.mouse.get_pos()
                # i and j are the array positions of the tile clicked
                j = x // (WIDTH//rows)
                i = y // (WIDTH//rows)
                n = t.get_neighbours(i, j)
                for _, v in enumerate(n):
                    # checks if the empty tile is a neighbour of the pressed tile and if so switch them
                    if v.return_value()[0] == len(t)-1:
                        t.swap(i, j)
                if t.check_game_over():
                    print('Game Over')
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    t.refresh(rows)
                if event.key == pygame.K_r:
                    # brings up box to input change for amount of rows
                    root = tk.Tk()

                    new_rows = tk.StringVar()
                    new_rows.set(str(rows))

                    canvas1 = tk.Canvas(
                        root, width=400, height=300, relief='raised')
                    canvas1.pack()

                    label1 = tk.Label(
                        root, text='Enter the amount of rows you would like:')
                    label1.config(font=('helvetica', 14))
                    canvas1.create_window(200, 25, window=label1)

                    label2 = tk.Label(root, text='Type your Number:')
                    label2.config(font=('helvetica', 10))
                    canvas1.create_window(200, 100, window=label2)

                    entry1 = tk.Entry(root)
                    canvas1.create_window(200, 140, window=entry1)

                    def get_rows():
                        new_rows.set(entry1.get())
                        root.destroy()

                    button1 = tk.Button(text='Enter', command=get_rows,
                                        bg='brown', fg='white', font=('helvetica', 9, 'bold'))
                    canvas1.create_window(200, 180, window=button1)

                    root.mainloop()
                    rows = int(new_rows.get())
                    t.refresh(rows)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            # checks while the up arrow is held down to show the original image
            t.show_image(screen)
        else:
            update_display(screen, t, rows)


main()
