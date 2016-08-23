import pygame, sys, os, random

class Resources:

	@staticmethod
	def load_image(name):

		fullpath = os.path.join("images", name);

		image = pygame.image.load(fullpath);
		image = image.convert_alpha();

		return image, image.get_rect();

	@staticmethod
	def get_block():
		r = random.choice((1, 2, 3));

		if r == 1:
			temp = BlockI();
			return temp;
		elif r == 2:
			temp = BlockZ();
			return temp;
		elif r == 3:
			temp = BlockO();
			return temp;
		elif r == 4:
			temp = BlockL();
			return temp;

class Ground(pygame.sprite.Sprite):

	def __init__(self, image):

		pygame.sprite.Sprite.__init__(self);

		self.image, self.rect = Resources.load_image(image);
		self.rect.centery = self.rect.y + 30*21;

class Board:

	def __init__(self, ground_image, background_color, screen):
		self.screen = screen;
		self.min = 19;

		self.display = [];
		self.row = [];
		width, height = screen.get_size();

		self.background = pygame.Surface((width, height));
		self.background = self.background.convert();
		self.background.fill(background_color);

		self.ground = Ground(ground_image);
		self.groundsprite = pygame.sprite.Group(self.ground);

		screen.blit(self.background, (0, 0));

		for i in range(0, 22):
			temp = [];
			self.row.append(0);
			for j in range(0, 20):
				temp.append(0);
			self.display.append(temp);

	def add_ground(self):
		for i in range(20, 22):
			for j in range(0, 20):
				self.display[i][j] = 1;

	def add_block(self, block):
		self.block = block;

	def delete_row(self, r):
		zero = [];

		new_surface = pygame.Surface((30*20, 30*(r+1)));
		new_surface.fill(pygame.Color(255, 255, 255, 255));

		del self.row[r];
		self.row.insert(0, 0);

		del self.display[r];
		for i in range(0, 20):
			zero.append(0);

		self.display.insert(0, zero);

		print(self.min);

		for i in range(self.min, 30*(r)+1):

			for j in range(0, 30*20):
				color = self.screen.get_at((j, i));
				new_surface.set_at((j, i+30), color);

		self.screen.blit(new_surface, (0, 0));

	def check_rotate(self):
		one = self.block.one;
		two = self.block.two;
		three = self.block.three;
		four = self.block.four;

		block_type = self.block.block_type;

		if(block_type == "Z"):
			if(self.block.is_vertical == True):
				if(self.display[one["y"]][one["x"]+2] == 0 and self.display[four["y"]-2][four["x"]] == 0):
					one["x"] = one["x"] + 2;
					four["y"] = four["y"] - 2;
					return False;
				else:
					return True;
			else:
				if(self.display[one["y"]][one["x"]-2] == 0 and self.display[four["y"]+2][four["x"]] == 0):
					one["x"] = one["x"] - 2;
					four["y"] = four["y"] + 2;
					return False;
				else:
					return True;
		elif(block_type == "I"):
			if(self.block.is_vertical == True):
				if(self.display[two["y"]-1][two["x"]+1] == 0 and self.display[three["y"]-2][three["x"]+2] == 0 and self.display[four["y"]-3][four["x"]+3] == 0):
					two["x"], two["y"] = two["x"] + 1, two["y"] - 1;
					three["x"], three["y"] = three["x"] + 2, three["y"] - 2;
					four["x"], four["y"] = four["x"] + 3, four["y"] - 3;
					return False;
				else:
					return True;
			else:
				if(self.display[two["y"]+1][two["x"]-1] == 0 and self.display[three["y"]+2][three["x"]-2] == 0 and self.display[four["y"]+3][four["x"]-3] == 0):
					two["x"], two["y"] = two["x"] - 1, two["y"] + 1;
					three["x"], three["y"] = three["x"] - 2, three["y"] + 2;
					four["x"], four["y"] = four["x"] - 3, four["y"] + 3;
					return False;
				else:
					return True;
		elif(block_type == "O"):
			pass;
		elif(block_type == "L"):
			if(self.block.is_vertical == 1):
				if(self.display[one["y"]][one["x"]-1] == 0 and self.display[two["y"]-1][two["x"]] == 0 and self.display[three["y"]-2][three["x"]+1] == 0 and self.display[four["y"]-1][four["x"]+2] == 0):
					one["x"], one["y"] = one["x"] - 1, one["y"];
					two["x"], two["y"] = two["x"], two["y"] - 1;
					three["x"], three["y"] = three["x"] + 1, three["y"] - 2;
					four["x"], four["y"] = four["x"] + 2, four["y"] - 1;
					return False;
				else:
					return True;
			elif self.block.is_vertical == 2:
				if(self.display[three["y"]+1][three["x"]-2] == 0 and self.display[four["y"]+1][four["x"]-2] == 0):
					three["x"], three["y"] = three["x"] - 2, three["y"] + 1;
					four["x"], four["y"] = four["x"] - 2, four["y"] + 1;
					return False;
				else:
					return True;
			elif self.block.is_vertical == 3:
				if(self.display[two["y"]+1][two["x"]] == 0 and self.display[four["y"]-1][four["x"]+2] == 0):
					two["x"], two["y"] = two["x"], two["y"] + 1;
					four["x"], four["y"] = four["x"] + 2, four["y"] - 1;
					return False;
				else:
					return True;
			else:
				if(self.display[one["y"]][one["x"]+1] == 0 and self.display[two["y"]+1][two["x"]] == 0 and self.display[three["y"]][three["x"]+1] == 0 and self.display[four["y"]+1][four["x"]-2] == 0):
					one["x"], one["y"] = one["x"] + 1, one["y"];
					two["x"], two["y"] = two["x"], two["y"] + 1;
					three["x"], three["y"] = three["x"] + 1, three["y"];
					four["x"], four["y"] = four["x"] - 2, four["y"] + 1;
					return False;
				else:
					return True;

	def check_right(self):
		one = self.block.one;
		two = self.block.two;
		three = self.block.three;
		four = self.block.four;

		if(self.display[one["y"]][one["x"]+1] == 0 and self.display[two["y"]][two["x"]+1] == 0 and self.display[three["y"]][three["x"]+1] == 0 and self.display[four["y"]][four["x"]+1] == 0):
			one["x"] = one["x"] + 1;
			two["x"] = two["x"] + 1;
			three["x"] = three["x"] + 1;
			four["x"] = four["x"] + 1;

			return False;
		else:
			return True;

	def check_left(self):
		one = self.block.one;
		two = self.block.two;
		three = self.block.three;
		four = self.block.four;

		if(self.display[one["y"]][one["x"]-1] == 0 and self.display[two["y"]][two["x"]-1] == 0 and self.display[three["y"]][three["x"]-1] == 0 and self.display[four["y"]][four["x"]-1] == 0):
			one["x"] = one["x"] - 1;
			two["x"] = two["x"] - 1;
			three["x"] = three["x"] - 1;
			four["x"] = four["x"] - 1;

			return False;
		else:
			return True;

	def check_down(self):
		one = self.block.one;
		two = self.block.two;
		three = self.block.three;
		four = self.block.four;

		if(self.display[one["y"]+1][one["x"]] == 0 and self.display[two["y"]+1][two["x"]] == 0 and self.display[three["y"]+1][three["x"]] == 0 and self.display[four["y"]+1][four["x"]] == 0):
			one["y"] = one["y"] + 1;
			two["y"] = two["y"] + 1;
			three["y"] = three["y"] + 1;
			four["y"] = four["y"] + 1;

			return False;
		else:
			print("Commit");
			self.display[one["y"]][one["x"]] = 1;
			self.display[two["y"]][two["x"]] = 1;
			self.display[three["y"]][three["x"]] = 1;
			self.display[four["y"]][four["x"]] = 1;

			self.min = min(one["y"], two["y"], three["y"], four["y"]);

			self.row[one["y"]] = self.row[one["y"]] + 1;
			self.row[two["y"]] = self.row[two["y"]] + 1;
			self.row[three["y"]] = self.row[three["y"]] + 1;
			self.row[four["y"]] = self.row[four["y"]] + 1;

			print(self.row[one["y"]], self.row[two["y"]], self.row[three["y"]], self.row[four["y"]])

			if self.row[one["y"]] == 20:
				print("RowFull");

				self.delete_row(one["y"]);
			if self.row[two["y"]] == 20:
				print("RowFull");

				self.delete_row(two["y"]);
			if self.row[three["y"]] == 20:
				print("RowFull");

				self.delete_row(three["y"]);
			if self.row[four["y"]] == 20:
				print("RowFull");

				self.delete_row(four["y"]);

			return True;

class Block(pygame.sprite.Sprite):

	def __init__(self):
		print("Created");

		pygame.sprite.Sprite.__init__(self);

	def move_to_bottom(self, screen, board, blocksprite):

		while(self.move_down(screen, board, blocksprite) == True):
			blocksprite.draw(screen);

	def move_down(self, screen, board, blocksprite):
		obj_collided = board.check_down();

		if obj_collided == True:
			print("Collision");

			return False;
		else:
			self.rect.centery = self.rect.centery + 30;
			blocksprite.clear(screen, board.background);

			return True;

	def move_right(self, screen, board, blocksprite):

		obj_collided = board.check_right();

		if obj_collided == True:
			print("Collision");
		else:
			self.rect.centerx = self.rect.centerx + 30;
			blocksprite.clear(screen, board.background);

	def move_left(self, screen, board, blocksprite):

		obj_collided = board.check_left();

		if obj_collided == True:
			print("Collision");
		else:
			self.rect.centerx = self.rect.centerx - 30;
			blocksprite.clear(screen, board.background);

	def rotate(self, screen, board, blocksprite):
		obj_collided = board.check_rotate();

		if obj_collided == True:
			print("Collision");
		else:
			image_type = self.block_type;
			scale = (0, 0);

			if self.is_vertical == True:
				image = "block-"+image_type+"R.png";
				scale = self.y_scale, self.x_scale;

				self.is_vertical = False;
			else:
				image = "block-"+image_type+".png";
				scale = self.x_scale, self.y_scale;

				self.is_vertical = True;

			self.image, new_rect = Resources.load_image(image);
			self.image = pygame.transform.scale(self.image, scale);
			new_rect = self.image.get_rect();

			new_rect.x = self.rect.x;
			new_rect.y = self.rect.y;

			self.rect = new_rect;

			blocksprite.clear(screen, board.background);

class BlockZ(Block):

	def __init__(self):
		Block.__init__(self);

		self.is_vertical = True;
		self.block_type = "Z";

		self.one = {"x":0, "y":0};
		self.two = {"x":0, "y":1};
		self.three = {"x":1, "y":1};
		self.four = {"x":1, "y":2};

		self.image, self.rect = Resources.load_image("block-Z.png");
		self.image = pygame.transform.scale(self.image, (60, 90));
		self.rect = self.image.get_rect();

		self.x_scale = 60;
		self.y_scale = 90;

class BlockI(Block):

	def __init__(self):
		Block.__init__(self);

		self.is_vertical = True;
		self.block_type = "I";

		self.one = {"x":0, "y":0};
		self.two = {"x":0, "y":1};
		self.three = {"x":0, "y":2};
		self.four = {"x":0, "y":3};

		self.image, self.rect = Resources.load_image("block-I.png");
		self.image = pygame.transform.scale(self.image, (30, 120));
		self.rect = self.image.get_rect();

		self.x_scale = 30;
		self.y_scale = 120;

class BlockO(Block):

	def __init__(self):
		Block.__init__(self);

		self.is_vertical = True;
		self.block_type = "O";

		self.one = {"x":0, "y":0};
		self.two = {"x":0, "y":1};
		self.three = {"x":1, "y":0};
		self.four = {"x":1, "y":1};

		self.image, self.rect = Resources.load_image("block-O.png");
		self.image = pygame.transform.scale(self.image, (60, 60));
		self.rect = self.image.get_rect();

		self.x_scale = 60;
		self.y_scale = 60;

class BlockL(Block):

	def __init__(self):
		Block.__init__(self);

		self.is_vertical = 1;
		self.block_type = "L";

		self.one = {"x":1, "y":0};
		self.two = {"x":1, "y":1};
		self.three = {"x":1, "y":2};
		self.four = {"x":0, "y":2};

		self.image, self.rect = Resources.load_image("block-L.png");
		self.image = pygame.transform.scale(self.image, (60, 90));
		self.rect = self.image.get_rect();

		self.x_scale = 60;
		self.y_scale = 90;

	def rotate(self, screen, board, blocksprite):
		obj_collided = board.check_rotate();

		if obj_collided == True:
			print("Collision");
		else:
			image_type = self.block_type;
			scale = (0, 0);

			if self.is_vertical == 1:
				image = "block-"+image_type+"R.png";
				scale = self.y_scale, self.x_scale;

				self.is_vertical = 2;
			elif self.is_vertical == 2:
				image = "block-"+image_type+"RR.png";
				scale = self.x_scale, self.y_scale;

				self.is_vertical = 3;
			elif self.is_vertical == 3:
				image = "block-"+image_type+"RRR.png";
				scale = self.y_scale, self.x_scale;

				self.is_vertical = 4;
			else:
				image = "block-"+image_type+".png";
				scale = self.x_scale, self.y_scale;

				self.is_vertical = 1;

			self.image, new_rect = Resources.load_image(image);
			self.image = pygame.transform.scale(self.image, scale);
			new_rect = self.image.get_rect();

			new_rect.x = self.rect.x;
			new_rect.y = self.rect.y;

			self.rect = new_rect;

			blocksprite.clear(screen, board.background);

def main():

	width, height = 30*20, 30*22;

	pygame.init();
	screen = pygame.display.set_mode((width, height));
	pygame.display.set_caption("Tetris - Aakash");

	board = Board("ground.png", (255, 255, 255), screen);

	block = Resources.get_block();
	blocksprite = pygame.sprite.Group(block);

	board.add_block(block);
	board.add_ground();

	pygame.display.update();

	clock = pygame.time.Clock();
	frames = 1;

	global collide_group 
	collide_group = pygame.sprite.Group(board.ground);

	while(1):
		clock.tick(40);

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit();
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RIGHT:
					block.move_right(screen, board, blocksprite);
				elif event.key == pygame.K_LEFT:
					block.move_left(screen, board, blocksprite);
				elif event.key == pygame.K_DOWN:
					block.move_to_bottom(screen, board, blocksprite);

					block = Resources.get_block();
					board.add_block(block);

					blocksprite = pygame.sprite.Group(block);

					frames = 1;
				elif event.key == pygame.K_r:
					block.rotate(screen, board, blocksprite);

		if(frames >= 40):
			if block.move_down(screen, board, blocksprite) == False:
				block = BlockI();
				board.add_block(block);

				blocksprite = pygame.sprite.Group(block);

			frames = 1;

		blocksprite.draw(screen);
		board.groundsprite.draw(screen);

		pygame.display.update();

		frames += 1;

if __name__ == "__main__":
	main();
