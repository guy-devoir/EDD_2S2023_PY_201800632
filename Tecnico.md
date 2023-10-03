# Proyecto Fase 2 - Manual Técnico

## Hash Table

### Nodo de Hash

El nodo de Hash tiene la siguiente estructura:

1. ID de la tabla Hash
2. ID del Empleado
3. Nombre de Empleado
4. Contraseña
5. Puesto del Empleado

Para obtener el ID de la Tabla Hash se utiliza el siguiente código

```
def hash_code(string):
    lst = 0
    for letter in string:
        lst += int(ord(letter))
    return lst

```
### Ordenar la Tabla Hash
Para ordenar la tabla Hash se utiliza un Quick Sort

```
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
```

 ## Arbol AVL

 ### Nodo del Arbol

 La estructura del Nodo del Árbol es la siguiente:

 ```
class TreeNode(object):
	def __init__(self, val, content):
		self.val = val
		self.content = content
		self.left = None
		self.right = None
		self.height = 1
  ```
  El atributo de content es de la clase Proyecto
 ```
class Proyect(object):
	def __init__(self, id, nombre, prioridad):
		self.id = id
		self.nombre = nombre
		self.prioridad = prioridad
```

### Métodos del Árbol AVL

 Para ingresar los nodos al Arbol se utiliza el método "insert":

```
 class AVL_Tree(object):

	def insert(self, root, key, content):
		if not root:
			return TreeNode(key, content)
		elif key < root.val:
			root.left = self.insert(root.left, key, content)
		else:
			root.right = self.insert(root.right, key, content)

		root.height = 1 + max(self.getHeight(root.left),
						self.getHeight(root.right))

		balance = self.getBalance(root)

		if balance > 1 and key < root.left.val:
			return self.rightRotate(root)

		if balance < -1 and key > root.right.val:
			return self.leftRotate(root)

		if balance > 1 and key > root.left.val:
			root.left = self.leftRotate(root.left)
			return self.rightRotate(root)

		if balance < -1 and key < root.right.val:
			root.right = self.rightRotate(root.right)
			return self.leftRotate(root)

		return root
```

Para Rotar se utilizán los siguientes métodos:
1. Rotar a la Izquiera
2. Rotar a la Derecha
3. Balancear

 ```
    def leftRotate(self, z):

		y = z.right
		T2 = y.left

		y.left = z
		z.right = T2

		z.height = 1 + max(self.getHeight(z.left),
						self.getHeight(z.right))
		y.height = 1 + max(self.getHeight(y.left),
						self.getHeight(y.right))

		return y

	def rightRotate(self, z):

		y = z.left
		T3 = y.right

		y.right = z
		z.left = T3

		z.height = 1 + max(self.getHeight(z.left),
						self.getHeight(z.right))
		y.height = 1 + max(self.getHeight(y.left),
						self.getHeight(y.right))

		return y

    def getBalance(self, root):
		if not root:
			return 0

		return self.getHeight(root.left) - self.getHeight(root.right)


 ```

 ## Árbol B

### Nodo del Arbol B

```
class Nodo:
    def __init__(self, clave, id, valor, empleado, proyecto,tamanio=0):
        self.clave = clave
        self.id = id
        self.valor = valor
        self.empleado = empleado
        self.proyecto = proyecto
        self.tamanio = tamanio
```
### Métodos del Árbol B

Método Inicial

```
def __init__(self):
        self.raiz = NodoArbolB(True)
        self.grado = 3
```

Métodos para insertar

```
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
```

## Reportes

Para los reportes se utilizó Graphviz. De forma simple se crea una cadena que se guarda en un archivo .dot que luego con el comando siguiente se crea una imagén de la estructura deseada

```
#Se tiene que importar la librería os para usar el comando
#os.system(cmd)

import os
cmd = "dot -Tpng arbolB.dot -o arbolB.png"
```