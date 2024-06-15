import pygame
from pygame import Vector2
import sys
import time

class PLAYER():
	def __init__(self, x, width, length):
		self.color = (255, 255, 255)
		self.width = width
		self.length = length
		self.x = x
		self.y = RESOLUTION[1] / 2 - self.length / 2
		self.pos = Vector2(self.x, self.y)
		self.speed = 7
	def draw_player(self):
		self.player_rect = pygame.Rect(self.pos.x, self.pos.y, self.width, self.length)
		pygame.draw.rect(screen, self.color, self.player_rect)

class BALL():
	def __init__(self):
		self.size = 20
		self.x = 50
		self.y = RESOLUTION[1] / 2 - self.size/2
		self.color = (204, 204, 88)
		self.pos = Vector2(self.x, self.y)
		self.dir = Vector2(7, 7)

	def draw_ball(self):
		self.ball_rect = pygame.Rect(self.pos.x, self.pos.y, self.size, self.size)
		pygame.draw.ellipse(screen, self.color, self.ball_rect)

	def move_ball(self):
		self.pos.x += self.dir.x
		self.pos.y += self.dir.y


pygame.init()

RESOLUTION = (800, 600)

screen = pygame.display.set_mode(RESOLUTION)
pygame.display.set_caption("Pong")


width = 15
length = 100 

player_1 = PLAYER(30, width, length)
player_2 = PLAYER(RESOLUTION[0] - 30 - width, width, length)

def setup():
	#setup
	global player_1, player_2, ball, clock, winner, game_over_font, font, running
	player_1.pos = Vector2(30, RESOLUTION[1] / 2 - length / 2)
	player_2.pos = Vector2(RESOLUTION[0] - 30 - width, RESOLUTION[1] / 2 - length / 2)
	ball = BALL()
	clock = pygame.time.Clock()
	winner = ""
	game_over_font = pygame.font.Font('/System/Library/Fonts/Supplemental/Verdana Bold.ttf', 40)
	font = pygame.font.Font('/System/Library/Fonts/Supplemental/Verdana Bold.ttf', 20)
	

def game():
	global length, width, restart_btn_color, exit_btn_color
	running = True
	while running:
		screen.fill((0, 0, 0))
		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				running = False
				pygame.quit()
				sys.exit()


		#draw
		player_1.draw_player()
		player_2.draw_player()
		ball.draw_ball()

		#move the ball
		ball.move_ball()



		#check wall collision
		if(ball.pos.x + ball.size <= 0):
			winner = "Player 2"
			running = False
		elif(ball.pos.x >= RESOLUTION[0]):
			winner = "Player 1"
			running = False
		if(ball.pos.y <= 0 or ball.pos.y >= RESOLUTION[1] - ball.size):
			ball.dir.y *= -1

		
		#check collision
		player_1_collide = pygame.Rect.colliderect(player_1.player_rect, ball.ball_rect)
		player_2_collide = pygame.Rect.colliderect(player_2.player_rect, ball.ball_rect)

		if(player_1_collide):
			ball.dir.x *= -1
			ball.pos.x = player_1.pos.x + width + 1
		elif(player_2_collide):
			ball.dir.x *= -1
			ball.pos.x = player_2.pos.x - 1 - ball.size

		
		keys = pygame.key.get_pressed()
		if(keys[pygame.K_UP] and player_2.pos.y >= 0):
			player_2.pos.y -= player_2.speed
		elif(keys[pygame.K_DOWN] and player_2.pos.y + length <= RESOLUTION[1]):
			player_2.pos.y += player_2.speed
		if(keys[pygame.K_w] and player_1.pos.y >= 0):
			player_1.pos.y -= player_1.speed
		elif(keys[pygame.K_s] and player_1.pos.y + length <= RESOLUTION[1]):
			player_1.pos.y += player_1.speed

		#draw halfline
		pygame.draw.line(screen, (150, 151, 153), (RESOLUTION[0] / 2, 0), (RESOLUTION[0] / 2, RESOLUTION[1]), 1)

		

		pygame.display.update()
		clock.tick(60)

	#end screen logic
	end_running = True
	while end_running:
		#length and width for both buttons
		length = 120
		width = 40
		
		#restart button information
		restart_rect_x = (RESOLUTION[0]) / 2
		restart_rect_y = 300
		x_min_restart = restart_rect_x - length / 2
		x_max_restart = restart_rect_x + length / 2
		y_min_restart = restart_rect_y - width / 2
		y_max_restart = restart_rect_y + width / 2
		

		#exit button information
		exit_rect_x = (RESOLUTION[0]) / 2
		exit_rect_y = 350
		x_min_exit = exit_rect_x - length / 2
		x_max_exit = exit_rect_x + length / 2
		y_min_exit = exit_rect_y - width / 2
		y_max_exit = exit_rect_y + width / 2

		mouse = pygame.mouse.get_pos() 

		for event in pygame.event.get():
			if(event.type == pygame.QUIT):
				end_running = False
				pygame.quit()
				sys.exit()
			if(event.type == pygame.MOUSEBUTTONDOWN):
				clicked = True
				if(x_min_restart <= mouse[0] <=  x_max_restart and y_min_restart <= mouse[1] <= y_max_restart):
					restart_btn_color = (0, 120, 20)
				if(x_min_exit <= mouse[0] <=  x_max_exit and y_min_exit <= mouse[1] <= y_max_exit):
					exit_btn_color = (0, 70, 70)
			if(event.type == pygame.MOUSEBUTTONUP and clicked == True):
				clicked = False
				if(x_min_restart <= mouse[0] <=  x_max_restart and y_min_restart <= mouse[1] <= y_max_restart):
					restart_btn_color = (0, 150, 50)
					setup()
					game()
				if(x_min_exit <= mouse[0] <=  x_max_exit and y_min_exit <= mouse[1] <= y_max_exit):
					exit_btn_color = (0, 100, 100)
					pygame.quit()
					sys.exit()
		screen.fill((0, 0, 0))
		winner_text = game_over_font.render(winner + " wins.", True, (255, 255, 255))
		winner_rect = winner_text.get_rect(center = ((RESOLUTION[0] / 2, 50)))
		screen.blit(winner_text, winner_rect)
		if(x_min_restart <= mouse[0] <=  x_max_restart and y_min_restart <= mouse[1] <= y_max_restart):
			restart_btn_color = (0, 135, 35)
		elif(x_min_exit <= mouse[0] <=  x_max_exit and y_min_exit <= mouse[1] <= y_max_exit):
			exit_btn_color = (0, 85, 85)
		else:
			restart_btn_color = (0, 150, 50)
			exit_btn_color = (0, 70, 70)
		#Restart button
		restart = "RESTART"
		restart_text = font.render(restart, True, (255, 255, 255))
		
		restart_rect = restart_text.get_rect(center = (restart_rect_x, restart_rect_y))
		
		restart_rect_rectangle = pygame.Rect(restart_rect_x - length / 2, restart_rect_y - width / 2, length, width)
		pygame.draw.rect(screen, restart_btn_color, restart_rect_rectangle)
		screen.blit(restart_text, restart_rect)

		#Exit button
		exit = "EXIT"
		exit_text = font.render(exit, True, (255, 255, 255))
		
		exit_rect = exit_text.get_rect(center = (exit_rect_x, exit_rect_y))
		exit_rect_rectangle = pygame.Rect(exit_rect_x - length / 2, exit_rect_y - width / 2, length, width)
		pygame.draw.rect(screen, exit_btn_color, exit_rect_rectangle)
		screen.blit(exit_text, exit_rect)
		pygame.display.update()

setup()
game()

pygame.quit()
sys.exit()