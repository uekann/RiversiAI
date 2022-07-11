class Node:
    def __init__(self, parent_idx : int, data : any, child_idx : list = []) -> None:
        self.parent = parent_idx
        self.data = data
        self.child = child_idx
    
    def __str__(self) -> str:
         return str(self.data)


class Tree(list):
    def __init__(self, root) -> None:
        super(Tree, self).__init__([[Node(None, root)]])
        self.att_idx = [0]
        self.att_node = self[len(self.att_idx)-1][self.att_idx[-1]]
    
    def add(self, data):
        if len(self) > len(self.att_idx):
            l = self[len(self.att_idx)]
            l.append(Node(self.att_idx[-1], data))
            l = len(l)-1
            self.att_node.child.append(l)
            self.att_idx.append(l)
            self.att_node = self[len(self.att_idx)-1][self.att_idx[-1]]
        else:
            self.append([Node(self.att_idx[-1], data)])
            self.att_idx.append(0)
            self.att_node = self[len(self.att_idx)-1][self.att_idx[-1]]
    
    def back(self, number=1):
        count = 0
        for i in range(number):
            if len(self.att_idx) == 1:
                self.att_node = self[len(self.att_idx)-1][self.att_idx[-1]]
                return count
            
            self.att_idx.pop()
    
    def get_child(self):
        l = self[len(self.att_idx)]
        return [l[i] for i in range(len(l)) if i in self.att_node.child]
    
    def get_child_idx(self):
        return self.att_node.child
    
    def get_parent(self):
        if len(self.att_idx) <= 1:
            return None
        else:
            return self[len(self.att_idx)-2][self.att_node.parent]
    
    def get_parent_idx(self):
        if len(self.att_idx) <= 1:
            return None
        else:
            return self.att_node.parent
    
    def get_attention_data(self):
        return self.att_node.data

    
    def __str__(self) -> str:
        s = "["
        for i in self:
            s += "[" + ", ".join(map(str, i)) + "],\n"
        s = s[:-2] + "]"
        return s
