import requests
import threading
from urllib.parse import urlparse
import os

def download(link, directory, filename):
    path = urlparse(link).path
    ext = os.path.splitext(path)[1]

    dir_file = os.path.join(directory, filename + ext)

    if link.startswith("file://"):
        local_path = link[len("file://"):]
        with open(local_path, "rb") as src_file, open(dir_file, "wb") as dst_file:
            dst_file.write(src_file.read())
    else:
        r = requests.get(link, stream=True)
        with open(dir_file, "wb") as file:
            for chunk in r.iter_content(1024):
                if chunk:
                    file.write(chunk)

def createthread(nb_thread, link, directory, filename):
    if nb_thread > 99:
        print("The number of threads is too high. Please correct the number using the 'thd' command.")
    else:
        for i in range(nb_thread):
            threads = threading.Thread(target=download, args=(link, directory, filename))
            threads.start()


with open("setup.txt", "r") as file:
    content = file.readline()
    try:
        path, thread = content.split(";")
        thread = int(thread)
    except ValueError:
        file.close()
        file = open("setup.txt", "r+")
        print("The 'setup.txt' configuration file is corrupted. It will be reset to default settings.")
        file.write(f"{os.path.join(os.path.expanduser('~'), 'downloads')};10")
        file.close()
        file = open("setup.txt", "r")
        content = file.readline()
        path, thread = content.split(";")
        thread = int(thread)
        file.close()

    file.close()

print("Welcome to your download manager!")
print(f"The current number of threads is {thread}")
print(f"The download directory path is: {path}")
print("To download: dl *link*")
print("To configure the download directory: dir *path*")
print("To configure the number of threads: thd *number between 0 and 99*")

while True:
    command = input(">")

    if command[0:2] == "dl":
        _, link, filename = command.split(" ")
        createthread(thread, link, path, filename)
    elif command[0:3] == "thd":
        _, new_thd = command.split(" ")
        setup_file = open("setup.txt", "r+")
        setup_data = setup_file.read()
        setup_data = setup_data.replace(str(thread), new_thd)
        setup_file.seek(0)
        setup_file.truncate()
        setup_file.write(setup_data)
        setup_file.close()
        print(f"The number of threads has been changed from {thread} to {new_thd}")
        with open("setup.txt", "r") as file:
            content = file.readline()
            path, thread = content.split(";")
            thread = int(thread)
            file.close()
    elif command[0:3] == "dir":
        _, new_path = command.split(" ")
        setup_file = open("setup.txt", "r+")
        setup_data = setup_file.read()
        semicolon_index = setup_data.find(";")
        old_path_index = setup_data[:semicolon_index]
        setup_data = setup_data.replace(old_path_index, new_path)
        print(setup_data)
        setup_file.seek(0)
        setup_file.truncate()
        setup_file.write(setup_data)
        setup_file.close()
    elif command == "exit":
        print("Goodbye!")
        break
    else:
        print("Unrecognized command.")
