import tkinter

from Dice import Dice
from Player import Player
from tkinter import *
from PIL import Image, ImageTk
import random


BASE_IMG_PATH = "./Dice Images/"
dice1, dice2 = Dice(6), Dice(6)
GREEN = '#35654d'

def get_players():
    file = open('three_man_players.txt', 'r')
    lines = file.readlines()

    players = []

    for line in lines:
        line = line.rstrip()
        player = Player(line)
        players.append(player)

    return players


PLAYER_LIST = get_players()
current_player = PLAYER_LIST[1]
current_player_number = PLAYER_LIST.index(current_player)
current_three = current_player

def rolled_off():
    global current_player
    global current_three

    if current_player.points >= 5:
        off_chance = random.randint(1, current_player.points)
    else:
        off_chance = random.randint(1, 5)

    if off_chance == 1:
        print(f'{current_player.name} Rolled off the table!')
        if current_player != current_three:
            print(f'{current_player.name} is the new Three Man')
            current_player.toggle_three()
            current_three.toggle_three()
        else:
            print(f'{current_player.name} remains Three Man')
        next_player()
        return True
    else:
        return False


def roll_dice():
    ani_counter = 0
    while ani_counter < 45:
        app.update()
        dice1.roll()
        dice2.roll()
        dice1image = Image.open(f'{BASE_IMG_PATH}{dice1.sides}-{dice1.value}.png').convert('RGBA')
        dice1image = dice1image.resize((108, 144))
        dice1image = ImageTk.PhotoImage(dice1image)
        dice1_space.configure(image=dice1image)
        dice1_space.img = dice1image
        dice2image = Image.open(f'{BASE_IMG_PATH}{dice2.sides}-{dice2.value}.png').convert('RGBA')
        dice2image = dice2image.resize((108, 144))
        dice2image = ImageTk.PhotoImage(dice2image)
        dice2_space.configure(image=dice2image)
        dice2_space.img = dice2image
        ani_counter += 1
    if not rolled_off():
        dice_actions()
    update_player_frame()


def update_player_frame():
    counter = 0
    for player in PLAYER_LIST:
        if player.is_three:
            exec(f'Player{counter}_three.configure(image=three_man_image)')
            exec(f'Player{counter}_three.img = three_man_image')
        else:
            exec(f'Player{counter}_three.configure(image="")')
            exec(f'Player{counter}_three.img = ""')
        if player.is_current:
            exec(f'Player{counter}_three.configure(bg=\'black\')')
            exec(f'Player{counter}_name.configure(bg=\'black\', fg=\'white\')')
            exec(f'Player{counter}_point.configure(bg=\'black\', fg=\'red\')')
        else:
            exec(f'Player{counter}_three.configure(bg=\'gray\')')
            exec(f'Player{counter}_name.configure(bg=\'white\', fg=\'black\')')
            exec(f'Player{counter}_point.configure(bg=\'red\', fg=\'white\')')
        exec(f'Player{counter}_point.configure(text=\'{player.points}\')')
        counter += 1


def social_roll():
    for player in PLAYER_LIST:
        player.sub_points(1)


def three_doubles():
    if current_player.double_count == 3:
        print(f'{current_player.name} has rolled 3 doubles in their turn!')
        print(f'{current_player.name} gains 10 points!')
        current_player.add_points(10)
        current_player.reset_double_count()


def dice_actions():
    dice_total = dice1.value + dice2.value
    global current_player, current_three
    for player in PLAYER_LIST:
        if player.is_current:
            current_player = player
        if player.is_three:
            current_three = player
    player_ahead_number = (PLAYER_LIST.index(current_player) + 1) % len(PLAYER_LIST)
    player_behind_number = (PLAYER_LIST.index(current_player) - 1) % len(PLAYER_LIST)
    player_ahead, player_behind = PLAYER_LIST[player_ahead_number], PLAYER_LIST[player_behind_number]
    if dice1.value == dice2.value:
        if dice_total == 2:
            print(f'{current_player.name} rolled double 1s!')
            current_player.add_double_count(1)
        elif dice_total == 4:
            print(f'{current_player.name} rolled double 2s!')
            current_player.add_double_count(1)
        elif dice_total == 6:
            if current_player.is_three:
                print(f'Three Man{current_player.name} rolled double 3s! - Double Three Man!')
                print(f'{current_player.name} passed Three Man to {player_behind.name}!')
                print(f'{player_behind.name} loses 2 points!')
                current_player.toggle_three()
                player_behind.toggle_three()
                player_behind.sub_points(2)
            else:
                print(f'{current_player.name} rolled double 3s! - Double Three Man!')
                print(f'{current_three.name} loses 2 points!')
                current_three.sub_points(2)
            current_player.add_double_count(1)
        elif dice_total == 8:
            print(f'{current_player.name} rolled double 4s!')
            current_player.add_double_count(1)
        elif dice_total == 10:
            print(f'{current_player.name} rolled double 5s! - Social')
            social_roll()
            current_player.add_double_count(1)
        elif dice_total == 12:
            print(f'{current_player.name} rolled double 6s!')
            current_player.add_double_count(1)

    elif dice_total == 3:
        if current_player.is_three:
            print(f'Three Man {current_player.name} rolled 3, the hard way!')
            print(f'{current_player.name} passed Three Man to {player_behind.name}!')
            print(f'{player_behind.name} loses 2 points!')
            current_player.toggle_three()
            player_behind.toggle_three()
            player_behind.sub_points(2)
        else:
            print(f'{current_player.name} rolled 3, the hard way! - Three Man {current_three.name} loses 2 points!')
            current_three.sub_points(2)
    elif dice_total == 7:
        if dice1.value == 3 or dice2.value == 3:
                if current_player.is_three:
                    print(f'Three Man {current_player.name} rolled a 7, with 1 die being a 3! - '
                          f'Seven Ahead and Three Man')
                    print(f'{current_player.name} passed Three Man to {player_behind.name}!')
                    current_player.toggle_three()
                    player_behind.toggle_three()
                    player_behind.sub_points(1)
                    player_ahead.sub_points(1)
                else:
                    print(f'{current_player.name}, rolled a 7, with 1 die being a 3! - Seven Ahead and Three Man')
                    player_ahead.sub_points(1)
                    current_three.sub_points(1)
        else:
            print(f'{current_player.name}, rolled a 7! - Seven Ahead')
            player_ahead.sub_points(1)
    elif dice_total == 10:
        if dice1.value == 3 or dice2.value == 3:
            if current_player.is_three:
                print(f'Three Man {current_player.name} rolled a 10, with 1 die being a 3! - '
                      f'Social and Three Man')
                print(f'{current_player.name} passed Three Man to {player_behind.name}!')
                social_roll()
                current_player.toggle_three()
                player_behind.toggle_three()
                player_behind.sub_points(1)
            else:
                print(f'{current_player.name}, rolled a 10, with 1 die being a 3! - Social and Three Man')
                social_roll()
                current_three.sub_points(1)
        else:
            print(f'{current_player.name} rolled a 10! - Social')
            social_roll()
    elif dice_total == 11:
        print(f'{current_player.name}, rolled an 11! - Eleven Behind')
        player_behind.sub_points(1)
    elif dice1.value == 3 or dice2.value == 3:
        if current_player.is_three:
            print(f'Three Man {current_player.name}, rolled a {dice_total}, with 1 die being a 3! - Three Man')
            new_three_number = (PLAYER_LIST.index(current_three) - 1) % len(PLAYER_LIST)
            new_three = PLAYER_LIST[new_three_number]
            print(f'{current_player.name} passed Three Man to {new_three.name}!')
            current_player.toggle_three()
            new_three.toggle_three()
            new_three.sub_points(1)
        else:
            print(f'{current_player.name} rolled a 3 - Three Man')
            current_three.sub_points(1)
    else:
        print(f'{current_player.name} rolled a {dice_total}, which does nothing!')
        print(f'It is now {player_ahead.name}\'s turn!')
        next_player()


def next_player():
    current_player.toggle_current()
    current_player.reset_double_count()
    player_ahead_number = (PLAYER_LIST.index(current_player) + 1) % len(PLAYER_LIST)
    PLAYER_LIST[player_ahead_number].toggle_current()


app = Tk()
app.title('Three Man')
app.iconbitmap('three_man_icon.ico')
app.configure(background=GREEN)
app.columnconfigure(0, minsize=20)
app.columnconfigure(2, minsize=50)

three_man_image = Image.open(f'{BASE_IMG_PATH}three_man_icon.png').convert('RGBA')
three_man_image = three_man_image.resize((30, 30))
three_man_image = ImageTk.PhotoImage(three_man_image)

dice1image = Image.open(f'{BASE_IMG_PATH}{dice1.sides}-{dice1.value}.png').convert('RGBA')
dice1image = dice1image.resize((108, 144))
dice1image = ImageTk.PhotoImage(dice1image)
dice2image = Image.open(f'{BASE_IMG_PATH}{dice2.sides}-{dice2.value}.png').convert('RGBA')
dice2image = dice2image.resize((108, 144))
dice2image = ImageTk.PhotoImage(dice2image)

dice_frame = Frame(app, background=GREEN)
dice_frame.grid(row=0, column=1, rowspan=6)
dice_frame.rowconfigure(0, minsize=20)
dice_frame.rowconfigure(2, minsize=20)
dice_frame.rowconfigure(4, minsize=20)

player_frame = Frame(app, background='white')
player_frame.grid(row=0, column=3, rowspan=6)

dice_head_space = Label(dice_frame, background=GREEN)
dice_head_space.grid(row=0, rowspan=3, sticky='nesw')
dice1_space = Label(dice_frame, image=dice1image, background=GREEN)
dice1_space.grid(row=1, column=0)
dice_spacer = Label(dice_frame, text='', width=1, background=GREEN)
dice_spacer.grid(row=1, column=1, sticky='nesw')
dice2_space = Label(dice_frame, image=dice2image, background=GREEN)
dice2_space.grid(row=1, column=2)
dice_base_space = Label(dice_frame, background=GREEN)
dice_base_space.grid(row=2, rowspan=3, sticky='nesw')
roll_button = Button(dice_frame, bg='white', fg='red', activebackground='red', activeforeground='white', relief='groove',
                     text='Roll Dice', command=roll_dice)
roll_button.grid(row=3, column=0, columnspan=3, sticky='esw')

counter = 0
for player in PLAYER_LIST:
    exec(f'Player{counter}_box = Frame(player_frame, background=\'white\')')
    exec(f'Player{counter}_box.grid(row={counter}, column=1)')
    exec(f'Player{counter}_box.rowconfigure(0, minsize=50)')
    exec(f'Player{counter}_box.columnconfigure(1, minsize=50)')
    exec(f'Player{counter}_box.columnconfigure(3, minsize=50)')
    exec(f'Player{counter}_three = Label(Player{counter}_box, image=\'\', bg=\'gray\')')
    exec(f'Player{counter}_three.grid(row=0, column=1, sticky=\'nesw\')')
    exec(f'Player{counter}_name = Label(Player{counter}_box, text=\'{player.name}\', width=15,'
         f' font=(\'Arial\', 15, \'bold\'), anchor=\'w\')')
    exec(f'Player{counter}_name.grid(row=0, column=2, sticky=\'nesw\')')
    exec(f'Player{counter}_point = Label(Player{counter}_box, text=\'{player.points}\', bg=\'red\', fg=\'white\',  font=(\'Arial\', 15, \'bold\'), anchor=\'w\')')
    exec(f'Player{counter}_point.configure(anchor=\'center\')')
    exec(f'Player{counter}_point.grid(row=0, column=3, sticky=\'nesw\')')

    counter += 1

current_player.toggle_current()
current_three.toggle_three()
update_player_frame()
app.mainloop()

