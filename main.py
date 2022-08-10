# -------------------------------- IMPORTS -------------------------------- #
import json
import random
from tkinter import *

import pandas

# -------------------------------- CONSTANTS -------------------------------- #

BACKGROUND_COLOR = "#B1DDC6"
current_word = None
working_after = None

# -------------------------------- WORD COLLECTION -------------------------------- #

df = pandas.read_csv("data/fr.csv")
wordlist = df.to_dict(orient="records")


# -------------------------------- DATA READ FUNCTION -------------------------------- #

def get_ignored_data():
    with open("data/ignored.json", mode="r") as file:
        ignored_words_object = json.load(file)
    word_list = [word.strip() for word in ignored_words_object["words"]]
    return word_list


def get_working_dictionary():
    ignored_words = get_ignored_data()
    working_dictionary = []
    items = 0
    for word in wordlist:
        if items == 50:
            break
        if word["French"] not in ignored_words:
            working_dictionary.append(word)
            items += 1
    return working_dictionary


def set_ignored_data():
    working_word = current_word["French"]
    current_ignored_wordlist = get_ignored_data()
    current_ignored_wordlist.append(working_word)
    data = {
        "words": current_ignored_wordlist
    }
    with open("data/ignored.json", mode="w") as file:
        json.dump(data, file, indent=4)


# -------------------------------- WORD COLLECTION -------------------------------- #

def random_word_generate():
    global current_word
    current_word = random.choice(get_working_dictionary())


# -------------------------------- DISPLAY CHANGE FUNCTION -------------------------------- #

def ignore():
    set_ignored_data()
    canvas_change()


def canvas_change():
    global working_after
    random_word_generate()
    if working_after is not None:
        window.after_cancel(working_after)
    canvas.itemconfigure(can_img, image=front_screen)
    canvas.itemconfigure(title_text, text="French")
    canvas.itemconfigure(main_word, text=current_word["French"])
    working_after = window.after(3000, show_back_canvas, current_word["English"])


def show_back_canvas(WORD):
    global working_after
    working_after = None
    canvas.itemconfigure(can_img, image=back_screen)
    canvas.itemconfigure(title_text, text="English")
    canvas.itemconfigure(main_word, text=WORD)


# -------------------------------- UI SETUP -------------------------------- #


window = Tk()
window.title("Flash French")
window.config(pady=40, padx=40, bg=BACKGROUND_COLOR)

front_screen = PhotoImage(file="images/card_front.png")
back_screen = PhotoImage(file="images/card_back.png")
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")

canvas = Canvas(height=526, width=800, highlightthickness=0, borderwidth=0, bg=BACKGROUND_COLOR)
can_img = canvas.create_image(400, 263, image=front_screen)
title_text = canvas.create_text(400, 160, text="French", font=("Arial", 24, "normal"))
main_word = canvas.create_text(400, 270, text="Word", font=("Arial", 60, "bold"))

next_button = Button(image=right_image, highlightthickness=0, borderwidth=0, command=canvas_change)
ignore_button = Button(image=wrong_image, highlightthickness=0, borderwidth=0, command=ignore)

canvas.grid(row=0, column=0, columnspan=2)
next_button.grid(row=1, column=1)
ignore_button.grid(row=1, column=0)

# -------------------------------- FUNCTION WORKING -------------------------------- #

random_word_generate()
canvas_change()

window.mainloop()
