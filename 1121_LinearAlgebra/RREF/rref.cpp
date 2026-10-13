#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <iomanip>
#include <cmath>
using namespace std;

void printMatrix(const vector<vector<double>> &matrix) {
    for (int i = 0; i < matrix.size(); ++i) {
        for (int j = 0; j < matrix[i].size(); ++j) {
            double element = matrix[i][j];
            if(element==0.0) cout<<"0\t";
            else cout << matrix[i][j] << "\t";
        }
        cout << endl;
    }
}

void calculateRREF(vector<vector<double>> &matrix) {
    long long numRows = matrix.size();
    long long numCols = matrix[0].size();

    int lead = 0;
    for (int row = 0; row < numRows; ++row) {
        if (lead >= numCols) {
            break;
        }

        int i = row;
        while (matrix[i][lead] == 0.0) {
            ++i;
            if (i == numRows) {
                i = row;
                ++lead;
                if (numCols == lead) break;
            }
        }

        // Swap rows
        for (int j = 0; j < numCols; ++j) {
            swap(matrix[row][j], matrix[i][j]);
        }

        // Scale to make the leading entry 1
        double scale = matrix[row][lead];
        if (scale != 0.0) {
            for (int j = 0; j < numCols; ++j) {
                matrix[row][j] /= scale;
            }
        }

        // Eliminate other entries in the column
        for (int i = 0; i < numRows; ++i) {
            if (i != row) {
                double factor = matrix[i][lead];
                for (int j = 0; j < numCols; ++j) {
                    matrix[i][j] -= factor * matrix[row][j];
                }
            }
        }

        ++lead;
    }
}

int RankA(const vector<vector<double>> &matrix) {
    int rank = 0;
    for (int i = 0; i < matrix.size(); ++i) {
        bool isZeroRow = true;
        for (int j = 0; j < matrix[i].size()-1; ++j) {
            if (matrix[i][j] != 0.0) {
                isZeroRow = false;
                break;
            }
        }
        if (!isZeroRow) ++rank;
    }
    return rank;
}

int RankAb(const vector<vector<double>> &matrix){
    int rank = 0;
    for (int i = 0; i < matrix.size(); ++i) {
        bool isZeroRow = true;
        for (int j = 0; j < matrix[i].size(); ++j) {
            if (matrix[i][j] != 0.0) {
                isZeroRow = false;
                break;
            }
        }
        if (!isZeroRow) ++rank;
    }
    return rank;
}

bool isConsistent(int rankA, int rankAb) {
    return rankA == rankAb;
}

bool isIdentity(const vector<vector<double>> &matrix){
    bool isIdentity = true;
    for(int i=0; i<matrix.size(); ++i){
        for(int j=0; j<matrix[i].size()-1; ++j){
            if(i==j && matrix[i][j]!=1.0){
                isIdentity = false;
                break;
            }
            else if(i!=j && matrix[i][j]!=0.0){
                isIdentity = false;
                break;
            }
        }
    }
    return isIdentity;
}

int main() {
    string name;
    cout << "Input file name (not include input_.csv): ";
    cin >> name;
    ifstream inputFile(name + "_input.csv");
    if (!inputFile.is_open()) {
        cerr << "Error opening the file." << endl;
        return 1;
    }

    vector<vector<double>> matrix;
    string line;
    while (getline(inputFile, line)) {
        istringstream iss(line);
        vector<double> row;
        string value;
        while (getline(iss, value, ',')) row.push_back(stod(value));
        matrix.push_back(row);
    }

    // Display the original matrix
    cout << "Original Matrix:" << endl;
    printMatrix(matrix);
    cout << endl;

    // Calculate and display the RREF
    calculateRREF(matrix);
    cout << "Reduced Row Echelon Form (RREF):" << endl;
    printMatrix(matrix);

    // Calculate and display the rank
    int rankA = RankA(matrix);
    int rankAb = RankAb(matrix);
    cout << "Rank(A): " << rankA << endl;
    cout << "Rank(Ab): " << rankAb << endl;

    // Check consistency
    bool consistent = isConsistent(rankA, rankAb);
    cout << "Consistent: " << (consistent ? "Yes" : "No") << endl;

    // Display solutions
    if (consistent) {
        if (isIdentity(matrix)) {
            cout << "Unique Solution:" << endl;
            for (int i = 0; i < rankAb; ++i) {
                cout << "x" << i + 1 << "=" << matrix[i][matrix[0].size() - 1] << endl;
            }
        } else {
            string output;
            cout << "Infinite Solutions (Parametric Representation):" << endl;
            int cols=matrix[0].size()-1,countvar=0;
            int* varcount = new int[cols];
            for(int i=0;i<cols;++i){
                varcount[i]=0;
            }
            for (int i = 0; i < matrix.size(); ++i) {
                bool firstIsZero=false,first = true,allZero=true,var=false;
                for (int j = 0; j < cols; ++j) {
                    if (matrix[i][j] != 0.0) {
                        if (!first && matrix[i][j] > 0){
//                            cout << "+";
                        }
                        if (matrix[i][j] == 1.0){
//                            cout << "x" << j+1;
                            string subject = "x" + to_string(j+1);
                            if (matrix[i][cols]==0.0){
                                var=true;
                                firstIsZero=true;
                                output += subject + "=";
                                countvar++;
                                varcount[j]=1;
                            }
                            else{
                                allZero=false;
                                var=true;
                                ostringstream oss;
                                oss << std::setprecision(5) << matrix[i][cols];
                                output += subject + "=" + oss.str();
                                countvar++;
                                varcount[j]=1;
                            }
                        }
                        else{
                            allZero=false;
//                            cout << matrix[i][j] << "*x" << j + 1;
                            if(matrix[i][j] < 0.0){
                                ostringstream oss;
                                oss << std::setprecision(5) << abs(matrix[i][j]);
                                if(abs(matrix[i][j])!=1){
                                    if(!firstIsZero) output += "+" + oss.str();
                                    else output += oss.str();
                                }
                            }
                            else{
                                ostringstream oss;
                                oss << std::setprecision(5) << matrix[i][j];
                                output += "-" + oss.str();
                            }
                            if(abs(matrix[i][j])!=1) output += "*";
                            output += "x" + to_string(j+1);
                        }
                        first = false;
                    }
                    if(j == cols && matrix[i][j] == 0.0){
//                        cout << "x" << j+1;
                        output += "x" + to_string(j+1);
                    }
                }
//                if(var) cout << "=" << matrix[i][cols] << endl;
                if(allZero && var) output += "0";
                if(var) output+="\n";
            }
            if(countvar<cols){
                for(int i=0;i<cols;++i){
                    if(varcount[i]==0) output += "x" + to_string(i+1) + "=x" + to_string(i+1) + "\n";
                }
            }
            cout<<output;
        }
    }
    return 0;
}
