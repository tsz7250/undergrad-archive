#include "s1111452_mCiper.h"
#include <iostream>
using namespace std;

int main()
{
    mCiper<char> cipher;
    cipher.setMode(1);
    cipher.setMapper("wertyuiopas_dfg:hjk!l.zx,cv-bnm?q", "_:-?!,.zyxwvutsrqponmlkjihgfedcba");
    cout << "Encrypted result: " << cipher.encode('a') << endl;
    cout << "Encrypted result: " << cipher.encode("abcde") << endl;
    cout << "History log: " << cipher.history() << endl;
    cipher.reset();

    cout<<endl;
    cipher.setMapper("wertyuiopas_dfg:hjk!l.zx,cv-bnm?q", "_:-?!,.zyxwvutsrqponmlkjihgfedcba");
    cout << "Encrypted result: " << cipher.encode("Hello World!") << endl;
    cipher.reset();
    cipher.setMapper("wertyuiopas_dfg:hjk!l.zx,cv-bnm?q", "_:-?!,.zyxwvutsrqponmlkjihgfedcba");
    cout << "Encrypted result: " << cipher.encode("kgnix zd?-:b") << endl;
    cout << "History log: " << cipher.history() << endl;


    cout<<endl;
    cipher.setMode(0);
    cipher.setMapper("wertyuiopas_dfg:hjk!l.zx,cv-bnm?q", "_:-?!,.zyxwvutsrqponmlkjihgfedcba");
    cout << "Encrypted result: " << cipher.encode("Lab-one-seven-zero-seven-b") << endl;
    cout << "Encrypted result: " << cipher.encode("jstfvygfagogyf,gxvfagogyft") << endl;
    return 0;
}
