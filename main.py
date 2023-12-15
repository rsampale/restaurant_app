from customer import process_customer_order
from manager import process_manager_commands

# Define a couple restaurants with some base items (items can be added or removed later)

default_rest = {
    "name" : "Frank's Fantastic Bites",
    "food" : {
        "Burger" : [8.0, False],
        "Grilled Cheese" : [6.0, False],
        "Chicken Noodle Soup" : [4.5, False],
        "BBQ Brisket" : [11.5, False],
        "Chicken Fingers" : [5.0, False],
        "Soup of The Day" : [10.25, True],
        "Pepper Steak" : [32.0, True]
    },
    "drink" : {
        "Coke" : [2.50, False],
        "Apple Juice" : [3.50, False],
        "Chocolate Milk" : [3.50, False],
        "Banana Smoothie" : [4.00, False],
        "Milkshake" : [4.50, False],
        "Champagne" : [16.75, True]
    },
    "dessert" : {
        "Chocolate Cake" : [6.50, False],
        "Apple Pie" : [6.00, False],
        "Ice Cream" : [4.00, False],
        "Churros" : [5.50, True],
        "Chocolate Lava Cake": [6.0, True]
    }
}

second_rest = {
    "name" : "Sam's Fancy Diner",
    "food" : {
        "Oysters" : [44.5, False],
        "Baked Lasagna" : [31.0, False],
        "Wagyu Beef Steak" : [180.0, False],
        "Spanish Iberian Ham" : [3000.0, False],
        "Beluga Caviar" : [85.75, False],
        "Fugu" : [350.0, True],
        "Foie Gras" : [45.25, True]
    },
    "drink" : {
        "Pisco Sour" : [22.50, False],
        "French Martini" : [18.00, False],
        "Hemingway Daqiri" : [24.50, False],
        "Golden Cadillac" : [21.25, True],
        "Negroni" : [20.00, False],
        "Espresso Martini" : [16.5, False]
    },
    "dessert" : {
        "Chocolate Ganache" : [18.50, False],
        "Mixed Berry Compote" : [15.00, False],
        "French Apple Tart" : [22.00, False],
        "Classic Tiramisu" : [15.75, True],
        "Macarons": [12.00, False]
    }
}

restaurants = [default_rest, second_rest] # The list of restaurants

'''
BEGIN CUSTOMER MODE SELECTION LOOP BLOCK

Repeatedly prompt user for the mode they wish to use until they quit, and perform the duties 
required by each of those modes.

'''

while True:
    
    print("\nHello! Please enter the digit of the operating mode to be used:")
    print("\n'1': Customer Mode. Make orders from the restaurant menu.\n")
    print("'2': Manager Mode. Add, modify, or delete items from the menu.\n")
    print("'q': Quit.\n")
    
    mode_input = input("Mode: ")
    
    if mode_input == "1": ### CUSTOMER MODE ###
        
        invalid = True
        while invalid: # Make sure user gives a valid restaurant number
            print(f"\nWhich restaurant will you be shopping at?\n\nRESTAURANT LIST:\n")
            for i, rest in enumerate(restaurants):
                print(f"{i+1}: {rest['name']}")
            selected_rest = input("\nPLEASE SELECT THE RESTAURANT BY NUMBER: ")
            invalid = False
            if not selected_rest.isnumeric():
                invalid = True
            elif float(selected_rest) > len(restaurants) or float(selected_rest) <= 0: # Number can't be more or less than the number of restaurants
                invalid = True
                
        rest_in_use = restaurants[int(selected_rest)-1] # create a var for the dictionary object for the restaurant in use
        
        process_customer_order(rest_in_use) # This function handles all customer inputs and commands, imported from customer.py
        
    elif mode_input == "2": ### MANAGER MODE ###
        
        invalid = True
        while invalid: # Make sure user gives a valid restaurant number (same as above)
            print(f"\nWhich restaurant are you the manager at?\n\nRESTAURANT LIST:\n")
            for i, rest in enumerate(restaurants):
                print(f"{i+1}: {rest['name']}")
            selected_rest = input("\nPLEASE SELECT THE RESTAURANT BY NUMBER: ")
            invalid = False
            if not selected_rest.isnumeric():
                invalid = True
            elif float(selected_rest) > len(selected_rest) or float(selected_rest) <= 0:
                invalid = True
        
        process_manager_commands(restaurants[int(selected_rest)-1] ) # This function handles all manager inputs and commands, imported from manager.py
        
    elif mode_input.lower() == "q": # Exit if user wants to
        break
    else:
        print("\nPlease enter a VALID operating mode.\n")