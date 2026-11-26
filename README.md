# Ecla Track

A desktop app (Python + Tkinter) that runs the **ECLAT** algorithm on a transactions dataset to find frequent itemsets and strong association rules, and can export the results to an Excel report.

## How the data flows

```
Excel / CSV file
      |
 preprocessing.py   (reads the Excel file, cleans it)
      |
 transformer.py     (horizontal -> vertical format)
      |
 eclat.py           (frequent itemsets + strong rules)
      |
 main.py            (GUI: shows the results in tables)
      |
 eclat_reporting.py (Export button -> Excel report)
```

## Files

- **main.py** – The GUI and the entry point. Connects all the other modules: loads the file, runs ECLAT, shows the results in two tabs (Frequent Itemsets, Strong Rules), calculates the lift for each rule, and handles the Export button.
- **eclat.py** – The ECLAT algorithm. Builds the frequent itemsets from the vertical data (item -> set of transaction IDs) and calculates the strong rules.
- **transformer.py** – Converts transactions from horizontal format (one row per transaction) to vertical format (one row per item), which is the format ECLAT needs. Also reads horizontal CSV files.
- **preprocessing.py** – Reads the input Excel file, removes empty rows and rows with missing values, and cleans the items.
- **eclat_reporting.py** – Builds the Excel report: formats the results and writes three sheets (Frequent Itemsets, Association Rules, Strong Rules).
- **eclat_vertical_dataset.csv** – Sample dataset in vertical format.
- **horizontal_dataset.csv** – Sample dataset in horizontal format (`;` separated).
- **test_dataset.xlsx** – Sample dataset in Excel format.

## Input files

| Type | Format |
|------|--------|
| Excel (`.xlsx` only, not `.xls`) | Two columns named exactly `Tid` and `items`. Items are separated by commas, e.g. `Bread,Milk,Eggs` |
| CSV, horizontal | `;` separated: `"Bread,Milk";T1` |
| CSV, vertical | `Item,TID_Set` header, e.g. `Bread,"T1,T2,T4"` |

## Excel export

Press **Export** after **Calculate** and choose where to save. The report is created by `eclat_reporting.py` and has three sheets:

1. **Frequent Itemsets** – itemset, size, support count, support %, lift (lift is shown only for itemsets with 2+ items)
2. **Association Rules** – antecedent, consequent, support %, confidence %, lift
3. **Strong Rules** – the rules that pass the minimum support and confidence

Note for the report module: `main.py` sends it dictionaries with the keys `itemset`, `support_count`, `antecedent`, `consequent`, `confidence` and `lift`. If these key names change, `main.py` must be updated too.

## Run

```
pip install pandas openpyxl
python main.py
```

1. Type the file path (e.g. `test_dataset.xlsx`).
2. Type the minimum support as a **count** (e.g. `4`).
3. Set the confidence between 0 and 1 (default `0.6`).
4. Press **Calculate**, then **Export** if you want the Excel report.

With the sample data, support `4` and confidence `0.6` gives 12 frequent itemsets and 8 strong rules.
