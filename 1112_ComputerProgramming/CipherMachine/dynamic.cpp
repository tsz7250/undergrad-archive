#include <iostream>
#include "s1111452_mString.h"
using namespace std;

template <typename T>
mString<T> encrypt(const mString<T>& input) {
    const mString<T> table = "abcdefghijklmnopqrstuvwxyz.,!?-:_";
    mString<T> table2 = "abcdefghijklmnopqrstuvwxyz.,!?-:_";
    mString<T> rotor = "wertyuiopas_dfg:hjk!l.zx,cv-bnm?q";
    const mString<T> reflector = "_:-?!,.zyxwvutsrqponmlkjihgfedcba";
    mString<T> output = "";
    for (size_t i = 0; i < input.size(); i++) {
        T c = input[i];
        c = tolower(c);
        if (c == ' ') output.push_back(' ');
        else{
            if(i!=0){
                T temp=table2[0];
                T temp2=rotor[0];
                table2.erase(0,1);
                rotor.erase(0,1);
                table2.push_back(temp);
                rotor.push_back(temp2);
            }
            int pos1 = table.find(c);
            T n = rotor[pos1];
            T m = reflector[table2.find(n)];
            T pos2 = table2[table.find(m)];
            T j = table[rotor.find(pos2)];
            output.push_back(j);
        }
    }
    output.push_back('\0');
    return output;
}

int main() {
    mString<char> s("aabcde");
    mString<char> encrypted = encrypt(s);
    cout << "Encrypted string: " << encrypted << endl;
    return 0;
}
