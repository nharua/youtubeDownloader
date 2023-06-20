from tkinter import *
from tkinter import filedialog
from pytube import YouTube
import os
import glob
import ffmpeg

BITRATE = "192k"


# https://stackoverflow.com/questions/31836104/pyinstaller-and-onefile-how-to-include-an-image-in-the-exe-file
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def ask_save_location():
    folder_path = filedialog.askdirectory()
    return folder_path


def getVideo():
    link = yt_link.get()
    yt = YouTube(
        link,
    )
    save_location = ask_save_location()
    yd = yt.streams.get_highest_resolution()
    yd.download(save_location)
    return save_location


def getMP3():
    global BITRATE
    save_folder = getVideo()
    os.chdir(save_folder)
    current_folder = os.getcwd()
    mp4_files = glob.glob("*.mp4")
    mp4_file = mp4_files[0]
    print(mp4_file)
    file_name = os.path.splitext(os.path.basename(mp4_file))[0]
    mp3_file = ".".join([file_name, "mp3"])
    ffmpeg.input(mp4_file).output(mp3_file, format="mp3", audio_bitrate=BITRATE).run()
    # Delete mp4 after convert
    os.remove(mp4_file)


def getAAC():
    global BITRATE
    save_folder = getVideo()
    os.chdir(save_folder)
    current_folder = os.getcwd()
    mp4_files = glob.glob("*.mp4")
    mp4_file = mp4_files[0]
    file_name = os.path.splitext(os.path.basename(mp4_file))[0]
    aac_file = ".".join([file_name, "aac"])
    ffmpeg.input(mp4_file).output(
        aac_file, codec="aac", ac=2, ar="44100", ab=BITRATE
    ).run()
    # Delete mp4 after convert
    os.remove(mp4_file)


window = Tk()  # Instantiate an instance of a window.

# window.geometry("420x70")  # Size (WxH)
window.title("Youtube Downloader")

icon = PhotoImage(file=resource_path("images/yt_icon.png"))
window.iconphoto(True, icon)

# change background color
window.config(
    background="#384531"
)  # or you can search google with "hex color picker" keyword

# Code in here ....................
# Create a entry box to user paste the youtube link
# Link test https://www.youtube.com/watch?v=_8vekzCF04Q&pp=ygUNdmFuIG1haSBodW9uZw%3D%3D

yt_label = Label(window, text="Youtube Link", border=5)
yt_label.grid(row=0, column=0, padx=5, pady=10)

yt_link = Entry(
    window,
    width=50,
    border=5,
)
yt_link.grid(row=0, column=1, padx=3)

yt_linkVideo = Button(window, text="Get MP4 Video File", command=getVideo, border=5)
yt_linkVideo.grid(row=1, column=0, columnspan=2, pady=2)

yt_linkMP3 = Button(window, text="Get MP3 Audio", command=getMP3, border=5)
yt_linkMP3.grid(row=2, column=0, columnspan=2, pady=2)

yt_linkAAC = Button(window, text="Get AAC Audio", command=getAAC, border=5)
yt_linkAAC.grid(row=3, column=0, columnspan=2, pady=2)


window.mainloop()  # Place window o computer screen, listen for events.
