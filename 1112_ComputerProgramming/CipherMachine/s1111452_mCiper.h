#include "s1111452_mString.h"
template <typename T>
class mCiper{
private:
    int mode;
    const mString<T> table = "abcdefghijklmnopqrstuvwxyz.,!?-:_";;
    mString<T> table2 = "abcdefghijklmnopqrstuvwxyz.,!?-:_";
    mString<T> rotor;
    mString<T> reflector;
    mString<T> history_log = "";
public:
    //constructor
    mCiper(){
        rotor;
        reflector;
    };

    //destructor
    ~mCiper(){};

    void setMapper(mString<char> rotor,mString<char> reflector){
       this->rotor=rotor;
        this->reflector=reflector;
    }

    char encode(const char input){
        char c = tolower(input);
        if (c == ' ') return(' ');
        int pos1 = table.find(c);
        if(mode==0){
            T n = rotor[pos1];
            T m = reflector[table.find(n)];
            T pos2 = table[rotor.find(m)];
            return pos2;
        }
        else if(mode==1){
            int pos1 = table.find(c);
            T n = rotor[pos1];
            T m = reflector[table2.find(n)];
            T pos2 = table2[table.find(m)];
            T j = table[rotor.find(pos2)];
            history_log.push_back(j);
            T temp=table2[0];
            T temp2=rotor[0];
            table2.erase(0,1);
            rotor.erase(0,1);
            table2.push_back(temp);
            rotor.push_back(temp2);
            return j;
        }
    }

    mString<char> encode(const mString<char>& input){
        mString<T> output("");
        for (size_t i = 0; i < input.size(); i++) {
            T c=input[i];
            output.push_back(encode(c));
        }
        output.push_back('\0');
        if(mode==1) history_log.push_back('\0');
        return output;
    }

    void reset(){
        table2 = "abcdefghijklmnopqrstuvwxyz.,!?-:_";
        rotor.clear();
        history_log.clear();
    }

    mString<char> history(){
        return history_log;
    }

    void setMode(int x){
        if(x==0) mode=0;
        else if(x==1) mode=1;
    }
};