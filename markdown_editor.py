
def plain(txt):
    return txt

def bold(txt):
    return "**" + txt + "**"

def italic(txt):
    return "*" + txt + "*"

def header():
    while True:
        level = input("Level: ")

        if level not in ["1", "2", "3", "4", "5", "6"]:
            print("The level should be within the range of 1 to 6")
            continue
        else:
            txt = input("Text: ")
            return "#" * int(level) + " " + txt + "\n"

def link():
    label = input("Label: ")
    url = input("URL: ")
    return "[" + label + "](" + url + ")"

def inline_code(txt):
    return "`" + txt + "`"

def new_line():
    return "\n"

def ordered_list():
    my_list = []
    while True:
        rows = input("Number of rows: ")
        if int(rows) <= 0:
            print("The number of rows should be greater than zero")
            continue
        else:
            for i in range(int(rows)):
                element_name = input('Row #' + str(i + 1) + ": ")
                my_list.append(str(i + 1) + '. ' + element_name)
            break
    return my_list


def unordered_list():
    my_list = []
    while True:
        rows = input("Number of rows: ")
        if int(rows) <= 0:
            print("The number of rows should be greater than zero")
            continue
        else:
            for i in range(int(rows)):
                element_name = input('Row #' + str(i + 1) + ": ")
                my_list.append('* ' + element_name)
            break
    return my_list

def done():
    with open("output.md", "w") as file:
        file.write(text)

text = ""  # Moved outside the loop to maintain state
while True:
    cmd = input("Choose a formatter: ")

    formatter = ["plain", "bold", "italic", "header", "link", "inline-code", "new-line", "ordered-list", "unordered-list"]
    if cmd in formatter:
        if cmd == "plain" or cmd == "bold" or cmd == "italic" or cmd == "inline-code":
            input_text = input("Text: ")
            if cmd == "plain":
                text += plain(input_text)
            elif cmd == "bold":
                text += bold(input_text)
            elif cmd == "italic":
                text += italic(input_text)
            elif cmd == "inline-code":
                text += inline_code(input_text)
        elif cmd == "header":
            text += header()
        elif cmd == "link":
            text += link()
        elif cmd == "new-line":
            text += new_line()
        elif cmd == "ordered-list":
            for element in ordered_list():
                text += element + "\n"
        elif cmd == "unordered-list":
            for element in unordered_list():
                text += element + "\n"
        print(text)
    elif cmd == "!help":
        print("Available formatters: plain bold italic header link inline-code new-line")
        print("Special commands: !help !done")
    elif cmd == "!done":
        done()
        break
    else:
        print("Unknown formatting type or command")
