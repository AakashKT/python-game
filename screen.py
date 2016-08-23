
class Screen:

	def __init__(self, width, height):
		self.width = width;
		self.height = height;

		self.displayMatrix = [];
		self.drawBounds();


	def update(self):
		for i in range(self.height):
			for j in range(self.width):
				print(self.displayMatrix[i][j], end=' ');

			print("");


	def drawBounds(self):
		self.height = self.height+2;
		self.width = self.width+2;

		self.hasBounds = True;

		for i in range(self.height):
			tempMatrix = [];

			if(i==0 or i==self.height-1):
				for j in range(self.width):
					tempMatrix.append("-");
			else:
				for j in range(self.width):
					if(j==0 or j==self.width-1):
						tempMatrix.append("|");
					else:
						tempMatrix.append(" ");

			self.displayMatrix.append(tempMatrix);


	def drawObject(self, obj, x, y):
		self.displayMatrix[y-1][x-1] = obj;


