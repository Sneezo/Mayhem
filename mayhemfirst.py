"""
Main code file for Mayhem clone INF-1400
"""



# Import stuff, initiate pygame
import pygame
import random
import math
import precode
import config
import text

CENTER_POINT = (config.SCREEN_SIZE[0]/2,config.SCREEN_SIZE[1]/2)


class Game():
	"""
	Implements a game class that holds the broader variables and methods for the game.
	"""
	def __init__(self):
		"""	
		Initializes broad variables that don't have the most direct connection to other classes.
		
		Variables:
		screen 			the pygame display
		clock 			pygames clock object to keep track of time and maintain FPS
		bullets 		list that contains all bullets currently in motion
		players 		list containing both spaceships
		environments	lists containing walls, floor, ceiling and the asteroid (moving block)
		winner			variable to hold the winner name at the end of each "round" of the game

		Load images the game needs to run.
		Initialize pygame.
		Instanciate classes and append them to their respective lists.
		"""
		self.screen = pygame.display.set_mode(config.SCREEN_SIZE)
		self.clock = pygame.time.Clock()
		self.gamestate = 0
		self.bullets = []
		self.players = []
		self.environments = []
		self.winner = "None"

		#init pygame fonts, solved an error regarding font initializing
		pygame.font.init()

		#Display title of game, Thunder Mayhem (because of the background)
		pygame.display.set_caption("Thunder Mayhem")

		self.backgroundImage = pygame.image.load("background2.png")
		self.fueltankImage = pygame.image.load("fueltank.png")
		self.platformImage = pygame.image.load("platform.png")
		self.ceilingImage = pygame.image.load("ceiling.png")
		self.leftWallImage = pygame.image.load("brickwall.png")
		self.rightWallImage = pygame.image.load("brickwall.png")
		self.movingBlockImage = pygame.image.load("obstacle.png")
		self.bulletImage1 = pygame.image.load("bullet1.png")
		self.bulletImage2 = pygame.image.load("bullet2.png")
		self.shipImage1 = pygame.image.load("spaceship1.png")
		self.shipImage2 = pygame.image.load("spaceship2.png")


		#init pygame
		pygame.init()


		#instanciate stuff and append to lists
		#instanciate ships
		self.player1 = Spaceship(150,450,self.shipImage1,self.bulletImage1)
		self.player2 = Spaceship(config.SCREEN_SIZE[0]-150,450,self.shipImage2,self.bulletImage2)

		#instanciate walls
		self.leftWall = Environment(0,0,self.leftWallImage)
		self.environments.append(self.leftWall)

		self.rightWall = Environment(config.SCREEN_SIZE[0]-self.rightWallImage.get_rect().width,0,self.rightWallImage)
		self.environments.append(self.rightWall)

		#instanciate fueltank
		self.fueltank = Fueltank(config.SCREEN_SIZE[0]/2-self.fueltankImage.get_rect().width/2,50,self.fueltankImage)
		self.environments.append(self.fueltank)

		#instanciate asteroid / moving block
		self.movingBlock = MovingObstacle(200 - self.movingBlockImage.get_rect().width,600,50,6,self.movingBlockImage)
		self.environments.append(self.movingBlock)

		#instanciate platform / floor
		self.platform = Environment(0,config.SCREEN_SIZE[1]-self.platformImage.get_rect().height,self.platformImage)
		self.environments.append(self.platform)

		#instanciate ceiling / roof
		self.ceiling = Environment(0,0,self.ceilingImage)
		self.environments.append(self.ceiling)

		self.players.append(self.player1)
		self.players.append(self.player2)

	#prepare to print players variables
	def loadStats(self):
		"""
		Define the 6 bits of string that shows the players their lives, health and fuel.
		It's a method because it needs to be called often to update the variables.
		"""
		self.player1fuel = config.font.render("Fuel: " + str(self.player1.fuel),1,config.white)
		self.player2fuel = config.font.render("Fuel: " + str(self.player2.fuel),1,config.white)
		self.player1health = config.font.render("Health: " + str(self.player1.health),1,config.white)
		self.player2health = config.font.render("Health: " + str(self.player2.health),1,config.white)
		self.player1lives = config.font.render("Lives: " + str(self.player1.lives),1,config.white)
		self.player2lives = config.font.render("Lives: " + str(self.player2.lives),1,config.white)

	#print players variables
	def showStats(self):
		"""
		Blit the 6 bits of string from the loadStats method.
		Each line has 20 pixels between them.
		"""
		self.screen.blit(self.player1fuel,(50,30))
		self.screen.blit(self.player2fuel,(config.SCREEN_SIZE[0]-130,30))
		self.screen.blit(self.player1health,(50,50))
		self.screen.blit(self.player2health,(config.SCREEN_SIZE[0]-130,50))
		self.screen.blit(self.player1lives,(50,70))
		self.screen.blit(self.player2lives,(config.SCREEN_SIZE[0]-130,70))

	#apply gravity
	def gravitation(self):
		"""
		Apply graviational acceleration to the spaceships.
		"""
		for player in self.players:
			player.vel.y += config.gravity

	#draw different backgrounds for different gamestates
	def drawBackground(self):
		"""
		Draw a black background or an image depending on the gamestate.
		"""
		if self.gamestate == 0 or self.gamestate == 3:
			game.screen.fill((0,0,0))
		else:
			self.screen.blit(self.backgroundImage,(0,0))

	def mainLoop(self):
		"""
		Recursive method that calls all the methods necessary to run the game.
		It loops through gamestates depending on what's happened in the game.
		When all gamestates are done and it's time to restart the game,
		the method calls itself.
		"""

		while self.gamestate == 0:
			#keep FPS
			self.clock.tick(config.FPS)
			#quit if supposed to
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				#listen for input
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_f:
						self.gamestate = 1


			self.loadStats()

			self.drawBackground()
			self.showStats()

			#print instructions
			self.screen.blit(text.guideText,(100,220))
			self.screen.blit(text.guideText2,(100,240))
			self.screen.blit(text.guideText3,(100,260))
			self.screen.blit(text.guideText4,(100,280))
			self.screen.blit(text.guideText5,(100,300))
			self.screen.blit(text.guideText6,(100,320))

			#draw environments
			if len(game.environments) > 0:
				for env in game.environments:
					env.draw()

			#update players
			for player in game.players:

				player.draw()
				game.gravitation()
				player.rotateLeft()
				player.rotateRight()
				player.thrust()
				player.update()
				player.shoot()
				player.collideObjects()
				player.collideBullets()
				player.collideShips()

			#move asteroid
			game.movingBlock.move()

			#update display
			pygame.display.update()

		#change gamestate
		while self.gamestate == 1:
			self.clock.tick(config.FPS)

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				#player1 event listening
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_SPACE:
						game.player1.shooting = True
					if event.key == pygame.K_w:
						game.player1.thrusting = True
					if event.key == pygame.K_a:
						game.player1.rotatingLeft = True
					if event.key == pygame.K_d:
						game.player1.rotatingRight = True
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						game.player1.shooting = False
					if event.key == pygame.K_w:
						game.player1.thrusting = False
					if event.key == pygame.K_a:
						game.player1.rotatingLeft = False
					if event.key == pygame.K_d:
						game.player1.rotatingRight = False
				#player2 event listening
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RCTRL:
						game.player2.shooting = True
					if event.key == pygame.K_UP:
						game.player2.thrusting = True
					if event.key == pygame.K_LEFT:
						game.player2.rotatingLeft = True
					if event.key == pygame.K_RIGHT:
						game.player2.rotatingRight = True
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_RCTRL:
						game.player2.shooting = False
					if event.key == pygame.K_UP:
						game.player2.thrusting = False
					if event.key == pygame.K_LEFT:
						game.player2.rotatingLeft = False
					if event.key == pygame.K_RIGHT:
						game.player2.rotatingRight = False

			self.loadStats()

			self.drawBackground()

			self.showStats()


			if len(game.bullets) > 0:
				for bullet in game.bullets:
					bullet.update()

			if len(game.environments) > 0:
				for env in game.environments:
					env.draw()

			for player in game.players:

				player.draw()
				game.gravitation()
				player.rotateLeft()
				player.rotateRight()
				player.thrust()
				player.update()
				player.shoot()
				player.collideObjects()
				player.collideBullets()
				player.collideShips()

			game.movingBlock.move()

			pygame.display.update()

		self.gamestate = 3

		#load wintext displaying the winner and offer to play again
		self.wintext = config.font.render("Congratulations! " + self.winner + " won!",1,config.white)
		self.wintext2 = config.font.render("Press F to play again.",1,config.white)

		while self.gamestate == 3:
			self.clock.tick(config.FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_f:
						#reset game
						self.gamestate = 0
						game.player1.reset()
						game.player2.reset()

			self.loadStats()

			self.drawBackground()

			self.showStats()

			#display winner
			self.screen.blit(self.wintext,(100,220))
			self.screen.blit(self.wintext2,(100,240))


			if len(game.environments) > 0:
				for env in game.environments:
					env.draw()

			for player in game.players:

				player.draw()
				game.gravitation()
				player.rotateLeft()
				player.rotateRight()
				player.thrust()
				player.update()
				player.shoot()
				player.collideObjects()
				player.collideBullets()
				player.collideShips()

			game.movingBlock.move()

			pygame.display.update()

		#have the method call itself to keep the game running
		self.mainLoop()




class Spaceship(pygame.sprite.Sprite):
	"""
	Implements a spaceship inheriting from pygame.sprite.Sprite.
	Uses fuel to thrust, loses health when hit by bullets and dies when crashing into obstacles.
	"""
	def __init__(self,x,y,image,bulletImage):
		"""
		Variables:
		lives 			amount of lives before losing the round
		health 			amount of damage one can take before dying
		maxfuel 		maximum amount of fuel to be held at one time
		fuel 			current amount of fuel
		maxspeed 		maximum amount of speed in either direction at any time

		bulletImage 	image used for bullets fired by "this ship"
		imageOrigin 	original unrotated image of the ship
		image 			transformed version of imageOrigin that is blitted to the screen
		rect 			rectangle defining the spaceship, used for rotating the image

		rotationRate	how much to rotate the ship per frame when rotating
		angle			current angle of the ship

		pos				vector for position
		vel 			vector for velocity
		dir 			vector for direction

		lastBulletTime 	time passed at time of last bullet fired
		currentTime 	time passed til now

		hitbox 			rect used for collision

		Booleans:
			-To determine whether or not their respective methods should be called
		shooting
		rotatingLeft
		rotatingRight
		thrusting
		"""
		pygame.sprite.Sprite.__init__(self)


		self.x = x
		self.y = y
		self.lives = config.lives
		self.health = config.health
		self.maxfuel = config.maxfuel
		self.fuel = self.maxfuel
		self.maxspeed = config.maxspeed

		self.bulletImage = bulletImage
		self.imageOrigin = image
		self.image = self.imageOrigin
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y

		self.width = self.image.get_rect().width
		self.height = self.image.get_rect().height

		self.shooting = False
		self.rotatingLeft = False
		self.rotatingRight = False
		self.thrusting = False

		self.rotationRate = config.rotationRate
		self.angle = 0

		self.pos = precode.Vector2D(x,y)
		self.vel = precode.Vector2D(0,0)
		self.dir = precode.Vector2D(0,-1)

		self.lastBulletTime = 0
		self.currentTime = 0

		self.hitbox = pygame.Rect(self.pos.x,self.pos.y,self.width,self.height)


	def draw(self):
		"""
		Draw the spaceship.
		"""
		game.screen.blit(self.image,(self.pos.x,self.pos.y))

	def reset(self):
		"""
		Completely reset a ship
		"""
		self.respawn()
		self.lives = 5


	def rotateLeft(self):
		"""
		Rotate left by rotationRate degrees
		"""
		if not self.rotatingLeft:
			return
		self.angle += self.rotationRate
		if self.angle > 360:
			self.angle = self.rotationRate

		self.dir.x = -math.sin(math.radians(self.angle))
		self.dir.y = -math.cos(math.radians(self.angle))

	def rotateRight(self):
		"""
		Rotate right by rotationRate degrees
		"""
		if not self.rotatingRight:
			return
		self.angle -= self.rotationRate
		if self.angle < 0:
			self.angle = 360 - self.rotationRate

		self.dir.x = -math.sin(math.radians(self.angle))
		self.dir.y = -math.cos(math.radians(self.angle))

	def update(self):
		"""
		Rotate the spaceships original image rather than the current one,
		while keeping the original image as it is and at the correct position

		Move the ship according to speed

		Enforce speed limit

		Die and respawn if health is below 1

		update hitbox

		Determine winner if out of lives
		"""
		oldCenter = self.rect.center
		self.image = pygame.transform.rotate(self.imageOrigin, self.angle)
		self.rect = self.image.get_rect()
		self.rect.x = self.x
		self.rect.y = self.y
		self.rect.center = oldCenter

		self.pos = self.pos + self.vel

		if(abs(self.vel.x) > self.maxspeed):
			if self.vel.x > 0:
				self.vel.x = self.maxspeed
			else:
				self.vel.x = -self.maxspeed
		if(abs(self.vel.y) > self.maxspeed):
			if self.vel.y > 0:
				self.vel.y = self.maxspeed
			else:
				self.vel.y = -self.maxspeed

		if self.health <1:
			self.respawn()

		self.hitbox = pygame.Rect(self.pos.x,self.pos.y,self.width,self.height)

		if self.lives < 1:
			if self == game.player1:
				game.winner = "Player2"
			else:
				game.winner = "Player1"

			game.gamestate = 3


	def thrust(self):
		"""
		Thrust if thrusting, lose fuel
		"""
		if self.thrusting == True:
			if self.fuel >0:
				self.vel.x = self.vel.x + self.dir.x*2
				self.vel.y = self.vel.y + self.dir.y*2
				self.fuel -= 1


	def shoot(self):
		"""
		shoot if shooting, but only once each fifth of a second
		"""
		if self.shooting == True:
			self.currentTime = pygame.time.get_ticks()
			if self.currentTime - self.lastBulletTime > 200:
				game.bullets.append(Bullet(self))
				self.lastBulletTime = pygame.time.get_ticks()

	def collideObjects(self):
		"""
		Check for collision between different objects and behave accordingly.

		Floor 						-dont go further down, die if out of fuel
		leftWall 					-Die
		rightWall 					-Die
		ceiling 					-Dont go further up
		movingBlock  / asteroid 	-Die
		fuelcan						-refuel
		"""
		collides = self.hitbox.colliderect(game.platform.hitbox)
		if collides == True:
			if self.fuel < 1:
				self.respawn()
			else:
				self.pos.y = game.platform.rect.y - self.height
				self.vel.x*= 0.9
		collides = self.hitbox.colliderect(game.leftWall.hitbox)
		if collides == True:
			self.respawn()
		collides = self.hitbox.colliderect(game.rightWall.hitbox)
		if collides == True:
			self.respawn()
		collides = self.hitbox.colliderect(game.ceiling.hitbox)
		if collides == True:
			self.pos.y = game.ceiling.y + game.ceiling.image.get_rect().height
		collides = self.hitbox.colliderect(game.movingBlock.hitbox)
		if collides == True:
			self.respawn()
		collides = self.hitbox.colliderect(game.fueltank.hitbox)
		if collides == True:
			self.fuel = self.maxfuel

	def respawn(self):
		"""
		Reset spaceship variables but lose one life.
		"""
		self.lives -= 1

		self.maxfuel = 200
		self.fuel = self.maxfuel
		self.health = 100
		self.vel.x = 0
		self.vel.y = 0
		self.angle = 0
		self.dir.x = -math.sin(math.radians(self.angle))
		self.dir.y = -math.cos(math.radians(self.angle))

		if self == game.player1:
			self.pos.x = 150
			self.pos.y = 450
		else:
			self.pos.x = config.SCREEN_SIZE[0] - 150
			self.pos.y = 450


	def collideBullets(self):
		"""
		Check if the spaceship collides with any bullets.
		If enemy bullets, lose health, otherwise don't.
		"""
		for bullet in game.bullets:
			if self.hitbox.colliderect(bullet.hitbox):
				if bullet.player == self:
					return
				else:
					self.health -= bullet.damage
					game.bullets.remove(bullet)

	def collideShips(self):
		"""
		Check if ships collide, if so, both die and respawn.
		"""
		if self == game.player1:
			if self.hitbox.colliderect(game.player2.hitbox):
				game.player1.respawn()
				game.player2.respawn()
		else:
			if self.hitbox.colliderect(game.player1.hitbox):
				game.player1.respawn()
				game.player2.respawn()





class Bullet(pygame.sprite.Sprite):
	"""
	Implement simple bullets that move in a straight line and are not affected by gravity.
	"""
	def __init__(self, player):
		"""
		Variables:

		damage 				health it takes from players
		image 				what to draw the bullet as
		player 				the player that shot the bullet
		dir 				direction vector bullet moves in
		vel 				speed vector of bullet
		pos 				position vector for bullet
		hitbox 				rect used for collision
		"""
		pygame.sprite.Sprite.__init__(self)

		self.damage = config.damage
		self.image = player.bulletImage
		self.player = player
		self.dir = precode.Vector2D(player.dir.x,player.dir.y)
		self.vel = precode.Vector2D(self.dir.x*15,self.dir.y*15)
		self.pos = precode.Vector2D(player.pos.x,player.pos.y)

		self.hitbox = pygame.Rect(self.pos.x,self.pos.y,self.image.get_rect().width,self.image.get_rect().height)

	def update(self):
		"""
		Draw bullet
		Move bullet
		update bullets hitbox
		remove bullet if out of screen
		"""
		game.screen.blit(self.image,(self.pos.x,self.pos.y))
		self.pos += self.vel

		self.hitbox = pygame.Rect(self.pos.x,self.pos.y,self.image.get_rect().width,self.image.get_rect().height)

		if self.pos.x > config.SCREEN_SIZE[0]:
			game.bullets.remove(self)
		elif self.pos.x < 0:
			game.bullets.remove(self)
		elif self.pos.y < 0:
			game.bullets.remove(self)
		elif self.pos.y > config.SCREEN_SIZE[1]:
			game.bullets.remove(self)

class Environment(pygame.sprite.Sprite):
	"""
	Implement a class for environments, such as walls, floor, ceiling, blocks.
	"""
	def __init__(self,x,y,image):
		"""
		Variables:

		image 			what to draw
		rect 			rect of image
		hitbox 			rect used for collision
		"""
		pygame.sprite.Sprite.__init__(self)

		self.image = image
		self.x = x
		self.y = y
		self.rect = self.image.get_rect()
		self.width = self.image.get_rect().width
		self.height = self.image.get_rect().height
		self.rect.x = self.x
		self.rect.y = self.y

		self.hitbox = pygame.Rect(self.x,self.y,self.width,self.height)


	def draw(self):
		"""
		Draw itself
		"""
		game.screen.blit(self.image,(self.x,self.y))

class Fueltank(Environment):
	"""
	Implement a fuel can spaceships can use to refuel
	"""
	def __init__(self,x,y,image):
		Environment.__init__(self,x,y,image)


class MovingObstacle(pygame.sprite.Sprite):
	"""
	Implement a moving obstacle, the asteroid.
	Player dies if it collides with it.
	"""
	def __init__(self,minx,maxx,y,speed,image):
		"""
		Variables:

		image 			what to draw
		minx 			as far left as the asteroid goes
		maxx 			as far right as the asteroid goes
		speed			how fast it goes left and right
		hitbox 			rect used for collision
		"""
		pygame.sprite.Sprite.__init__(self)

		self.image = image

		self.minx = minx
		self.maxx = maxx

		self.x = self.minx
		self.y = y

		self.speed = speed

		self.hitbox = pygame.Rect(self.x,self.y,self.image.get_rect().width,self.image.get_rect().height)

	def move(self):
		"""
		Move left or right, turn if at endpoint, dont go out of bounds.
		Update hitbox.
		"""
		self.x += self.speed
		if self.x > self.maxx:
			self.x = self.maxx
			self.speed = -self.speed
		elif self.x < self.minx:
			self.x = self.minx
			self.speed = -self.speed

		self.hitbox = pygame.Rect(self.x,self.y,self.image.get_rect().width,self.image.get_rect().height)

	def draw(self):
		"""
		Draw itself on screen.
		"""
		game.screen.blit(self.image,(self.x,self.y))
		


if __name__ == '__main__':
	game = Game()
	game.mainLoop()