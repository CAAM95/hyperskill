import requests

# get user input currency holding
user_currency1 = input().lower()
user_currency1 = user_currency1.lower()

data = requests.get(f'http://www.floatrates.com/daily/{user_currency1}.json').json()
cache = {}

# Filter for USD and EUR
currencies = ['usd', 'eur']  # The keys are in lowercase
for code in currencies:
    if code in data:
        cache[code] = data[code]


while True:
    # currency to change to
    user_currency2 = input().lower()
    
    # Exit if user enters nothing
    if not user_currency2:
        break
        
    currency1_amt = float(input())

    print('Checking the cache...')

    if user_currency2 in cache:
        print('Oh! It is in the cache!')
        conversion = currency1_amt * cache[user_currency2]['rate']
        print(f'You received {conversion:.2f} {user_currency2.upper()}.')
    else:
        print('Sorry, but it is not in the cache!')
        cache[user_currency2] = data[user_currency2]
        conversion = currency1_amt * cache[user_currency2]['rate']
        print(f'You received {conversion:.2f} {user_currency2.upper()}.')
