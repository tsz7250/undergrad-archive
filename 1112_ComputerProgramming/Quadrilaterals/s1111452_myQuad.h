#include "s1111452_myPoint2.h"
#include <iostream>
#include <string>
#include <cmath>
using namespace std;
class myQuadrilateral{
protected:
    int x1, y1, x2, y2, x3, y3, x4, y4;
    Point2 A,B,C,D;
public:
    myQuadrilateral(int x1,int y1,int x2,int y2,int x3,int y3,int x4,int y4){
        this->x1=x1;this->y1=y1;
        this->x2=x2;this->y2=y2;
        this->x3=x3;this->y3=y3;
        this->x4=x4;this->y4=y4;
        this->A=Point2(x1,y1);
        this->B=Point2(x2,y2);
        this->C=Point2(x3,y3);
        this->D=Point2(x4,y4);
    }

    friend ostream& operator<<(ostream& output,const myQuadrilateral& point){
        output<<point.A<<point.B<<point.C<<point.D;
        return output;
    }

    virtual string getType(){
        return "Quadrilateral";
    }

    virtual double getArea(){
        double a=Point2::getDistance(A,B),b=Point2::getDistance(B,C),c=Point2::getDistance(A,C),
                a1=Point2::getDistance(C,D),b1=Point2::getDistance(D,A),s=(a+b+c)/2,s1=(a1+b1+c)/2,
                cc=Point2::getDistance(B,D),ss=(a+b1+cc)/2,ss1=(a1+b+cc)/2,ans,ans1;
        ans=sqrt(s*(s-a)*(s-b)*(s-c))+sqrt(s1*(s1-a1)*(s1-b1)*(s1-c));
        ans1=sqrt(ss*(ss-a)*(ss-b1)*(ss-cc))+sqrt(ss1*(ss1-a1)*(ss1-b)*(ss1-cc));
        if(ans!=ans1) {
            double area=Point2::getConcaveQuad(A,B,C,D);
            return area;
        }
        else return ans;
    }

    virtual bool isValid(){
        if(A==B||A==C||A==D||B==C||B==D||C==D) return false;
        else if(Point2::isColinear(A,B,C)||Point2::isColinear(A,B,D)||Point2::isColinear(A,C,D)||Point2::isColinear(B,C,D)) return false;
        else return true;
    }

};

class myTrapezium: public myQuadrilateral{
public:
    myTrapezium(int x1,int y1,int x2,int y2,int x3,int y3,int x4,int y4):myQuadrilateral(x1, y1, x2, y2, x3, y3, x4, y4){};

    string getType(){
        return myQuadrilateral::getType()+"-Trapezium";
    }

    bool isValid(){
        if(myQuadrilateral::isValid()
           &&(Point2::isParallel(A,B,C,D)
           || Point2::isParallel(B,C,D,A)
           || Point2::isParallel(C,D,A,B)
           || Point2::isParallel(D,A,B,C))
           && !(Point2::isParallel(A,B,C,D)&&Point2::isParallel(D,A,B,C))) return true;
        else return false;
    }

    double getArea(){
        double a=Point2::getDistance(A,B),b=Point2::getDistance(B,C),c=Point2::getDistance(A,C),
               a1=Point2::getDistance(C,D),b1=Point2::getDistance(D,A),s=(a+b+c)/2,s1=(a1+b1+c)/2,ans;
        ans=sqrt(s*(s-a)*(s-b)*(s-c))+sqrt(s1*(s1-a1)*(s1-b1)*(s1-c));
        return ans;
    }
};

class myParallelogram: public myQuadrilateral{
public:
    myParallelogram(int x1,int y1,int x2,int y2,int x3,int y3,int x4,int y4):myQuadrilateral(x1, y1, x2, y2, x3, y3, x4, y4){};

    string getType(){
        return myQuadrilateral::getType()+"-Parallelogram";
    }

    bool isValid(){
        if(myQuadrilateral::isValid()
           &&Point2::isParallel(A,B,C,D)
           &&Point2::isParallel(D,A,B,C)) return true;
        else return false;
    }

    double getArea(){
        double a=Point2::getDistance(A,B),b=Point2::getDistance(B,C),c=Point2::getDistance(A,C),s=(a+b+c)/2,ans;
        ans=sqrt(s*(s-a)*(s-b)*(s-c))*2;
        return ans;
    }

};

class myRectangle: public myParallelogram{
public:
    myRectangle(int x1,int y1,int x2,int y2,int x3,int y3,int x4,int y4):myParallelogram(x1, y1, x2, y2, x3, y3, x4, y4){};

    string getType(){
        return myParallelogram::getType()+"-Rectangle";
    }

    double getArea(){
        return Point2::getDistance(A,B)*Point2::getDistance(B,C);
    }

    bool isValid(){
        double a=Point2::getDistance(A,B),b=Point2::getDistance(B,C),c=Point2::getDistance(A,C),angle;
        angle=acos((pow(c,2)-pow(a,2)-pow(b,2))/double((-2*a*b)))*180/M_PI;
        angle=round(angle);
        if(myParallelogram::isValid()&&angle==90) return true;
        else return false;
    }
};

class mySquare: public myRectangle{
private:
    Point2 A,B,C,D;
public:
    mySquare(int x1,int y1,int x2,int y2,int x3,int y3,int x4,int y4):myRectangle(x1, y1, x2, y2, x3, y3, x4, y4){};

    string getType(){
        return myRectangle::getType()+"-Square";
    }

    double getArea(){
        return Point2::getDistance(A,B)*Point2::getDistance(C,D);
    }

    bool isValid(){
        if(myRectangle::isValid()&&
           Point2::getDistance(A,B)==Point2::getDistance(B,C)
           &&Point2::getDistance(B,C)==Point2::getDistance(C,D)
           &&Point2::getDistance(C,D)==Point2::getDistance(D,A)) return true;
        else return false;
    }
};
