users = {
    "admin": "admin123",
    "staff": "staff123",
}

# Each item is a dictionary. All items are stored in this list.
inventory = []


# ---------- LOG IN SYSTEM ----------
def login():
    print("\n===== RIMORA LOG IN =====")

    for attempt in range(3):                      # 3 tries only
        username = input("Username: ")
        password = input("Password: ")

        if username in users and users[username] == password:
            print("Welcome,", username)
            return True                           # login success

        print("Wrong username or password.", 2 - attempt, "tries left.")

    return False                                  # login failed


# ---------- HELPER ----------
def get_status(item):
    if item["quantity"] <= item["minimum"]:
        return "LOW STOCK"
    return "IN STOCK"


def show_items(items):
    print(f"{'ID':<5}{'NAME':<18}{'CATEGORY':<15}{'QTY':<12}{'COST':<10}STATUS")
    print("-" * 70)
    for item in items:
        qty = str(item["quantity"]) + " " + item["unit"]
        print(f"{item['id']:<5}{item['name']:<18}{item['category']:<15}"
              f"{qty:<12}{item['cost']:<10.2f}{get_status(item)}")


# ---------- INVENTORY ----------
def add_item():
    print("\n===== ADD ITEM =====")
    name = input("Name: ")
    category = input("Category: ")
    unit = input("Unit (kg, pcs, L): ")

    try:
        quantity = float(input("Quantity: "))
        minimum = float(input("Minimum stock: "))
        cost = float(input("Unit cost (PHP): "))
    except ValueError:
        print("Please enter numbers only.")
        return

    # new ID = highest ID + 1 (1 if the list is empty)
    new_id = max([i["id"] for i in inventory], default=0) + 1

    inventory.append({
        "id": new_id,
        "name": name,
        "category": category,
        "unit": unit,
        "quantity": quantity,
        "minimum": minimum,
        "cost": cost,
    })
    print("Item added!")


def view_inventory():
    print("\n===== INVENTORY =====")
    if len(inventory) == 0:
        print("No items yet.")
        return
    show_items(inventory)


def adjust_stock():
    view_inventory()
    if len(inventory) == 0:
        return

    try:
        item_id = int(input("\nItem ID to adjust: "))
        amount = float(input("Amount (+ to add, - to remove): "))
    except ValueError:
        print("Please enter numbers only.")
        return

    for item in inventory:
        if item["id"] == item_id:
            if item["quantity"] + amount < 0:
                print("Not enough stock!")
            else:
                item["quantity"] += amount
                print("New quantity:", item["quantity"], item["unit"])
            return

    print("Item not found.")


def delete_item():
    view_inventory()
    if len(inventory) == 0:
        return

    try:
        item_id = int(input("\nItem ID to delete: "))
    except ValueError:
        print("Please enter a number.")
        return

    for item in inventory:
        if item["id"] == item_id:
            inventory.remove(item)
            print("Item deleted!")
            return

    print("Item not found.")


# ---------- SEARCH FUNCTION ----------
def search_item():
    print("\n===== SEARCH =====")
    print("1. By name")
    print("2. By category")
    choice = input("Choose (1-2): ")

    keyword = input("Search for: ").lower()
    results = []

    for item in inventory:
        if choice == "1" and keyword in item["name"].lower():
            results.append(item)
        elif choice == "2" and keyword in item["category"].lower():
            results.append(item)

    if len(results) == 0:
        print("No match found.")
    else:
        print("\nFound", len(results), "item(s):")
        show_items(results)


# ---------- INVENTORY REPORT ----------
def inventory_report():
    print("\n===== INVENTORY REPORT =====")

    total_value = 0
    low_stock = []

    for item in inventory:
        total_value += item["quantity"] * item["cost"]
        if get_status(item) == "LOW STOCK":
            low_stock.append(item)

    print("Total items:", len(inventory))
    print(f"Total value: PHP {total_value:,.2f}")
    print("Low-stock items:", len(low_stock))

    if len(low_stock) > 0:
        print("\nITEMS TO RESTOCK:")
        for item in low_stock:
            print("-", item["name"], ":", item["quantity"], item["unit"], "left")


# ---------- MAIN MENU ----------
def main():
    if not login():
        print("Too many failed attempts. Goodbye!")
        return

    while True:
        print("""
===== RIMORA INVENTORY SYSTEM =====
1. Add Item
2. View Inventory
3. Search Item
4. Adjust Stock
5. Delete Item
6. Inventory Report
7. Log Out
===================================""")

        choice = input("Choose (1-7): ")

        if choice == "1":
            add_item()
        elif choice == "2":
            view_inventory()
        elif choice == "3":
            search_item()
        elif choice == "4":
            adjust_stock()
        elif choice == "5":
            delete_item()
        elif choice == "6":
            inventory_report()
        elif choice == "7":
            print("Logged out. Thank you for using Rimora!")
            break
        else:
            print("Invalid choice.")


main()
