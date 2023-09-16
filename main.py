import shutil
import tkinter as tk
import subprocess
import threading
import argparse

#   COLORS:
#    --whitepurple: #fbf5ff;
#    --blackpurple: #251531;
#    --poppypurple: #b26ee8;
#    --greypurple: #9075a6;

LOFI_GIRL_URL = "https://www.youtube.com/watch?v=jfKfPfyJRdk"
mpv_command = ["mpv", "--ytdl-format=bestaudio", LOFI_GIRL_URL]

is_pause = True
is_pomo = True
timer_id = None
lofi_mpv_process = None

pause_time = 5
pomo_time = 25


def run_mpv_mp3(file):
    try:
        subprocess.run(
            ["mpv", "--no-video", file],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running MPV: {e}")
    except Exception as e:
        print(f"Error running MPV: {e}")


def play_sound(file):
    threading.Thread(target=run_mpv_mp3, args=(file,)).start()


def is_mpv_installed():
    if shutil.which("mpv") is None:
        return False
    return True


def play_lofi_girl():
    global lofi_mpv_process
    if lofi_mpv_process is not None:
        lofi_mpv_process.terminate()
        play_lofi_button["text"] = "Play"
        lofi_mpv_process = None
        return
    play_lofi_button["text"] = "Stop"
    lofi_mpv_process = subprocess.Popen(
        mpv_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def secs_to_min_and_sec_str(secs):
    mins = secs // 60
    secs = secs % 60
    return f"{mins:02d}:{secs:02d}"


def mins_to_minstr(mins):
    return f"{mins:02d}:00"


def get_secs_from_label(label):
    return int(label["text"].split(":")[0]) * 60 + int(label["text"].split(":")[1])


def close_window():
    if lofi_mpv_process is not None:
        lofi_mpv_process.terminate()
    root.destroy()


def start_timer():
    global is_pause, timer_id, is_pomo

    play_sound("sounds/click.mp3")
    if is_pause:
        start_button["text"] = "Pause"
        start_countdown(get_secs_from_label(timer_label))
        is_pause = False
    else:
        start_button["text"] = "Start"
        is_pause = True
        root.after_cancel(timer_id)


def change_timer():
    global is_pause, timer_id, is_pomo
    play_sound("sounds/click.mp3")

    if timer_id:
        root.after_cancel(timer_id)
    if is_pomo:
        timer_label["text"] = mins_to_minstr(pause_time)
        is_pomo = False
    else:
        timer_label["text"] = mins_to_minstr(pomo_time)
        is_pomo = True
    is_pause = True
    start_button["text"] = "Start"


def start_countdown(count):
    global timer_id, is_pomo, is_pause

    timer_label["text"] = secs_to_min_and_sec_str(count)

    if count >= 0:
        timer_id = root.after(1000, start_countdown, count - 1)
    else:
        play_sound("sounds/alarm.mp3")
        is_pause = True
        start_button["text"] = "Start"
        if is_pomo:
            timer_label["text"] = mins_to_minstr(pause_time)
            is_pomo = False
        else:
            timer_label["text"] = mins_to_minstr(pomo_time)
            start_button["text"] = "Start"
            is_pomo = True


root = tk.Tk()

# Set the window to stay on top of all other windows and remove the window decorations(making it borderless)
root.attributes("-topmost", True)
# root.wm_attributes("-type", "splash")
root.overrideredirect(True)

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = screen_width - 200
y = 0

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


timer_label = tk.Label(
    root, text=mins_to_minstr(pomo_time), font=("Poppins", 18), bg="#251531", fg="#fbf5ff"
)
timer_label.pack()

buttons = tk.Frame(root, bg="#251531")
buttons.pack(side=tk.BOTTOM, pady=20)

start_button = tk.Button(
    buttons,
    text="Start",
    command=start_timer,
    bg="#251531",
    fg="#fbf5ff",
    relief=tk.FLAT,
)
start_button.pack(side=tk.LEFT)

play_lofi_button = tk.Button(
    buttons,
    text="Play",
    command=play_lofi_girl,
    bg="#251531",
    fg="#fbf5ff",
    relief=tk.FLAT,
)
play_lofi_button.pack(side=tk.LEFT)

change_timer_button = tk.Button(
    buttons,
    text=">",
    command=change_timer,
    bg="#251531",
    fg="#fbf5ff",
    relief=tk.FLAT,
)
change_timer_button.pack(side=tk.LEFT)


if __name__ == "__main__":
    if not is_mpv_installed():
        print(
            "mpv is not installed.\nPlease install mpv according to the README and try again!"
        )
        exit(1)

    parser = argparse.ArgumentParser(description="pomogui")
    parser.add_argument(
        "-layout",
        choices=["left", "right"],
        help="Specify the layout of the window. Either left or right. Default is right.",
        default="right",
    )
    parser.add_argument(
        "-url",
        help="Specify the url that MPV will stream from. This defaults to LoFi girl (https://www.youtube.com/watch?v=jfKfPfyJRdk)",
        default=LOFI_GIRL_URL,
        type=str,
    )
    parser.add_argument(
        "-pomo",
        help="Specify the length of a pomodoro in minutes. Default is 25.",
        default=25,
        type=int,
    )
    parser.add_argument(
        "-pause",
        help="Specify the length of a pause in minutes. Default is 5.",
        default=5,
        type=int,
    )
    if parser.parse_args().layout == "left":
        x = 0

    if parser.parse_args().pause:
        pause_time = parser.parse_args().pause

    if parser.parse_args().url:
        mpv_command[2] = parser.parse_args().url

    if parser.parse_args().pomo:
        pomo_time = parser.parse_args().pomo

    root.geometry(f"200x150+{x}+{y}")
    timer_label["text"] = f"{parser.parse_args().pomo}:00"
    root.mainloop()
