# Budget Expense Tracker
# CTP project - Bennett University
# keeps track of daily spending and tells you when the budget is almost over

import csv
import os
from datetime import datetime

DEFAULT_BUDGET = 5000.0
EXPENSE_FILE = "expenses.csv"
BUDGET_FILE = "budget.txt"
CATEGORIES = ["Food", "Travel", "Academics", "Entertainment", "Bills", "Miscellaneous"]


def setup_files():
    # make the files if they are not there yet
    if not os.path.exists(EXPENSE_FILE):
        f = open(EXPENSE_FILE, "w", newline="")
        writer = csv.writer(f)
        writer.writerow(["Date", "Category", "Amount", "Description"])
        f.close()

    if not os.path.exists(BUDGET_FILE):
        f = open(BUDGET_FILE, "w")
        f.write(str(DEFAULT_BUDGET))
        f.close()


def get_budget():
    try:
        f = open(BUDGET_FILE, "r")
        budget = float(f.read())
        f.close()
        if budget <= 0:
            return DEFAULT_BUDGET
        return budget
    except:
        # if file is empty or broken just use default
        return DEFAULT_BUDGET


def save_budget(amount):
    f = open(BUDGET_FILE, "w")
    f.write(str(amount))
    f.close()


def get_all_expenses():
    expenses = []
    f = open(EXPENSE_FILE, "r")
    reader = csv.reader(f)
    next(reader)  # skip the header

    for row in reader:
        if len(row) == 4:
            exp = {
                "date": row[0],
                "category": row[1],
                "amount": float(row[2]),
                "note": row[3]
            }
            expenses.append(exp)

    f.close()
    return expenses


def save_expense(category, amount, note):
    now = datetime.now().strftime("%d-%m-%Y %H:%M")
    f = open(EXPENSE_FILE, "a", newline="")
    writer = csv.writer(f)
    writer.writerow([now, category, amount, note])
    f.close()


def get_valid_amount(message):
    while True:
        try:
            amount = float(input(message))
            if amount > 0:
                return amount
            else:
                print("Amount should be more than 0, try again")
        except ValueError:
            print("Please enter a number only")


def choose_category():
    print("\nChoose a category:")
    for i in range(len(CATEGORIES)):
        print(str(i + 1) + ". " + CATEGORIES[i])

    while True:
        choice = input("Enter category number (1-6): ")
        if choice.isdigit() and 1 <= int(choice) <= 6:
            return CATEGORIES[int(choice) - 1]
        print("Invalid choice, pick a number from 1 to 6")


def add_expense():
    print("\n--- Add Expense ---")
    amount = get_valid_amount("Amount (INR): ")
    category = choose_category()
    note = input("Short note: ").strip()
    if note == "":
        note = "No description"

    save_expense(category, amount, note)
    print("Expense saved!")


def view_expenses():
    expenses = get_all_expenses()

    if len(expenses) == 0:
        print("\nNo expenses added yet.")
        return

    print("\n--- All Expenses ---")
    print("-" * 70)
    count = 1
    for e in expenses:
        print(str(count) + ".", e["date"], "|", e["category"], "| INR", format(e["amount"], ".2f"), "|", e["note"])
        count += 1
    print("-" * 70)


def view_summary():
    expenses = get_all_expenses()
    budget = get_budget()

    category_totals = {}
    for c in CATEGORIES:
        category_totals[c] = 0.0

    total_spent = 0.0
    for e in expenses:
        total_spent += e["amount"]
        category_totals[e["category"]] += e["amount"]

    remaining = budget - total_spent
    usage_percent = (total_spent / budget) * 100

    print("\n" + "-" * 40)
    print("MONTHLY BUDGET SUMMARY")
    print("-" * 40)
    print("Monthly Budget    : INR", format(budget, ".2f"))
    print("Total Spent       : INR", format(total_spent, ".2f"))
    print("Remaining Balance : INR", format(remaining, ".2f"))
    print("Budget Used       :", format(usage_percent, ".1f") + "%")

    # alert depending on how much of the budget is used
    print("\nBudget Status:")
    if usage_percent < 50:
        print("[SAFE] You are chilling, spending is well within limit.")
    elif usage_percent < 85:
        print("[MODERATE] You have crossed 50% of your budget. Spend carefully.")
    elif usage_percent < 100:
        print("[WARNING] Almost out of monthly budget, over 85% gone!")
    else:
        overspent = total_spent - budget
        print("[CRITICAL] You hit or crossed your limit! Overspent by INR", format(overspent, ".2f"))

    print("\nSpending by Category:")
    top_category = ""
    top_amount = 0.0
    for c in CATEGORIES:
        amt = category_totals[c]
        if total_spent > 0:
            percent = (amt / total_spent) * 100
        else:
            percent = 0.0
        print("- " + c.ljust(14) + ": INR", format(amt, ".2f"), "(" + format(percent, ".1f") + "%)")

        if amt > top_amount:
            top_amount = amt
            top_category = c

    if top_category != "":
        print("\nHighest Spending :", top_category, "(INR " + format(top_amount, ".2f") + ")")
    print("-" * 40)


def update_budget():
    print("\nCurrent budget: INR", format(get_budget(), ".2f"))
    new_budget = get_valid_amount("Enter new monthly budget: ")
    save_budget(new_budget)
    print("Budget updated!")


def main():
    setup_files()

    while True:
        print("\n" + "=" * 40)
        print("BUDGET EXPENSE TRACKER")
        print("=" * 40)
        print("1. Add Daily Expense")
        print("2. View All Expenses")
        print("3. View Summary & Budget Alert")
        print("4. Update Monthly Budget")
        print("5. Exit")
        print("=" * 40)

        choice = input("Select an option (1-5): ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            view_summary()
        elif choice == "4":
            update_budget()
        elif choice == "5":
            print("Bye! Keep tracking your spends.")
            break
        else:
            print("Invalid option, enter a number from 1 to 5")


main()
