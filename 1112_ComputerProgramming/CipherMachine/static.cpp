#include <iostream>
#include "s1111452_mString.h"
using namespace std;

template <typename T>
mString<T> encrypt(const mString<T>& input) {
    const mString<T> table = "abcdefghijklmnopqrstuvwxyz.,!?-:_";
    const mString<T> rotor = "wertyuiopas_dfg:hjk!l.zx,cv-bnm?q";
    const mString<T> reflector = "_:-?!,.zyxwvutsrqponmlkjihgfedcba";
    mString<T> output="";

    for (size_t i = 0; i < input.size(); i++) {
        T c = input[i];
        c = tolower(c);
        if (c == ' ') output.push_back(' ');
        else {
            int pos1 = table.find(c);
            T n = rotor[pos1];
            T m = reflector[table.find(n)];
            T pos2 = table[rotor.find(m)];
            output.push_back(pos2);
        }
    }
    output.push_back('\0');
    return output;
}

int main() {
    mString<char> s("a");
    mString<char> encrypted = encrypt(s);
    cout << "Encrypted string: " << encrypted << endl;
    return 0;
}
