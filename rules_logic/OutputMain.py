
import pygame as p

import ChessItems

images = {}
if __name__ == '__main__' : 
    blackPieces = sorted(ChessItems.Chessitems().getBlackItems())
    whitePieces = sorted(ChessItems.Chessitems().getWhiteItems())
    print(whitePieces)
    print(blackPieces)
    for i in blackPieces : 
        images[i] = p.transform.scale(p.image.load('GameView/Images/'+i+'.png'),(512,512//8))
    for i in whitePieces : 
        images[i] = p.transform.scale(p.image.load('GameView/Images/'+i+'.png'),(512,512//8))