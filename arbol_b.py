import os
cmd = "dot -Tpng arbolB.dot -o arbolB.png"

class Nodo:
    def __init__(self, clave, id, valor, empleado, proyecto, precio = 0, anteriores = [], tamanio=0):
        self.clave = clave
        self.id = id
        self.valor = valor
        self.empleado = empleado
        self.proyecto = proyecto
        self.tamanio = tamanio
        self.estado = "Sin comenzar"
        self.anteriores = anteriores
        self.precio = 0

class NodoArbolB:
    def __init__(self, esHoja=False):
        self.esHoja = esHoja
        self.clavesValores = []
        self.hijos = []

class ArbolB:
    def __init__(self):
        self.raiz = NodoArbolB(True)
        self.grado = 3

    def insertar(self, nuevoNodo):
        raiz = self.raiz
        if len(raiz.clavesValores) == (2 * self.grado) - 1:
            temporal = NodoArbolB()
            self.raiz = temporal
            temporal.hijos.insert(0, raiz)
            self.dividir_hijos(temporal, 0)
            self.insertar_con_espacio(temporal, nuevoNodo)
        else:
            self.insertar_con_espacio(raiz, nuevoNodo)

    def insertar_con_espacio(self, nodo, nuevoNodo):
        posicionActual = len(nodo.clavesValores) - 1
        if nodo.esHoja:
            nodo.clavesValores.append(Nodo(None, None, None, None, None))
            while posicionActual >= 0 and nuevoNodo.clave < nodo.clavesValores[posicionActual].clave:
                nodo.clavesValores[posicionActual +
                                   1] = nodo.clavesValores[posicionActual]
                posicionActual -= 1
            nodo.clavesValores[posicionActual + 1] = nuevoNodo
        else:
            while posicionActual >= 0 and nuevoNodo.clave < nodo.clavesValores[posicionActual].clave:
                posicionActual -= 1
            posicionActual += 1
            if len(nodo.hijos[posicionActual].clavesValores) == (2 * self.grado) - 1:
                self.dividir_hijos(nodo, posicionActual)
                if nuevoNodo.clave > nodo.clavesValores[posicionActual].clave:
                    posicionActual += 1
            self.insertar_con_espacio(nodo.hijos[posicionActual], nuevoNodo)

    def dividir_hijos(self, nodo, posicionActual):
        grado = self.grado
        y = nodo.hijos[posicionActual]
        z = NodoArbolB(y.esHoja)
        nodo.hijos.insert(posicionActual + 1, z)
        nodo.clavesValores.insert(posicionActual, y.clavesValores[grado - 1])
        z.clavesValores = y.clavesValores[grado: (2 * grado) - 1]
        y.clavesValores = y.clavesValores[0: grado - 1]
        if not y.esHoja:
            z.hijos = y.hijos[grado: 2 * grado]
            y.hijos = y.hijos[0: grado - 1]

    def buscar(self, clave, nodo=None):
        if nodo is not None:
            i = 0
            while i < len(nodo.clavesValores) and clave > nodo.clavesValores[i].clave:
                i += 1
            if i < len(nodo.clavesValores) and clave == nodo.clavesValores[i].clave:
                return nodo.clavesValores[i].valor
            elif nodo.esHoja:
                return None
            else:
                return self.buscar(clave, nodo.hijos[i])
        else:
            return self.buscar(clave, self.raiz)

    def whole_tree(self, emp, x, root=False, l=0):
        dotContent = []

        l += 1
        for i in x.clavesValores:
            print(emp, "-", i.empleado)
            if emp == i.empleado:
                dotContent.append([i.clave, i.valor, i.proyecto])

        if len(x.hijos) > 0:
            for i in x.hijos:
                print( emp, "==" ,i.clavesValores[0].empleado)
                if emp == i.clavesValores[0].empleado:
                    dotContent.append([i.clavesValores[0].clave, i.clavesValores[0].valor, i.clavesValores[0].proyecto])
                    aux = self.whole_tree(emp, i, l)
                    for value in aux:
                        dotContent.append(value)
                #dotContent.append(value)
        return dotContent

    def generate_dot_b_tree(self, x):
        dotContent = "digraph G {\n node [shape=record]" + \
            self.aux_export_graphviz(x) + "}"
        f = open("arbolB.dot", "w")
        f.write(dotContent)
        f.close()
        os.system(cmd)

    def aux_export_graphviz(self, x, l=0):
        dotContent = ""
        dotContent += "node" + str(x.clavesValores[0].clave) + " [label=\""
        dotContent += '|'.join([str(i.clave) + "\\n" + i.valor for i in x.clavesValores])
        dotContent += "\"];\n"
        l += 1
        if len(x.hijos) > 0:
            for i in x.hijos:
                dotContent += "node" + \
                    str(x.clavesValores[0].clave) + "->" + "node" + \
                    str(i.clavesValores[0].clave) + "\n"
                dotContent += self.aux_export_graphviz(i, l)
        return dotContent