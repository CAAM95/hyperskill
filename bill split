import math
import random

def who_is_lucky(dict):
    temp_list = []
    for key in dict.keys():
        temp_list.append(key)
    lucky_person = random.choice(temp_list)
    return lucky_person

print("Enter the number of friends joining (including you):")
num_users = int(input())
user_dict = dict()
bill = 0

if num_users <= 0:
    print("No one is joining for the party")
else:
    print("Enter the name of every friend (including you), each on a new line:")
    
    for i in range(num_users):
        person = input()
        user_dict[person] = 0
        
    print('Enter the total bill value:')
    bill = int(input())
        
    print('Do you want to use the "Who is lucky?" feature? Write Yes/No:')
    choice = input()
    
    if choice == 'Yes':
        bill_split = bill / (num_users - 1)
        
        for key, value in user_dict.items():
            user_dict[key] = round(bill_split, 2)
            
        person = who_is_lucky(user_dict)
        print('{} is the lucky one!'.format(person))
        temp_dict = dict()
        temp_dict.update(user_dict)
        
        for key in temp_dict.keys():
            if key == person:
                temp_dict[key] = 0
                break
                
        print(temp_dict)
        
    elif choice == 'No':
        bill_split = bill / num_users
        
        for key, value in user_dict.items():
            user_dict[key] = round(bill_split, 2)
            
        print('No one is going to be lucky')
        print(user_dict)


