"""

Name : Aakash K.T.
20161202

If possible, compile using python3
This game was made and tested keeping python3 in mind.

Should also work with python2.7


"""


import pygame, sys, os, random, math

THRESH = 30;

class BlockGroup(pygame.sprite.Sprite):

	def __init__(self, surf):
		pygame.sprite.Sprite.__init__(self);
		self.image = surf;
		self.rect = self.image.get_rect();

class Resources:

	board_width, board_height = 20, 22;
	loaded_images = {};

	@staticmethod
	def init():
		block_I = Resources.load_image("block-I.png");
		block_IR = Resources.load_image("block-IR.png");

		block_Z = Resources.load_image("block-Z.png");
		block_ZR = Resources.load_image("block-ZR.png");

		block_O = Resources.load_image("block-O.png");
		block_OR = Resources.load_image("block-OR.png");

		block_L = Resources.load_image("block-L.png");
		block_LR = Resources.load_image("block-LR.png");
		block_LRR = pygame.transform.flip(block_L[0], True, True);
		block_LRR = (block_LRR, block_LRR.get_rect());
		block_LRRR = Resources.load_image("block-LRRR.png");

		ground = Resources.load_image("ground.png");

		Resources.loaded_images = {
			"ground.png":ground,
			"block-I.png":block_I,
			"block-IR.png":block_IR,
			"block-Z.png":block_Z,
			"block-ZR.png":block_ZR,
			"block-O.png":block_O,
			"block-OR.png":block_OR,
			"block-L.png":block_L,
			"block-LR.png":block_LR,
			"block-LRR.png":block_LRR,
			"block-LRRR.png":block_LRRR
		};

	@staticmethod
	def get_image(name):

		return Resources.loaded_images[name];

	@staticmethod
	def load_image(name):

		fullpath = os.path.join("images", name);

		image = pygame.image.load(fullpath);
		image = image.convert_alpha();

		return image, image.get_rect();

	@staticmethod
	def get_block(gplay):
		r = random.choice((1, 2, 3, 4));

		if r == 1:
			temp = BlockI(gplay);
			return temp;
		elif r == 2:
			temp = BlockZ(gplay);
			return temp;
		elif r == 3:
			temp = BlockO(gplay);
			return temp;
		elif r == 4:
			temp = BlockL(gplay);
			return temp;

class Ground(pygame.sprite.Sprite):

	def __init__(self, image):

		pygame.sprite.Sprite.__init__(self);

		self.image, self.rect = Resources.get_image(image);
		self.rect.centery = self.rect.y + 30*(Resources.board_height-1);

class Board:

	def __init__(self, ground_image, background_color, screen):
		self.screen = screen;
		self.min = Resources.board_height-2;

		self.display = [];
		self.row = [];
		width, height = screen.get_size();

		self.background = pygame.Surface((width, height));
		self.background = self.background.convert_alpha();
		self.background.fill(background_color);

		self.ground = Ground(ground_image);
		self.groundsprite = pygame.sprite.Group(self.ground);

		screen.blit(self.background, (0, 0));

		for i in range(0, Resources.board_height):
			temp = [];
			self.row.append(0);
			for j in range(0, Resources.board_width):
				temp.append(0);
			self.display.append(temp);

	def add_ground(self):
		for i in range(20, Resources.board_height):
			for j in range(0, Resources.board_width):
				self.display[i][j] = 1;

	def add_block(self, block, blocksprite):
		self.block = block;
		self.blocksprite = blocksprite;

	def delete_row(self, r):
		global block_group_sprite;
		zero = [];

		new_surface = pygame.Surface((30*Resources.board_width, 30*(r+1)));
		new_surface.fill(pygame.Color(255, 255, 255, 255));
		new_surface = new_surface.convert_alpha();

		del self.row[r];
		self.row.insert(0, 0);

		del self.display[r];
		for i in range(0, Resources.board_width):
			zero.append(0);

		self.display.insert(0, zero);
		self.min = self.min - 1;

		for i in range(self.min, 30*(r)+1):

			for j in range(0, 30*(Resources.board_width)):
				color = self.screen.get_at((j, i));
				new_surface.set_at((j, i+30), color);

		self.blocksprite.empty();

		new_surface = new_surface.convert_alpha();
		block_group_sprite = pygame.sprite.RenderUpdates(BlockGroup(new_surface));
		block_group_sprite.draw(self.screen);

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
				if(self.display[one["y"]][one["x"]+1] == 0 and self.display[three["y"]+1][three["x"]+1] == 0 and self.display[four["y"]+1][four["x"]-2] == 0):
					one["x"], one["y"] = one["x"] + 1, one["y"];
					three["x"], three["y"] = three["x"] + 1, three["y"]+1;
					four["x"], four["y"] = four["x"] - 2, four["y"] + 1;
					return False;
				else:
					return True;

	def check_right(self):
		one = self.block.one;
		two = self.block.two;
		three = self.block.three;
		four = self.block.four;

		if(one["x"]+1 >= Resources.board_width or two["x"]+1 >= Resources.board_width or three["x"]+1 >= Resources.board_width or four["x"]+1 >= Resources.board_width):
			return True;

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

		if(one["x"]-1 < 0 or two["x"]-1 < 0 or three["x"]-1 < 0 or four["x"]-1 < 0):
			return True;

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
			self.display[one["y"]][one["x"]] = 1;
			self.display[two["y"]][two["x"]] = 1;
			self.display[three["y"]][three["x"]] = 1;
			self.display[four["y"]][four["x"]] = 1;

			self.min = min(one["y"], two["y"], three["y"], four["y"]);

			if(self.min <= 0):
				self.block.gplay.lost(self.blocksprite);

			self.row[one["y"]] = self.row[one["y"]] + 1;
			self.row[two["y"]] = self.row[two["y"]] + 1;
			self.row[three["y"]] = self.row[three["y"]] + 1;
			self.row[four["y"]] = self.row[four["y"]] + 1;

			if self.row[one["y"]] == Resources.board_width:

				self.block.gplay.add_row_score();
				self.delete_row(one["y"]);
			if self.row[two["y"]] == Resources.board_width:

				self.block.gplay.add_row_score();
				self.delete_row(two["y"]);
			if self.row[three["y"]] == Resources.board_width:

				self.block.gplay.add_row_score();
				self.delete_row(three["y"]);
			if self.row[four["y"]] == Resources.board_width:

				self.block.gplay.add_row_score();
				self.delete_row(four["y"]);

			return True;

class Block(pygame.sprite.Sprite):

	def __init__(self):
		pygame.sprite.Sprite.__init__(self);

	def move_to_bottom(self, screen, board, blocksprite):

		while(self.move_down(screen, board, blocksprite) == True):
			blocksprite.draw(screen);

	def move_down(self, screen, board, blocksprite):
		obj_collided = board.check_down();

		if obj_collided == True:
			return False;
		else:
			self.rect.centery = self.rect.centery + 30;
			blocksprite.clear(screen, board.background);

			return True;

	def move_right(self, screen, board, blocksprite):

		obj_collided = board.check_right();

		if obj_collided == False:
			self.rect.centerx = self.rect.centerx + 30;
			blocksprite.clear(screen, board.background);

	def move_left(self, screen, board, blocksprite):

		obj_collided = board.check_left();

		if obj_collided == False:
			self.rect.centerx = self.rect.centerx - 30;
			blocksprite.clear(screen, board.background);

	def rotate(self, screen, board, blocksprite):
		obj_collided = board.check_rotate();

		if obj_collided == False:
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

			self.image, new_rect = Resources.get_image(image);
			self.image = pygame.transform.scale(self.image, scale);
			new_rect = self.image.get_rect();

			new_rect.x = self.rect.x;
			new_rect.y = self.rect.y;

			self.rect = new_rect;

			blocksprite.clear(screen, board.background);

class BlockZ(Block):

	def __init__(self, gplay):
		Block.__init__(self);

		self.gplay = gplay;
		gplay.add_block_score();

		x_offset = math.floor(Resources.board_width/2);

		self.is_vertical = True;
		self.block_type = "Z";

		self.one = {"x": x_offset + 0, "y":0};
		self.two = {"x": x_offset + 0, "y":1};
		self.three = {"x": x_offset + 1, "y":1};
		self.four = {"x": x_offset + 1, "y":2};

		self.image, self.rect = Resources.get_image("block-Z.png");
		self.image = pygame.transform.scale(self.image, (60, 90));
		self.rect = self.image.get_rect();

		self.rect.centerx = self.rect.centerx + 30*x_offset;

		self.x_scale = 60;
		self.y_scale = 90;

class BlockI(Block):

	def __init__(self, gplay):
		Block.__init__(self);

		self.gplay = gplay;
		gplay.add_block_score();

		x_offset = math.floor(Resources.board_width/2);

		self.is_vertical = True;
		self.block_type = "I";

		self.one = {"x": x_offset + 0, "y":0};
		self.two = {"x": x_offset + 0, "y":1};
		self.three = {"x": x_offset + 0, "y":2};
		self.four = {"x": x_offset + 0, "y":3};

		self.image, self.rect = Resources.get_image("block-I.png");
		self.image = pygame.transform.scale(self.image, (30, 120));
		self.rect = self.image.get_rect();

		self.rect.centerx = self.rect.centerx + 30*x_offset;

		self.x_scale = 30;
		self.y_scale = 120;

class BlockO(Block):

	def __init__(self, gplay):
		Block.__init__(self);

		self.gplay = gplay;
		gplay.add_block_score();

		x_offset = math.floor(Resources.board_width/2);

		self.is_vertical = True;
		self.block_type = "O";

		self.one = {"x": x_offset + 0, "y":0};
		self.two = {"x": x_offset + 0, "y":1};
		self.three = {"x": x_offset + 1, "y":0};
		self.four = {"x": x_offset + 1, "y":1};

		self.image, self.rect = Resources.get_image("block-O.png");
		self.image = pygame.transform.scale(self.image, (60, 60));
		self.rect = self.image.get_rect();

		self.rect.centerx = self.rect.centerx + 30*x_offset;

		self.x_scale = 60;
		self.y_scale = 60;

class BlockL(Block):

	def __init__(self, gplay):
		Block.__init__(self);

		self.gplay = gplay;
		gplay.add_block_score();

		x_offset = math.floor(Resources.board_width/2);

		self.is_vertical = 1;
		self.block_type = "L";

		self.one = {"x": x_offset + 1, "y":0};
		self.two = {"x": x_offset + 1, "y":1};
		self.three = {"x": x_offset + 1, "y":2};
		self.four = {"x": x_offset + 0, "y":2};

		self.image, self.rect = Resources.get_image("block-L.png");
		self.image = pygame.transform.scale(self.image, (60, 90));
		self.rect = self.image.get_rect();

		self.rect.centerx = self.rect.centerx + 30*x_offset;

		self.x_scale = 60;
		self.y_scale = 90;

	def rotate(self, screen, board, blocksprite):
		obj_collided = board.check_rotate();

		if obj_collided == False:
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

			self.image, new_rect = Resources.get_image(image);
			self.image = pygame.transform.scale(self.image, scale);
			new_rect = self.image.get_rect();

			new_rect.x = self.rect.x;
			new_rect.y = self.rect.y;

			self.rect = new_rect;

			blocksprite.clear(screen, board.background);

class Gameplay:

	def __init__(self, screen):
		self.score = 0;
		self.screen = screen;
		self.did_lose = False;
		self.update_screen_text();

	def add_block_score(self):
		self.score = self.score + 10;

	def add_row_score(self):
		self.score = self.score + 100;

	def update_screen_text(self):
		self.font = pygame.font.Font(None, 36);

		self.text = self.font.render("Score : "+str(self.score), True, (255, 255, 255));
		self.textpos = self.text.get_rect();
		self.textpos.x = (Resources.board_width)*30 - 150;
		self.textpos.y = (Resources.board_width)*30 + 30;

		self.screen.fill((166, 87, 50), self.textpos);
		self.screen.blit(self.text, self.textpos);

	def lost(self, blocksprite):
		global block_group_sprite;
		self.did_lose = True;

		gfont = pygame.font.Font(None, 50);

		gover = gfont.render("Game Over!", True, (1, 1, 1));
		goverpos = gover.get_rect();
		goverpos.centerx = int(30*Resources.board_width/2);
		goverpos.centery = int(30*Resources.board_height/2);

		block_group_sprite.empty();
		block_group_sprite.draw(self.screen);

		blocksprite.empty();
		blocksprite.draw(self.screen);

		self.screen.blit(gover, goverpos);

def main():
	global THRESH;

	width, height = 30*(Resources.board_width), 30*(Resources.board_height);

	pygame.init();
	screen = pygame.display.set_mode((width, height));

	pygame.display.set_caption("Tetris - Aakash");

	Resources.init();

	board = Board("ground.png", (255, 255, 255), screen);
	gplay = Gameplay(screen);

	block = Resources.get_block(gplay);
	blocksprite = pygame.sprite.Group(block);

	global block_group_sprite;
	block_group = BlockGroup(pygame.Surface((0, 0)));
	block_group_sprite = pygame.sprite.RenderUpdates(block_group);

	board.add_block(block, blocksprite);
	board.add_ground();

	pygame.display.update();

	clock = pygame.time.Clock();
	frames = 1;

	while(1):
		clock.tick(60);

		if gplay.did_lose == True:
			break;

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

					block_group_sprite.draw(screen);

					block = Resources.get_block(gplay);
					blocksprite.add(block);

					board.add_block(block, blocksprite);

					frames = 1;
				elif event.key == pygame.K_r:
					block.rotate(screen, board, blocksprite);

		if(frames >= THRESH):
			if block.move_down(screen, board, blocksprite) == False:
				block = Resources.get_block(gplay);
				blocksprite.add(block);

				board.add_block(block, blocksprite);

			frames = 1;

		block_group_sprite.draw(screen);

		blocksprite.draw(screen);
		board.groundsprite.draw(screen);
		gplay.update_screen_text();

		pygame.display.update();

		frames += 1;

		if(gplay.score >= 500):
			THRESH = 10;
		elif(gplay.score >= 100):
			THRESH = 20;
		elif(gplay.score >= 1000):
			THRESH = 5;

	while(1):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit();

		pygame.display.update();

if __name__ == "__main__":
	main();
