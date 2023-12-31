from typing import List
import hashlib
import os

class Node:
    def __init__(self, left, right, value: str, content, is_copied=False) -> None:
        self.left: Node = left
        self.right: Node = right
        self.value = value
        self.content = content
        self.is_copied = is_copied

    @staticmethod
    def hash(val: str) -> str:
        return hashlib.sha256(val.encode('utf-8')).hexdigest()
 
    def __str__(self):
        return (str(self.value))
 
    def copy(self):
        """
        class copy function
        """
        return Node(self.left, self.right, self.value, self.content, True)
       
class MerkleTree:

    def __init__(self) -> None:
        pass

    def __init__(self, values: List[str]) -> None:
        self.__buildTree(values)
 
    def __buildTree(self, values: List[str]) -> None:
 
        leaves: List[Node] = [Node(None, None, Node.hash(e), e) for e in values]
        if len(leaves) % 2 == 1:
            leaves.append(leaves[-1].copy())  # duplicate last elem if odd number of elements
        self.root: Node = self.__buildTreeRec(leaves)
 
    def exportGraphviz(self, root, filename) -> None:
        cmd = "dot -Tpng " + filename + ".dot -o " + filename + ".png"

        dotContent = "digraph G {\n node [margin=0 fontcolor=blue fontsize=10 width=0.5 shape=rec ] \n" + self.__exportGraphviz(root) + "}"
        f = open("arbolAVL.dot", "w")
        f.write(dotContent)
        f.close()
        os.system(cmd)

    def __exportGraphviz(self, node):
        if not node:
            return
        rootNode = "node{0}".format(node.value) + \
                "[label=\"{0}-{1}\"]\n".format(node.val, node.content)
        value = rootNode + "\n"

        leftNode = self.aux_export_graphviz(node.left)
        rightNode = self.aux_export_graphviz(node.right)

        if node.left:
            value += "node{0}".format(node.value) + \
                " -> node{0}\n".format(node.left.value) + leftNode
        if node.right:
            value += "node{0}".format(node.value) + \
                    " -> node{0}\n".format(node.right.value) + rightNode

        return value

    def __buildTreeRec(self, nodes: List[Node]) -> Node:
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1].copy())  # duplicate last elem if odd number of elements
        half: int = len(nodes) // 2
 
        if len(nodes) == 2:
            return Node(nodes[0], nodes[1], Node.hash(nodes[0].value + nodes[1].value), nodes[0].content+"+"+nodes[1].content)
 
        left: Node = self.__buildTreeRec(nodes[:half])
        right: Node = self.__buildTreeRec(nodes[half:])
        value: str = Node.hash(left.value + right.value)
        content: str = f'{left.content}+{right.content}'
        return Node(left, right, value, content)
 
    def printTree(self) -> None:
        self.__printTreeRec(self.root)
         
    def __printTreeRec(self, node: Node) -> None:
        if node != None:
            if node.left != None:
                print("Left: "+str(node.left))
                print("Right: "+str(node.right))
            else:
                print("Input")
                 
            if node.is_copied:
                print('(Padding)')
            print("Value: "+str(node.value))
            print("Content: "+str(node.content))
            print("")
            self.__printTreeRec(node.left)
            self.__printTreeRec(node.right)
 
    def getRootHash(self) -> str:
      return self.root.value