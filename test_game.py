import tetris
import pygame, sys, os, random, math

class TestClass:

    pygame.init();
    screen = pygame.display.set_mode((30*tetris.Resources.board_width, 30*tetris.Resources.board_height));
    tetris.Resources.init();

    def make_board(self):
        """ Function to make the board """

        return tetris.Board("ground.png", (255, 255, 255), self.screen);

    def make_block(self):
        gplay = tetris.Gameplay(self.screen);
        block = tetris.Resources.get_block(gplay);
        blocksprite = pygame.sprite.Group(block);

        return block, blocksprite;

    def test_board_create(self):
        """ Function to test whether the board object has been successfully created """

        board = self.make_board();

        assert board != None;

    def test_ground_added(self):
        """ Function to test whether the ground has been added and the display matrix updated accordingly """

        board = self.make_board();
        board.add_ground();

        for i in range(20, tetris.Resources.board_height):
            for j in range(0, tetris.Resources.board_width):
                assert board.display[i][j]==1;

    def test_board_empty(self):
        """ Function to test that rest of the board remains empty after ground is added """

        board = self.make_board();
        board.add_ground();

        for i in range(0, tetris.Resources.board_height-20):
            for j in range(0, tetris.Resources.board_width):
                assert board.display[i][j]==0;

    def test_block_added(self):
        """ Function to test whether block object is initialised """

        board = self.make_board();
        board.add_ground();

        block, blocksprite = self.make_block();
        board.add_block(block, blocksprite);

        assert board.block != None and board.blocksprite != None;

    def test_row_deleted(self):
        """ Function to test deletion of one row as per gameplay """

        board = self.make_board();
        board.add_ground();

        block, blocksprite = self.make_block();
        board.add_block(block, blocksprite);

        mini = board.min;

        for i in range(0, tetris.Resources.board_width):
            board.display[tetris.Resources.board_height-6][i] = 1;

        board.delete_row(tetris.Resources.board_height-6);

        for i in range(0, tetris.Resources.board_width):
            assert board.display[tetris.Resources.board_height-6][i] == 0;

        assert board.min <= mini;

    def test_score(self):
        """ Function to test increasing score """

        gplay = tetris.Gameplay(self.screen);
        ini_score = gplay.score;

        gplay.add_block_score();
        assert gplay.score >= ini_score;

        ini_score = gplay.score;
        gplay.add_row_score();
        assert gplay.score >= ini_score;
