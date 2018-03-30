#!/usr/bin/env python

import sys, logging, pygame
from Board import Board, Piece, Square
from AI import AI
assert sys.version_info >= (3,4), 'This script requires at least Python 3.4'

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


#easy to divide by sixteen
size = (width,height) = (400,400)
constraints = (cols,rows) = (8,8)
FPS = 20

red = (224,49,49)
black = (33,37,41)
board_colors = [(98,80,87),(222,226,230)]
board_alternate = [(73,80,87),(222,226,230)]
board_highlight = (255,224,102)


pygame.init()
font = pygame.font.SysFont("arial",30)
		
#----------------------------------------
# helper functions

def draw_board(board, alternate, pieces, draw, screen):
	board.draw(draw,screen,alternate)
	for p in pieces:
		p.draw(draw,screen)
	pygame.display.flip()

def move_piece(square,board,pieces,opponents,all_pieces,pos,selected,jumping,jumps,moves):
	selected = True
	if square.highlighted:
		for p in pieces:
			if p.alive and p.selected:
				p.move(square.col,square.row)
				p.check_king(rows)
				for j in jumps:
					if square.position == j['position']:
						j['piece'].alive = False
						jumping = p
						sq = board.get_squares()
						jumps = jumping.check_jump(all_pieces,sq)
						if not len(jumps):
							jumping = None
				if jumping is None:
					moves += 1
	for p in pieces:
		p.selected = False
	for s in board.get_squares():
		s.highlighted = False
	if jumping is not None:
		jumping.selected = True
		for j in jumps:
			sq = board.get_squares()
			for s in sq:
				if j['position'] == s.position:
					s.highlighted = True
		selected = True
	else:
		selected = False
		jumps = []
	return (board,pieces,selected,jumping,jumps,moves)

def select_piece(square,board,pieces,all_pieces,pos,jumps):
	selected = False
	for p in pieces:
		if p.alive and p.position == square.position:
			p.selected = True
			possibilities = p.get_possibilities(board.get_squares())
			for h in possibilities:
				c = board.get_square_coord(h)
				if c is not None:
					add = True
					for a in all_pieces:
						if a.alive and a.col == c.col and a.row == c.row:
							add = False
					if add:
						c.highlighted = True
					else:
						sq = board.get_squares()
						jumps = p.check_jump(all_pieces,sq)
						for j in jumps:
							for s in sq:
								if j['position'] == s.position:
									s.highlighted = True
			selected = True
	return (board,pieces,selected,jumps)

#----------------------------------------

def main():
	screen = pygame.display.set_mode(size)
	pygame.display.set_caption("Checkers")
	clock = pygame.time.Clock()

	moves = 0
	
	board = Board(size,constraints,board_colors,board_alternate,board_highlight)
	
	# add red pieces to the board
	red_pieces = []
	for p in board.red_starting_positions:
		piece = Piece(p, 'Red', red, board_highlight, board.dim,-1,font)
		red_pieces.append(piece)

	# add black pieces to the board
	black_pieces = []
	for p in board.black_starting_positions:
		piece = Piece(p, 'Black', black, board_highlight, board.dim,1,font)
		black_pieces.append(piece)

	all_pieces = red_pieces + black_pieces

	draw_board(board, 0, all_pieces, pygame.draw, screen)
	
	selected = False
	jumping = None
	jumps = []
	playing = True
	winner = ''
	players = ["Red","Black"]
	
	ai = AI('Black')
	
	while playing:
		clock.tick(FPS)
		currentPlayer = players[moves % len(players)]

		if currentPlayer == "Black":
			pieces = black_pieces
			opponents = red_pieces
			(piece,jumps) = ai.choose_piece(board,pieces,opponents)
			while len(jumps):
				(piece,jumps,pieces,opponents) = ai.move_piece(piece,board,pieces,opponents)
				for p in pieces:
					p.check_king(rows)
			draw_board(board, moves % len(players), all_pieces, pygame.draw, screen)
			moves += 1
			
		else:
			pieces = red_pieces
			opponents = black_pieces

			for event in pygame.event.get():
				if event.type == pygame.QUIT: sys.exit()
				# handle MOUSEBUTTONUP
				if event.type == pygame.MOUSEBUTTONUP:
					pos = pygame.mouse.get_pos()
					square = board.get_square(pos)
					if selected:
						(board,pieces,selected,jumping,jumps,moves) = move_piece(square,board,pieces,opponents,all_pieces,pos,selected,jumping,jumps,moves)
					else:
						(board,pieces,selected,jumps) = select_piece(square,board,pieces,all_pieces,pos,jumps)


					draw_board(board, moves % len(players), all_pieces, pygame.draw, screen)

				#check for winning condition
				red_count = 0
				black_count = 0

				for p in all_pieces:
					if p.alive:
						if p.player == 'Red':
							red_count += 1
						if p.player == 'Black':
							black_count += 1

				if red_count == 0:
					winner = 'Black'
					playing = False

				if black_count == 0:
					winner = 'Red'
					playing = False

	
	print(winner + ' won in only ' + str(moves//2) + ' turns! Good job!')


if __name__ == "__main__":
	main()