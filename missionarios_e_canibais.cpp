// mis_e = Missionários na margem esquerda
// mis_d = Missionários na margem direita
// can_e = Canibais na margem esquerda
// can_d = Canibais na margem direita
// boat = Posição do barco (d = direita ou e = esquerda)
//
//  O usuário é questionado em qual margem deseja que se inicie o problema.

#include <iostream>
#include <list>

class State
{
public:
    State *father;
    std::list<State *> sons;
    State(int newMis_e, int newMis_d, int newCan_e, int newCan_d, char newBoat) : mis_e{newMis_e}, mis_d{newMis_d}, can_e{newCan_e}, can_d{newCan_d}, boat{newBoat}
    {
        State *father = nullptr;
    }

    // Imprime o estado atual
    void print()
    {
        std::cout << "mis_e: " << mis_e << " can_e: " << can_e << " mis_d: " << mis_d << " can_d: " << can_d << " boat: " << boat << std::endl;
    }

    // Verifica se achou uma solução
    bool check(char margin)
    {
        bool mis = false;
        bool can = false;

        if (margin == 'e')
        {
            if (mis_e == 0 && mis_d == 3)
            {
                mis = true;
            }
            if (can_e == 0 && can_d == 3)
            {
                can = true;
            }
        }
        else if (margin == 'd')
        {
            if (mis_e == 3 && mis_d == 0)
            {
                mis = true;
            }
            if (can_e == 3 && can_d == 0)
            {
                can = true;
            }
        }
        return (mis && can);
    }

    // Verifica se é um nó válido
    bool is_valid()
    {
        if (mis_e > 3 || mis_e < 0)
        {
            return false;
        }
        if (mis_d > 3 || mis_d < 0)
        {
            return false;
        }
        if (can_e > 3 || can_e < 0)
        {
            return false;
        }
        if (can_d > 3 || can_d < 0)
        {
            return false;
        }

        if ((mis_e == 0 || mis_e >= can_e) && (mis_d == 0 || mis_d >= can_d))
        {
            return true;
        }

        return false;
    }

    // Gera os filhos
    void generate_sons()
    {
        int moves[5][2] = {{1, 0}, {1, 1}, {2, 0}, {0, 1}, {0, 2}}; // Movimentos possíveis

        char newBoat = 't';
        if (boat == 'e')
        {
            newBoat = 'd';
        }
        else if (boat == 'd')
        {
            newBoat = 'e';
        }

        for (int i = 0; i < 5; i++)
        {
            int newMis_e = 0, newMis_d = 0, newCan_e = 0, newCan_d = 0;

            if (newBoat == 'd')
            {
                newMis_e = mis_e - moves[i][0];
                newMis_d = mis_d + moves[i][0];

                newCan_e = can_e - moves[i][1];
                newCan_d = can_d + moves[i][1];
            }

            else if (newBoat == 'e')
            {
                newMis_e = mis_e + moves[i][0];
                newMis_d = mis_d - moves[i][0];

                newCan_e = can_e + moves[i][1];
                newCan_d = can_d - moves[i][1];
            }

            State *newState = new State(newMis_e, newMis_d, newCan_e, newCan_d, newBoat);

            newState->father = this;

            if (newState->is_valid())
            {
                this->sons.push_back(newState);
            }
        }
    }

private:
    int mis_e, mis_d, can_e, can_d;
    char boat;
};

int main()
{
    // Cria listas de estados e do caminho a ser encontrado.
    std::list<State *> states;
    std::list<State *> path;
    char margin = 'a';

    // Solicita a margem inicial
    while (margin != 'e' && margin != 'd')
    {
        std::cout << "Indique a margem inicial(e ou d): ";
        std::cin >> margin;
    }

    // Define o estado inicial
    State *start = nullptr;
    if (margin == 'e')
    {
        start = new State(3, 0, 3, 0, margin);
    }
    if (margin == 'd')
    {
        start = new State(0, 3, 0, 3, margin);
    }
    states.push_back(start);

    // Percorre a lista de estados e verifica se é solução, caso contrário gera os filhos
    std::list<State *>::iterator it;
    for (it = states.begin(); it != states.end(); ++it)
    {
        if ((*it)->check(margin))
        {
            // Caso seja solução, retorna para guardar o caminho da solução
            while ((*it)->father != nullptr)
            {
                path.push_front((*it));
                (*it) = (*it)->father;
            }
            break;
        }

        (*it)->generate_sons();
        std::list<State *>::iterator it2;
        for (it2 = (*it)->sons.begin(); it2 != (*it)->sons.end(); ++it2)
        {
            states.push_back((*it2));
        }
    }

    // Percorre o caminho da solução e imprime
    for (it = path.begin(); it != path.end(); ++it)
    {
        (*it)->print();
    }

    return 0;
}