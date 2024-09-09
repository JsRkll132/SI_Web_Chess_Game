

class Chessitems() :
    
    def __init__(self) -> None:
        
        self.white_items = ["Rb","RNb","Cb","Ab","Tb","Cb","Ab","Tb","Pb"]
        self.black_items = ["Rn","RNn","Cn","An","Tn","Cn","An","Tn","Pn"]
        
    def getWhiteItems(self) : 
        return self.white_items
    def getBlackItems(self) : 
        return self.black_items