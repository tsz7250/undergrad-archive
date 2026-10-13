#include "s1111452_Hand.h"
#include <iostream>
using namespace std;

int main(){
    DeckOfCards deck;
    deck.shuffle();

    Hand hand(deck);
    cout << "Hand 1:\n" << hand;

    Hand anotherHand(deck);
    cout << "\nHand 2:\n" << anotherHand;

    cout << "\nComparison: " << endl;
    cout << "Hand 1 == Hand 2: " << boolalpha << (hand == anotherHand) << endl;
    cout << "Hand 1 != Hand 2: " << (hand != anotherHand) << endl;


    cout << "\nType of Hand 1: " << hand.type() << endl;
    cout << "Type of Hand 2: " << anotherHand.type() << endl;
}
