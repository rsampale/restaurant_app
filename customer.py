'''
display_menu()

Takes a restaurant dictionary and iterates through it, printing out every menu item and its
associated price. Does not show specials (these are shown through a different command)

'''

def display_menu(rest_dict):
    count = 1 # A counter variable put in front of each menu item, shows the customer how many items there are
    print(f"\nFOOD OPTIONS:")
    for food, price_special in rest_dict["food"].items():
        if price_special[1] == False: # Only show the non-special items
            print(f"{count}: {food} - ${price_special[0]}")
            count += 1
    print(f"\nDRINK OPTIONS:")
    for drink, price_special in rest_dict["drink"].items():
        if price_special[1] == False:
            print(f"{count}: {drink} - ${price_special[0]}")
            count += 1
    print(f"\nDESSERT OPTIONS:")
    for dessert, price_special in rest_dict["dessert"].items():
        if price_special[1] == False:
            print(f"{count}: {dessert} - ${price_special[0]}")
            count += 1
    return

'''
display_order()

Takes an order dictionary (item: [quantity,price]) and iterates through it, printing out every item and
associated price in the order. Both specials and normal menu items are shown.

'''

def display_order(order_dict):
    print("\nHERE IS YOUR CURRENT ORDER:\n")
    
    for item, quant_price in order_dict.items():
        print(f"{item} --- x{quant_price[0]} --- ${quant_price[1]}")
    return

'''
price_from_item_on_menu()

Takes a restaurant dictionary and an item name. If the item exists, it returns the price of that item.
If the item does not exist, it returns a unique negative value, -1.

'''

def price_from_item_on_menu(rest_dict, item): # Function returns price of an item on the menu if it is there, or -1 if not
    combined_menu = {**rest_dict['food'], **rest_dict['drink'], **rest_dict['dessert']}
    for key in combined_menu:
        if key.lower() == item.lower():
            return combined_menu[key][0]
    return -1

'''
matching_rest_key()

Takes a restaurant dictionary and an item name that is potentially not capitalized properly. If an item
with that name exists on the menu (including specials), it returns the correctly capitalized item name/key.
If no item with that name exists, it returns None.

'''

def matching_rest_key(rest_dict, item): # Function to find and return the 'properly spelled' version of a food item from the restaurant menu 
    combined_menu = {**rest_dict['food'], **rest_dict['drink'], **rest_dict['dessert']}
    for item2 in combined_menu.keys():
        if item2.lower() == item.lower():
            return item2  # Return the matching key from dict2
    return None # return none if not found

'''
add_to_order()

Takes a restaurant dictionary, order dictionary, an item name, and a quantity number/value. If the item is on the menu
(whether it is in the order or not), it will add the quantity amount of that item to the order. It always returns the order
dictionary, whether it has been changed or not.

'''

def add_to_order(rest_dict, order_dict, item, quant):
    try:
        quant = int(quant)
        price = price_from_item_on_menu(rest_dict, item)
        if price > 0:
            item = matching_rest_key(rest_dict, item) # Get properly spelled item, with proper capitalization
            if item in order_dict: # add to values if already there
                order_dict[item][0] += quant
                order_dict[item][1] += (price * quant)
            else:
                order_dict[item] = [0,0] # initialize empty quant and price list at the item index
                order_dict[item][0] = quant
                order_dict[item][1] = (price * quant)
        else:
            print("\nERROR: Item selected is not on the menu. Watch out for spelling.\n")
    except:
        print("\nERROR: Please select a valid number of items to add.\n")
        return order_dict
    return order_dict

'''
remove_from_order()

Takes a restaurant dictionary, order dictionary, an item name, and a quantity number/value. If the item is on the menu
AND already a part of the user's order, it will remove the quantity amount of that item from the order - completely deleting
it from the order if appropriate. Always returns the order dictionary, whether it has been changed or not.

'''

def remove_from_order(rest_dict, order_dict, item, quant):
    try:
        quant = int(quant)
        price = price_from_item_on_menu(rest_dict, item)
        
        # Check if item is actually in the current order:
        item_in_order = any(item.lower() == key.lower() for key in order_dict)
        
        if price > 0 and item_in_order:
            item = matching_rest_key(rest_dict, item) # Get properly spelled item, with proper capitalization
            if order_dict[item][0] <= quant:
                del order_dict[item] # If removing more or equal to the amount on the order, delete it from the order entirely
            else:
                order_dict[item][0] -= quant
                order_dict[item][1] -= (price * quant)
        else:
            print("\nERROR: Item not in the order, or was spelled incorrectly.")
    except:
        print("\nERROR: Please select a valid number of items to remove.\n")
        return order_dict
    return order_dict

'''
checkout_customer()

Takes an order dictionary as an argument. Iterates through the order, adding up costs as appropriate. Adds a
sales tax at the end, and displays the subtotal and total costs to the customer.

'''

def checkout_customer(order_dict):
    total_cost = 0
    print("\nTHANK YOU FOR YOUR ORDER!\nHERE IS YOUR RECEIPT:\n")
    for item, quant_price in order_dict.items():
        total_cost += quant_price[1]
        print(f"{item} --- x{quant_price[0]} --- ${quant_price[1]}")
    print("------------------------------")
    print(f"SUBTOTAL = ${total_cost:.2f}")
    tax_amount = total_cost * 0.1175
    print(f"SALES TAX (11.75%) = ${tax_amount:.2f}")
    print(f"TOTAL = ${(total_cost + tax_amount):.2f}")
    print(f"\nPlease Note: The cost of tips have been factored into the menu \nprices, so there is no need to leave any additional amount.")
    
    return

'''
order_from_specials()

Takes a restaurant dictionary, and an order dictionary. Looks through the restaurant dictionary for the specials (contain a True value in
the [price,specials] list found in the key:value pair for a given item), and prints them out for the customer. Allows them to add any amount
of one of the given specials (using the add_to_order() function). These specials can be removed by the customer the same way as any other item
in their order.

'''

def order_from_specials(rest_dict, order_dict):
    
    print("Here is a list of our specials: \n")
    combined_menu = {**rest_dict['food'], **rest_dict['drink'], **rest_dict['dessert']}
    for item, price_special in combined_menu.items():
        if price_special[1] == True:
            print(f"- {item} --- ${price_special[0]}")
        
    # Get customer to order one of the specials
    item_ordered = input("\nEnter the NAME of the special you would like, or type 'q' to exit: ")
    if item_ordered.lower() != "q":
        quantity = input("Enter QUANTITY of the special you are ordering: ")
        order_dict = add_to_order(rest_dict, order_dict, item_ordered, quantity)
        
    return order_dict

'''
process_customer_order()

This is the main logic loop for handling customer commands and inputs. It takes as an argument a restaurant dictionary. Allows users
to change their order (add items to order, remove items from order), show what is currently on their order, show the restaurant menu,
check out (get a receipt), or quit. Each option uses functions defined above.

'''    

def process_customer_order(rest_dict):
    
    current_order = {}
    
    print(f"\nHello! You are ordering from {rest_dict['name']}! Please take a look at the menu:\n")
    display_menu(rest_dict)
    while True: # Loop until user provides 'q' input
        inp = input("\nWhat would you like to do?\n'1': Change order (add/remove an item)\n'2': Display current order\n'3': Show menu again\n'4': Order from specials\n'5': CHECK OUT\n'q': QUIT\n\nSELECTION: ")
        if inp.lower() == "q":   
            break
        elif inp == "1": # CHANGE ORDER
            
            item_ordered = input("Enter the NAME of the item you want to add or remove: ")
            add_or_sub = input("Do you want to ADD or REMOVE this item (type 'add' or 'remove'): ")
            quantity = input("Enter QUANTITY to add/remove: ")
            
            if add_or_sub.lower() == "add":
                current_order = add_to_order(rest_dict, current_order, item_ordered, quantity)
            elif add_or_sub.lower() == "remove":
                current_order = remove_from_order(rest_dict, current_order, item_ordered, quantity)
            else:
                print("\nINVALID OPTION, please type 'add' or 'remove'.\n")
            
        elif inp == "2": # DISPLAY ORDER
            display_order(current_order)
        elif inp == "3": # DISPLAY MENU
            display_menu(rest_dict)
        elif inp == "4": # ORDER FROM SPECIALS
            current_order = order_from_specials(rest_dict, current_order)
        elif inp == "5": # PRINT RECEIPT AND CHECK OUT
            checkout_customer(current_order)
            break # Exit loop if the customer checks out
        else:
            print("\nERROR - INVALID SELECTION\n")
        
    return