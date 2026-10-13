#include "s1111452_DeckOfCards.h"
#include <string>
#include <algorithm>
using namespace std;

class Hand{
private:
    Card Cards[5]{};
public:
    Hand(DeckOfCards &deck){
        for(int i=0;i<5;++i){
            Cards[i]=deck.dealCard();
        }
        deck.delete5Card();
    }

    friend ostream &operator<<(ostream &output, const Hand &hand){
        for(int i=0;i<5;++i){
            output<<hand.Cards[i].toString()<<endl;
        }
        return output;
    }

    void print(){
        cout<<"Hand is:\n";
        for(int i=0;i<5;++i){
            cout<<Cards[i].toString()<<endl;
        }
    }

    Hand takeAgain(DeckOfCards &deck){
        for(int i=0;i<5;++i){
            Cards[i]=deck.dealCard();
        }
        deck.delete5Card();
        return *this;
    }

    bool pair(){
        bool isSame;
        for(int i=0;i<5;++i){
            for(int j=i+1;j<5;++j){
                if(Cards[i].getFace()==Cards[j].getFace()){
                    isSame=true;
                }
                else{
                    isSame=false;
                    return false;
                }
            }
        }
        if(isSame) return true;
        else return false;
    }

    bool twoPair(){
        int count=0;
        for(int i=0;i<2;++i){
            if(pair()) count++;
        }
        return (count==2);
    }

    bool threeOfAKind(){
        bool isSame;
        for(int i=0;i<5;++i){
            for(int j=i+1;j<5;++j){
                for(int k=j+1;k<5;++k){
                    if(Cards[i].getFace()==Cards[j].getFace()&&Cards[j].getFace()==Cards[k].getFace()){
                        isSame=true;
                    }
                    else{
                        isSame=false;
                        return false;
                    }
                }
            }
        }
        if(isSame) return true;
        else return false;
    }

    bool fourOfAKind(){
        bool isSame;
        for(int i=0;i<5;++i){
            for(int j=i+1;j<5;++j){
                for(int k=j+1;k<5;++k){
                    for(int l=k+1;l<5;++l){
                        if(Cards[i].getFace()==Cards[j].getFace()
                           &&Cards[j].getFace()==Cards[k].getFace()
                           &&Cards[k].getFace()==Cards[l].getFace()){
                            isSame=true;
                        }
                        else{
                            isSame=false;
                            return false;
                        }
                    }
                }
            }
        }
        if(isSame) return true;
        else return false;
    }

    bool fullHouse(){
        return (pair()&&threeOfAKind());
    }

    bool flush(){
        bool isSame;
        for(int i=0;i<5;++i){
            for(int j=i+1;j<5;++j){
                if(Cards[i].getSuit()!=Cards[j].getSuit()){
                    return false;
                }
            }
        }
        return true;
    }

    bool straight() {
        int arr[5]{0};
        for(int i=0;i<5;++i){
            arr[i]=Cards[i].getFaceIndex();
        }
        sort(arr,arr+5);


        for(int i=0;i<4;++i){
            if(arr[i]+1!=arr[i+1]){
                return false;
            }
        }
        return true;
    }

    string type(){
        if(straight()&&flush()) return "straight flush";
        else if(straight()) return "straight";
        else if(flush()) return "flush";
        else if(fourOfAKind()) return "four of a kind";
        else if(fullHouse()) return "full house";
        else if(threeOfAKind()) return "three of a kind";
        else if(twoPair()) return "two pair";
        else if(pair()) return "a pair";
        else return "none";
    }

    bool operator==(const Hand &other)const{
        bool isSame;
        for(int i=0;i<5;++i){
            if(Cards[i]==other.Cards[i]) isSame=true;
            else{
                return false;
            }
        }
        if(isSame==true) return true;
    }

    bool operator!=(const Hand &other)const{
        bool isDiff;
        for(int i=0;i<5;++i){
            if(Cards[i]!=other.Cards[i]) isDiff=true;
            else{
                return false;
            }
        }
        if(isDiff==false) return true;
    }
};
