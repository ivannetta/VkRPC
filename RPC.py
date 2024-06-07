import requests
from bs4 import BeautifulSoup
import re
from pypresence import Presence
import time
import os
from colorama import Fore
import ctypes
from tabulate import tabulate

cfp = "config.txt"


def GetStatus():
    try:
        with open("index.html", "r", encoding="utf-8") as file:
            html_content = file.read()
            match = re.search(r'"status_audio":\s*({.*?})', html_content, re.DOTALL)
            if match:
                status_audio_json = match.group(1)
                print("Found 'status_audio' in the HTML content:")
                print(status_audio_json)
                return status_audio_json
            else:
                print("where is status_audio")
    except Exception as e:
        print(f"cant read html: {e}")


try:
    with open(cfp, "r") as file:
        lines = file.read().strip().split("\n")
        if len(lines) < 2:
            raise ValueError("Invalid format in config.txt")
        username = lines[0].strip()
        lang = lines[1].strip()
        if not username:
            raise ValueError("Username is empty in config.txt")
        if not lang:
            raise ValueError("Language is empty in config.txt")

except FileNotFoundError:
    print(f"ваше имя пользователя VK, (vk username): ")
    username = input().strip()
    lang = input("выберите язык [RU/EN], (choose language [EN/RU]) : ").strip()

    with open(cfp, "w") as file:
        file.write(username + "\n" + lang)


def language():
    if lang.lower() == "en":
        return "en"
    elif lang.lower() == "ru":
        return "ru"
    else:
        return "en"


url = f"https://vk.com/{username}"


def set_cmd_window_size(width, height):
    std_output_handle = -11
    handle = ctypes.windll.kernel32.GetStdHandle(std_output_handle)
    buf_size = ctypes.wintypes._COORD(width, height)
    ctypes.windll.kernel32.SetConsoleScreenBufferSize(handle, buf_size)
    rect = ctypes.wintypes.SMALL_RECT(0, 0, width - 1, height - 1)
    ctypes.windll.kernel32.SetConsoleWindowInfo(handle, True, ctypes.byref(rect))


width, height = 43, 21
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
DEFAULT_SMALL_IMAGE_URL = "https://cdn.sussy.dev/augustf.gif"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
old_audio_id = "null"
while True:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            with open("index.html", "w", encoding="utf-8") as file:
                file.write(response.text)
            script_tag = GetStatus()
            if script_tag:
                match = re.search(
                    r'"artist":"([^"]+)","id":(\d+),"owner_id":(-?\d+),"title":"([^"]+)","duration":(\d+)',
                    script_tag,
                )

                if match:
                    artist = match.group(4)
                    title = match.group(1)
                    duration = match.group(5)
                    audio_id = match.group(2)
                    owner_id = match.group(3)

                    if not owner_id.startswith("-"):
                        owner_id = "-" + owner_id

                    clear()
                    pro()
                    if language() == "en":
                        data = [
                            ["Artist", artist],
                            ["Title", title],
                            ["Duration", duration],
                            ["Audio ID", audio_id],
                            ["Owner ID", owner_id],
                        ]
                    else:
                        data = [
                            ["Исполнитель", artist],
                            ["Название", title],
                            ["Длительность", duration],
                            ["ID аудиозаписи", audio_id],
                            ["ID владельца", owner_id],
                        ]

                    table = tabulate(
                        data,
                        tablefmt="rounded_grid",
                        numalign="center",
                        stralign="center",
                    )

                    print(table)

                    if audio_id == old_audio_id:
                        time.sleep(5)
                        continue
                    old_audio_id = audio_id

                    titleReady = requests.get(
                        f"https://vk.com/audio{owner_id}_{audio_id}", headers=headers
                    )

                    imgSoup = BeautifulSoup(titleReady.content, "html.parser")

                    imageUrl = DEFAULT_LARGE_IMAGE_URL
                    img = imgSoup.select_one("div.AudioPlaylistSnippet__cover[style]")
                    if img:
                        imageUrl = img["style"].split("'")[1]

                    if language() == "en":
                        Rdetail = f"Listening to: {title + ' by ' + artist}"
                        Rstate = "In VKontakte"
                    else:
                        Rdetail = f"Слушает: {title + ' от ' + artist}"
                        Rstate = "ВКонтакте"

                    RPC.update(
                        details=Rdetail,
                        state=Rstate,
                        large_image=imageUrl if imageUrl else DEFAULT_LARGE_IMAGE_URL,
                        small_image=DEFAULT_SMALL_IMAGE_URL,
                        large_text="vk",
                        small_text="ivan",
                    )
                else:
                    print("zesty error occurred couldent find regex thing")

            else:
                if language() == "ru":
                    clear()
                    pro()
                    print("не могу найти вашу песню, включена ли ваша трансляция?")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"request died: {response.status_code}")
    time.sleep(3)
