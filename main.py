from tkinter import *
import copy
import random
random.seed()

# TO DO
# 1. Store rectangle ids in a matrix and only draw color changed tiles
# 2. Only calculate tile creation in neighbors of stored elligible tiles

width, height = 960, 540
speed = 500
rate = 1000 / speed
size = 50
object_list = ("tree", "city")
selected_object = object_list[1]
tile_list = []
outline_tiles = False
running = True

if width < height:
    square_size = (width - 10) / size
else:
    square_size = (height - 10) / size
font = ('Helvetica', str(round(square_size / 3)), 'bold')
offset = (square_size * size) / 2
left_bound = (width / 2) - offset
right_bound = (width / 2) + offset
top_bound = (height / 2) - offset
bottom_bound = (height / 2) + offset
if selected_object == "tree":
    tile_list = ["Empty", "Grass", "Vertical Wood", "Horizontal Wood", "Leaf Wood", "Inner Bark", "Outer Bark", "Inner Leaf", "Outer Leaf"]
    tile_colors = ('black', 'green', '#964f03', '#964f03', '#964f03', '#753d01', '#522b01', '#075209', '#012e07')
    u_rules = [(0,), (2,)*1, (2,)*90+(3,)*5+(4,)*8+(5,)*2, (0,)*8+(2,)*2+(5,)*8+(7,)*2, (7,)*1, (0,)*15+(5,)*1+(6,)*4, (-1,)*1, (0,)*1+(7,)*3+(8,)*5, (-1,)*1]
    d_rules = [(0,), (-1,)*1, (2,)*20+(3,)*5+(4,)*65+(5,)*10, (0,)*8+(2,)*2+(5,)*8+(7,)*2, (6,)*1, (0,)*15+(5,)*1+(6,)*4, (-1,)*1, (0,)*1+(7,)*3+(8,)*5, (-1,)*1]
    l_rules = [(0,), (2,)*1, (0,)*8+(3,)*2+(5,)*8+(7,)*2, (2,)*1+(3,)*6+(4,)*3, (7,)*1, (0,)*16+(5,)*1+(6,)*3, (-1,)*1, (0,)*1+(7,)*3+(8,)*5, (-1,)*1]
    r_rules = [(0,), (2,)*1, (0,)*8+(3,)*2+(5,)*8+(7,)*2, (2,)*1+(3,)*6+(4,)*3, (7,)*1, (0,)*16+(5,)*1+(6,)*3, (-1,)*1, (0,)*1+(7,)*3+(8,)*5, (-1,)*1]
elif selected_object == "city":
    tile_list = ["Empty", "Vertical 2-Way Straight", "Horizontal 2-Way Straight", "2-Way Cross Intersection", "Office", "Store", "Land"]
    tile_colors = ('black', 'blue', 'red', 'green', 'purple', "yellow", 'black')
    #tile_colors = ('black', '#2e2e2e', '#2e2e2e', '#2e2e2e', 'purple', "yellow", 'black')
    u_rules = [(0,), (1,)*7+(3,)*2+(6,)*1, (6,)*7+(4,)*2+(5,)*1, (1,)*1, (-1,), (-1,), (-1,)]
    d_rules = [(0,), (1,)*7+(3,)*2+(6,)*1, (6,)*7+(4,)*2+(5,)*1, (1,)*1, (-1,), (-1,), (-1,)]
    l_rules = [(0,), (6,)*7+(4,)*2+(5,)*1, (2,)*7+(3,)*2+(6,)*1, (2,)*1, (-1,), (-1,), (-1,)]
    r_rules = [(0,), (6,)*7+(4,)*2+(5,)*1, (2,)*7+(3,)*2+(6,)*1, (2,)*1, (-1,), (-1,), (-1,)]
highest_tile_value = len(tile_list)


def draw_tiles(canvas, field):
    canvas.delete('all')
    for y in range(size):
        y_pos = top_bound + (square_size * y)
        for x in range(size):
            x_pos = left_bound + (square_size * x)
            value = field[x][y]
            color = tile_colors[value]
            if outline_tiles:
                outline = 'black'
            else:
                outline = color
            canvas.create_rectangle(x_pos, y_pos, x_pos + square_size, y_pos + square_size, fill=color, outline=outline)


def check_empty_neighbors(field, x, y):
    empty_neighbor_list = []
    if x > 0:
        if field[x-1][y] == 0:
            empty_neighbor_list.append((2, x-1, y))
    if y > 0:
        if field[x][y-1] == 0:
            empty_neighbor_list.append((0, x, y-1))
    if x < (size - 1):
        if field[x+1][y] == 0:
            empty_neighbor_list.append((3, x+1, y))
    if y < (size - 1):
        if field[x][y+1] == 0:
            empty_neighbor_list.append((1, x, y+1))
    return empty_neighbor_list


def check_neighbors(field, x, y):
    neighbor_list = []
    if x > 0:
        neighbor_list.append(field[x-1][y])
    if y > 0:
        neighbor_list.append(field[x][y-1])
    if x < (size - 1):
        neighbor_list.append(field[x+1][y])
    if y < (size - 1):
        neighbor_list.append(field[x][y+1])
    return neighbor_list


def calculate_rules(field):
    global running
    finished = True
    new_field = copy.deepcopy(field)
    for y in range(size):
        for x in range(size):
            tile_value = field[x][y]
            if not tile_value == 0:
                if not tile_value > highest_tile_value:
                    empty_neighbor_list = check_empty_neighbors(field, x, y)
                    for n in empty_neighbor_list:
                        if n[0] == 0:
                            current_rules = u_rules
                        elif n[0] == 1:
                            current_rules = d_rules
                        elif n[0] == 2:
                            current_rules = l_rules
                        else:
                            current_rules = r_rules
                        if not current_rules[tile_value][0] == -1:
                            highest_rule = len(current_rules[tile_value]) - 1
                            finished = False
                            choice = random.randint(0, highest_rule)
                            new_field[n[1]][n[2]] = current_rules[tile_value][choice]
    if finished:
        running = False
    return new_field


def update(canvas, field):
    global running
    field = calculate_rules(field)
    draw_tiles(canvas, field)
    if running:
        canvas.master.after(round(rate), update, canvas, field)
    else:
        draw_tiles(canvas, field)
        counter = 0
        for y in range(size):
            for x in range(size):
                if not field[x][y] == 0:
                    counter += 1
        if counter < size*size/5:
            running = True
            setup(canvas)
        else:
            draw_tiles(canvas, field)


def setup(canvas):
    empty_line = [0]*size
    field = []
    for i in range(size):
        field.append(empty_line.copy())
    draw_tiles(canvas, field)
    if selected_object == "tree":
        field[round(size/2)][size-1] = 1
    elif selected_object == "city":
        mode = random.randint(0, 1)
        if mode == 0:
            x = random.randint(0, 1) * (size - 1)
            y = random.randint(0, size - 1)
        else:
            x = random.randint(0, size - 1)
            y = random.randint(0, 1) * (size - 1)
        o = random.randint(1, 3)
        field[x][y] = o
    draw_tiles(canvas, field)
    canvas.master.after(round(rate), update, canvas, field)


def main():
    root = Tk()
    window = Canvas(root, width=width, height=height)
    screen_width, screen_height = root.winfo_screenwidth(), root.winfo_screenheight()
    win_x = int(screen_width / 2 - width / 2)
    win_y = int(screen_height / 2 - height / 2)
    root.geometry(str(width) + "x" + str(height) + "+" + str(win_x) + "+" + str(win_y))
    window.configure(background='#a1a1a1')
    root.title("Wave Collapse")
    window.pack()

    root.after(round(rate), setup, window)
    root.mainloop()


if __name__ == '__main__':
    main()
