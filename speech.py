import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import speech_recognition as sr
from pygame import mixer

r = sr.Recognizer()

mixer.init()


def recognize_file():
    lang = var.get()
    conv = str()
    if lang == 1:
        conv = "en-US"
    elif lang == 2:
        conv = "hi-IN"
    else:
        conv = "mr-IN"

    f = select_file()

    mixer.music.load(f)
    mixer.music.play()

    with sr.AudioFile(f) as source:
        audio = r.record(source)

        try:
            text_widget.delete("0.0", "end")
            text = r.recognize_google(audio, language=conv)
            text_widget.insert("0.0", text)

        except sr.UnknownValueError:
            print("Could not recognize the audio")

        except sr.RequestError as e:
            print(e)


def save_file():
    f = select_file()
    with open(f, "w") as file:
        file.write(text_widget.get("0.0", "end"))


def select_file():
    file_path = filedialog.askopenfilename(title="Select a File")
    return file_path


root = tk.Tk()
root.title("Speech to Text")


text_widget = tk.Text(font=("Arial", 15))
text_widget.grid(column=0, row=0)

check_frame = tk.Frame()
check_frame.grid(column=0, row=1)

var = tk.IntVar()

R1 = tk.Radiobutton(check_frame, text="English", variable=var, value=1)
R2 = tk.Radiobutton(check_frame, text="Hindi", variable=var, value=2)
R3 = tk.Radiobutton(check_frame, text="Marathi", variable=var, value=3)

R1.grid(column=0, row=0)
R2.grid(column=1, row=0)
R3.grid(column=2, row=0)

button_frame = tk.Frame()
button_frame.grid(column=0, row=2)

recognize_btn = ttk.Button(button_frame, text="Recognize", command=recognize_file)
save_btn = ttk.Button(button_frame, text="Save as", command=save_file)

recognize_btn.grid(column=0, row=0)
save_btn.grid(column=1, row=0)

root.mainloop()
