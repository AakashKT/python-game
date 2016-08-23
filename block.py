import pygame, sys, os

class Block:

	def __init__(self):
		self.block_types = [1];

	def get_block(self, speed):
		block = pygame.image.load(os.path.join("images", "block-1.gif"));
		block = pygame.transform.scale(block, (120, 30));

		return block;