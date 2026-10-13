#include <iostream>
#include <iomanip>
using namespace std;

class BigInt {
private:
    int* digits;
    int size;
public:
    // constructor
    BigInt(int num = 0) {
        int count = 0;
        int temp = num;
        while (temp > 0) {
            count++;
            temp /= 1000;
        }

        if (count == 0) size = 1;
        else size = count;
        digits = new int[size];

        for (int i = 0; i < size; ++i) {
            digits[i] = num % 1000;
            num /= 1000;
        }
    }

    // copy constructor
    BigInt(const BigInt& other) {
        size = other.size;
        digits = new int[size];
        for (int i = 0; i < size; ++i) {
            digits[i] = other.digits[i];
        }
    }

    // destructor
    ~BigInt(){}

    // assignment operator
    BigInt& operator=(const BigInt& other) {
        if (this != &other) {
            delete[] digits;
            size = other.size;
            digits = new int[size];
            for (int i = 0; i < size; ++i) {
                digits[i] = other.digits[i];
            }
        }
        return *this;
    }

    // addition operator
    BigInt operator+(const BigInt& other) const {
        int carry = 0, i;
        BigInt result;
        for (i = 0; (i < size || i < other.size || carry>0); ++i) {
            if (i < size) carry += digits[i];
            if (i < other.size) carry += other.digits[i];
            result.digits[i] = carry % 1000;
            carry /= 1000;
        }
        result.size = i;
        return result;
    }

    // multiplication operator
    BigInt operator*(const BigInt& other) const {
        BigInt result;
        result.size = size + other.size;
        result.digits = new int[result.size];
        for (int i = 0; i < result.size; ++i) {
            result.digits[i] = 0;
        }
        for (int i = 0; i < size; ++i) {
            for (int j = 0; j < other.size; ++j) {
                result.digits[i+j] += digits[i] * other.digits[j];
                result.digits[i+j+1] += result.digits[i+j] / 1000;
                result.digits[i+j] %= 1000;
            }
        }
        while (result.size > 1 && result.digits[result.size-1] == 0) result.size--;
        return result;
    }

    // output operator
    friend ostream& operator<<(ostream& output, const BigInt& num) {
        output << num.digits[num.size-1];
        for (int i = num.size - 2; i >= 0; --i) {
            output<<",";
            output.width(3);
            output << num.digits[i];
        }
        return output;
    }
};

class N2Comp {
private:
    BigInt x;
    BigInt y;
public:
    // constructor
    N2Comp(BigInt xval = 0, BigInt yval = 0) : x(xval), y(yval) {};

    // copy constructor
    N2Comp(const N2Comp &other) : x(x), y(y) {
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
    BigInt operator[](int j) {
        if (j == 0) return x;
        else if (j == 1) return y;
    }

   // input operator
//    friend istream& operator>>(istream& input, const N2Comp& num) {
//        input >> num.x >> num.y;
//        return input;
//    }

    // output operator
    friend ostream& operator<<(ostream& output, const N2Comp& num) {
        output << "(" << num.x << ", " << num.y << ")";
        return output;
    }
};
