#!/usr/bin/python
class AI:
	def __init__(self, player):
		self.player = player
	
	def choose_piece(self, board, pieces, opponents):
		'''
		By whatever criteria you choose, select a piece to move. You will need to return the piece and its available jumps		
		'''
		squares = board.get_squares()
		for p in pieces:
			if p.alive:
				jumps = p.get_valid_possibilities(squares,pieces + opponents)
				if len(jumps):
					return (p,jumps)			
		return (p,[])
	
	def move_piece(self, piece,board,pieces,opponents):
		'''
		Move the piece to its new location
		'''
		squares = board.get_squares()
		jumps = piece.get_valid_possibilities(squares, pieces+opponents)
		#move the piece
		if len(jumps):
			(row,column) = jumps[0]
			piece.move(row,column)
			#get any new jumps (i.e., double-jumps)
			jumps = piece.check_jump(pieces + opponents,squares)		
		return (piece,jumps,pieces,opponents)