#include <iostream>
using namespace std;

class N2Comp {
private:
    int x;
    int y;
public:
    // constructor
    N2Comp(int xval = 0, int yval = 0) : x(xval), y(yval) {};

    // copy constructor
    N2Comp(const N2Comp& other) {
        x = other.x;
        y = other.y;
    }

    // destructor
    ~N2Comp() {}

    // assignment operator
    N2Comp& operator=(const N2Comp& other) {
        if (this != &other) {
            x = other.x;
            y = other.y;
        }
        return *this;
    }

    // addition operator
    N2Comp operator+(const N2Comp& other){
        N2Comp result;
        result.x = x + other.x;
        result.y = x + other.x + y * other.y;
        return result;
    }

    // subscript operator
    int operator[](int j) {
        if (j == 0) return x;
        else if (j == 1) return y;
    }

    // input operator
    friend istream& operator>>(istream& input, N2Comp& num) {
        input >> num.x >> num.y;
        return input;
    }

    // output operator
    friend ostream& operator<<(ostream& output, const N2Comp& num) {
        output << "(" << num.x << ", " << num.y << ")";
        return output;
    }
};
