#include "s1111452_N2CompV2.h"
#include <iostream>
using namespace std;

N2Comp diNFib(int n = 0) {
    if (n == 0)
        return N2Comp(0, 0);
    if (n == 1)
        return N2Comp(1, 0);
    return diNFib(n-1) + diNFib(n-2);
}

int main() {
    int level=12;
	cout << "Hello s1234567! how many level do you want to reach?" << endl;
//    cin >> level;

    N2Comp ANS(0,0);

    for (int i = 0; i <= level; ++i) {
        ANS = diNFib(i);
        cout << "F(" << i << ") = ";
        cout << ANS[0] << " , " << ANS[1] << endl;
//        cout << ANS << endl;
    }

    // test codes
//    cout << "\n[Test prog. for operator >>]" << endl;
//   	N2Comp A1(0), A2(0);
//    cout << "Input A1: ";
//	cin >> A1;
//    cout << "Input A2: ";
//	cin >> A2;
//    cout << "Exec A1+A2 = " << A1+A2 << endl;

    return 0;
}
