import csv
import time

class POS:
    def __init__(self):
        self.basket = []
        self.bill_number = 1
        self.transactions = {}

    def add_to_basket(self):
        item_code = input("Enter item code: ")
        internal_price = float(input("Enter internal price: "))
        discount = float(input("Enter discount: "))
        sale_price = float(input("Enter sale price: "))
        quantity = int(input("Enter quantity: "))

        line_tot = (sale_price - (sale_price * (discount / 100))) * quantity
        item = {
            "item_code": item_code,
            "internal_price": internal_price,
            "sale_price": sale_price,
            "discount": discount,
            "quantity": quantity,
            "line_tot": line_tot
        }

        self.basket.append(item)
        self.view_basket()

    def view_basket(self):
        if len(self.basket) == 0:
            print("Basket is empty.")
            return

        print("\nItems in Basket:")
        print("-" * 80)
        print(f"{'Line No.':<10}{'Item Code':<15}{'Internal Price':<15}{'Sale Price':<15}{'Discount (%)':<15}{'Line Total':<15}")
        print("-" * 80)
        for idx, item in enumerate(self.basket, start=1):
            print(f"{idx:<10}{item['item_code']:<15}{item['internal_price']:<15}{item['sale_price']:<15}{item['discount']:<15}{item['line_tot']:<15}")
        print("-" * 80)

    def delete_item(self):
        self.view_basket()
        if len(self.basket) > 0:
            line_number = int(input("Enter line number to delete: ")) - 1
            if 0 <= line_number < len(self.basket):
                deleted_item = self.basket.pop(line_number)
                print(f"Item {deleted_item['item_code']} removed from basket.")
            else:
                print("Invalid line number.")
        else:
            print("No items to delete.")

    def update_item(self):
        self.view_basket()
        if len(self.basket) > 0:
            line_number = int(input("Enter line number to update: ")) - 1
            if 0 <= line_number < len(self.basket):
                item = self.basket[line_number]
                item['sale_price'] = float(input(f"Enter new sale price for {item['item_code']}: "))
                item['discount'] = float(input(f"Enter new discount for {item['item_code']}: "))
                item['quantity'] = int(input(f"Enter new quantity for {item['item_code']}: "))
                item['line_tot'] = (item['sale_price'] - (item['sale_price'] * (item['discount'] / 100))) * item['quantity']
                print(f"Item {item['item_code']} updated.")
            else:
                print("Invalid line number.")
        else:
            print("No items to update.")

    def generate_bill(self):
        if len(self.basket) > 0:
            print("\nGenerating Bill...")
            print("-" * 80)
            print(f"{'Line No.':<10}{'Item Code':<15}{'Internal Price':<15}{'Sale Price':<15}{'Discount (%)':<15}{'Line Total':<15}")
            print("-" * 80)
            total = 0
            for idx, item in enumerate(self.basket, start=1):
                print(f"{idx:<10}{item['item_code']:<15}{item['internal_price']:<15}{item['sale_price']:<15}{item['discount']:<15}{item['line_tot']:<15}")
                total += item['line_tot']
            print("-" * 80)
            print(f"{'Total Amount':<55}{total:<15}")
            print(f"Bill Number: {self.bill_number}")
            self.transactions[self.bill_number] = self.basket
            self.bill_number += 1
            self.basket = []
        else:
            print("No items in the basket to generate a bill.")

    def search_bill(self):
        bill_number = int(input("Enter Bill Number to search: "))
        if bill_number in self.transactions:
            print("\nBill Details:")
            print("-" * 80)
            print(f"{'Line No.':<10}{'Item Code':<15}{'Internal Price':<15}{'Sale Price':<15}{'Discount (%)':<15}{'Line Total':<15}")
            print("-" * 80)
            total = 0
            for idx, item in enumerate(self.transactions[bill_number], start=1):
                print(f"{idx:<10}{item['item_code']:<15}{item['internal_price']:<15}{item['sale_price']:<15}{item['discount']:<15}{item['line_tot']:<15}")
                total += item['line_tot']
            print("-" * 80)
            print(f"{'Total Amount':<55}{total:<15}")
            print(f"Bill Number: {bill_number}")
        else:
            print("Bill not found.")

    def generate_tax_file(self):
        if len(self.transactions) > 0:
            filename = f"tax_transaction_{int(time.time())}.csv"
            with open(filename, "w", newline='') as file:
                writer = csv.DictWriter(file, fieldnames=["item_code", "internal_price", "sale_price", "discount", "quantity", "line_tot", "checksum"])
                writer.writeheader()
                for bill in self.transactions.values():
                    for item in bill:
                        item['checksum'] = self.calculate_checksum(item)
                        writer.writerow(item)
            print(f"Tax file generated successfully: {filename}")
        else:
            print("No bills to generate a tax file.")

    def calculate_checksum(self, item):
        count_capital = sum(1 for c in item['item_code'] if c.isupper())
        count_lower = sum(1 for c in item['item_code'] if c.islower())
        count_digits = sum(1 for c in item['item_code'] if c.isdigit())
        checksum = count_capital + count_lower + count_digits
        return checksum

def main():
    pos = POS()
    while True:
        print("\n-- POS System --")
        print("1. Add Item to Basket")
        print("2. Display Basket")
        print("3. Delete Item from Basket")
        print("4. Update Item in Basket")
        print("5. Generate Bill")
        print("6. Search Bill")
        print("7. Generate Tax Transaction File")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            pos.add_to_basket()
        elif choice == "2":
            pos.view_basket()
        elif choice == "3":
            pos.delete_item()
        elif choice == "4":
            pos.update_item()
        elif choice == "5":
            pos.generate_bill()
        elif choice == "6":
            pos.search_bill()
        elif choice == "7":
            pos.generate_tax_file()
        elif choice == "8":
            print("Exiting POS system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
