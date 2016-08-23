import pygame
import sys
import os

class Block:

	def __init__(self, block_type):
		self.block_type = block_type;

		self.block_scale = [(0, 0), (120, 30), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1), (1, 1)];

	def init_block(self, x):
		block_type = str(self.block_type);
		block = pygame.image.load(os.path.join("images", "block-"+block_type+".gif"));
		block = pygame.transform.scale(block, self.block_scale[self.block_type]);

		block_rect = block.get_rect();
		block_rect.centerx = x;

		return (block, block_rect);

class Board:

	def __init__(self, height, width):
		print("inited");

		self.width = width;
		self.height = height;
		self.board_matrix = [];

	def init_board(self):
		for i in range(0, self.height):
			temp_matrix = [];
			for j in range(0, self.width):
				temp_matrix.append(0);

			self.board_matrix.append(temp_matrix);

class Gameplay():

	def __init__(self, width, height, background_color):
		self.background_color = background_color;

		pygame.init();

		size = (width, height);
		self.screen = pygame.display.set_mode(size);

		self.width = width;
		self.height = height;
		self.background_color = background_color;

		print("inited gameplay");

	def create_board(self):

		board_handler = Board(self.width, self.height);
		board_handler.init_board();

	def create_block(self, x, y):
		block_type = 1 #put random.randomint(1, 8) here

		block_handler = Block(block_type);
		(self.block, self.block_rect) = block_handler.init_block(x);

	def update_screen(self):
		self.screen.fill(self.background_color);

		self.screen.blit(self.block, self.block_rect);
		pygame.display.flip();
