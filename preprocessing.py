

import pandas as pd


def preprocess_data(file_path):
    
    df = pd.read_excel(file_path, engine="openpyxl")

   
    df = df.dropna(how="all")

    
    df = df.dropna(subset=["Tid", "items"])

    transactions = {}

    
    for _, row in df.iterrows():

        TransactionId = row["Tid"]
        Items = str(row["items"])

        
        items_list = Items.split(",")

        
        items_list = [
            product.strip()
            for product in items_list
            if product.strip()
        ]

        
        if TransactionId not in transactions:
            transactions[TransactionId] = []

        transactions[TransactionId].extend(items_list)

    return transactions






       

   


        









