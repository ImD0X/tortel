import os
import stem
import zipfile
from progressbar import ProgressBar, Percentage, Bar
from urllib.request import urlretrieve
from time import sleep
import stem.client
import stem.connection
import stem.control
import stem.process
from art import *


TOR_EXP_URL = "https://github.com/matinrco/tor/releases/download/v0.4.5.10/tor-expert-bundle-v0.4.5.10.zip"
TOR_ZIP_FILENAME = "tor-expert-bundle.zip"
tordl_progress_bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=100)


BANNER = "TORTEL"


def banner():
    tprint(BANNER)
    print("Ver 1.0.2                 ")
    print("TG: @itsd0x")
    print("A Tor local proxy, Anonymous and free of Ads!")
    print("= = = = = = =" * 4)


def update_progress(count, block_size, total_size):
    if total_size > 0:
        percent = int(count * block_size * 100 / total_size)
    else:
        percent = 0
    tordl_progress_bar.update(percent)


def download_tor_exp():
    print("Downloading Tor... \n")
    sleep(1.5)
    if not os.path.isfile(path=f"./{TOR_ZIP_FILENAME}") and not os.path.isdir(
        "./tor-files"
    ):
        tordl_progress_bar.start()
        urlretrieve(
            url=TOR_EXP_URL, filename=TOR_ZIP_FILENAME, reporthook=update_progress
        )
        tordl_progress_bar.finish()
        if os.path.isfile(path=f"./{TOR_ZIP_FILENAME}"):
            unzip_install_tor()
        else:
            print("Trying again...")
            download_tor_exp()
    else:
        print("Tor is already exist...")
        sleep(3)
        clsterm()
        banner()


def unzip_install_tor():
    torzip = zipfile.ZipFile(f"./{TOR_ZIP_FILENAME}")
    os.mkdir("tor-files")
    torzip.extractall("./tor-files")
    torzip.close()
    os.remove(f"./{TOR_ZIP_FILENAME}")
    os.rename("./tor-files/tor-real.exe", "./tor-files/tor.exe")

    print("Files Extracted and Ready to Launch...")
    sleep(2)


def launch_tor():
    input("Press ENTER to launch Tor SOCKS5 Local Proxy")
    clsterm()
    banner()
    os.chdir("./tor-files")
    global tor_service
    tor_service = stem.process.subprocess.Popen(
        args=["tor"],
        universal_newlines=True,
        stderr=stem.process.subprocess.PIPE,
        stdout=stem.process.subprocess.PIPE,
    )
    tasklist = stem.process.subprocess.Popen(
        ["tasklist"],
        universal_newlines=True,
        text=True,
        stderr=stem.process.subprocess.PIPE,
        stdout=stem.process.subprocess.PIPE,
    ).stdout.read()
    if "tor.exe" in tasklist:
        print("Tor Has Been Launched Successfully!")
        print(
            "Proxy (SOCKS5) Address: 127.0.0.1\nProxy (SOCKS5) Port: 9050\n[!] Press Ctrl + C to Exit"
        )
    else:
        exit("Error in launching tor!")


def clsterm():
    os.system("cls || clear")


def main():
    banner()
    download_tor_exp()
    launch_tor()
    while True:
        sleep(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exiting...")
        stem.process.subprocess.call(
            args=["taskkill", "/IM", "tor.exe"],
            stderr=stem.process.subprocess.DEVNULL,
            stdout=stem.process.subprocess.DEVNULL,
        )
