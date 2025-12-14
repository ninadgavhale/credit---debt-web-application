import json
import os

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_entry(data):
    entry_type = input("Type (credit/debt): ").strip().lower()
    amount = float(input("Amount: "))
    note = input("Note: ")

    if entry_type not in ["credit", "debt"]:
        print("Invalid type")
        return

    data.append({
        "type": entry_type,
        "amount": amount,
        "note": note
    })

def summary(data):
    credit = sum(e["amount"] for e in data if e["type"] == "credit")
    debt = sum(e["amount"] for e in data if e["type"] == "debt")

    print(f"\nTotal Credit: ₹{credit}")
    print(f"Total Debt: ₹{debt}")
    print(f"Net Balance: ₹{credit - debt}\n")

def main():
    data = load_data()

    while True:
        print("1. Add Entry")
        print("2. View Summary")
        print("3. Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_entry(data)
            save_data(data)
        elif choice == "2":
            summary(data)
        elif choice == "3":
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()
