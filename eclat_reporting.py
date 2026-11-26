# -*- coding: utf-8 -*-
"""
Exports the results shown in the GUI (main.py) to an Excel file.

Both GUI tables are saved in ONE sheet, side by side, with the same columns
and the same value format as the GUI:
    Frequent Itemsets : Item Set | Support Count
    Strong Rules      : Rule | Support Count | Confidence | Lift
"""

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

# column names, same as the GUI headings
ITEMSET_COLUMNS = ["Item Set", "Support Count"]
RULE_COLUMNS = ["Rule", "Support Count", "Confidence", "Lift"]

SHEET_NAME = "ECLAT Report"


def prepare_frequent_itemsets_report(
    frequent_itemsets,
    transactions_count=None
):
    # GUI shows the item set as "A,B,C" and its support count
    rows = [
        {
            "Item Set": ",".join(item["itemset"]),
            "Support Count": item["support_count"]
        }
        for item in frequent_itemsets
    ]
    return pd.DataFrame(rows, columns=ITEMSET_COLUMNS)


def prepare_association_rules_report(
    association_rules,
    transactions_count=None
):
    # GUI shows the rule as "A  ->  B", confidence and lift rounded to 2 decimals
    rows = [
        {
            "Rule": ",".join(rule["antecedent"]) + "  ->  " + ",".join(rule["consequent"]),
            "Support Count": rule["support_count"],
            "Confidence": round(rule["confidence"], 2),
            "Lift": round(rule["lift"], 2)
        }
        for rule in association_rules
    ]
    return pd.DataFrame(rows, columns=RULE_COLUMNS)


def prepare_strong_rules_report(
    rules_df,
    min_support_percent=None,
    min_confidence_percent=None
):
    # the algorithm already filtered the rules by the confidence the user entered,
    # and the GUI shows exactly these rules, so nothing more is filtered here
    return rules_df.copy()


def export_eclat_report(
    itemsets_df,
    rules_df,
    strong_rules_df=None,
    output_file="ECLAT_Report.xlsx"
):
    # keep the GUI headings even when there are no results
    if itemsets_df.empty:
        itemsets_df = pd.DataFrame(columns=ITEMSET_COLUMNS)
    if rules_df.empty:
        rules_df = pd.DataFrame(columns=RULE_COLUMNS)

    # layout (0-based for pandas): row 0 = table titles, row 1 = headings
    # itemsets table first, one empty column, then the rules table
    itemset_start = 0
    rule_start = len(ITEMSET_COLUMNS) + 1

    with pd.ExcelWriter(
        output_file,
        engine="openpyxl"
    ) as writer:

        itemsets_df.to_excel(
            writer,
            sheet_name=SHEET_NAME,
            index=False,
            startrow=1,
            startcol=itemset_start
        )

        rules_df.to_excel(
            writer,
            sheet_name=SHEET_NAME,
            index=False,
            startrow=1,
            startcol=rule_start
        )

    wb = load_workbook(output_file)
    ws = wb[SHEET_NAME]

    # table titles (same names as the GUI tabs)
    ws.cell(row=1, column=itemset_start + 1, value="Frequent Itemsets").font = Font(bold=True, size=12)
    ws.cell(row=1, column=rule_start + 1, value="Strong Rules").font = Font(bold=True, size=12)

    # Format column headers (row 2) of both tables
    header_columns = (
        list(range(itemset_start + 1, itemset_start + 1 + len(ITEMSET_COLUMNS))) +
        list(range(rule_start + 1, rule_start + 1 + len(RULE_COLUMNS)))
    )
    for col in header_columns:
        cell = ws.cell(row=2, column=col)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill(
            fill_type="solid",
            fgColor="1F4E78"
        )

    # Center headings and values, like the GUI tables
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(horizontal="center")

    # Adjust column widths (the title row is skipped, titles may overflow)
    for col in range(1, ws.max_column + 1):
        max_length = 0
        for row in range(2, ws.max_row + 1):
            value = ws.cell(row=row, column=col).value
            if value is not None:
                max_length = max(max_length, len(str(value)))
        letter = get_column_letter(col)
        ws.column_dimensions[letter].width = max_length + 3 if max_length else 4

    wb.save(output_file)

    return output_file
