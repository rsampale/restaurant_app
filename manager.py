from customer import price_from_item_on_menu, matching_rest_key, display_menu # import a view dependencies from the customer file

'''
manager_add_remove()

Takes a restaurant dictionary, add or remove command, item name, and a [price, special] list (price, and a boolean True/False value).
If the item isn't already on the menu, and the command was to add - it will create an item on the menu with a given food type and the 
[price, special] value. If the command was to remove an item, a check is done to see if it is on the menu, and the appropriate key:value
pair is deleted.

'''

def manager_add_remove(rest_dict, add_or_remove, item, price_special):
    
    # Check to see if item is on the menu already
    on_menu_check = price_from_item_on_menu(rest_dict, item) # will return negative if not on the menu already
    
    if add_or_remove == "add":
        if on_menu_check < 0: # Can add if the item isn't on the menu already
            food_type = input("Is your item a food, drink, or dessert? (Type 'food'/'drink'/'dessert'): ").lower()
            # CONFIRM SELECTION:
            print(f"\nYou are trying to add the following special:\n")
            print(f"- {item} --- ${price_special[0]:.2f}\n")
            confirm = input("\nARE YOU SURE YOU WANT TO ADD THIS ITEM? (Type 'yes' or 'quit'): ")
            if confirm.lower() == "yes":
                if food_type == "food" or food_type == "drink" or food_type == "dessert":
                    rest_dict[food_type][item] = price_special
                    print("\nITEM SUCCESSFULLY ADDED TO THE MENU.")
                else:
                    print("\nERROR: Next time please select a valid food type.")
            else:
                print("\nItem adding attempt abandoned.")
                return
        else:
            print("\nERROR: Cannot add an item that is already on the menu.")
                
    else: # if removing an item
        if on_menu_check > 0: # Can only remove if the item is actually on the menu
            # CONFIRM SELECTION:
            print(f"\nYou are trying to remove the following special:\n")
            print(f"- {item} --- ${on_menu_check:.2f}\n")
            confirm = input("\nARE YOU SURE YOU WANT TO REMOVE THIS ITEM? (Type 'yes' or 'quit'): ")
            if confirm.lower() == "yes":
                # Go through food, drink, and dessert categories until you find the item and then delete it
                properly_spelled_item = matching_rest_key(rest_dict, item)
                for food in rest_dict['food']:
                    if food == properly_spelled_item:
                        del rest_dict['food'][food]
                        print("\nITEM SUCCESSFULLY REMOVED FROM THE MENU.")
                        return
                for drink in rest_dict['drink']:
                    if drink == properly_spelled_item:
                        del rest_dict['drink'][drink]
                        print("\nITEM SUCCESSFULLY REMOVED FROM THE MENU.")
                        return
                for dessert in rest_dict['dessert']:
                    if dessert == properly_spelled_item:
                        del rest_dict['dessert'][dessert]
                        print("\nITEM SUCCESSFULLY REMOVED FROM THE MENU.")
                        return
            else:
                print("\nItem removal attempt abandoned.")
                return
        else:
            print("\nERROR: Cannot remove an item that isn't on the menu.")
    
    return

'''
manager_modify_specials()

Takes a restaurant dictionary as an argument. Lets the user add or remove specials from the menu, and see all the current specials.
Uses the manager_add_remove() function defined above for the adding or removing of these special items.

'''

def manager_modify_specials(rest_dict):
    while True:
        inp = input("\n'1': Add a special to the menu.\n'2': Remove an existing special.\n'3': View current specials.\n'q': QUIT\n\nSELECTION: ")
        if inp.lower() == "q":   
            break
        elif inp == "1": # ADD A SPECIAL
            item_toadd = input("Enter the NAME of the item you want to add: ")
            try: # Make sure user gives proper price number
                item_toadd_price = float(input ("Enter the PRICE of the added item as a decimal (e.g. $5.0, or $2.50): "))
                manager_add_remove(rest_dict,"add",item_toadd,[item_toadd_price, True])
            except ValueError:
                print("\nERROR: Please enter a valid price number.")
            
        elif inp == "2": # REMOVE A SPECIAL
            item_toremove = input("Enter the NAME of the item you want to remove: ")
            
            manager_add_remove(rest_dict,"remove",item_toremove,[999, True]) # Placeholder price 999 just so we have some value to pass, price not needed for removal
            
        elif inp == "3": # DISPLAY ALL CURRENT SPECIALS
            print(f"Here are the current specials:\n")
            combined_menu = {**rest_dict['food'], **rest_dict['drink'], **rest_dict['dessert']}
            for item, price_special in combined_menu.items():
                if price_special[1] == True:
                    print(f"- {item} --- ${price_special[0]}")
        else:
            print("\nERROR - INVALID SELECTION\n")
    return

'''
manager_change_price()

Takes a restaurant dictionary. Allows the user to provide an item name from the restaurant menu, and modify its price.
Directly changes the value found at that key within the restaurant dictionary.

'''

def manager_change_price(rest_dict):
    print(f"\nHere is the current menu:\n")
    display_menu(rest_dict)
    while True:
        inp = input("\nType the name of the item you want to change, or type 'q' to exit: ")
        if inp == 'q':
            break
        properly_spelled_item_key = matching_rest_key(rest_dict, inp) # is None if the item doesn't exist
        if not properly_spelled_item_key:
            print("\nERROR: That item was not on the menu.")
        else:
            old_price = price_from_item_on_menu(rest_dict, properly_spelled_item_key) # Get old price
            new_price_string = input(f"\nThe current price is ${old_price}. Please enter the new price (as a decimal with no dollar sign): ")
            try:
                new_price_num = float(new_price_string)
                # Go through food, drink, and dessert categories until you find the item and then change its price
                for food in rest_dict['food']:
                    if food == properly_spelled_item_key:
                        rest_dict['food'][food] = [new_price_num, False]
                        print(f"\nPRICE OF {food} CHANGED SUCCESSFULLY.")
                for drink in rest_dict['drink']:
                    if drink == properly_spelled_item_key:
                        rest_dict['drink'][drink] = [new_price_num, False]
                        print(f"\nPRICE OF {drink} CHANGED SUCCESSFULLY.")
                for dessert in rest_dict['dessert']:
                    if dessert == properly_spelled_item_key:
                        rest_dict['dessert'][dessert] = [new_price_num, False]
                        print(f"\nPRICE OF {dessert} CHANGED SUCCESSFULLY.")
            except ValueError:
                print("\nERROR: Please enter a valid price number.")
            
'''
process_manager_commands()

Takes a restaurant dictionary as an argument. This is the main logic and command prompting loop for the manager mode. Allows the
user to give a number corresponding to the command they wish to use. They can either add items to the menu, remove them from the menu,
view the current menu, change the specials, change item prices, or quit. Each user selection employs the appropriate function(s) defined
above.

'''

def process_manager_commands(rest_dict):
    
    print(f"\nYou are in the {rest_dict['name']} manager menu. Please select a command:\n")
    while True:
        inp = input("\n'1': Add an item to the menu\n'2': Delete an item from the menu\n'3': Show the current menu\n'4': Modify specials\n'5': Change price of a menu item\n'q': QUIT\n\nSELECTION: ")
        if inp.lower() == "q":   
            break
        elif inp == "1": # ADD AN ITEM TO THE MENU
            
            item_toadd = input("Enter the NAME of the item you want to add: ")
            try:
                item_toadd_price = float(input ("Enter the PRICE of the added item as a decimal, WITHOUT the dollar sign (e.g. 5.0, or 2.50): "))
                manager_add_remove(rest_dict,"add",item_toadd,[item_toadd_price, False])
            except ValueError:
                print("\nERROR: Please enter a valid price number.")
            
        elif inp == "2": # REMOVE AN ITEM FROM THE MENU
            
            item_toremove = input("Enter the NAME of the item you want to remove: ")
            manager_add_remove(rest_dict,"remove",item_toremove,[999, False]) 
             
        elif inp == "3": # SHOW THE CURRENT MENU
            display_menu(rest_dict)
        elif inp == "4": # ADD/REMOVE SPECIALS
            manager_modify_specials(rest_dict)
        elif inp == "5": # CHANGE ITEM PRICES
            manager_change_price(rest_dict)
        else:
            print("\nERROR - INVALID SELECTION\n")
        
    return