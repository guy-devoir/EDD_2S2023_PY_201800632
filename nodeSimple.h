#pragma once

#include "header.h"

#ifndef NODE_H
#define NODE_H

class NodeSimple
{
public:
    Empleado value_emp ;
    Proyecto value_pry ;
    NodeSimple *next;
    NodeSimple *prev;
    NodeSimple(Empleado value);
    NodeSimple(Proyecto value);
};

#endif // !NODE_H