#include <iostream>
#include "s1111452_mString.h"
using namespace std;

int main(){
    mString<char> s1("aaa");

    cout<<"operator <<\n";
    cout<<s1<<endl;

    cout<<"\nGet size and capacity\n";
    cout<<s1.size()<<" "<<s1.capacity()<<endl;

    cout<<"\nResize\n";
    s1.resize(15);
    cout<<s1;
    cout<<", size and capacity: ";
    cout<<s1.size()<<" "<<s1.capacity()<<endl;

    s1.resize(5,'b');
    cout<<s1;
    cout<<", size and capacity: ";
    cout<<s1.size()<<" "<<s1.capacity()<<endl;

    cout<<"\nClear\n";
    s1.clear();
    cout<<"After clear: "<<s1<<endl;

    cout<<"\npush_back and pop_back\n";
    s1.push_back('c');
    s1.push_back('d');
    cout<<s1<<endl;
    s1.pop_back();
    cout<<s1<<endl;

    cout<<"\nappend, erase, substr, find\n";
    s1.append("atdog");
    cout<<s1<<endl;
    s1.erase(3,3);
    cout<<s1<<endl;
    cout<<s1.substr(1,2)<<endl;
    cout<<s1.find('t')<<endl;

    cout<<"\noperator +\n";
    mString<char> s2("bbb");
    cout<<s1+s2<<endl;
    cout<<s1+"ccc\n";
    cout<<"bbb"+s1<<endl;

    cout<<"\noperator == and !=\n";
    if(s1==s2) cout<<"Same\n";
    else cout<<"Not Same\n";
    if(s1!=s2) cout<<"Different\n";
    else cout<<"Not Different\n";

    cout<<"\noperator[]const, non const\n";
    s1[0]='b';
    cout<<s1<<" "<<s1[0]<<endl;

    const mString<char> s3("abc");
    cout<<s3[2]<<endl;

    cout<<"\noperator >>\n";
    cout<<"s1: "<<s1<<"\nInput new value: ";
    cin>>s1;
    cout<<"New value: "<<s1<<endl;

    return 0;
}