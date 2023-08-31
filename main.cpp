#include <iostream>
#include <stdio.h>
#include <string.h>
#include <sstream>
#include <fstream>
#include <algorithm>
#include <string>
#include "header.h"
#include "matriz.h"
#include "doubleList.h"
/*
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/stringbuffer.h"
*/

SparseMatrix *matrix = new SparseMatrix();
DoubleList *empleados = new DoubleList();
DoubleList *proyectos = new DoubleList();
int no_empl = 0;
int no_pry = 0;

void find_str(string s)
{
    // Use find function to find 1st position of delimiter.
    std::string aux[4];
    bool control = true;
    int i = 0;
    int end = s.find(",");
    std::transform(s.begin(), s.end(), s.begin(), ::toupper);
    while (end != -1)
    {
        if (s.substr(0, end) == "ID" || s.substr(0, end) == "NOMBRE" || s.substr(0, end) == "CONTRASE├▒A" || s.substr(0, end) == "CONTRASEÑA" || s.substr(0, end) == "PUESTO")
        {
            control = false;
        }
        else
        {
            aux[i] = s.substr(0, end);
            i++;
        }
        s.erase(s.begin(), s.begin() + end + 1);
        end = s.find(",");
    }
    aux[3] = s.substr(0, end);

    if (control)
    {
        empleados->addEmp(Empleado(aux[0], aux[1], aux[2], aux[3]));
        no_empl++;
    }
}

void readCSV(std::string nombreArchivo)
{
    ifstream archivo(nombreArchivo.c_str());
    string linea;
    while (getline(archivo, linea))
    {
        find_str(linea);
    }
}

void convert_char(std::string aux_name, std::string aux_prioridad)
{
    std::string id = "PY-" + to_string(no_pry);
    char *cstr = new char[aux_prioridad.length() + 1];
    proyectos->add(Proyecto(id, aux_name, *cstr));
    strcpy(cstr, aux_prioridad.c_str());
    // do stuff
    delete[] cstr;
    no_pry++;
}

void menu_proyectos()
{
    int choice;
    int choice_two;

    std::string aux_prioridad;
    std::string aux_name;

    bool control = true;

    while (control)
    {
        std::cout << "Seleccione una opción:\n";
        std::cout << "2 - Crear Proyecto\n2 - Salir\n";

        std::cin >> choice;
        switch (choice)
        {
        case 1:
            std::cin >> aux_name;
            std::cin >> choice_two;
            if (choice_two == 1)
            {
                aux_prioridad = "A";
            }
            else if (choice_two == 2)
            {
                aux_prioridad = "B";
            }
            else if (choice_two == 3)
            {
                aux_prioridad = "C";
            }
            else
            {
                std::cout << "Invalido" << endl;
                control = false;
            }
            convert_char(aux_name, aux_prioridad);
            proyectos->generateGraphvizFile("Proyectos");
            break;
        case 2:
            control = false;
            break;
        default:
            break;
        }
    }
}

void menu_empleados()
{
    int choice;
    int roleChoice;
    int auxInt;
    bool control = true;
    /*
    Para el Empleado auxiliar
    */
    std::string tempName;
    std::string tempPassword;
    std::string tempRole;
    std::string tempID;
    std::string aux;

    // Empleado *aux = new Empleado;

    while (control)
    {
        std::cout << "Seleccione una opción:\n";
        std::cout << "1 - Carga Manual\n2 - Carga Masiva\n3 - Menu principal\n";

        std::cin >> choice;
        switch (choice)
        {
        case 1:
            std::cout << "Nombre: \n";
            std::cin >> tempName;
            std::cout << "\nContraseña:\n";
            std::cin >> tempPassword;
            std::cout << "\nSeleccionar el tipo de rol\n1-FDEV\n2-BDEV\n3-QA\n";
            std::cin >> roleChoice;
            switch (roleChoice)
            {
            case 1:
                no_empl++;
                tempID = "FDEV-" + to_string(no_empl);
                tempRole = "FRONTEND DEVELOPER";
                break;
            case 2:
                no_empl++;
                tempID = "BDEV-" + to_string(no_empl);
                tempRole = "BACKEND DEVELOPER";
                break;
            case 3:
                no_empl++;
                tempID = "QA-" + to_string(no_empl);
                tempRole = "QUALITY ASSURANCE";
                break;
            default:
                std::cout << "Valor invalido";
                control = false;
                break;
            }

            empleados->addEmp(Empleado(tempID, tempName, tempPassword, tempRole));
            empleados->generateGraphvizFileEmp("Empleados");
            break;
        case 2:
            std::cout << "Nombre del archivo: ";
            std::cin >> aux;
            std::cout << "\n";
            readCSV(aux);
            empleados->generateGraphvizFileEmp("Empleados");
            break;
        case 3:
            control = false;
            break;
        default:
            std::cout << "Valor invalido" << endl;
            break;
        }
    }
}

void desp()
{
    int aux1;
    int aux2;
    std::string tarea;
    std::cout << "Seleccionar EMPLEADOS" << endl;
    empleados->printListEmp();
    std::cin >> aux1;
    std::cout << "Seleccionar PROYECTOS" << endl;
    proyectos->printList();
    std::cin >> aux2;
    std::cout << "Nombre de la tarea: ";
    std::cin >> tarea;

    matrix->createNodeTarea(aux1, aux2, tarea);
    matrix->getGraphviz();
}

void menu()
{
    int choice;
    bool control = true;

    while (control)
    {
        std::cout << "Seleccione una opción:\n";
        std::cout << "1 - Cargar empleados\n2 - Crear proyecto\n3 - Asignar tareas\n4 - Ver Empleados \n5 - Salir\n";

        std::cin >> choice;
        switch (choice)
        {
        case 1:
            menu_empleados();
            break;
        case 2:
            menu_proyectos();
            break;
        case 3:
            desp();
            break;
        case 4:
            std::cout << "ID    :  NOMBRE   :   ROL \n";
            empleados->printListEmp();
            break;
        case 5:
            control = false;
            break;
        default:
            std::cout << "Valor invalido" << endl;
            break;
        }
    }
}

int main()
{
    menu();
    return 0;
}