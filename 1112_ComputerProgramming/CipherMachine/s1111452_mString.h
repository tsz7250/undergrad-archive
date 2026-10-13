#include <iostream>
#include <cstring>
using namespace std;

template <typename T>
class mString{
private:
    T* ptr;
    unsigned int mSize = 0;
    unsigned int mCapacity = 10;
public:
    static const unsigned int npos = -1;
    mString(){};

    //constructor
    mString(const T *s, unsigned int len = npos){
        if (len == npos) {
            mSize = strlen(s);
        } else {
            mSize = len;
        }
        ptr = new T[mSize];
        strncpy(ptr, s, mSize);
        ptr[mSize] = '\0';
        while(mSize>mCapacity) mCapacity*=2;
    };

    //copy constructor
    mString(const mString &str){
        mSize=str.mSize;
        mCapacity=str.mCapacity;
        ptr=new T[mSize];
        strncpy(ptr, str.ptr, mSize);
    }

    //destructor
    ~mString(){};

    unsigned int size() const {
        return mSize;
    }

    unsigned int capacity() const {
        return mCapacity;
    }

    void resize(size_t n, T c = '\0')
    {
        if (n < mSize) {
            mSize = n;
            for(size_t i = mSize; i>=0; --i){
                if(ptr[i]==0) ptr[i]=c;
                else break;
            }
            ptr[mSize] = '\0';
        } else if (n > mSize) {
            if (n > mCapacity) {
                mCapacity *= 2;
                T* newPtr = new T[n];
                strncpy(newPtr, ptr, mSize);
                delete[] ptr;
                ptr = newPtr;
            }
            for (size_t i = mSize; i < n; ++i) {
                ptr[i] = c;
            }
            ptr[n] = '\0';
            mSize = n;
        }
    }

    void clear(){
        for (int i = 0; i < mSize; i++) {
            ptr[i] = 0;
        }
        mSize = 0;
    }

    void push_back(T c){
        if (mSize + 1 == mCapacity || mSize == mCapacity) {//if over the size
            mCapacity += 10;
            char* temp = new char[mCapacity];
            for (int i = 0; i < mSize; i++) {
                temp[i] = ptr[i];
            }
            delete[]ptr;
            ptr = temp;
        }
        ptr[mSize] = c;
        mSize++;
        return;
    }

    void pop_back(){
        ptr[--mSize]='\0';
    }

    mString& append(const mString &str){
        for(unsigned i=0;i<str.mSize;++i){
            ptr[mSize++]=str.ptr[i];
        }
        ptr[mSize]='\0';
        return *this;
    }

    mString& erase(unsigned int pos = 0, unsigned int len = npos){
        if(len==npos){
            ptr[pos]='\0';
            mSize=pos;
        }
        else {
            for (unsigned int i = pos; i + len < mSize; ++i) {
                ptr[i] = ptr[i + len];
            }
            mSize-=len;
        }
        ptr[mSize]='\0';
        return *this;
    }

    mString substr(unsigned int pos = 0, unsigned int len = npos){
        mString output(ptr+pos, len);
        return output;
    }

    unsigned int find( T c, unsigned int pos = 0 ) const{
        for(unsigned int i=pos;i<mSize;++i){
            if(ptr[i]==c) return i;
        }
        return npos;
    }

    //mString+mString
    mString operator+ (const mString& rhs) const{
        mString output(*this);
        output.append(rhs);
        return output;
    }

    //mString+T
    mString operator+ (const T* rhs) const{
        mString output(*this);
        output.append(rhs);
        return output;
    }

    //T+mString
    friend mString operator+ (const T* lhs, const mString& rhs){
        mString output(lhs);
        output.append(rhs);
        return output;
    }

    //mString=mString
    mString& operator= (const mString& str){
        if(this!=&str){
            clear();
            mSize=str.mSize;
            mCapacity=str.mCapacity;
            ptr=new T[mSize];
            strncpy(ptr, str.ptr, mSize);
            ptr[mSize]='\0';
        }
        return *this;
    }

    //mString=String
    mString& operator= (const T* s){
        clear();
        mSize=strlen(s);
        while(mSize>mCapacity) mCapacity*=2;
        ptr=new T[mSize];
        strncpy(ptr, s, mSize);
        ptr[mSize]='\0';
        return *this;
    }

    bool operator==(const mString &other) const{
        if(mSize!=other.mSize) return false;
        for(size_t i=0;i<mSize;++i){
            if(ptr[i]!=other.ptr[i]) return false;
        }
        return true;
    }

    bool operator!=(const mString &other) const{
        if(mSize!=other.mSize) return true;
        for(size_t i=0;i<mSize;++i){
            if(ptr[i]!=other.ptr[i]) return true;
        }
        return false;
    }

    T &operator[](int n){
        return ptr[n];
    }

    T operator[](int n) const{
        return ptr[n];
    }

    friend istream &operator>>(istream &input, mString &string){
        string.clear();
        string.mSize = 0;
        string.mCapacity = 10;
        T c;
        while (input.get(c)) {
            if (c == '\n' || c == '\r') {
                break;
            }
            string.push_back(c);
            if (string.mSize > string.mCapacity) {
                string.mCapacity *= 2;
                T* newPtr = new T[string.mSize];
                strncpy(newPtr, string.ptr, string.mSize);
                delete[] string.ptr;
                string.ptr = newPtr;
            }
        }
        string.ptr[string.mSize] = '\0';
        return input;
    }

    friend ostream &operator<<(ostream &output, const mString &string){
        output<<string.ptr;
        return output;
    }
};
