#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <list>
using namespace std;

class Graph {
private:
    int numNodes;
    list<pair<int, int>>* adjList;
    vector<int> minPath;
    int minCost;
    int TotalCost;
public:
    Graph(int numNodes) {
        this->numNodes = numNodes;
        adjList = new list<pair<int, int>>[numNodes];
        minCost = INT_MAX;
    }

    void addEdge(int nodeA, int nodeB, int cost) {
        adjList[nodeA].push_back(make_pair(nodeB, cost));
        adjList[nodeB].push_back(make_pair(nodeA, cost));
    }

    void findAllPathsUtil(int currentNode, int targetNode, vector<bool>& visited, vector<int>& path, int totalCost) {
        visited[currentNode] = true;
        path.push_back(currentNode);

        if (currentNode == targetNode) {
            if (totalCost < minCost) {
                minCost = totalCost;
                minPath = path;
            }
        }
        else {
            for (auto edge : adjList[currentNode]) {
                int nextNode = edge.first;
                int edgeCost = edge.second;
                if (!visited[nextNode]) {
                    findAllPathsUtil(nextNode, targetNode, visited, path, totalCost + edgeCost);
                }
            }
        }

        path.pop_back();
        visited[currentNode] = false;
    }

    void findAllPaths(int startNode, int targetNode) {
        vector<bool> visited(numNodes, false);
        vector<int> path;
        int total = 0;
        findAllPathsUtil(startNode, targetNode, visited, path, total);
    }

    void getMinPathAndCost(int source,int destination) {
        minPath.clear();
        minCost=INT_MAX;
        findAllPaths(source,destination);
        if (minCost == INT_MAX) {
            cout << "no route" << endl;
        }
        else {
            ofstream outfile;
            outfile.open("paths.txt",ios::app);
            int count=0;
            for (int node : minPath) {
//                if(count++==0) cout << node;
//                else cout << "-" << node;
                if(count++==0) outfile<<node;
                else outfile<<"-"<<node;
            }
//            cout<<" (cost="<<minCost<<")\n";
            outfile<<" (cost="<<minCost<<")\n";
            outfile.close();
        }
    }

    void generateSpanningTreeUtil(int currentNode, vector<bool>& visited,ofstream& outfile) {
        visited[currentNode] = true;
        for (auto edge : adjList[currentNode]) {
            int nextNode = edge.first;
            if (!visited[nextNode]) {
//                cout << currentNode << " " << nextNode << " " << edge.second << endl;
                outfile<< currentNode << " " << nextNode << " " << edge.second << endl;
                TotalCost+=edge.second;
                generateSpanningTreeUtil(nextNode, visited,outfile);
            }
        }
    }

    void generateSpanningTree(int root) {
        vector<bool> visited(numNodes, false);
        TotalCost=0;
        static int fileCount = 0;
        string fileName = "tree" + to_string(fileCount) + ".txt";
        ofstream outfile(fileName, ios::app);
        outfile<<numNodes<<" // # of Nodes, Nodes = {0,1,2,3,4,5,6,7}\n";
        outfile<<"7 // # of Edges\n";
        outfile<<root<<" // ID of root\n";
        generateSpanningTreeUtil(root, visited,outfile);
//        cout<<TotalCost<<endl;
        outfile<<TotalCost<<endl;
        outfile.close();
        fileCount++;
    }

    void printGraph() {
        for (int i = 0; i < numNodes; ++i) {
            cout << "Node " << i << " -> ";
            for (auto edge : adjList[i]) {
                cout << "(Node: " << edge.first << ", Cost: " << edge.second << ") ";
            }
            cout << endl;
        }
    }
};

int main() {
    ifstream file("graph0_v2.txt");

    if (!file.is_open()) {
        cout << "fail" << endl;
        return 1;
    }

    string line;
    int numNodes, numEdges;
    getline(file, line);
    stringstream(line) >> numNodes;

    getline(file, line);
    stringstream(line) >> numEdges;

    Graph graph(numNodes);

    for (int i = 0; i < numEdges; i++) {
        getline(file, line);
        if (line.empty() || line[0] == '/')
            continue;

        stringstream ss(line);
        int nodeA, nodeB, cost;
        ss >> nodeA >> nodeB >> cost;
        graph.addEdge(nodeA,nodeB,cost);
    }

//    graph.printGraph();

    int path;
    getline(file, line);
    stringstream(line) >> path;

    for(int i = 0; i < path; i++){
        getline(file,line);
        if (line.empty() || line[0] == '/')
            continue;
        stringstream ss(line);
        int start,end;
        ss>>start>>end;
        graph.getMinPathAndCost(start,end);
    }

    int tree;
    getline(file, line);
    stringstream(line) >> tree;

    for(int i = 0; i < tree; i++){
        getline(file,line);
        if (line.empty() || line[0] == '/')
            continue;
        stringstream ss(line);
        int root;
        ss>>root;
        graph.generateSpanningTree(root);
    }
    file.close();

    return 0;
}
