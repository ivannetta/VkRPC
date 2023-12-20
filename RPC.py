import requests
from bs4 import BeautifulSoup
import re
from pypresence import Presence
import time
import os
from colorama import Fore, Back, Style
import ctypes

cfp = "config.txt"

try:
    with open(cfp, "r") as file:
        username = file.read().strip()
        if not username:
            raise ValueError("Username is empty in config.txt")

except FileNotFoundError:
    print(f"Config not found. Please enter your VK username:")
    username = input().strip()

    with open(cfp, "w") as file:
        file.write(username)

link = f"https://vk.com/{username}"
print("Your link is", link, "crazy")
url = link


def set_cmd_window_size(width, height):
    std_output_handle = -11
    handle = ctypes.windll.kernel32.GetStdHandle(std_output_handle)
    buf_size = ctypes.wintypes._COORD(width, height)
    ctypes.windll.kernel32.SetConsoleScreenBufferSize(handle, buf_size)
    rect = ctypes.wintypes.SMALL_RECT(0, 0, width - 1, height - 1)
    ctypes.windll.kernel32.SetConsoleWindowInfo(handle, True, ctypes.byref(rect))


width, height = 43, 20
set_cmd_window_size(width, height)

RPC = Presence(client_id="1184547216287862844")
RPC.connect()


def pro():
    print(
        Fore.CYAN
        + """
██╗░░░██╗██╗░░██╗  ██████╗░██████╗░░█████╗░
██║░░░██║██║░██╔╝  ██╔══██╗██╔══██╗██╔══██╗
╚██╗░██╔╝█████═╝░  ██████╔╝██████╔╝██║░░╚═╝
░╚████╔╝░██╔═██╗░  ██╔══██╗██╔═══╝░██║░░██╗
░░╚██╔╝░░██║░╚██╗  ██║░░██║██║░░░░░╚█████╔╝
░░░╚═╝░░░╚═╝░░╚═╝  ╚═╝░░╚═╝╚═╝░░░░░░╚════╝░



    """
        + Fore.WHITE
    )


def clear():
    if os.name == "nt":
        os.system("cls")
        os.system("title VkRPC")
    else:
        os.system("clear")


DEFAULT_LARGE_IMAGE_URL = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/VK_Compact_Logo_%282021-present%29.svg/2048px-VK_Compact_Logo_%282021-present%29.svg.png"
DEFAULT_SMALL_IMAGE_URL = "https://media1.tenor.com/m/6NRM5QqZja8AAAAC/boykisser.gif"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
old_audio_id = "null"
while True:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            soup = BeautifulSoup(response.content, "html.parser")
            script_tag = soup.find(
                "script",
                {"type": "text/javascript"},
                string=lambda s: "status_audio" in str(s),
            )

            if script_tag:
                script_content = script_tag.string
                match = re.search(
                    r'"artist":"([^"]+)","id":(\d+),"owner_id":(-?\d+),"title":"([^"]+)","duration":(\d+)',
                    script_content,
                )

                if match:
                    artist = match.group(1)
                    title = match.group(4)
                    duration = match.group(5)
                    audio_id = match.group(2)
                    owner_id = match.group(3)
                    clear()
                    pro()
                    print(f"Artist: {artist}")
                    print(f"Title: {title}")
                    print(f"Duration: {duration}")
                    print(f"Audio ID: {audio_id}")
                    print(f"Owner ID: {owner_id}")

                    if audio_id == old_audio_id:
                        time.sleep(15)
                        continue
                    old_audio_id = audio_id

                    titleReady = requests.get(
                        f"https://vk.com/audio{owner_id}_{audio_id}", headers=headers
                    )
                    imgSoup = BeautifulSoup(titleReady.content, "html.parser")

                    imageUrl = DEFAULT_LARGE_IMAGE_URL
                    img = imgSoup.select_one("div.AudioPlaylistSnippet__cover[style]")
                    if img:
                        print(img["style"].split("'")[1])
                        imageUrl = img["style"].split("'")[1]
                    RPC.update(
                        details=f"Listening to: {artist + ' ' + title}",
                        state="In VKontakte",
                        large_image=imageUrl if imageUrl else DEFAULT_LARGE_IMAGE_URL,
                        small_image=DEFAULT_SMALL_IMAGE_URL,
                        large_text="vk",
                        small_text="ivan",
                    )
                    print("rpc updated")
                else:
                    print("zesty error occurred couldent find regex thing")

            else:
                clear()
                pro()
                print("couldent find ur song, is ur broadcast on?")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"request died: {response.status_code}")
    time.sleep(3)
