import tkinter
import json
import avl_tree
#from tabulate import tabulate
from tkinter import Entry, Frame, Button, Label
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.messagebox as tkmb

cabezera = [["","ID","Nombre","Contraseña","Puesto"]]
hash_table = []
hash_table_len = 5

datos = None

class Table:
    def __init__(self, root, table, cab):
        total_rows = len(table)
        total_columns = len(table[0])
        for i in range(total_rows):
            for j in range(1, total_columns):
                if cab:
                    self.e = Entry(root, width=20, fg='red', font=('Arial',16,'bold'))
                    self.e.grid(row=i, column=j)
                    self.e.insert(0 , table[i][j])
                    pass
                else:
                    self.e = Entry(root, width=20, fg='blue', font=('Arial',16,'normal'))
                    self.e.grid(row=i, column=j)
                    self.e.insert(1 , table[i][j])

def read_file():
    filetypes = (
        ('text files', '*.json'),
        ('All files', '*.*')
    )
    path = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )

    with open(path) as archivo:
        datos = json.load(archivo)
    
def hash_code(string):
    lst = 0
    for letter in string:
        lst += int(ord(letter))
    return lst

def partition(sub_tabla, low, high):
    pivote = sub_tabla[high][0]

    i = low - 1

    for j in range(low, high):
        if sub_tabla[j][0] <= pivote:
            i = i + 1
            (sub_tabla[i], sub_tabla[j]) = (sub_tabla[j], sub_tabla[i])

    (sub_tabla[i + 1], sub_tabla[high]) = (sub_tabla[high], sub_tabla[i + 1])

    return i + 1

def sort_hash(sub_tabla, low, high):
    if (low < high):
        pi = partition(sub_tabla, low, high)
        sort_hash(sub_tabla, low, pi - 1)
        sort_hash(sub_tabla, pi + 1, high)

def next_fib(current):
    aux = 0
    actual = 1
    last = 0
    while(True):
        aux = actual
        actual = actual + last
        last = aux
        if current < actual:
            global hash_table_len 
            hash_table_len = actual
            break

def load_users():
    filetypes = (
        ('text files', '*.csv'),
        ('All files', '*.*')
    )

    path = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )

    with open(path) as archivo:
        string_file = archivo.read().split("\n")

        for i in range(len(string_file)):
            list = []
            subdiv = string_file[i].split(",")
            if subdiv[0].upper().replace("\"", "") == "ID" or subdiv[1].upper().replace("\"", "") == "NOMBRE" or subdiv[2].upper().replace("\"", "") == "CONTRASEÑA" or subdiv[3].upper().replace("\"", "") == "PUESTO" :
                pass
            else:
                list.append(hash_code(subdiv[0].replace("\"", "")))
                list.append(subdiv[0].replace("\"", ""))
                list.append(subdiv[1].replace("\"", ""))
                list.append(subdiv[2].replace("\"", ""))
                list.append(subdiv[3].replace("\"", ""))
                
                hash_table.append(list)

                if (len(hash_table)/hash_table_len) >= 0.7:
                    next_fib(hash_table_len)
                
        archivo.close()

        print(hash_table)

        sort_hash(hash_table, 0, len(hash_table) - 1)

        print("\n", hash_table)

        global t2
        t2 = Table(root=frame, table=hash_table, cab=False)

def log_out():
    main_gui.pack_forget()
    #tkmb.showinfo(title="Login Successful", message="...")
    login_frame.pack()

def log_in():
    user = txt_w.get()
    password = psw_w.get()
    try:
        if user == "admin" and password == "admin":
            login_frame.pack_forget()
            main_gui.pack()
            tkmb.showinfo(title="Login Successful", message="Admin")
        else:
            pass
    except Exception as e:
        raise e

root = tkinter.Tk()

#Para los elementos del Login
login_frame = Frame(root)
internal_frame = Frame(login_frame)
internal_frame.pack(padx=30, pady=30)

lbl = Label(internal_frame, text="Usuario")
lbl.pack()
txt_w = Entry(internal_frame, width = 45)
txt_w.pack()
lbl2 = Label(internal_frame, text="Contraseña")
lbl2.pack()
psw_w = Entry(internal_frame, width = 45, show="*")
psw_w.pack()

send_bttn = Button(internal_frame, text="Log In", command=log_in)
send_bttn.pack()

#Para los demás formas del GUI
main_gui = Frame(root)

#Tab Control
tabControl = ttk.Notebook(main_gui)
tab1 = Frame(tabControl)
tab2 = Frame(tabControl)
tab3 = Frame(tabControl)

tabControl.add(tab1, text="Usuarios")
tabControl.add(tab2, text="Proyecto")
tabControl.add(tab3, text="Tareas")

tabControl.pack()
top_frame = Frame(tab1)
top_frame.pack( side = "top", padx=10, pady=10 )
#redbutton = Button(top_frame, text="Cargar Json", fg="red", command=read_file)
#redbutton.pack()

users_load_bttn = Button(top_frame, text="Cargar Usuarios", fg="red", command=load_users)
users_load_bttn.pack()

frame = Frame(tab1)
frame.pack(padx=20, pady=20)

t = Table(root=frame, table=cabezera, cab=True)

'''
usuarios_button = Button(bottom_frame, text="Log Out", fg="red", command=log_out)
usuarios_button.grid(row = 0, column = 0, pady = 2)
pry_bttn = Button(bottom_frame, text="Log Out", fg="red", command=log_out)
pry_bttn.grid(row = 0, column = 1, pady = 2)
ass_bttn = Button(bottom_frame, text="Log Out", fg="red", command=log_out)
ass_bttn.grid(row = 0, column = 2, pady = 2)
'''
bottom_frame = Frame(main_gui)
bottom_frame.pack(padx=5, pady=5)

log_out_button = Button(bottom_frame, text="Log Out", fg="red", command=log_out)
log_out_button.grid(row = 1, column = 1, pady = 2)


main_gui.pack()

root.mainloop()