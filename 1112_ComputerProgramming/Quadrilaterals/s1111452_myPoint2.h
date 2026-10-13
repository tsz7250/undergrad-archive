#include <cmath>
#include <iostream>
class Point2{
private:
    int x;
    int y;
public:
    Point2(){};
    Point2(int x,int y):x(x),y(y){};

    static double getDistance(const Point2& a, const Point2& b){
        return sqrt(pow((a.x-b.x),2)+pow((a.y-b.y),2));
    }

    static double getSlope(const Point2& a, const Point2& b){
        double vert=0.365981;
        if(b.y-a.y==0) return 0;
        else if(b.x-a.x==0) return vert;
        else return (b.y-a.y)/double((b.x-a.x));
    }

    static double getConcaveQuad(const Point2 &A, const Point2 &B, const Point2 &C, const Point2 &D){
        double i0=(A.x*B.y-B.x*A.y),i1=(B.x*C.y-C.x*B.y),i2=(C.x*D.y-D.x*C.y),last=(A.x*D.y-D.x*A.y);
        double ans=abs(i0+i1+i2-last)/double(2);
        return ans;

    }

    static bool isParallel(const Point2 &A, const Point2 &B, const Point2 &C, const Point2 &D){
        double mAB=getSlope(A,B),mCD=getSlope(C,D);
        if(mAB==mCD) return true;
        else return false;
    }

    bool operator==(const Point2& other)const{
        if(x==other.x&&y==other.y) return true;
        else return false;
    }
    
    static bool isColinear(const Point2 &A, const Point2 &B, const Point2 &C){
        double mAB=getSlope(A,B),mBC=getSlope(B,C);
        if(mAB==mBC) return true;
        else return false;
    }

    friend std::ostream& operator<<(std::ostream& output,const Point2& point){
        output<<"("<<point.x<<","<<point.y<<")\n";
        return output;
    }
};