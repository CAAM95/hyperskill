def preprocess(user_input):
    regex, user_string = user_input.split("|")
    return regex.strip(), user_string.strip()

def preprocess_beginning_end(regex, user_string):
    if regex == "":
        return True
    if user_string == "":
        return False

    # and regex[1] == user_string[0] and regex[-2] == user_string[-1] and " " not in user_string:
    if regex[0] == "^" and regex[-1] == "$" and recursion(regex[1], user_string[0]) and recursion(regex[-2], user_string[-1]) and " " not in user_string: # recursion(regex[1], user_string[0]) and recursion(regex[-2], user_string[-1]):
        #print(regex[2:-1], user_string[1:])
        return recursion(regex[1:-1], user_string)
    elif regex[0] == "^":
        return recursion(regex[1:], user_string[:len(regex) - 1])
    elif regex[-1] == "$":
        if "\\" in regex:
            regex = regex.replace("\\", "")
            return recursion(regex[:-1], user_string[-len(regex) + 1:])
        return recursion(regex[:-1], user_string[-len(regex) + 1:])
    else:
        return is_substring(regex, user_string)

def is_substring(regex, user_string):
    if regex == "":
        return True
    if user_string == "":
        return False
    for i in range(len(user_string)):
        if recursion(regex, user_string[i:]):
            return True
    return False

def recursion(regex, word):
    if regex == "": # true because consumed
        return True
    if word == "":
        return False
    if len(regex) > 1 and regex[0] == "\\":
        if regex[1] == word[0]:
            return recursion(regex[2:], word[1:])
        return False
    if len(regex) > 1 and regex[1] == "?":
        if recursion(regex[2:], word):
            return True
        if regex[0] == word[0]:
            return recursion(regex[2:], word[1:])
        return False
    if len(regex) > 1 and regex[1] == "*":
        if recursion(regex[2:], word):
            return True
        if regex[0] == word[0]:
            return recursion(regex, word[1:])
        if recursion(regex, word[1:]):
            return True
    if len(regex) > 1 and regex[1] == "+":
        if regex[0] == word[0] or regex[0] == ".":
            return (recursion(regex, word[1:]) or recursion(regex[2:], word[1:]))
        return False
    if regex[0] == ".":
        return recursion(regex[1:], word[1:])
    if regex[0] == word[0]:
        return recursion(regex[1:], word[1:])
    return False

def main():
    user_input = input()
    regex, word = preprocess(user_input)
    print(preprocess_beginning_end(regex, word))

if __name__ == "__main__":
    standard_input = "colou\?r|colour"
    main()
