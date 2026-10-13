// Card shuffling and dealing program.
#include <iostream>
#include <iomanip>
#include "s1111452_Hand.h" // Card, DeckOfCards, Hand class definition
using namespace std;

bool PressEnterToContinue(string mesg = "Press ENTER to continue... ")
{
	int c;
	cout << mesg << endl;
	cout.flush();
	do c = getchar(); while ((c != '\n') && (c != EOF));
	return true;
}

int main()
{
   DeckOfCards myDeckOfCards;
   myDeckOfCards.shuffle(); // place Cards in random order

   // ISSUEs 01 - print all 52 Cards in the order in which they are dealt
   for (int i = 1; myDeckOfCards.moreCards(); i++)
   {
	   // deal and display a Card
	   cout << left << setw(19) << myDeckOfCards.dealCard().toString();

	   if (i % 5 == 0) // output newline every 5 cards
		   cout << endl;
   } // end for

   cout << endl << "--------------------------------------" << endl;
   myDeckOfCards.reset(); // place Cards in random order (reset current card #)
   Hand hand(myDeckOfCards);

   // ISSUEs 02 - deal a hand from the deck
   do
   {
	   hand.print(); // display hand

	   // check for each type of hand
	   if (hand.fourOfAKind())
		   cout << "Hand contains four of a kind" << endl;
	   if (hand.flush())
		   cout << "Hand contains a flush" << endl;
	   if (hand.straight())
		   cout << "Hand contains a straight" << endl;
	   if (hand.threeOfAKind())
		   cout << "Hand contains three of a kind" << endl;
	   if (hand.twoPair())
		   cout << "Hand contains two pairs" << endl;
	   if (hand.pair())
		   cout << "Hand contains a pair" << endl;
	   if (hand.fullHouse())
	       cout << "Hand contains a fullHouse" << endl;

		// check for each type of hand
	   if (hand.type() == "none")
		   cout << "\nToo bad, you get nothing..." << endl;
	   else
	       cout << "\nYou get " << hand.type() << " !!!" << endl;

	   hand.takeAgain(myDeckOfCards);
   } while (PressEnterToContinue() && myDeckOfCards.moreCards());

   PressEnterToContinue("Press ENTER to endgame... ");
} // end main
