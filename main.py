from tkinter import *
from tkinter import filedialog
from pytube import YouTube
import os
import glob
import ffmpeg

BITRATE = "192k"


def ask_save_location():
    folder_path = filedialog.askdirectory()
    return folder_path


def getVideo():
    link = yt_link.get()
    yt = YouTube(
        link,
        # use_oauth=True,
        # allow_oauth_cache=True,
    )
    save_location = ask_save_location()
    # print("Title:", yt.title)
    # print("Author:", yt.author)
    # print("Published date:", yt.publish_date.strftime("%Y-%m-%d"))
    # print("Number of views:", yt.views)
    # print("Length of video:", yt.length, "seconds")
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

window.geometry("420x420")  # Size 420px x 420px
window.title("Youtube Downloader")

icon = PhotoImage(file="images/yt_icon.png")
window.iconphoto(True, icon)

# change background color
window.config(
    background="#777f85"
)  # or you can search google with "hex color picker" keyword

# Code in here ....................
# Create a entry box to user paste the youtube link
# Link test https://www.youtube.com/watch?v=_8vekzCF04Q&pp=ygUNdmFuIG1haSBodW9uZw%3D%3D

yt_link = Entry(
    window,
    width=50,
)
yt_link.pack()

yt_linkVideo = Button(window, text="Get MP4 Video File", command=getVideo)
yt_linkVideo.pack()

yt_linkMP3 = Button(window, text="Get MP3 Audio", command=getMP3)
yt_linkMP3.pack()

yt_linkAAC = Button(window, text="Get AAC Audio", command=getAAC)
yt_linkAAC.pack()


window.mainloop()  # Place window o computer screen, listen for events.
