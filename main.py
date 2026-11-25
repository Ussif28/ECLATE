
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import eclat
root = tk.Tk()
#wedges add here

root.geometry("1200x700")
#title
root.title("Ecla Track")
#Entries
min_supp = tk.Entry(root)
path = tk.Entry(root)

#labels
head = tk.Label(root,text="Ecla Track",font=("Arial",40,"bold"))
line = tk.Frame(root, bg="black", height=2, width=300)
line.place(relx=0.5, y=90,anchor="center",width=600)

minsup = tk.Label(root, text="Minimum Support  :",font=("Arial",12))
file_path = tk.Label(root, text=" file path : ",font=("Arial",12))
#algo = tk.Label(root, text="Algorithm")

# validate function
#---------------------


def calc():
    for old in table.get_children():
        table.delete(old)
    # here data taken from aclate algorithm
    # reassign variable (data) to aclate algorithm function
    eclat.candidate_item_sets.clear()
    try:
        item_sets = eclat.convert_csv_dictionaries(path.get())
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found")
        return
    min_count = int(min_supp.get())
    eclat.get_candidate_item_sets(item_sets, 0, min_count, min_count)
    data = [[k, len(v)] for k, v in eclat.candidate_item_sets.items()]
    for text , num in data:
        table.insert("" ,tk.END,values=(text,num))
    table.yview_moveto(1)
# validate from support count number passes by user
def check():
    try:
        num = int(min_supp.get())
        file = path.get()
        if 0 > num :
            messagebox.showerror("Error", "Number must be positive integer")
        elif len(file) == 0 :
            messagebox.showerror("Error", "No File Path specified")
        else:
            calc()
            # return min support (num) and file path (file)
            return num , file
    except ValueError:
        messagebox.showerror("Error", "Enter a valid integer")
#----------------------

#algo
box = tk.Label(root, text=" Choose Algorithm ",padx=10,pady=10,font=("Arial",12))
#buttons
#stop = tk.Button(root ,text ="Stop",width=10, command = root.destroy)
export = tk.Button(root ,text ="Export",width=10)
calculate = tk.Button(root ,text ="Calculate",width=10,command =check)


# combo box
def select(event):
    selected_item = combo_box.get()
    box.config(text="Selected Item: " + selected_item)




#box.grid(row=0, column=0)
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

# TABLE FRAME
frame = tk.Frame(root)
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
#table setting
style = ttk.Style()
style.theme_use("clam")
style.configure(
    "Treeview.Heading",
    background="black",
    foreground="white",
    relief="flat",
    #font=("Arial",12,"bold"),
)
table = ttk.Treeview(frame,columns=("Name","num"),show="headings")
table.heading("Name",text="Item Set")
table.heading("num",text="Support Count")
table.column("Name",width=450,anchor="center")
table.column("num",width=350,anchor="center")
# scroller or slider
scroll_y = tk.Scrollbar(frame,orient="vertical",command=table.yview)
scroll_x = tk.Scrollbar(frame,orient="horizontal",command=table.xview)


# geometry by place function for Elements
head.place(relx=0.5 , y = 40 , anchor="center")
box.place( relx = 0.1  , y=120 )
combo_box.place( relx = 0.12  , y=170 )
file_path.place( relx=0.4 , y=180 , anchor="center")
path.place( relx=0.5 , y=180 , anchor="center" ,width=150)
minsup.place( relx=0.8 , y=180 , anchor="center")
min_supp.place( relx=0.91 , y=180 , anchor="center")
frame.place(relx=0.5,y=450,width=800,height=420,anchor="center")
table.grid(row=0,column=0,sticky="nsew")
scroll_y.grid(row=0,column=1,sticky="ns")
scroll_x.grid(row=1,column=0,sticky="ew")
export.place(relx=0.2,rely=0.9,anchor="center")
calculate.place(relx=0.8,rely=0.9,anchor="center")

root.mainloop()
