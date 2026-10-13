#include <string>
using namespace std;

class Card{
protected:
    int face;
    int suit;
    static const string faceNames[];
    static const string suitNames[];

public:
    Card(){};
    Card(int face,int suit):face(face),suit(suit){};
    string toString() const{
        return faceNames[face]+" of "+suitNames[suit];
    }

    string getFace() const{
        return faceNames[face];
    }

    string getSuit() const{
        return suitNames[suit];
    }

    int getFaceIndex() const{
        return face;
    }
    bool operator==(const Card &other) const{
        if(face==other.face&&suit==suit) return true;
        else return false;
    }

    bool operator!=(const Card &other) const{
        if(face==other.face&&suit==suit) return false;
        else return true;
    }

};

const string Card::faceNames[] = {"Ace", "Deuce", "Three", "Four", "Five", "Six",
                                  "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King" };
const string Card::suitNames[] = { "Hearts", "Diamonds", "Clubs", "Spades" };
