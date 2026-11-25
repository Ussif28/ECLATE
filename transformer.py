import csv
def read_transactions_from_csv(file_path):
    transactions = {}
    with open(file_path, "r", newline="", encoding="utf-8-sig") as excel_data:
        reader = csv.reader(excel_data, delimiter=";")
        next(reader, None)

        for row in reader:
            if len(row) < 2:
                continue

            items = {item.strip() for item in row[0].strip('"').split(",") if item.strip()}
            T_ID = row[1].strip()

           # if T_ID in transactions:
            #    print(f"duplicate error nomber {T_ID}")

            transactions[T_ID] = items

    return transactions


def transform_to_vertical(transactions):
    vertical_data = {}
    for T_ID, items in transactions.items():
        # to go rhrough all the items and add them in vertical and and the T_ID in them
        for item in items:
            if item not in vertical_data:
                vertical_data[item] = set()

            vertical_data[item].add(T_ID)

    return vertical_data, len(transactions)


def T_ID_sort_key(T_ID):
    #arrange them by T_ID numbers
    if T_ID.startswith("T") and T_ID[1:].isdigit():
        return (0, int(T_ID[1:]))
    return (1, T_ID)


def print_vertical_table(vertical_data, total_transaction):
    
    print(f"total transaction: {total_transaction}\n")
    print(f"'Item' | TID_Set")

    for item in sorted(vertical_data):
        tids = sorted(vertical_data[item], key=T_ID_sort_key)
        print(f"{item:<12} | {','.join(tids)}")


if __name__ == "__main__":
    file_paht = input("Enter the CSV file path: ").strip()

    try:
        trans = read_transactions_from_csv(file_paht)
        vertical_data, total_transaction = transform_to_vertical(trans)
        print_vertical_table(vertical_data, total_transaction)

    except Exception as e:
        print(f"error {e}")

