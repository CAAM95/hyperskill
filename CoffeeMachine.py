
class CoffeeMachine:
    def __init__(self):
        self.water = 400
        self.milk = 540
        self.coffee = 120
        self.money = 550
        self.cups = 9
        self.inventory = [('espresso', [250, 0, 16, 4]),('latte', [350, 75, 20, 7]),('cappuccino', [200, 100, 12, 6])]

    def report_coffee_inventory(self):
        print('The Coffee machine has:')
        print(f"{self.water} ml of water")
        print(f"{self.milk} ml of milk")
        print(f"{self.coffee} g of coffee beans")
        print(f"{self.cups} disposable cups")
        print(f"${self.money} of money")

    def fill_machine(self, water, milk, coffee, cups):
        self.water += water
        self.milk += milk
        self.coffee += coffee
        self.cups += cups

    def purchase_beverage(self, beverage):
        self.water -= beverage[0]
        self.milk -= beverage[1]
        self.coffee -= beverage[2]
        self.money += beverage[3]
        self.cups -= 1
        
    def is_enough_resources(self, beverage):
        if self.water >= beverage[0] and self.milk >= beverage[1] and self.coffee >= beverage[2] and self.cups >= 1:
            print('I have enough resources, making you a coffee!')
            return True
        elif  self.water < beverage[0]:
            print('Sorry, not enough water!')
        elif self.milk < beverage[1]:
            print('Sorry, not enough milk!')
        elif self.coffee < beverage[2]:
            print('Sorry, not enough coffee!')
        elif self.cups < 1:
            print('Sorry, not enough cups!')
        return False

    def main(self):
        while True:
            print()
            user_input = input("Write action (buy, fill take):")
        
            if user_input == "buy":
                coffee_type = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino: ")

                if coffee_type == "back":
                    continue
                elif int(coffee_type) == 1 and self.is_enough_resources(self.inventory[0][1]):
                    self.purchase_beverage(self.inventory[0][1])
                elif int(coffee_type) == 2 and self.is_enough_resources(self.inventory[1][1]):
                    self.purchase_beverage(self.inventory[1][1])
                elif int(coffee_type) == 3 and self.is_enough_resources(self.inventory[2][1]):
                    self.purchase_beverage(self.inventory[2][1])
        
            elif user_input == "fill":
                water_amt = int(input("Write how many ml of water you want to add: "))
                milk_amt = int(input("Write how many ml of milk you want to add: "))
                coffee_amt = int(input("Write how many grams of coffee beans you want to add: "))
                cups_amt = int(input("Write how many disposable cups you want to add: "))
        
                self.fill_machine(water_amt, milk_amt, coffee_amt, cups_amt)
            elif user_input == "take":
                print(f"I gave you ${self.money}")
                self.money = 0
            elif user_input == "remaining":
                self.report_coffee_inventory()
            elif user_input == "exit":
                break

if __name__ == '__main__':
    CoffeeMachine().main()
