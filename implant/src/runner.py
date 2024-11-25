from src.error import *
from os import listdir
from PIL import ImageGrab

def run(command, allowed_commands, stop_event):
    if not command in allowed_commands:
        print("Not recognized command")
        return False
    else:
        match command:
            case "ls":
                return ls()
            case "kill":
                stop_event.set()
            case "create":
                create('tempfile.txt')
            case "screen":
                screen()
            case "screenshot":
                screen()
        return True


def ls():
    return listdir('.')


def create(path):
    try:
        with open(path, 'w') as file:
            file.close()
        return True
    except Error:
        return False


def screen():
    sc = ImageGrab.grab()
    sc.save("temp.png")
    sc.close()