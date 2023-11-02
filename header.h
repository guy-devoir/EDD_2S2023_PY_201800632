#pragma once
#include <string>

#ifndef _NODE_H_
#define _NODE_H_

struct Empleado
{
    std::string id, name, password, role ;
    

    Empleado(){

    }

    Empleado(std::string id,std::string name,std::string password,std::string role){
        this->id = id ;
        this->name = name ;
        this->password = password ;
        this->role = role ;
    }
};

struct Proyecto
{
    char prioridad ;
    std::string nombre, id ;
    Proyecto(){

    }

    Proyecto(std::string id, std::string name, char prioridad){
        this->id = id ;
        this->nombre = name;
        this->prioridad = prioridad;
    }
};

class Node
{
public:
    int row;
    int col;
    std::string val ;
    Node *up;
    Node *down;
    Node *left;
    Node *right;
};

#endif // _NODE_H_