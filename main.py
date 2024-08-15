import threading
from tkinter import *
import time

with open("wordsList.txt") as data:
    words_list_basic = data.read().split(",")

    words_list = [word.strip(' ""') for word in words_list_basic]
print(words_list)
root = Tk()
root.title("Typing speed app")
root.config(pady=20, padx=20)
frame = Frame(root)
frame.pack(padx=30, pady=30, fill='x', expand=True)
user_word = StringVar()
user_words_list = []
errors_list = []
first_key_triggered = False
finish_label = None
restart_text = None
errors_label = None
errors_labels = []
index = 0


def on_key_pressed(event):
    global first_key_triggered
    if not first_key_triggered:
        first_key_triggered = True
        threading.Thread(target=test_speed, args=(60,), daemon=True).start()
    return


def test_results():
    global finish_label
    global restart_text
    global errors_label
    global index
    wpm = 0
    for word1, word2 in zip(words_list, user_words_list):
        if word1 == word2:
            wpm += 1
            errors_list.append("good")
        else:
            errors_list.append(word2)
    user_entry.pack_forget()
    for word1, word2 in zip(words_list,errors_list):
        if word2 != "good":
            errors_label = Label(frame, text=f"Your wrote {word2} instead of {word1}")
            errors_label.pack()
            errors_labels.append(errors_label)
    finish_label = Label(frame, text=f"Your score is {wpm} words per minute.")
    finish_label.pack()
    restart_text = Button(frame, text="Restart", command=starting_test)
    restart_text.pack()


def test_speed(duration):
    start_time = time.time()

    while time.time() - start_time < duration:
        timer = 60 + int(start_time - time.time())
        timer_box = Label(frame, text="time: 60")
        timer_box.pack()
        timer_box.config(text=f"time: {timer}")
        time.sleep(1)
        timer_box.pack_forget()

    print("Time's up! The function has stopped.")
    test_results()


def word_entered(event):
    global index
    user_words_list.append(user_word.get())
    user_entry.delete(0, END)
    index += 1
    content = text_box.get("1.0", END)
    start_idx = content.find(words_list[index])
    end_idx = start_idx + len(words_list[index])
    start = f"0.0 + {start_idx} chars"
    end = f"0.0 + {end_idx} chars"
    text_box.tag_add("red_word", start, end)
    text_box.tag_config("red_word", foreground="red")


def starting_test():
    global index
    global finish_label
    global errors_labels
    global restart_text
    global user_words_list
    global errors_list
    global first_key_triggered
    index = 0
    for error_label in errors_labels:
        error_label.pack_forget()
    errors_labels = []
    if finish_label is not None:
        finish_label.pack_forget()
        finish_label = None
    if restart_text is not None:
        restart_text.pack_forget()
        restart_text = None
    first_key_triggered = False
    user_words_list = []
    errors_list = []
    text_box.config(state=NORMAL)
    text_box.tag_remove("red_word", "1.0", END)
    text_box.tag_add("red_word", "1.0", "1.5")
    text_box.tag_config("red_word", foreground="red")
    text_box.config(state=DISABLED)

    user_entry.bind('<Key>', on_key_pressed)
    user_entry.bind('<Return>', word_entered)
    user_label.pack()
    user_entry.pack()
    user_entry.focus()
    text_box.tag_add("red_word", "1.0", "1.5")
    text_box.tag_config("red_word", foreground="red")


user_label = Label(frame, text="Start the test", font=("Helvetica", 18))
user_entry = Entry(frame, textvariable=user_word)

title_label = Label(frame, text="Typing Speed Test", font=("Arial", 24))
title_label.pack()


text_box = Text(root, width=50, height=20, wrap="word", borderwidth=2, relief="solid", font=("Helvetica", 12))
text_box.pack(padx=10, pady=10)

for i, word in enumerate(words_list):
    text_box.insert(END, word + "  ")
    if (i + 1) % 10 == 0:
        text_box.insert(END, "\n")
text_box.tag_add("red_word", "1.0", "1.5")
text_box.tag_config("red_word", foreground="red")
text_box.config(state=DISABLED)

starting_test()


root.mainloop()
