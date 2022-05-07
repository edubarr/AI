// ESTE CÓDIGO NÃO ESTÁ FUNCIONAL. EXISTEM BUGS DE REFERÊNCIAS A SEREM CORRIGIDOS.
// VERSÃO FUNCIONAL EM PYTHON NO ARQUIVO metro_paris.py

#include <iostream>
#include <algorithm>
#include <list>

class Node
{
public:
    int id, cost, weight;
    Node *father;
    Node(int newId, int newAdj[14], const char newStations[3]) : id{newId}
    {
        std::copy(newAdj, newAdj + 14, adj);
        std::copy(newStations, newStations + 2, stations);
        cost = 0;
        weight = 0;
        father = nullptr;
        station = '0';
    }

    // Verifica se achou uma solução
    bool check(Node *destiny)
    {
        if (id == destiny->id)
        {
            return true;
        }
        return false;
    }

    // Verifica se houve troca de estação
    bool check_change(Node *current)
    {
        for (int i = 0; i < 2; i++)
        {
            for (int j = 0; j < 2; j++)
            {
                if (current->stations[i] == stations[j])
                {
                    if (station == '0')
                    {
                        station = current->station;
                    }
                    current->station = station;
                    break;
                }
            }
        }
        if (station == current->station)
        {
            return 0;
        }
        return 4;
    }

    // Gera os filhos
    void generate_sons(std::list<Node *>& frontier, std::list<Node *> nodes, int visiteds[14], int heuristic[14])
    {
        for (int i = 0; i < 14; i++)
        {
            if (adj[i] != 0 && visiteds[i] == 0)
            {

                auto nodeIt = std::next(nodes.begin(), i);
                Node *node = (*nodeIt);
                int change = check_change(node);

                node->cost = cost + adj[i] + change;
                node->weight = heuristic[i] + cost;

                node->father = this;
                bool inserted = 0;

                for (int j = 0; j < frontier.size(); j++)
                {
                    auto frontierIt = std::next(frontier.begin(), j);
                    if (node->weight < (*frontierIt)->weight)
                    {
                        frontier.insert(frontierIt, node);
                        inserted = 1;
                        break;
                    }
                }
                if (!inserted)
                {
                    frontier.push_back(node);

                    // std::list<Node *>::iterator it;
                    // for (it = frontier.begin(); it != frontier.end(); ++it)
                    // {
                    //     std::cout << "ID: " << (*it)->id << " , Tempo Total (minutos): " << (*it)->cost << std::endl;
                    // }
                }
            }
        }
    }

private:
    int adj[14];
    char station;
    char stations[2];
};

class Solve
{

public:
    std::list<Node *> nodes;
    Solve(Node *origin, Node *newDestiny, std::list<Node *> newNodes, int newHeuristic[14])
    {
        nodes = newNodes;
        std::copy(newHeuristic, newHeuristic + 14, heuristic);
        destiny = newDestiny;
        frontier.push_back(origin);
    }

    void print()
    {
        std::list<Node *>::iterator it;
        for (it = path.begin(); it != path.end(); ++it)
        {
            std::cout << "ID: " << (*it)->id << " , Tempo Total (minutos): " << (*it)->cost << std::endl;
        }
    }

    void run_a_star()
    {
        while (frontier.size() != 0)
        {
            auto nodeIt = std::next(frontier.begin(), 0);
            Node *node = (*nodeIt);
            
            if (visiteds[node->id] == 1)
            {
                frontier.pop_front();
                continue;
            }
            
            if (node->check(destiny))
            {
                
                while (node->father != nullptr)
                {
                    path.push_front(node);
                    node = node->father;
                    frontier.pop_front();
                    break;
                }
            }
            else
            {
                node->generate_sons(frontier, nodes, visiteds, heuristic);
                visiteds[node->id] = 1;
                frontier.pop_front();
            }
        }
    }

private:
    int heuristic[14];
    Node *destiny;
    std::list<Node *> frontier;
    int visiteds[14] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    std::list<Node *> path;
};

int main()
{
    // Heuristica: Custo estimado do nó: do nó cujo seja número da linha para os outros
    int heuristic[14][14] = {
        {0, 22, 40, 54, 80, 86, 78, 56, 36, 20, 36, 60, 60, 64},
        {22, 0, 18, 32, 58, 64, 56, 38, 22, 8, 34, 46, 42, 48},
        {40, 18, 0, 14, 40, 44, 38, 30, 20, 22, 42, 42, 26, 36},
        {54, 32, 14, 0, 26, 32, 24, 26, 26, 36, 52, 42, 22, 34},
        {80, 58, 40, 26, 0, 6, 4, 42, 50, 62, 76, 54, 32, 40},
        {86, 64, 44, 32, 6, 0, 8, 46, 56, 66, 82, 60, 34, 40},
        {78, 56, 38, 24, 4, 8, 0, 44, 50, 58, 76, 56, 26, 34},
        {56, 38, 30, 26, 42, 46, 44, 0, 18, 44, 36, 14, 50, 60},
        {36, 22, 20, 26, 50, 56, 50, 18, 0, 26, 24, 24, 46, 56},
        {20, 8, 22, 36, 62, 66, 58, 44, 26, 0, 40, 54, 40, 46},
        {36, 34, 42, 52, 76, 82, 76, 36, 24, 40, 0, 30, 70, 78},
        {60, 46, 42, 42, 54, 60, 56, 14, 24, 54, 30, 0, 62, 74},
        {60, 42, 26, 22, 32, 34, 26, 50, 46, 40, 70, 62, 0, 10},
        {64, 48, 36, 34, 40, 40, 34, 60, 56, 46, 78, 74, 10, 0}};

    // Adjacencias: 0 = impossível. !=0: Custo
    int cost[14][14] = {
        {0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {22, 0, 18, 0, 0, 0, 0, 0, 22, 8, 0, 0, 0, 0},
        {0, 18, 0, 14, 0, 0, 0, 0, 0, 20, 0, 0, 26, 0},
        {0, 0, 14, 0, 26, 0, 0, 26, 0, 0, 0, 0, 22, 0},
        {0, 0, 0, 26, 0, 6, 4, 42, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 26, 42, 0, 0, 0, 18, 0, 0, 14, 0, 0},
        {0, 22, 20, 0, 0, 0, 0, 18, 0, 0, 24, 0, 0, 0},
        {0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 0, 24, 0, 0, 0, 0, 0},
        {0, 0, 0, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0},
        {0, 0, 26, 22, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10},
        {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 0}};

    int origin = -1, destiny = -1;

    // Solicita a origem
    while (origin < 0 || origin > 14)
    {
        std::cout << "Indique a origem(1 - 14): ";
        std::cin >> origin;
    }
    // Solicita o destino
    while (destiny < 0 || destiny > 14)
    {
        std::cout << "Indique o destino(1 - 14): ";
        std::cin >> destiny;
    }

    // Decrementa para corrigir posição no array
    origin--;
    destiny--;

    Node *e1 = new Node(0, cost[0], "B");
    Node *e2 = new Node(1, cost[1], "BY");
    Node *e3 = new Node(2, cost[2], "BR");
    Node *e4 = new Node(3, cost[3], "BG");
    Node *e5 = new Node(4, cost[4], "BY");
    Node *e6 = new Node(5, cost[5], "B");
    Node *e7 = new Node(6, cost[6], "Y");
    Node *e8 = new Node(7, cost[7], "YG");
    Node *e9 = new Node(8, cost[8], "YR");
    Node *e10 = new Node(9, cost[9], "Y");
    Node *e11 = new Node(10, cost[10], "R");
    Node *e12 = new Node(11, cost[11], "G");
    Node *e13 = new Node(12, cost[12], "RG");
    Node *e14 = new Node(13, cost[13], "G");

    std::list<Node *> nodes({e1, e2, e3, e4, e5, e6, e7, e8, e9, e10, e11, e12, e13, e14});

    // Define o estado inicial

    auto originIt = std::next(nodes.begin(), origin);
    Node *originNode = (*originIt);
    auto destinyIt = std::next(nodes.begin(), destiny);
    Node *destinyNode = (*destinyIt);

    Solve *solution = new Solve(originNode, destinyNode, nodes, heuristic[destiny]);


    solution->run_a_star();

    solution->print();

    return 0;
}