#pragma once

#ifndef DOUBLELIST_H
#define DOUBLELIST_H

#include <string>
#include "nodeSimple.h"
#include <iostream>


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
    
};

#endif // !DOUBLELIST_H