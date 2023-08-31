# Proyecto Fase 1 - Estructura de Datos

## Lista Doblemente Enlazada
Definición de la lista doblemente enlazada

```
class DoubleList
{
public:
    DoubleList();
    void add(Proyecto value);
    void remove(std::string value);
    void addEmp(Empleado value);
    void removeEmp(std::string value);
    void generateGraphvizFile(std::string fileName);
    void printList();
    void generateGraphvizFileEmp(std::string fileName);
    void printListEmp();

private:
    NodeSimple *head;
    NodeSimple *search(std::string value);
    NodeSimple *searchEmp(std::string value);
    NodeSimple *searchByIndex(int value);
    
};
```
Se añade con el siguiente método

```
void DoubleList::add(Proyecto value)
{
    NodeSimple *search = this->search(value.nombre);
    if (search != NULL)
    {
        printf("El valor %d ya existe en la lista\n", value);
        return;
    }

    NodeSimple *newNode = new NodeSimple(value);
    if (this->head == NULL)
    {
        this->head = newNode;
    }
    else
    {
        NodeSimple *current = this->head;
        while (current->next != NULL)
        {
            current = current->next;
        }
        current->next = newNode;
        newNode->prev = current;
    }
}
```

Añadir un nodo a una lista doblemente enlazada, debes crear el nodo con el valor que quieres insertar y luego enlazarlo con los nodos anterior y siguiente de la lista.
Este método se ha duplicado para la estructura de Empleado también

De la misma manera la siguiente función ha sido usada para la creación de la grafica de graficas en Graphviz

```
void DoubleList::generateGraphvizFile(std::string fileName)
{
    FILE *file;
    std::string fileNameWithExtension = fileName + ".dot";
    file = fopen(fileNameWithExtension.c_str(), "w");
    if (file != NULL)
    {
        std::string text = "digraph G {\n";
        text += "node [shape=record];\n";

        NodeSimple *current = this->head;
        while (current != NULL)
        {
            text += current->value_pry.nombre + ";\n";
            if (current->next != NULL)
            {
                text += current->value_pry.nombre + "->" + current->next->value_pry.nombre + ";\n";
            }
            if (current->prev != NULL)
            {
                text += current->value_pry.nombre + "->" + current->prev->value_pry.nombre + ";\n";
            }
            current = current->next;
        }

        text += "}";
        fputs(text.c_str(), file);
        fclose(file);

        std::string command = "dot -Tpng " + fileNameWithExtension + " -o " + fileName + ".png";
        system(command.c_str());
    }
    else
    {
        printf("Error al generar el archivo\n");
    }
}
```

Igualmente se ha duplicado para su utilización con la estructura de Empleado.

## Matriz Esparcida
Utilizada para relacionar los empleados, proyectos y tareas

```
Node *SparseMatrix::createNodeTarea(int row, int col, std::string val)
{
    Node *newNode = new Node;
    newNode->row = row;
    newNode->col = col;
    newNode->val = val;
    newNode->up = NULL;
    newNode->down = NULL;
    newNode->left = NULL;
    newNode->right = NULL;

    Node *temp = createVertHead(row);
    Node *temp2 = createHorzHead(col);

    Node *temp3 = temp->right;
    Node *temp4 = temp2->down;

    while (temp3 != NULL)
    {
        if (temp3->col > col)
        {
            break;
        }
        temp = temp->right;
        temp3 = temp3->right;
    }

    while (temp4 != NULL)
    {
        if (temp4->row > row)
        {
            break;
        }
        temp2 = temp2->down;
        temp4 = temp4->down;
    }

    newNode->right = temp3;
    newNode->left = temp;
    newNode->up = temp2;
    newNode->down = temp4;

    if (temp3 != NULL)
    {
        temp3->left = newNode;
    }
    if (temp4 != NULL)
    {
        temp4->up = newNode;
    }
    temp->right = newNode;
    temp2->down = newNode;

    return newNode;
}
```
Se le da como argumento el numero de columna y fila para que sea ubicada.

El constructor de esta matriz es la siguiente:

```
SparseMatrix::SparseMatrix()
{
    head = new Node;
    head->row = -1;
    head->col = -1;
    head->val = -1;
    head->up = NULL;
    head->down = NULL;
    head->left = NULL;
    head->right = NULL;
}
```
Solo contiene la estructura tarea