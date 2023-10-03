import tkinter
import json
import os
from avl_tree import AVL_Tree, TreeNode, Proyect
from arbol_b import ArbolB, Nodo
from tkinter import Entry, Frame, Button, Label
from tkinter import ttk
from tkinter import filedialog as fd
import tkinter.messagebox as tkmb

cabezera = [["","ID","Nombre","Contraseña","Puesto"]]

#values_box = []

hash_table = []
hash_table_len = 5

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

def read_json():
    global control_AVL
    global control_B
    global PRY_TREE
    global root
    global B

    B = ArbolB()
    control_AVL = 1
    control_B = 1
    PRY_TREE = AVL_Tree()
    root = None

    filetypes = (
        ('text files', '*.json'),
        ('All files', '*.*')
    )
    path = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )

    json_file = open(path, "r", encoding="utf-8")

    datos = json.load(json_file)

    for proyecto in datos['Proyectos']:
        try:
            root = PRY_TREE.insert(root, control_AVL, Proyect(id=proyecto['id'], nombre=proyecto['nombre'], prioridad=proyecto['prioridad']))
            control_AVL += 1
            for tarea in proyecto['tareas']:
                #Acá se pondra el Árbol B
                tarea_id = "T" + str(control_B) + "-" + proyecto['id']
                B.insertar(
                    Nodo(
                        clave=hash_code(tarea_id), 
                        id=tarea_id , 
                        valor=tarea['nombre'], 
                        empleado=tarea['empleado'],
                        proyecto=proyecto['id'])
                    )
                #combo.insert(control_B, tarea['nombre'])
                control_B += 1
        except Exception as e:
            raise e
    
    PRY_TREE.export_graphviz(root)

    B.generate_dot_b_tree(B.raiz)
    
    #PRY_TREE.preOrder(root)
    
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

        sort_hash(hash_table, 0, len(hash_table) - 1)

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
            ##tkmb.showinfo(title="Login Successful", message="Admin")
        else:
            for i in range(len(hash_table)):
                print(user == hash_table[i][1], "fs", password ==hash_table[i][3])

                if user == hash_table[i][1] or user == hash_table[i][2]:
                    if password == hash_table[i][3]:
                        login_frame.pack_forget()
                        main_gui.pack()
                        #tkmb.showinfo(title="Login Successful", message="Admin")
                    else:
                        login_frame.pack_forget()
                        main_gui.pack()
    except Exception as e:
        raise e

def exportar_hash():
    dotContent = "digraph G {\n node [shape=record ] \n" + aux_export_graphiz() + "}"
    f = open("HashTable.dot", "w")
    f.write(dotContent)
    f.close()
    cmd = "dot -Tpng HashTable.dot -o HashTable.png"
    os.system(cmd)

def aux_export_graphiz():
    string = ""

    for i in range(0, hash_table_len):
        print(i, " ", hash_table_len)
        if i <= (len(hash_table)-1):
            string += "nodo{0}".format(str(i)) + "[label=\"<f0> {0} |<f1> {1} |<f2> {2} \"]\n".format(hash_table[i][0],hash_table[i][1],hash_table[i][2])
        else:
            string += "nodo{0}".format(str(i)) + "[label=\"Vacio\"]\n"
        
        if i != (hash_table_len - 1):
            string += "nodo{0}->nodo{1}\n".format(str(i), str(i+1))
        else:
            pass
    
    return string

root = tkinter.Tk()

root.title("Proyecto FASE 2")

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
#tab3 = Frame(tabControl)

tabControl.add(tab1, text="Usuarios")
tabControl.add(tab2, text="Proyecto y Tareas")
#tabControl.add(tab3, text="Tareas")

tabControl.pack()

top_frame = Frame(tab1)
top_frame.pack( side = "top", padx=10, pady=10 )

users_load_bttn = Button(top_frame, text="Cargar Usuarios", fg="red", command=load_users)
users_load_bttn.pack()

reporte_users = Button(top_frame, text="Reporte Usuarios", command=exportar_hash)
reporte_users.pack()

cab_frame = Frame(tab1)
cab_frame.pack(padx=20)

t = Table(root=cab_frame, table=cabezera, cab=True)

frame = Frame(tab1)
frame.pack(padx=20, pady=20)

####################

top_frame_pry = Frame(tab2)
top_frame_pry.pack(padx=20, pady=20)

def reporte_proyecto():
    PRY_TREE.export_graphviz(root)

def reporte_tareas():
    B.generate_dot_b_tree(B.raiz)

users_load_bttn = Button(top_frame_pry, text="Cargar JSON", fg="red", command=read_json)
users_load_bttn.pack()
report_pry = Button(top_frame_pry, text="Reporte Proyectos", fg="red", command=reporte_proyecto)
report_pry.pack()
ass_report = Button(top_frame_pry, text="Cargar JSON", fg="red", command=reporte_tareas)
ass_report.pack()


middle_frame_pry = Frame(tab2)
middle_frame_pry.pack()


###########

top_frame_tra = Frame(tab3)
top_frame_tra.pack(padx=20, pady=20)

combo = ttk.Combobox(top_frame_tra)
combo.pack()

cab_tar = Frame(tab3)
cab_tar.pack()

# NO TOCAR
bottom_frame = Frame(main_gui)
bottom_frame.pack(padx=5, pady=5)

log_out_button = Button(bottom_frame, text="Log Out", fg="red", command=log_out)
log_out_button.grid(row = 1, column = 1, pady = 2)
#######

login_frame.pack()

root.mainloop()