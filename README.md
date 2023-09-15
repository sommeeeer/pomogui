# pomogui

I wanted to make this pomogui for a long time. Finally started today. Gonna do it in **Python** and **tkinter**, with **mpv** as audio player.

While coding I usually listen to [LoFi girl](https://www.youtube.com/watch?v=jfKfPfyJRdk) or some similar channel. Usually on low volume. 

Im also using the pomodoro technique ([Wikipedia](https://en.wikipedia.org/wiki/Pomodoro_Technique)) while studying/coding. Its a nice way to get regular breaks, while focusing maximum when you are in an active pomo. 

The idea was that I wanted a GUI with a window that doesn't get in my way while im developing. It has to be borderless and always on top.

You can see it in action on the rop right corner here:
![Screenshot](https://magnus.dahleide.com/pomogui_screenshot.png "Optional title")


### Requirements
You need **mpv** and **yt-dlp** installed for playing the LoFi girl radio. On Ubuntu/Debian thats just: 
```bash
sudo apt install mpv
pip install yt-dlp
```
If you already have yt-dlp and mpv, you might need to update yt-dlp to the newest version. You can do so with:
```bash
pip install --upgrade 
# or
yt-dlp -U
```

For further instructions on how to install **mpv** and **yt-dlp** on other systems you can visit they're installation docs here:

[mpv installation guide](https://mpv.io/installation/)

[yt-dlp installation guide](https://github.com/yt-dlp/yt-dlp/wiki/Installation)
