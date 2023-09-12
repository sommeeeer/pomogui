import tkinter as tk
from tkinter import messagebox

#   COLORS:
#    --whitepurple: #fbf5ff;
#    --blackpurple: #251531;
#    --poppypurple: #b26ee8;
#    --greypurple: #9075a6;


is_pause = False
timer_id = None


def secs_to_min_and_sec_str(secs):
    mins = secs // 60
    secs = secs % 60
    return f"{mins:02d}:{secs:02d}"


def get_secs_from_label(label):
    return int(label["text"].split(":")[0]) * 60 + int(label["text"].split(":")[1])


def close_window():
    root.destroy()


def start_timer():
    global is_pause, timer_id
    print(timer_id)
    if not is_pause:
        start_button["text"] = "Pause"
        start_countdown(get_secs_from_label(label))
        is_pause = True
    else:
        start_button["text"] = "Start"
        is_pause = False
        root.after_cancel(timer_id)


def start_countdown(count):
    global timer_id

    label["text"] = secs_to_min_and_sec_str(count)
    print(get_secs_from_label(label))

    if count > 0:
        timer_id = root.after(1000, start_countdown, count - 1)
    else:
        label["text"] = "05:00"


root = tk.Tk()

# Set the window to stay on top of all other windows and remove the window decorations(making it borderless)
root.attributes("-topmost", True)
root.wm_attributes("-type", "splash")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


x = 300
y = 0

root.geometry(f"200x200+{x}+{y}")
root.configure(bg="#251531")


close_button = tk.Button(
    root,
    text="X",
    command=close_window,
    font=("Poppins", 12),
    bg="#251531",
    fg="#fbf5ff",
    relief=tk.FLAT,
)
close_button.pack(side=tk.TOP, anchor=tk.NE, padx=10, pady=10)


label = tk.Label(root, text="25:00", font=("Poppins", 18), bg="#251531", fg="#fbf5ff")
label.pack()

start_button = tk.Button(
    root,
    text="Start",
    command=start_timer,
    bg="#251531",
    fg="#fbf5ff",
    relief=tk.FLAT,
)
start_button.pack()

root.mainloop()
