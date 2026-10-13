template<typename T>
class List {
public:
    struct Node {
        T data;
        Node* next;
    };
    Node* now;
    Node* head;
    List() : now(nullptr) {}
    T getNow() const{
        return *now;
    }

    T getData() const{
        return now->data;
    }

    T getNextPtr() {
        Node* current = now;
        if(now==nullptr) throw std::runtime_error("no more card");
        now = now->next;
        return current->data;
    }

    void pushFront(const T& value) {
        Node* newNode = new Node{value, now};
        now = newNode;
    }

    void pushBack(const T& value) {
        if (now==nullptr) {
            pushFront(value);
            head = now;
        } else {
            Node* newNode = new Node{value, nullptr};
            Node* current = now;
            while (current->next) {
                current = current->next;
            }
            current->next = newNode;
        }
    }
};
