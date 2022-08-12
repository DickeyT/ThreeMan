import tkinter

from Dice import Dice
from Player import Player
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import random


BASE_IMG_PATH = "./Dice Images/"
diceA, diceB = Dice(6), Dice(6)
dice0, dice1, dice2, dice3, dice4, dice5 = Dice(6), Dice(6), Dice(6), Dice(6), Dice(6), Dice(6)
all_player_dice = [dice0, dice1, dice2, dice3, dice4, dice5]
current_player_dice = []



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
player_dice_counter = 0
for player in PLAYER_LIST:
    current_player_dice.append(all_player_dice[player_dice_counter])
    player_dice_counter += 1

current_player = PLAYER_LIST[0]
current_player_number = PLAYER_LIST.index(current_player)
current_three = current_player
player_ahead_number = (PLAYER_LIST.index(current_player) + 1) % len(PLAYER_LIST)
if PLAYER_LIST.index(current_player) == 0:
    player_behind_number = len(PLAYER_LIST) - 1
else:
    player_behind_number = (PLAYER_LIST.index(current_player) - 1) % len(PLAYER_LIST)
player_ahead, player_behind = PLAYER_LIST[player_ahead_number], PLAYER_LIST[player_behind_number]
action = 'And so it begins...'

def rolled_off():
    global current_player
    global current_three

    if current_player.points >= 5:
        off_chance = random.randint(1, current_player.points)
    else:
        off_chance = random.randint(1, 5)

    if off_chance == 1:
        action = f'{current_player.name} Rolled off the table!'
        if current_player != current_three:
            action += f'\n{current_player.name} is the new Three Man'
            current_player.toggle_three()
            current_three.toggle_three()
        else:
            action += f'\n{current_player.name} remains Three Man'
        next_player()
        return True
    else:
        return False


def roll_dice():
    ani_counter = 0
    while ani_counter < 45:
        app.update()
        diceA.roll()
        diceB.roll()
        diceAimage = Image.open(f'{BASE_IMG_PATH}{diceA.sides}-{diceA.value}.png').convert('RGBA')
        diceAimage = diceAimage.resize((108, 144))
        diceAimage = ImageTk.PhotoImage(diceAimage)
        diceA_space.configure(image=diceAimage)
        diceA_space.img = diceAimage
        diceBimage = Image.open(f'{BASE_IMG_PATH}{diceB.sides}-{diceB.value}.png').convert('RGBA')
        diceBimage = diceBimage.resize((108, 144))
        diceBimage = ImageTk.PhotoImage(diceBimage)
        diceB_space.configure(image=diceBimage)
        diceB_space.img = diceBimage
        ani_counter += 1
    if not rolled_off():
        dice_actions()
    update_player_frame()


def switch_buttons(number):
    buttons_off = []
    for num in range(0, len(PLAYER_LIST)):
        buttons_off.append(num)
    buttons_off.remove((number + 1) % len(PLAYER_LIST))
    for num in buttons_off:
        exec(f'open_roll_button{num}[\'state\'] = DISABLED')
    exec(f'open_roll_button{(number + 1) % len(PLAYER_LIST)}[\'state\'] = NORMAL')


def open_roll_dice(number):
    global player_ahead, player_behind
    ani_counter = 0
    while ani_counter < 45:
        app.update()
        exec(f'dice{number}.roll()')
        exec(f'dice{number}image = Image.open(f\'{{BASE_IMG_PATH}}{{dice{number}.sides}}-{{dice{number}.value}}.png\')'
             f'.convert(\'RGBA\')')
        exec(f'dice{number}image = dice{number}image.resize((108, 144))')
        exec(f'dice{number}image = ImageTk.PhotoImage(dice{number}image)')
        exec(f'open_dice{number}_space.configure(image=dice{number}image)')
        exec(f'open_dice{number}_space.img = dice{number}image')
        ani_counter += 1
    the_dice = current_player_dice[number]
    if the_dice.value == 3:
        print(f'{PLAYER_LIST[number].name} rolled the first 3!\n{PLAYER_LIST[number].name} is Three Man')
        PLAYER_LIST[number].set_three()
        tkinter.messagebox.showinfo(title='Three Man has been found!',
                                    message=f'{PLAYER_LIST[number].name} is the first 3 man!'
                                    )
        switch_to_main_game()
        next_player()
        update_player_frame()

    else:
        switch_buttons(number)
        next_player()
        update_open_player_frame()


def update_open_player_frame():
    counter = 0
    for player in PLAYER_LIST:
        if player.is_current:
            exec(f'open_Player{counter}_three.configure(bg=\'black\')')
            exec(f'open_Player{counter}_name.configure(bg=\'black\', fg=\'white\')')
            exec(f'open_Player{counter}_point.configure(bg=\'black\', fg=\'red\')')
        else:
            exec(f'open_Player{counter}_three.configure(bg=\'gray\')')
            exec(f'open_Player{counter}_name.configure(bg=\'white\', fg=\'black\')')
            exec(f'open_Player{counter}_point.configure(bg=\'red\', fg=\'white\')')
        exec(f'Player{counter}_point.configure(text=\'{player.points}\')')
        counter += 1
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

def remove_player(player):
    global PLAYER_LIST
    last_player = len(PLAYER_LIST)-1
    PLAYER_LIST.remove(player)
    exec(f'Player{last_player}_box.destroy()')
    exec(f'Player{last_player}_three.destroy()')
    exec(f'Player{last_player}_name.destroy()')

def update_player_frame():
    counter = 0
    action_label.configure(text=action)
    for player in PLAYER_LIST:
        if player.points <= 0:
            if player.is_three:
                player_ahead.set_three()
            remove_player(player)
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
        if player.points <= 0:
            if player.is_three:
                player_ahead.set_three()
            remove_player(player)
        exec(f'Player{counter}_point.configure(text=\'{player.points}\')')
        exec(f'Player{counter}_name.configure(text=\'{player.name}\')')
        counter += 1


def social_roll():
    for player in PLAYER_LIST:
        player.sub_points(1)


def three_doubles():
    global action, current_player
    if current_player.double_count == 3:
        action = (f'{current_player.name} has rolled 3 doubles in their turn!\n{current_player.name} gains 10 points!\n')
        current_player.add_points(10)
        current_player.reset_double_count()
    else:
        action = ''


def dice_actions():
    global action, player_ahead_number, player_behind_number, player_ahead, player_behind
    dice_total = diceA.value + diceB.value
    global current_player, current_three
    action = ''
    for player in PLAYER_LIST:
        if player.is_current:
            current_player = player
        if player.is_three:
            current_three = player
    player_ahead_number = (PLAYER_LIST.index(current_player) + 1) % len(PLAYER_LIST)
    player_behind_number = (PLAYER_LIST.index(current_player) - 1) % len(PLAYER_LIST)
    player_ahead, player_behind = PLAYER_LIST[player_ahead_number], PLAYER_LIST[player_behind_number]
    if diceA.value == diceB.value:
        current_player.add_double_count(1)
        three_doubles()
        print(current_player.double_count)
        if dice_total == 2:
            action += f'{current_player.name} rolled double 1s!'
        elif dice_total == 4:
            action += f'{current_player.name} rolled double 2s!'
        elif dice_total == 6:
            if current_player.is_three:
                action += (f'Three Man{current_player.name} rolled double 3s! - Double Three Man!\n{current_player.name} '
                      f'passed Three Man to {player_behind.name}!\n{player_behind.name} loses 2 points!')
                current_player.toggle_three()
                player_behind.toggle_three()
                player_behind.sub_points(2)
            else:
                action += f'{current_player.name} rolled double 3s! - Double Three Man!\n{current_three.name} loses 2 points!'
                current_three.sub_points(2)
        elif dice_total == 8:
            action += f'{current_player.name} rolled double 4s!'
        elif dice_total == 10:
            action += f'{current_player.name} rolled double 5s! - Social'
            social_roll()
        elif dice_total == 12:
            action += f'{current_player.name} rolled double 6s!'

    elif dice_total == 3:
        if current_player.is_three:
            action += f'Three Man {current_player.name} rolled 3, the hard way!\n{current_player.name} passed Three ' \
                     f'Man to {player_behind.name}!\n{player_behind.name} loses 2 points!'
            current_player.toggle_three()
            player_behind.toggle_three()
            player_behind.sub_points(2)
        else:
            action += f'{current_player.name} rolled 3, the hard way! \n Three Man {current_three.name} loses 2 points!'
            current_three.sub_points(2)
    elif dice_total == 7:
        if diceA.value == 3 or diceB.value == 3:
                if current_player.is_three:
                    action += f'Three Man {current_player.name} rolled a 7, with 1 die being a 3! \nSeven Ahead and Three' \
                             f' Man\n{current_player.name} passed Three Man to {player_behind.name}!'
                    current_player.toggle_three()
                    player_behind.toggle_three()
                    player_behind.sub_points(1)
                    player_ahead.sub_points(1)
                else:
                    action += f'{current_player.name}, rolled a 7, with 1 die being a 3! \n Seven Ahead and Three Man'
                    player_ahead.sub_points(1)
                    current_three.sub_points(1)
        else:
            action += f'{current_player.name}, rolled a 7! - Seven Ahead'
            player_ahead.sub_points(1)
    elif dice_total == 10:
        if diceA.value == 3 or diceB.value == 3:
            if current_player.is_three:
                action += f'Three Man {current_player.name} rolled a 10, with 1 die being a 3! \nSocial and Three ' \
                         f'Man\n{current_player.name} passed Three Man to {player_behind.name}!'
                social_roll()
                current_player.toggle_three()
                player_behind.toggle_three()
                player_behind.sub_points(1)
            else:
                action += f'{current_player.name}, rolled a 10, with 1 die being a 3! \nSocial and Three Man'
                social_roll()
                current_three.sub_points(1)
        else:
            action += f'{current_player.name} rolled a 10! - Social'
            social_roll()
    elif dice_total == 11:
        action += f'{current_player.name}, rolled an 11! - Eleven Behind'
        player_behind.sub_points(1)
    elif diceA.value == 3 or diceB.value == 3:
        if current_player.is_three:
            action += f'Three Man {current_player.name}, rolled a {dice_total}, with 1 die being a 3! - Three ' \
                     f'Man\n{current_player.name} passed Three Man to {player_behind.name}!'
            new_three_number = (PLAYER_LIST.index(current_three) - 1) % len(PLAYER_LIST)
            new_three = PLAYER_LIST[new_three_number]

            current_player.toggle_three()
            new_three.toggle_three()
            new_three.sub_points(1)
        else:
            action += f'{current_player.name} rolled a 3 - Three Man'
            current_three.sub_points(1)
    else:
        action += f'{current_player.name} rolled a {dice_total}, which does nothing!\nIt is now {player_ahead.name}\'s turn!'
        next_player()


def next_player():
    global current_player_number, player_ahead_number, current_player, player_ahead
    current_player.set_current(False)
    current_player.reset_double_count()
    current_player = player_ahead
    current_player.toggle_current()
    player_ahead_number = (PLAYER_LIST.index(current_player) + 1) % len(PLAYER_LIST)
    player_ahead = PLAYER_LIST[player_ahead_number]


app = Tk()
app.title('Three Man')
app.iconbitmap('three_man_icon.ico')
app.geometry('1716x300')
app.configure(background=GREEN)

MainGame = Frame(app, background=GREEN)
OpenRolls = Frame(app, background=GREEN)


def switch_to_main_game():
    MainGame.pack(fill='both', expand=1)
    OpenRolls.pack_forget()


def switch_to_open_rolls():
    OpenRolls.pack(fill='both', expand=1)
    MainGame.pack_forget()


# MainGame Widgets
MainGame.configure(background=GREEN)
MainGame.grid_rowconfigure(0, weight=1)
MainGame.columnconfigure(0, minsize=20)
MainGame.columnconfigure(2, minsize=50)

three_man_image = Image.open(f'{BASE_IMG_PATH}three_man_icon.png').convert('RGBA')
three_man_image = three_man_image.resize((30, 30))
three_man_image = ImageTk.PhotoImage(three_man_image)

diceAimage = Image.open(f'{BASE_IMG_PATH}{diceA.sides}-{diceA.value}.png').convert('RGBA')
diceAimage = diceAimage.resize((108, 144))
diceAimage = ImageTk.PhotoImage(diceAimage)
diceBimage = Image.open(f'{BASE_IMG_PATH}{diceB.sides}-{diceB.value}.png').convert('RGBA')
diceBimage = diceBimage.resize((108, 144))
diceBimage = ImageTk.PhotoImage(diceBimage)

dice_frame = Frame(MainGame, background=GREEN)
dice_frame.grid(row=0, column=3, rowspan=6)
dice_frame.rowconfigure(0, minsize=20)
dice_frame.rowconfigure(2, minsize=20)
dice_frame.rowconfigure(4, minsize=20)

player_frame = Frame(MainGame, background=GREEN)
player_frame.grid(row=0, column=0, rowspan=6)

dice_head_space = Label(dice_frame, background=GREEN)
dice_head_space.grid(row=0, rowspan=3, sticky='nesw')
diceA_space = Label(dice_frame, image=diceAimage, background=GREEN)
diceA_space.grid(row=1, column=0)
dice_spacer = Label(dice_frame, text='', width=1, background=GREEN)
dice_spacer.grid(row=1, column=1, sticky='nesw')
diceB_space = Label(dice_frame, image=diceAimage, background=GREEN)
diceB_space.grid(row=1, column=2)
dice_base_space = Label(dice_frame, background=GREEN)
dice_base_space.grid(row=2, rowspan=3, sticky='nesw')
roll_button = Button(dice_frame, bg='white', fg='red', activebackground='red', activeforeground='white', relief='groove',
                     text='Roll Dice', command=roll_dice)
roll_button.grid(row=3, column=0, columnspan=3, sticky='esw')

counter = 0
for player in PLAYER_LIST:
    exec(f'Player{counter}_box = Frame(player_frame, background=GREEN)')
    exec(f'Player{counter}_box.grid(row={counter}, column=0)')
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

action_frame = Frame(MainGame, width=600, background=GREEN)
action_frame.grid(row=0, column=5, rowspan=10)
action_frame.grid_rowconfigure(1, weight=1)
action_frame.grid_columnconfigure(1, weight=1, minsize=600)

actions = Frame(action_frame, width=500, background=GREEN)
actions.grid(row=1, column=1, sticky='')
actions.columnconfigure(1, minsize=500)

action_label = Label(actions, text='', background=GREEN)
action_label.configure(font='Arial 15 bold')
action_label.grid(row=1, column=1)

right_frame = Frame(MainGame, width=650, height=300, background='gray')
right_frame.grid(row=0, column=7, rowspan=10, sticky='ns')
right_frame.grid_rowconfigure(1, weight=1)
right_frame.grid_columnconfigure(1, weight=1)

rules_frame = Frame(right_frame, width=550, background='gray')
rules_frame.grid(row=1, column=1, sticky='')
rules_frame.columnconfigure(0, minsize=550)

rule_3 = Label(rules_frame, text='Three Man - Any 3 is rolled - The Three Man loses a point', background='gray',
               anchor='w')
rule_3.grid(row=0, column=0, sticky='nesw')
rule_3_hard = Label(rules_frame, text='Three Man the Hard Way - Dice total equals 3 - The Three Man loses 2 points',
                    background='gray', anchor='w')
rule_3_hard.grid(row=2, column=0, sticky='nesw')
rule_3_pass = Label(rules_frame, text='Pass Three Man - Three Man rolls a 3 - The Three Man passes Three Man to the '
                                      'player behind them', background='gray', anchor='w')
rule_3_pass.grid(row=2, column=0, sticky='nesw')
rule_7 = Label(rules_frame, text='Seven Ahead - Dice Total equals 7 - Seven Ahead - Player ahead of you loses a point',
               background='gray', anchor='w')
rule_7.grid(row=3, column=0, sticky='nesw')
rule_10 = Label(rules_frame, text='Social - Dice total equals 10 - All players lose a point', background='gray',
                anchor='w')
rule_10.grid(row=4, column=0, sticky='nesw')
rule_11 = Label(rules_frame, text='Eleven Behind - Dice total equals 11 - Player behind you loses a point',
                background='gray', anchor='w')
rule_11.grid(row=5, column=0, sticky='nesw')
rule_doubles = Label(rules_frame, text='Doubles - Both Dice show the same number - 3 doubles in turn gives you back 10 '
                                       'points', background='gray', anchor='w')
rule_doubles.grid(row=6, column=0, sticky='nesw')



# OpenRolls Widgets
OpenRolls.grid_rowconfigure(0, weight=1)
OpenRolls.grid_columnconfigure(0, weight=1)
dice0image = Image.open(f'{BASE_IMG_PATH}{dice0.sides}-{dice0.value}.png').convert('RGBA')
dice0image = dice0image.resize((108, 144))
dice0image = ImageTk.PhotoImage(dice0image)
dice1image = Image.open(f'{BASE_IMG_PATH}{dice1.sides}-{dice1.value}.png').convert('RGBA')
dice1image = dice1image.resize((108, 144))
dice1image = ImageTk.PhotoImage(dice1image)
dice2image = Image.open(f'{BASE_IMG_PATH}{dice2.sides}-{dice2.value}.png').convert('RGBA')
dice2image = dice2image.resize((108, 144))
dice2image = ImageTk.PhotoImage(dice2image)
dice3image = Image.open(f'{BASE_IMG_PATH}{dice3.sides}-{dice3.value}.png').convert('RGBA')
dice3image = dice3image.resize((108, 144))
dice3image = ImageTk.PhotoImage(dice3image)
dice4image = Image.open(f'{BASE_IMG_PATH}{dice4.sides}-{dice4.value}.png').convert('RGBA')
dice4image = dice4image.resize((108, 144))
dice4image = ImageTk.PhotoImage(dice4image)
dice5image = Image.open(f'{BASE_IMG_PATH}{dice5.sides}-{dice5.value}.png').convert('RGBA')
dice5image = dice5image.resize((108, 144))
dice5image = ImageTk.PhotoImage(dice5image)

open_player_frame = Frame(OpenRolls, background=GREEN)
open_player_frame.grid(row=0, column=0, sticky='')
open_player_frame.rowconfigure(0, minsize=20)
open_player_frame.rowconfigure(2, minsize=20)
open_player_frame.rowconfigure(4, minsize=20)

open_dice_head_space = Label(open_player_frame, background=GREEN)
open_dice_head_space.grid(row=0, rowspan=6, sticky='nesw')
open_dice_mid_space = Label(open_player_frame, background=GREEN)
open_dice_mid_space.grid(row=2, rowspan=6, sticky='nesw')
open_dice_base_space = Label(open_player_frame, background=GREEN)
open_dice_base_space.grid(row=4, rowspan=6, sticky='nesw')

counter = 0
for player in PLAYER_LIST:
    exec(f'open_dice{counter}_space = Label(open_player_frame, image=dice{counter}image, background=GREEN)')
    exec(f'open_dice{counter}_space.grid(row=1, column={counter})')
    exec(f'open_roll_button{counter} = Button(open_player_frame, bg=\'white\', fg=\'red\', activebackground=\'red\','
         f' activeforeground=\'white\', relief=\'groove\',text=\'Roll Dice\', state=\'disabled\','
         f' command=lambda: open_roll_dice({counter}))')
    exec(f'open_roll_button{counter}.grid(row=3, column={counter})')
    exec(f'open_Player{counter}_box = Frame(open_player_frame, background=\'white\')')
    exec(f'open_Player{counter}_box.grid(row=10, column={counter})')
    exec(f'open_Player{counter}_box.rowconfigure(0, minsize=50)')
    exec(f'open_Player{counter}_box.columnconfigure(1, minsize=50)')
    exec(f'open_Player{counter}_box.columnconfigure(3, minsize=50)')
    exec(f'open_Player{counter}_three = Label(open_Player{counter}_box, image=\'\', bg=\'gray\')')
    exec(f'open_Player{counter}_three.grid(row=0, column=1, sticky=\'nesw\')')
    exec(f'open_Player{counter}_name = Label(open_Player{counter}_box, text=\'{player.name}\', width=15,'
         f' font=(\'Arial\', 15, \'bold\'), anchor=\'w\')')
    exec(f'open_Player{counter}_name.grid(row=0, column=2, sticky=\'nesw\')')
    exec(
        f'open_Player{counter}_point = Label(open_Player{counter}_box, text=\'{player.points}\', bg=\'red\', fg=\'white\',  font=(\'Arial\', 15, \'bold\'), anchor=\'w\')')
    exec(f'open_Player{counter}_point.configure(anchor=\'center\')')
    exec(f'open_Player{counter}_point.grid(row=0, column=3, sticky=\'nesw\')')
    counter += 1


current_player.toggle_current()
update_player_frame()
update_open_player_frame()
switch_to_open_rolls()
tkinter.messagebox.showwarning(title='Roll for Three Man', message='Lets take turn rolling a single die to find the '
                                                                   'first Three Man\nFirst one to roll a three is the '
                                                                   'Three Man')
exec(f'open_roll_button{current_player_number}[\'state\'] = NORMAL')
app.mainloop()

