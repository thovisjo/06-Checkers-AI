#!/usr/bin/python
class AI:
	def __init__(self, player):
		self.player = player
	
	def choose_piece(self, board, pieces, opponents):
		'''
		By whatever criteria you choose, select a piece to move. You will need to return the piece and its available jumps		
		'''
		jumps = []
		piece = ''
		for p in pieces:
			piece = p
		squares = board.get_squares()
		jumps = piece.check_jump(pieces + opponents,sqares)		
		return (piece,jumps)
	
	def move_piece(piece,board,pieces,opponents):
		'''
		Move the piece to its new location
		'''
		squares = board.get_squares()
		jumps = piece.check_jump(pieces + opponents,sqares)		
		#move the piece
		
		#get any new jumps (i.e., double-jumps)
		jumps = piece.check_jump(pieces + opponents,sqares)		
		return (piece,jumps,pieces,opponents)