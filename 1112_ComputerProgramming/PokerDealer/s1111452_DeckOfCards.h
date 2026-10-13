#include "s1111452_List.h"
#include "s1111452_Card.h"
#include <ctime>
#include <iostream>
using namespace std;

class DeckOfCards:private List<Card> {
public:
    DeckOfCards() {
        for (int suit = 0; suit < 4; ++suit) {
            for (int face = 0; face < 13; ++face) {
                pushBack(Card(face, suit));
            }
        }
    }

    void reset() {
        now=head;
    }

    //get card from specific index
    Card getCard(int x){
        Node* current = head;
        for (int i = 0; i < x; ++i) {
            current = current->next;
        }
        return current->data;
    }

    void shuffle() {
        srand(time(0));

        Node* current = now;
        for (int i = 0; i < 52; ++i) {
            int randomIndex = i + rand() % (52 - i);

            Card temp = current->data;
            current->data = getCard(randomIndex);
            getCard(randomIndex) = temp;

            current = current->next;
        }
    }

    bool moreCards(){
        return (now!=nullptr);
    }

    Card dealCard() {
        return getNextPtr();
    }

    Card delete5Card(){
        Card temp=now->data;
        Node* current=head;
        for (int i = 0; i < 5; ++i) {
            Node* next = current->next;
            current=0;
            current = next;
        }
        head = current;
        now = current;
        return temp;
    }
};