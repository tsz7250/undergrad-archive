#include <iostream>
using namespace std;
#include "s1111452_myQuad.h"

int main(int argc, const char * argv[]) {
	int x1, y1, x2, y2, x3, y3, x4, y4, choice;
    myQuadrilateral* current = 0;
    
    while (true) {
        cout << "(1) Quadrilateral (default)" << endl;
        cout << "(2) Rectangle" << endl;
        cout << "(3) Parallelogram" << endl;
        cout << "(4) Square" << endl;
        cout << "(5) Trapezium" << endl;
        cout << "Choose one kind of shape(1~5)" << endl;
        cin >> choice;
        cout << "Input 4 point [x1] [y1] ... [x4] [y4]" << endl;
        cin >> x1 >> y1 >> x2 >> y2 >> x3 >> y3 >> x4 >> y4;
        
        switch (choice) {
            case 1:
				//3 3 6 6 9 3 6 0 Pass
				//1 1 3 3 2 2 4 4 Fail (a Line)
				//0 0 3 7 6 0 3 3 Pass (a concave shape)
				//0 0 3 7 6 0 3 0 Fail (a triangle)
				//0 0 1 3 0 7 5 3 Pass (a concave shape)
				//0 0 -5 3 0 7 -1 3 Pass (a concave shape)
                current = new myQuadrilateral(x1, y1, x2, y2, x3, y3, x4, y4);
                break;
            case 2:
				//3 3 6 6 9 3 6 0 Pass
				//0 2 0 6 3 4 3 0 Fail
                current = new myRectangle(x1, y1, x2, y2, x3, y3, x4, y4);
                break;
            case 3:
				//0 2 0 6 3 4 3 0 Pass
				//0 0 3 7 6 0 3 3 Fail (a concave shape)
                current = new myParallelogram(x1, y1, x2, y2, x3, y3, x4, y4);
                break;
            case 4:
                //1 1 3 3 1 5 -1 3 Pass
				//3 3 6 6 9 3 6 0 Pass
                current = new mySquare(x1, y1, x2, y2, x3, y3, x4, y4);
                break;
            case 5:
                //1 1 3 3 8 3 9 1 Pass
                //1 1 4 1 4 4 1 4 Fail
                current = new myTrapezium(x1, y1, x2, y2, x3, y3, x4, y4);
                break;
            default:
                current = new myQuadrilateral(x1, y1, x2, y2, x3, y3, x4, y4);
                break;
        }
        
		if (current->isValid()) {
			cout << "the input shape is valid and the type is : " << endl;
            cout << current->getType() << endl;
			cout << *current << endl;
			cout << "Area of this shape is = " << current->getArea() << endl;
		}
		else {
			cout << "Fail to pass the validation test of : " << endl;
			cout << current->getType() << endl;
		}
        
        delete current;
		system("pause");
    }
    return 0;
}
