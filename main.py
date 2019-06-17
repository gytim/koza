from tkinter import *
import random
import time
import config as cfg

# КОЗА [x, y, направлениеX, направлениеY, name, color]
# КУСТ [x, y, color]

# СКРИПТ
global END_GAME
END_GAME = False


# Генерируем и размещаем коз на поле
def fill_goat():
    # print("Размещаем коз")
    global goats
    goats = []

    for i in range(cfg.GOATS_COUNT):
        new_goat = [random.randint(0, cfg.GRID_SIZE - 1), random.randint(0, cfg.GRID_SIZE - 1), 1, 1, i,
                    "#FFFFFF"]
        c.itemconfig(area[new_goat[0]][new_goat[1]], fill=new_goat[5])
        ch_goat(new_goat)
        goats.append(new_goat)


# Генерируем и сажаем кусты на поле
def fill_tree():
    # print("Сажаем кусты")
    global trees
    trees = []

    for i in range(cfg.TREES_COUNT):
        new_tree = [random.randint(0, cfg.GRID_SIZE - 1), random.randint(0, cfg.GRID_SIZE - 1),
                    "#%06x" % random.randint(0, 0xFFFFFF)]

        # Одно дерево в одной клетке
        one_tree = True
        for tree in trees:
            if tree[0] == new_tree[0] and tree[1] == new_tree[1]:
                one_tree = False
                break

        if one_tree:
            trees.append(new_tree)
            c.itemconfig(area[new_tree[0]][new_tree[1]], fill=new_tree[2])


# Проверяем шанс ветра и сдвигаем козу
def next_step(goat, s_axis):
    # Проверяем наличие ветра
    is_chance = False
    if cfg.WIND_CHANCE_PERC != 0:
        int_change = round(100 / cfg.WIND_CHANCE_PERC)
        if int_change == random.randint(0, int_change):
            is_chance = True

    if is_chance:
        # print("Дует ветер")
        step = cfg.WIND_SPEED
    else:
        step = random.randint(0, cfg.GOAT_SPEED)

    # Проверка выхода за пределы поля
    next_coodinate = goat[cfg.AXIS[s_axis][0]] + step * goat[cfg.AXIS[s_axis][1]]
    if next_coodinate >= cfg.GRID_SIZE - 1:
        goat[cfg.AXIS[s_axis][0]] = (cfg.GRID_SIZE - 1) * 2 - next_coodinate
        goat[cfg.AXIS[s_axis][1]] = (-1) * goat[cfg.AXIS[s_axis][1]]
    elif next_coodinate <= 0:
        goat[cfg.AXIS[s_axis][0]] = (-1) * next_coodinate
        goat[cfg.AXIS[s_axis][1]] = (-1) * goat[cfg.AXIS[s_axis][1]]
    else:
        goat[cfg.AXIS[s_axis][0]] = next_coodinate


# сдвиг по Х
def run_X():
    global END_GAME

    if END_GAME:
        return

    for goat in goats:
        c.itemconfig(area[goat[0]][goat[1]], fill="gray")

        next_step(goat, "X")
        ch_goat(goat)

        c.itemconfig(area[goat[0]][goat[1]], fill=goat[5])

    root.after(cfg.TIME_S, run_Y)


# сдвиг по Y
def run_Y():
    global END_GAME

    if END_GAME:
        return

    for goat in goats:
        c.itemconfig(area[goat[0]][goat[1]], fill="gray")

        next_step(goat, "Y")
        ch_goat(goat)

        c.itemconfig(area[goat[0]][goat[1]], fill=goat[5])

    root.after(cfg.TIME_S, run_X)


# Проверка на попадение коз
def ch_goat(goat):
    global END_GAME

    for tree in trees:
        if tree[0] == goat[0] and tree[1] == goat[1]:
            # print("Коза " + str(goat[4]) + " сожрала куст "
            #                         + "в координатах [" + str(tree[0]) + "," + str(tree[1]) + "]")

            goat[5] = tree[2]

            trees.remove(tree)

            if len(trees) == 0:
                msg = Message(root, text="Коза апокалипсиса No." + str(goat[4]) + " под флагом цвета " + goat[5])
                msg.config(bg=tree[2])
                msg.pack()
                END_GAME = True

                # print("END_GAME")
                return


# Заполняем форму квадратами, генерим все остальное
def init():
    global c
    c = Canvas(root, width=cfg.GRID_SIZE * cfg.SQUARE_SIZE,
                     height=cfg.GRID_SIZE * cfg.SQUARE_SIZE)
    c.pack()
    global area
    area = []
    for i in range(cfg.GRID_SIZE):
        b = []
        for j in range(cfg.GRID_SIZE):
            b.append(c.create_rectangle(i * cfg.SQUARE_SIZE, j * cfg.SQUARE_SIZE,
                                        i * cfg.SQUARE_SIZE + cfg.SQUARE_SIZE,
                                        j * cfg.SQUARE_SIZE + cfg.SQUARE_SIZE, fill='gray'))
        area.append(b)

    msg = Message(root, text="Коз " + str(cfg.GOATS_COUNT)
                             + " \nКустов " + str(cfg.TREES_COUNT)
                             + " \nРазмер " + str(cfg.GRID_SIZE) + "х" + str(cfg.GRID_SIZE))
    msg.pack()

    fill_tree()
    fill_goat()

# Начинаем движение коз
def main():
    # print("START_GAME")
    root.after(cfg.TIME_S, run_X)
    root.mainloop()


if __name__ == "__main__":
    root = Tk()
    root.title("KoZa")

    init()
    main()
