import signal
from screen import Screen

class AlarmException(Exception):
    pass

class Gameplay:

	def checkInput(self, signum, frame):
		raise AlarmException;

	def __init__(self):
		self.screen = Screen(30, 32);
		self.input = "";

	def start(self):
		print("");
		self.screen.update();

		signal.signal(signal.SIGALRM, self.checkInput);
		signal.alarm(1);

		try:
			print("Enter move : ", end=" ");
			self.input = input();

			if(self.input != ""):
				print("haha");

			signal.alarm(0);
		except AlarmException:
			self.start();