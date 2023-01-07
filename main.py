from tkinter import *
import pandas
import random
BACKGROUND_COLOR = "#B1DDC6"
current_card = {}


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(language_front, text="French", fill="black")
    canvas.itemconfig(french_word, text=current_card["French"], fill="black")
    flip_timer = window.after(3000, func=flip_card)
    canvas.itemconfig(background, image=front_img)


def next_card_right():
    to_learn.remove(current_card)
    new_data = pandas.DataFrame(to_learn)
    new_data.to_csv("./data/words_to_learn.csv", index=False)
    next_card()


def flip_card():
    canvas.itemconfig(language_front, text="English", fill="white")
    canvas.itemconfig(french_word, text=current_card["English"], fill="white")
    canvas.itemconfig(background, image=back_img)


window = Tk()
window.title("Flashy")
window.minsize(800, 526)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

try:
    data = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("./data/french_words.csv")

to_learn = data.to_dict(orient="records")
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
back_img = PhotoImage(file="./images/card_back.png")
front_img = PhotoImage(file="./images/card_front.png")
background = canvas.create_image(400, 263, image=front_img)
canvas.grid(column=0, row=0, columnspan=2)
language_front = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
french_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))

right_img = PhotoImage(file="./images/right.png")
right_button = Button(image=right_img, command=next_card_right)
right_button.grid(column=1, row=1)
wrong_img = PhotoImage(file="./images/wrong.png")
wrong_button = Button(image=wrong_img, command=next_card)
wrong_button.grid(column=0, row=1)

next_card()


window.mainloop()
