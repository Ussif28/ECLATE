import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
import pandas as pd
import eclat
import transformer
import preprocessing
import eclat_reporting

root = tk.Tk()
# wedges add here

root.geometry("1200x700")
# title
root.title("Ecla Track")
# Entries
min_supp = tk.Entry(root)
min_conf = tk.Entry(root)
min_conf.insert(0, "0.6")
path = tk.Entry(root)

# last results (used by the Export button)
last = {}

# labels
head = tk.Label(root, text="Ecla Track", font=("Arial", 40, "bold"))
line = tk.Frame(root, bg="black", height=2, width=300)
line.place(relx=0.5, y=90, anchor="center", width=600)

minsup = tk.Label(root, text="Minimum Support  :", font=("Arial", 12))
minconf = tk.Label(root, text="Confidence (0-1)  :", font=("Arial", 12))
file_path = tk.Label(root, text=" file path : ", font=("Arial", 12))


# algo = tk.Label(root, text="Algorithm")

# validate function
# ---------------------


# read any supported file and return (vertical item_sets, number of transactions)
def load_item_sets(file):
    # Excel file: preprocessing -> horizontal transactions -> transformer -> vertical
    if file.lower().endswith(".xlsx"):
        transactions = preprocessing.preprocess_data(file)
        return transformer.transform_to_vertical(transactions)
    with open(file, 'r', encoding='utf-8-sig') as f:
        first_line = f.readline()
    # horizontal csv file (separated by ;) -> transformer -> vertical
    if ";" in first_line:
        transactions = transformer.read_transactions_from_csv(file)
        return transformer.transform_to_vertical(transactions)
    # already vertical csv file
    item_sets = eclat.convert_csv_dictionaries(file)
    all_tids = set()
    for tids in item_sets.values():
        all_tids |= tids
    return item_sets, len(all_tids)


def calc():
    for old in table.get_children():
        table.delete(old)
    for old in rules_table.get_children():
        rules_table.delete(old)
    last.clear()
    # here data taken from aclate algorithm
    # reassign variable (data) to aclate algorithm function
    eclat.candidate_item_sets.clear()
    try:
        item_sets, total = load_item_sets(path.get())
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found")
        return
    except Exception as e:
        messagebox.showerror("Error", "Could not read the file:\n" + str(e))
        return
    min_count = int(min_supp.get())
    try:
        conf = float(min_conf.get())
    except ValueError:
        messagebox.showerror("Error", "Confidence must be a number between 0 and 1")
        return
    if conf < 0 or conf > 1:
        messagebox.showerror("Error", "Confidence must be a number between 0 and 1")
        return
    eclat.get_candidate_item_sets(item_sets, 0, min_count, min_count)
    data = [[k, len(v)] for k, v in eclat.candidate_item_sets.items()]
    for text, num in data:
        table.insert("", tk.END, values=(text, num))
    table.yview_moveto(1)

    # strong rules (from eclat.py), plus support count and lift for the report
    rules = []
    for rule_key, confidence in eclat.get_strong_rules(conf).items():
        left, right = rule_key.split("->")
        antecedent = left.split(",")
        consequent = right.split(",")
        support_count = len(set.intersection(*[item_sets[i] for i in antecedent + consequent]))
        consequent_support = len(set.intersection(*[item_sets[i] for i in consequent])) / total
        lift = confidence / consequent_support
        rules.append({
            "antecedent": antecedent,
            "consequent": consequent,
            "support_count": support_count,
            "confidence": confidence,
            "lift": lift,
        })
        # EDIT 2: lift added as the 4th value shown in the table
        rules_table.insert("", tk.END,
                           values=(left + "  ->  " + right, support_count, round(confidence, 2), round(lift, 2)))

    last["itemsets"] = [{"itemset": k.split(","), "support_count": len(v)}
                        for k, v in eclat.candidate_item_sets.items()]
    last["rules"] = rules
    last["total"] = total
    last["min_count"] = min_count
    last["conf"] = conf


# export the last result to an excel file (uses eclat_reporting.py)
def export_excel():
    if not last:
        messagebox.showerror("Error", "Press Calculate first")
        return
    file = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                        filetypes=[("Excel files", "*.xlsx")],
                                        initialfile="ECLAT_Report.xlsx")
    if not file:
        return
    total = last["total"]
    if last["itemsets"]:
        itemsets_df = eclat_reporting.prepare_frequent_itemsets_report(last["itemsets"], total)
    else:
        itemsets_df = pd.DataFrame(columns=["Itemset", "Itemset Size", "Support Count", "Support %"])
    if last["rules"]:
        rules_df = eclat_reporting.prepare_association_rules_report(last["rules"], total)
    else:
        rules_df = pd.DataFrame(columns=["Antecedent", "Consequent", "Support %", "Confidence %", "Lift"])
    strong_df = eclat_reporting.prepare_strong_rules_report(
        rules_df,

        last["min_count"] / total * 100,
        last["conf"] * 100
    )
    try:
        eclat_reporting.export_eclat_report(itemsets_df, rules_df, strong_df, output_file=file)
    except PermissionError:
        messagebox.showerror("Error", "Close the Excel file first, then try again")
        return
    messagebox.showinfo("Export", "Saved successfully")


# validate from support count number passes by user
def check():
    try:
        num = int(min_supp.get())
        file = path.get()
        if 0 > num:
            messagebox.showerror("Error", "Number must be positive integer")
        elif len(file) == 0:
            messagebox.showerror("Error", "No File Path specified")
        else:
            calc()
            # return min support (num) and file path (file)
            return num, file
    except ValueError:
        messagebox.showerror("Error", "Enter a valid integer")


# ----------------------

# algo
box = tk.Label(root, text=" Choose Algorithm ", padx=10, pady=10, font=("Arial", 12))
# buttons
# stop = tk.Button(root ,text ="Stop",width=10, command = root.destroy)
export = tk.Button(root, text="Export", width=10, command=export_excel)
calculate = tk.Button(root, text="Calculate", width=10, command=check)


# combo box
def select(event):
    selected_item = combo_box.get()
    box.config(text="Selected Item: " + selected_item)


# box.grid(row=0, column=0)
combo_box = ttk.Combobox(
    root,
    values=["ECLATE"],
    state="readonly",
    width=40,
)

combo_box.set("ECLATE")

combo_box.bind("<<ComboboxSelected>>", select)
# toolbar
menu = tk.Menu(root)
root.config(menu=menu)
filemenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="New")
filemenu.add_command(label="Open...")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)

helpmenu = tk.Menu(menu)
menu.add_cascade(label="Help", menu=helpmenu)
helpmenu.add_command(label="About")

# TABLE FRAME (two tabs: itemsets / strong rules)
notebook = ttk.Notebook(root)
frame = tk.Frame(notebook)
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
rules_frame = tk.Frame(notebook)
rules_frame.rowconfigure(0, weight=1)
rules_frame.columnconfigure(0, weight=1)
notebook.add(frame, text="Frequent Itemsets")
notebook.add(rules_frame, text="Strong Rules")
# table setting
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview.Heading",
    background="black",
    foreground="white",
    relief="flat",
    # font=("Arial",12,"bold"),
)
table = ttk.Treeview(frame, columns=("Name", "num"), show="headings")
table.heading("Name", text="Item Set")
table.heading("num", text="Support Count")
table.column("Name", width=450, anchor="center")
table.column("num", width=350, anchor="center")
# EDIT 1: rules table now has a 4th column "Lift"
rules_table = ttk.Treeview(rules_frame, columns=("rule", "count", "conf", "lift"), show="headings")
rules_table.heading("rule", text="Rule")
rules_table.heading("count", text="Support Count")
rules_table.heading("conf", text="Confidence")
rules_table.heading("lift", text="Dependency")
rules_table.column("rule", width=350, anchor="center")
rules_table.column("count", width=150, anchor="center")
rules_table.column("conf", width=150, anchor="center")
rules_table.column("lift", width=150, anchor="center")
# scroller or slider
scroll_y = tk.Scrollbar(frame, orient="vertical", command=table.yview)
scroll_x = tk.Scrollbar(frame, orient="horizontal", command=table.xview)
table.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
rscroll_y = tk.Scrollbar(rules_frame, orient="vertical", command=rules_table.yview)
rscroll_x = tk.Scrollbar(rules_frame, orient="horizontal", command=rules_table.xview)
rules_table.configure(yscrollcommand=rscroll_y.set, xscrollcommand=rscroll_x.set)

# geometry by place function for Elements
head.place(relx=0.5, y=40, anchor="center")
box.place(relx=0.1, y=120)
combo_box.place(relx=0.12, y=170)
file_path.place(relx=0.4, y=180, anchor="center")
path.place(relx=0.5, y=180, anchor="center", width=150)
minsup.place(relx=0.8, y=180, anchor="center")
min_supp.place(relx=0.91, y=180, anchor="center")
minconf.place(relx=0.8, y=215, anchor="center")
min_conf.place(relx=0.91, y=215, anchor="center")
notebook.place(relx=0.5, y=450, width=800, height=420, anchor="center")
table.grid(row=0, column=0, sticky="nsew")
scroll_y.grid(row=0, column=1, sticky="ns")
scroll_x.grid(row=1, column=0, sticky="ew")
rules_table.grid(row=0, column=0, sticky="nsew")
rscroll_y.grid(row=0, column=1, sticky="ns")
rscroll_x.grid(row=1, column=0, sticky="ew")
export.place(relx=0.2, rely=0.9, anchor="center")
calculate.place(relx=0.8, rely=0.9, anchor="center")

root.mainloop()