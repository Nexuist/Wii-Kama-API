import pygame, serial

# Port of the arduino's map() function
def arduino_map(x, in_min, in_max, out_min, out_max):
    return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

class Color:
    white = (255, 255, 255)
    black = (0, 0, 0)
    red = (255, 0, 0)
    blue = (0, 0, 255)
    baby_blue = (137, 207, 240)
    yellow = (255, 255, 0)

class Scene:
	def __init__(self, args = None):
		self.screen = pygame.display.get_surface()
		self.background = pygame.Surface(self.screen.get_size())
		self.background = self.background.convert()
		self.background.fill(Color.white)
		self.center_x = self.background.get_rect().centerx
		self.center_y = self.background.get_rect().centery
		self.build_scene(args)
		self.done = False
		self.data = []
		self.clock = pygame.time.Clock()
		self.framerate = 60
		self.event_loop()

	def build_scene(self, args):
        # Called on init
		self.ser = serial.Serial("/dev/tty.usbmodem1411", 115200)
		self.font = pygame.font.SysFont("monospace", 12)

	def render_scene(self):
		# Called every frame
		label = self.font.render(self.rawData, 1, Color.black)
		self.background.blit(label, (5, 620))
		pygame.draw.circle(self.background, Color.black, (self.center_x, 130), 100, 5)
		if self.data:
			joy_x = int(self.data[0])
			joy_y = int(self.data[1])
			virtual_stick_x = arduino_map(joy_x, 0, 255, 50, 250)
			virtual_stick_y = arduino_map(joy_y, 0, 255, 230, 30)
			pygame.draw.circle(self.background, Color.black, (virtual_stick_x, virtual_stick_y), 20, 5)


	def parse_data(self):
		self.rawData = self.ser.readline()
		if "DATA" in self.rawData:
			# Data packet
			self.data = self.rawData[6:].split("|")
		print self.data


	def event_loop(self):
		while not self.done:
			self.parse_data()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
    					self.done = True
			self.background.fill(Color.white)
			self.render_scene()
			self.screen.blit(self.background, (0, 0))
			pygame.display.flip()
			self.clock.tick(self.framerate)

pygame.init()
resolution = (300, 640)
pygame.display.set_mode(resolution)
pygame.display.set_caption("Kama Demo")
Scene()
pygame.quit()
