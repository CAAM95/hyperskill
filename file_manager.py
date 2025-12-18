import os
import shutil


os.chdir("./module/root_folder")

#cd C:\folder1\folder2
#cd folder2

def cd(arg):
    if arg == "..":
        os.chdir('..')
        print(os.path.basename(os.getcwd()))
        return

    if not arg:
        print("No path provided")
        return

    if not os.path.isabs(arg):
        arg = os.path.join(os.getcwd(), arg)

    if os.path.exists(arg) and os.path.isdir(arg):
        os.chdir(arg)
        print(os.path.basename(os.getcwd()))
    else:
        print("Path does not exist")


def convert_bytes(value):
    value = int(value)
    if value < 1024:
        value = f"{value}B"
    elif value < 1024 ** 2:
        value = f"{round(value / 1024)}KB"
    elif value < 1024 ** 3:
        value = f"{round(value / (1024 ** 2))}MB"
    else:
        value = f"{round(value / (1024 ** 3))}GB"

    return value


def ls(command):
    possible_args = ["", "-l", "-lh"]
    item_names = []

    if command not in possible_args:
        print("Invalid command")
        return

    for item in os.listdir(os.getcwd()):
        full_path = os.path.join(os.getcwd(), item)
        if os.path.isdir(full_path):
            item_names.append(full_path)

    for item in os.listdir(os.getcwd()):
        full_path = os.path.join(os.getcwd(), item)
        if os.path.isfile(full_path):
            item_names.append(full_path)

    if command == possible_args[0]:
        for path in item_names:
            print(f"{path}")
        return

    if command == possible_args[1]:
        for path in item_names:
            if os.path.isfile(path):
                print(f"{path} {os.stat(path).st_size}")
            else:
                print(f"{path}")
        return

    if command == possible_args[2]:
        for path in item_names:
            if os.path.isfile(path):
                print(f"{path} {convert_bytes(os.stat(path).st_size)}")
            else:
                print(f"{path}")
        return


def rm(command):
    if not command:
        print("Specify the file or directory")
        return

    if command.startswith("."):
        extension = command
        found_file = remove_file_with_ext(extension, os.getcwd())
        if not found_file:
            print(f"File extension {extension} not found in this directory")
            return
    else:
        if not os.path.isabs(command):
            path = os.path.join(os.getcwd(), command)

        if not os.path.exists(path):
            print("No such file or directory")
            return

        if os.path.isdir(path):
            shutil.rmtree(path)
            return

        if os.path.isfile(path):
            os.remove(path)
            return


def mv(command):
    if not command:
        print("Specify the current name of the file or directory and the new location and/or name")
        return

    tokens = command.split()

    if len(tokens) < 2:
        print("Specify the current name of the file or directory and the new location and/or name")
        return

    if tokens[0].startswith("."):
        extension = tokens[0]
        found_file = move_file_with_ext(extension, os.getcwd(), tokens[1])
        if not found_file:
            print(f"File extension {extension} not found in this directory")
            return
    else:


        source = os.path.join(os.getcwd(), tokens[0])
        destination = os.path.join(os.getcwd(), tokens[1])

        if not os.path.exists(source):
            print("No such file or directory")
            return

        if os.path.exists(destination) and os.path.isfile(destination):
            print("The file or directory already exists")
            return

        if os.path.isfile(source) and os.path.isdir(destination): #folder to dir
            shutil.move(source, destination)
            return

        if os.path.isfile(source) and not os.path.isdir(destination): #file and file
            shutil.move(source, destination)
            return



def mkdir(command):
    if not command:
        print("Specify the name of the directory to be made")
        return

    if not os.path.isabs(command):
        command = os.path.abspath(command)

    if os.path.exists(command):
        print("The directory already exists")
        return

    os.makedirs(command)

def move_file_with_ext(extension, source, destination):
    found = False
    for name in os.listdir(source):
        source_path = os.path.join(source, name)
        destination_path = os.path.join(destination, name)
        if os.path.isfile(source_path) and source_path.endswith(extension):
            if os.path.exists(destination_path):
                print(f"{os.path.basename(source_path)} already exists in this directory. Replace? (y/n)")
                user_input = input()
                if user_input == "y":
                    shutil.move(source_path, destination_path)
                elif user_input == "n":
                    continue
            else:
                shutil.move(source_path, destination_path)
            found = True
    return found

def remove_file_with_ext(extension, directory):
    found = False
    for name in os.listdir(directory):
        full_path = os.path.join(directory, name)
        if os.path.isfile(full_path) and full_path.endswith(extension):
            os.remove(full_path)
            found = True
    return found

def copy_file_with_ext(extension, source, destination):
    found = False
    for name in os.listdir(source):
        source_path = os.path.join(source, name)
        destination_path = os.path.join(destination, name)
        if os.path.isfile(source_path) and source_path.endswith(extension):
            if os.path.exists(destination_path):
                print(f"{os.path.basename(source_path)} already exists in this directory. Replace? (y/n)")
                user_input = input()
                if user_input == "y":
                    shutil.copy2(source_path, destination_path)
                elif user_input == "n":
                    continue
            else:
                shutil.copy2(source_path, destination_path)
            found = True
    return found

def cp(command):
    current_dir = os.getcwd()
    command = command.split(" ")


    try:
        source = command[0]
        destination = command[1]
        if destination == "..":
            destination = os.path.dirname(os.getcwd())
    except (IndentationError, IndexError):
        print("Specify the file")
        return

    if len(command) > 2:
        print("Specify the current name of the file or directory and the new location and/or name")
        return


    if source.startswith("."):
        extension = source
        found_file = copy_file_with_ext(extension, os.getcwd(), destination)
        if not found_file:
            print(f"File extension {extension} not found in this directory")
            return
    else:
        if not os.path.isabs(source):
            source = os.path.join(current_dir, source)

        if not os.path.isabs(destination):
            destination = os.path.join(current_dir, destination)


        if not os.path.exists(source):
            print("No such file or directory")
            return

        if not os.path.exists(destination):
            print("No such file or directory")
            return

        for var in os.listdir(destination):
            if os.path.abspath(var) == source:
                print(f"{os.path.basename(source)} already exists in this directory")
                return

        if os.path.isfile(source) and os.path.isdir(destination):
            shutil.copy(source, destination)
            return

        if os.path.isdir(source) and os.path.isdir(destination):
            shutil.copy(source, destination)
            return

        print("cant do file to file or folder to file")


while True:
    user_input = input().strip()
    if not user_input:
        print("Invalid command")
        continue

    cmd = user_input.split()[0].lower()
    args = user_input[len(cmd):].strip()

    if cmd == "pwd":
        print(os.getcwd())
    elif cmd == "cd":
        cd(args)
    elif cmd == "ls":
        ls(args)
    elif cmd == "rm":
        rm(args)
    elif cmd == "mv":
        mv(args)
    elif cmd == "mkdir":
        mkdir(args)
    elif cmd == "cp":
        cp(args)
    elif cmd == "quit":
        break
    else:
        print("Invalid command")
