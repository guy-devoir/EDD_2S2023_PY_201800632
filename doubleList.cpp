#include <stdio.h>
#include <stdlib.h>
#include <string>
#include <iostream>
#include "nodeSimple.h"
#include "doubleList.h"

DoubleList::DoubleList()
{
    this->head = NULL;
}

NodeSimple::NodeSimple(Proyecto value){
        this->value_pry = value ;
        this->next = NULL;
        this->prev = NULL ;
}

NodeSimple::NodeSimple(Empleado value){
        this->value_emp = value ;
        this->next = NULL;
        this->prev = NULL ;
}

/* Para los proyectos */

NodeSimple *DoubleList::search(std::string value)
{
    NodeSimple *current = this->head;
    while (current != NULL)
    {
        if (current->value_pry.nombre == value)
        {
            return current;
        }
        current = current->next;
    }
    return NULL;
}

void DoubleList::printList()
{
    NodeSimple *current = this->head;
    int control = 1 ;
    while (current != NULL)
    {
        /*if (current->value == value)
        {
            return current;
        }*/
        std::cout << std::to_string(control) << " - Nombre de Proyecto: " << current->value_pry.nombre << "\n";
        current = current->next;
        control++ ;
    }
}

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
    //this->sortAsc();
}

void DoubleList::remove(std::string value)
{
    NodeSimple *node = this->search(value);
    if (node == NULL)
    {
        printf("El valor %d no existe en la lista\n", value);
        return;
    }

    if (node->prev != NULL)
    {
        node->prev->next = node->next;
    }
    else
    {
        head = node->next;
    }
    if (node->next != NULL)
    {
        node->next->prev = node->prev;
    }
    delete node;
}

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

/*Para Empleado*/

NodeSimple *DoubleList::searchEmp(std::string value)
{
    NodeSimple *current = this->head;
    while (current != NULL)
    {
        if (current->value_emp.id == value || current->value_emp.name == value)
        {
            return current;
        }
        current = current->next;
    }
    return NULL;
}

void DoubleList::printListEmp()
{
    NodeSimple *current = this->head;
    int control = 1;
    while (current != NULL)
    {
        /*if (current->value == value)
        {
            return current;
        }*/
        std::cout << std::to_string(control) << " - " << current->value_emp.id << " : " << current->value_emp.name << " : " << current->value_emp.role << "\n";
        current = current->next;
        control++;
    }
}

void DoubleList::addEmp(Empleado value)
{
    NodeSimple *search = this->searchEmp(value.name);
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
    //this->sortAsc();
}

void DoubleList::removeEmp(std::string value)
{
    NodeSimple *node = this->searchEmp(value);
    if (node == NULL)
    {
        printf("El valor %d no existe en la lista\n", value);
        return;
    }

    if (node->prev != NULL)
    {
        node->prev->next = node->next;
    }
    else
    {
        head = node->next;
    }
    if (node->next != NULL)
    {
        node->next->prev = node->prev;
    }
    delete node;
}

void DoubleList::generateGraphvizFileEmp(std::string fileName)
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
            text += current->value_emp.name + ";\n";
            if (current->next != NULL)
            {
                text += current->value_emp.name + "->" + current->next->value_emp.name + ";\n";
            }
            if (current->prev != NULL)
            {
                text += current->value_emp.name + "->" + current->prev->value_emp.name + ";\n";
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

/**/

NodeSimple *DoubleList::searchByIndex(int value)
{
    NodeSimple *current = this->head;
    int control = 1;
    while (current != NULL)
    {
        if (control == value)
        {
            return current;
        }
        current = current->next;
    }
    return NULL;
}