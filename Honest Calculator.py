msg_0 = "Enter an equation"

msg_1 = "Do you even know what numbers are? Stay focused!"

msg_2 = "Yes ... an interesting math operation. You've slept through all classes, haven't you?"

msg_3 = "Yeah... division by zero. Smart move..."

msg_4 = "Do you want to store the result? (y / n):" 

msg_5 = "Do you want to continue calculations? (y / n):"

msg_6 = " ... lazy"

msg_7 = " ... very lazy"

msg_8 = " ... very, very lazy"

msg_9 = "You are"

msg_10 = "Are you sure? It is only one digit! (y / n)"

msg_11 = "Don't be silly! It's just one number! Add to the memory? (y / n)"

msg_12 = "Last chance! Do you really want to embarrass yourself? (y / n)"

def is_one_digit(v):
    if v > -10 and v < 10 and type(v) == int:
        return True
    else:
        return False

def check_operation(v1, v2, v3):
    msg = ""

    if is_one_digit(v1) and is_one_digit(v2):
        msg = msg + msg_6
    
    if v1 == 1 or v2 == 1:
        msg = msg + msg_7
    
    if (v1 == 0 or v2 == 0) and (v3 == "*" or v3 == "+" or v3 == "-"):
        msg = msg + msg_8
    
    if msg != "":
        msg = msg_9 + msg
        print(msg)

    
    

memory = 0
while True:
    print(msg_0)
    calc = input().split(" ")
    
    result = 0

    x = calc[0]
    oper = calc[1]
    y = calc[2]

    if x == "M":
        x = memory
    if y == "M":
        y = memory


    try:
        x = float(x)
        y = float(y)
        if x.is_integer(): 
            x = int(x)
        if y.is_integer(): 
            y = int(y)
    except ValueError:
        print(msg_1)
        continue
        

    
    if len(oper) != 1 or oper not in ["*", "+", "-", "/"]:
        print(msg_2)
        continue

    check_operation(x, y, oper)

    if oper == "+":
        result = x + y
    elif oper == "-":
        result = x - y
    elif oper == "*":
        result = x * y
    elif oper == "/" and y != 0:
        result = x / y
    else:
        print(msg_3)
        continue

    print(float(result))

    while True:
        print(msg_4)
        msg_4_response = input()

        if msg_4_response == "n":
            break

        if msg_4_response == "y":
            if not is_one_digit(result):
                memory = float(result)
                break

            msg_index = 10
            while True:
                current_msg = globals().get(f"msg_{msg_index}")
                if current_msg is None:
                    break

                print(current_msg)
                answer = input()

                if answer == "y":
                    if msg_index < 12:
                        msg_index += 1
                    else:
                        memory = float(result)
                        break
                    
                
                if answer == "n":
                    break
        break 

    while True:
        print(msg_5)
        msg_5_response = input()
    
        if msg_5_response == "y":
            break
        elif msg_5_response == "n":
            exit()
