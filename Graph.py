class Graph:
    def __init__(self) -> None:
        self.root = {}

    def insert_nodes(self, data):
        
        if not self.root:
            pass
        else:
            self.root = data