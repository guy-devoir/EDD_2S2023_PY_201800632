import tkinter
import json
import os
from avl_tree import AVL_Tree, TreeNode, Proyect
from arbol_b import ArbolB, Nodo
from tkinter import Entry, Frame, Button, Label, Scrollbar
from tkinter import ttk
from tkinter import filedialog as fd
from datetime import datetime
from hashlib import sha256
from merkle import MerkleTree

cabezera = [["","ID","Nombre","Contraseña","Puesto", "Wallet"]]
ca_dos = [["","Clave","Tarea","Proyecto","Puesto", "..."]]

hash_table = []
hash_table_len = 5

wallets = []

class NodoGrafo:
    def __init__(self, name):
        self.name = name
        self.tareas = []

    def add(self, dato):
        self.tareas.append(dato)

    def exportGrafo(self):
        cmd = "dot -Tpng "+self.name+".dot -o "+self.name+".png"

        dotContent = "digraph G {\n node [shape=oval]" + \
            self.__exportGraph() + "}"
        
        filename = self.name + ".dot"

        f = open(filename, "w")
        f.write(dotContent)
        f.close()
        os.system(cmd)
    
    def __exportGraph(self):
        dotContent = ""
        for i in range(len(self.tareas)):
            dotContent += "node" + str(self.tareas[i].clave) + "[label=\""
            dotContent += self.tareas[i].valor
            dotContent += "\"];\n"
            for j in range(len(self.tareas[i].anteriores)):
                aox = hash_code(self.tareas[i].anteriores[j])
                dotContent += "node" + str(self.tareas[i].clave) + "->" + "node" + str(aox) +"\n"
        return dotContent

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
                else:
                    self.e = Entry(root, width=20, fg='blue', font=('Arial',16,'normal'))
                    self.e.grid(row=i, column=j)
                    self.e.insert(1 , table[i][j])

class TableAss:
    def __init__(self, root, table):
        total_rows = len(table)
        total_columns = len(table[0])
        for i in range(total_rows):
            for j in range(total_columns):
                self.e1 = Entry(root, width=20, font=('Arial',12,'bold'))
                self.e1.grid(row=i, column=j)
                self.e1.insert(0 , table[i][j])


def read_json():
    global control_AVL
    global control_B
    global PRY_TREE
    global root
    global B
    global graphs

    graphs = []

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

    second_file = open("ants.json", "r", encoding="utf-8")

    ant = json.load(second_file)
    
    for proyecto in datos['Proyectos']:
        try:
            root = PRY_TREE.insert(root, control_AVL, Proyect(id=proyecto['id'], nombre=proyecto['nombre'], prioridad=proyecto['prioridad']))
            control_AVL += 1
            tempGraph = NodoGrafo(proyecto['id'])
            
            for tarea in proyecto['tareas']:
                #Acá se pondra el Árbol B
                tarea_id = "T" + str(control_B) + "-" + proyecto['id']
                precio = 0
                aux = []

                for vidk in ant['Tareas']:
                    if vidk['codigo'] == tarea_id:
                        precio = vidk['pago']
                        for antecesor in vidk['antecesor']:
                            aux.append(antecesor['codigo'])


                B.insertar(
                    Nodo(
                        clave=hash_code(tarea_id), 
                        id=tarea_id , 
                        valor=tarea['nombre'], 
                        empleado=tarea['empleado'],
                        proyecto=proyecto['id'],
                        precio = precio,
                        anteriores = aux
                        )
                    )
                
                tempGraph.add(
                    Nodo(
                        clave=hash_code(tarea_id), 
                        id=tarea_id , 
                        valor=tarea['nombre'], 
                        empleado=tarea['empleado'],
                        proyecto=proyecto['id'],
                        precio = precio,
                        anteriores = aux
                    )
                )

                control_B += 1

            graphs.append(tempGraph)
        except Exception as e:
            raise e

    json_file.close()
    second_file.close()

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

                auxCon = subdiv[2].replace("\"", "")
                list.append(sha256(auxCon.encode('utf-8')).hexdigest())

                list.append(subdiv[3].replace("\"", ""))

                list.append("")

                hash_table.append(list)

                if (len(hash_table)/hash_table_len) >= 0.7:
                    next_fib(hash_table_len)
                
        archivo.close()

        sort_hash(hash_table, 0, len(hash_table) - 1)

        global t2
        t2 = Table(root=frame, table=hash_table, cab=False)

def log_out():
    main_gui.pack_forget()
    login_frame.pack()

def log_out_user():
    destroyMe.destroy()
    user_gui.pack_forget()
    login_frame.pack()

def log_in():
    user = txt_w.get()
    password = psw_w.get()
    try:
        if user == "admin" and password == "admin":
            login_frame.pack_forget()
            main_gui.pack()
        else:
            for i in range(len(hash_table)):
                auxCon = sha256(password.encode('utf-8')).hexdigest()
                if user == hash_table[i][1] or user == hash_table[i][2]:
                    if auxCon == hash_table[i][3]:
                        global CURRENT_USER
                        CURRENT_USER = i
                        login_frame.pack_forget()
                        user_gui.pack()
                        current_user_label.config(text=hash_table[i][1] + "-" + hash_table[i][2])
                        show_ass["state"] = "normal"
                    else:
                        pass
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




def openNewWindow():
    newWindow = ttk.Toplevel(root)
    newWindow.title("New Window")

    newWindow.geometry("200x200")

    Label(newWindow, text ="CLAVE").pack()

def trans(clave):
    myobj = datetime.now()
    print(entry_clave.get())
    aux = entry_clave.get()
    arrayBool = []

    x, y = 0

    for i in range(len(graphs)):
        for j in range(len(graphs[i].tareas)):
            if aux == graphs[i].tareas[j].clave:
                for k in range(len(graphs[i].tareas[j].anteriores)):
                    arrayBool.append(search_graph(graphs[i], graphs[i].tareas[j].anteriores[k]))
                x = i
                y = j
                break


    if len(arrayBool) > 0:
        for element in arrayBool:
            if element:
                pass
            else:
                return

    graphs[x][y].estado = "Terminado"
    hash_table[CURRENT_USER][1]

    hojaMerkle = str(myobj.day) +"-"+ str(myobj.month) +"-"+ str(myobj.year) + "::" + str(myobj.hour) + ":" + str(myobj.minute) + ":" + str(myobj.second) 
    hojaMerkle += hash_table[CURRENT_USER][2]
    hojaMerkle += str(graphs[x][y].precio)
    if hash_table[CURRENT_USER][5] == "":
        hojaMerkle += createWallet()
        hash_table[CURRENT_USER][5] = createWallet()
        wallets.append([createWallet(), [], MerkleTree()])
    else:
        hojaMerkle += hash_table[CURRENT_USER][5]

    for wallet in wallets:
        if wallet[0] == hash_table[CURRENT_USER][5]:
            wallet[1].append(hojaMerkle)
            mtree = MerkleTree(wallet[1])
            wallet[2] = mtree
            mtree.exportGraphviz(mtree.root)
            return

    return

def createWallet():
    return "DC" + str(CURRENT_USER) + str(hash_table[CURRENT_USER][0])

def changeProcess(clave):
    print(entry_clave.get())
    aux = entry_clave.get()
    arrayBool = []

    x, y = 0

    for i in range(len(graphs)):
        for j in range(len(graphs[i].tareas)):
            if aux == graphs[i].tareas[j].clave:
                for k in range(len(graphs[i].tareas[j].anteriores)):
                    arrayBool.append(search_graph(graphs[i], graphs[i].tareas[j].anteriores[k]))
                x = i
                y = j
                break


    if len(arrayBool) > 0:
        for element in arrayBool:
            if element:
                pass
            else:
                return
        graphs[x][y].estado = "En proceso"
    else:
        graphs[x][y].estado = "En proceso"
    
    return    

def search_graph(gactual, clave):
    for tarea in gactual.tareas:
        if clave == tarea.clave:
            if tarea.estado == "Terminado":
                return True
            else:
                return False
            

def load_assignments():
    global destroyMe
    global aux_table
    destroyMe = Frame(user_gui)
    destroyMe.pack(side = "bottom", padx=10, pady=10 )
    show_ass["state"] = "disabled" 
    aux_table = B.whole_tree(hash_table[CURRENT_USER][1], B.raiz)
    clean_table = []
    print(hash_table[CURRENT_USER][1])
    for value in aux_table:
        if value in clean_table:
            pass
        else:
            clean_table.append(value)
    aux_table = clean_table
    t_t = TableAss(root=destroyMe, table=aux_table)


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

#USER GUI

user_gui = Frame(root)
welcome_sign = Label(user_gui, text="Bienvenido:")
welcome_sign.pack()
current_user_label = Label(user_gui)
current_user_label.pack()

show_ass = Button(user_gui, text="Mostrar Tareas", fg="red", command=load_assignments)
show_ass["state"] = "normal"
show_ass.pack()

log_out_usr_btt = Button(user_gui, text="Log Out", fg="red", command=log_out_user)
log_out_usr_btt.pack()

comp_frame = Frame(user_gui)
comp_frame.pack(pady=8)

entry_clave = Entry(comp_frame, width = 45)
entry_clave.pack()

completeBtn = Button(comp_frame, text="Terminado",  command=trans)
completeBtn.pack()

processBtn = Button(comp_frame, text="En proceso",command=changeProcess)
processBtn.pack()

#ADMIN GUI
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

scrollbar = Scrollbar(tab1)
scrollbar.pack( side = 'right', fill='y' )

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

def all_graphs():
    for graph in graphs:
        graph.exportGrafo()

users_load_bttn = Button(top_frame_pry, text="Cargar JSON", fg="red", command=read_json)
users_load_bttn.pack(pady=8)
report_pry = Button(top_frame_pry, text="Reporte Proyectos", fg="red", command=reporte_proyecto)
report_pry.pack(pady=8)
ass_report = Button(top_frame_pry, text="Reporte Tareas", fg="red", command=reporte_tareas)
ass_report.pack(pady=8)

graphs_report = Button(top_frame_pry, text="Reporte de Grafos", command=all_graphs)
graphs_report.pack(pady=8)


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

log_out_button = Button(top_frame, text="Log Out", fg="red", command=log_out)
log_out_button.pack()
#######

login_frame.pack()

root.mainloop()

#def mixmerkletree() -> None:
#    elems = ["GeeksforGeeks", "A", "Computer", "Science", "Portal", "For", "Geeks"]
#    #as there are odd number of inputs, the last input is repeated
#    print("Inputs: ")
#    print(*elems, sep=" | ")
#    print("")
#    mtree = MerkleTree(elems)
#    print("Root Hash: "+mtree.getRootHash()+"\n")
#    mtree.printTree()
 
 
#mixmerkletree()