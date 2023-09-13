import shutil
import tkinter as tk
import subprocess
import threading

#   COLORS:
#    --whitepurple: #fbf5ff;
#    --blackpurple: #251531;
#    --poppypurple: #b26ee8;
#    --greypurple: #9075a6;

LOFI_GIRL_URL = "https://www.youtube.com/watch?v=jfKfPfyJRdk"
mpv_command = ["mpv", "--ytdl-format=bestaudio", LOFI_GIRL_URL]

is_pause = False
timer_id = None
process = None


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
    global process
    if process is not None:
        process.terminate()
        play_lofi_button["text"] = "Play"
        process = None
        return
    play_lofi_button["text"] = "Stop"
    process = subprocess.Popen(
        mpv_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
    )


def secs_to_min_and_sec_str(secs):
    mins = secs // 60
    secs = secs % 60
    return f"{mins:02d}:{secs:02d}"


def get_secs_from_label(label):
    return int(label["text"].split(":")[0]) * 60 + int(label["text"].split(":")[1])


def close_window():
    if process is not None:
        process.terminate()
    root.destroy()


def start_timer():
    global is_pause, timer_id

    play_sound("sounds/click.mp3")
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

    if count > 0:
        timer_id = root.after(1000, start_countdown, count - 1)
    else:
        label["text"] = "05:00"


root = tk.Tk()

# Set the window to stay on top of all other windows and remove the window decorations(making it borderless)
root.attributes("-topmost", True)
# root.wm_attributes("-type", "splash")
root.overrideredirect(True)

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = 300
y = 0

root.geometry(f"200x150+{x}+{y}")
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

buttons = tk.Frame(root, bg="#251531")
buttons.pack(side=tk.BOTTOM, pady=20)

start_button = tk.Button(
    buttons,
    text="Start",
    command=start_timer,
    bg="#251531",
    fg="#fbf5ff",
    relief=tk.FLAT,
    # padx=20
)
start_button.pack(side=tk.LEFT)

play_lofi_button = tk.Button(
    buttons,
    text="Play",
    command=play_lofi_girl,
    bg="#251531",
    fg="#fbf5ff",
    relief=tk.FLAT,
    # padx=20
)
play_lofi_button.pack(side=tk.LEFT)

if __name__ == "__main__":
    play_sound("sounds/alarm.mp3")
    if not is_mpv_installed():
        print(
            "mpv is not installed.\nPlease install mpv according to the README and try again!"
        )
        exit(1)
    root.mainloop()
