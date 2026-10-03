# Personal-Expense-and-Budget-Analyzer
# FUNCTION 1: To add a new expense
def add_new_expense(expense_list):
    print("\n--- Add a New Expense ---")
    
    # We use 'try...except' to handle incorrect user inputs (like typing letters instead of numbers)
    try:
        # Get the amount and convert it to a decimal number (float)
        amount = float(input("Enter expense amount: "))
        
        # Get the category. .strip() removes any accidental spaces the user typed.
        category = input("Enter category (e.g., Food, Travel, Books): ").strip()
        
        # Create a dictionary for this single expense
        single_expense = {"amount": amount, "category": category}
        
        # Add this dictionary to our main list
        expense_list.append(single_expense)
        
        print("Success: Expense added!\n")
        
    except ValueError:
        # If the user typed "abc" for the amount, it jumps here instead of crashing
        print("Error: Please enter a valid number for the amount.\n")


# FUNCTION 2: To calculate and show the summary (This is your Computational Feature)
def show_summary(expense_list, budget_amount):
    print("\n--- Expense Summary ---")
    
    # Check if the list is empty. 'len()' checks the length of the list.
    if len(expense_list) == 0:
        print("No expenses recorded yet.\n")
        return  # This stops the function here and goes back to the menu
        
    total_spent = 0
    category_totals = {}  # Empty dictionary to hold totals for each category
    
    # Loop through every expense in our list to calculate totals
    for item in expense_list:
        # 1. Add to the overall total spent
        total_spent = total_spent + item["amount"]
        
        # 2. Add to the specific category total
        cat_name = item["category"]
        
        if cat_name in category_totals:
            # If we already have this category in our dictionary, add to it
            category_totals[cat_name] = category_totals[cat_name] + item["amount"]
        else:
            # If it's a new category, create it in the dictionary
            category_totals[cat_name] = item["amount"]
            
    # Show the final numbers
    print("Total Spent: Rs.", total_spent)
    print("Total Budget: Rs.", budget_amount)
    
    # Rule-based logic: Check if the user is over budget
    if total_spent > budget_amount:
        print("ALERT: You have crossed your budget!")
    else:
        remaining = budget_amount - total_spent
        print("Remaining Balance: Rs.", remaining)
        
    # Show the breakdown for each category
    print("\nSpending by Category:")
    for cat, amt in category_totals.items():
        print(cat, ": Rs.", amt)
    print("-----------------------\n")


# --- MAIN PROGRAM STARTS HERE ---

print("Welcome to the Student Expense Analyzer!")
my_budget = 5000.0  # You can change this to any starting budget
my_expenses = []    # This empty list will hold all our expense dictionaries

# This 'while' loop keeps the menu running forever until the user chooses to exit
while True:
    print("1. Add Expense")
    print("2. View Summary")
    print("3. Exit")
    
    user_choice = input("Enter your choice (1/2/3): ")
    
    if user_choice == '1':
        add_new_expense(my_expenses)
    elif user_choice == '2':
        show_summary(my_expenses, my_budget)
    elif user_choice == '3':
        print("Goodbye!")
        break  # This breaks us out of the while loop, ending the program
    else:
        print("Invalid choice. Please type 1, 2, or 3.\n")
