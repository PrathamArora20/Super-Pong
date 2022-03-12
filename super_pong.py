# This program is written to execute and replicate the pong game. Pong game is a 2-player game where there are 2 peddles and 1 ball. The 2 players
# control each paddle and try their best to block the ball from hitting their side by blocking it with paddles. If the ball hits the side of 
# one player , the other player gets one point. First player to 11 wins the game. The player 1 can control his/her paddle by the buttons 
# 'q' and 'a' where q is to put the paddle up and a to put it down. Player 2 can control his/her paddle by the buttons 'p' and 'l'
# where p is to put the paddle up and l to put it down


import pygame
import math 
from time import time, sleep
import random

# User-defined functions

def main():
    # initialize all pygame modules (some need initialization)
    pygame.init()
    # create a pygame display window
    pygame.display.set_mode((600, 500))
    # set the title of the display window
    pygame.display.set_caption('Pong')   
    # get the display surface
    w_surface = pygame.display.get_surface() 
    # create a game object
    game = Game(w_surface)
    # start the main game loop by calling the play method on the game object
    game.play() 
    # quit pygame and clean up the pygame window
    pygame.quit() 


# User-defined classes

class Game:
    # An object in this class represents a complete game.

    def __init__(self, surface):
        # Initialize a Game.
        # - self is the Game to initialize
        # - surface is the display window surface object

        # === objects that are part of every game that we will discuss
        self.surface = surface
        self.bg_color = pygame.Color('black')

        self.FPS = 60  
        self.game_Clock = pygame.time.Clock()
        self.close_clicked = False
        self.continue_game=True

        # === game specific objects
        self.game_ball = Ball('white', 5, [300, 250], [5, 3], self.surface)
        x1=random.randint(150,400)
        y1=random.randint(50,400)
        self.powerup1=Ball('red',15,[x1,y1],[0,0],self.surface)        
        x2=random.randint(150,400)
        y2=random.randint(50,400)  
        self.powerup2=Ball('green',15,[x2,y2],[0,0],self.surface)
        x3=random.randint(150,400)
        y3=random.randint(50,400)    
        self.powerup3=Ball('blue',15,[x3,y3],[0,0],self.surface)
        x4=random.randint(150,400)
        y4=random.randint(50,400)    
        self.powerup4=Ball('yellow',15,[x4,y4],[0,0],self.surface)    
        
        #self.list_power[1,2,3,4]
        
        self.paddle = Paddle(80,250,10,60,'white',self.surface)
        self.paddle2 = Paddle(520,250,10,60,'white',self.surface)
        self.player1=0
        self.player2=0

    def play(self):
        # Play the game until the player presses the close box.
        # - self is the Game that should be continued or not.

        while not self.close_clicked:  # until player clicks close box
            # play frame
            self.handle_events()
            self.draw()            
            if self.continue_game:  # Checks if conditions are met to continue game(no player reached 11 points)
                self.update()
                self.game_win()  # Checks if any player won 
            self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

    def handle_events(self):
        # Handle each user event by changing the game state appropriately.
        # - self is the Game whose events will be handled

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.close_clicked = True
            elif event.type == pygame.KEYDOWN:  # When user presses down a key
                self.handle_key_down(event)
            elif event.type == pygame.KEYUP:  # When user releases the pressed down key 
                self.handle_key_up(event) 
    

    # This function dictated what happens when the player presses down a certian key. When a player presses a certain key 
    # their paddle moves at a certain velocity either up or down
    def handle_key_down(self,event):
        paddle_velocity=5
        if event.key == pygame.K_a:  # When a is pressed the paddle of player 1 moves down
            self.paddle.set_velocity(paddle_velocity)
        if event.key == pygame.K_q:  # When q is pressed the paddle of player 1 moves up
            self.paddle.set_velocity(-paddle_velocity) 
        if event.key == pygame.K_l:  # When l is pressed the paddle of player 2 moves down
            self.paddle2.set_velocity(paddle_velocity)
        if event.key == pygame.K_p:  # When p is pressed the paddle of player 2 moves up
            self.paddle2.set_velocity(-paddle_velocity)      

    # This function dictated what happens when the player releases a certian key. When a player releases a certain key 
    # their paddle stops moving
    def handle_key_up(self,event):
        stop_velocity=0
        if event.key == pygame.K_a:  # When a is releases the paddle of player 1 stops
            self.paddle.set_velocity(stop_velocity) 
        if event.key == pygame.K_q:  # When q is releases the paddle of player 1 stops
            self.paddle.set_velocity(stop_velocity) 
        if event.key == pygame.K_l:  # When l is releases the paddle of player 2 stops
            self.paddle2.set_velocity(stop_velocity)
        if event.key == pygame.K_p:  # When p is releases the paddle of player 2 stops
            self.paddle2.set_velocity(stop_velocity)     

    def draw(self):
        # Draw all game objects.
        # - self is the Game to draw

        self.surface.fill(self.bg_color) # clear the display surface first
        self.game_ball.draw()  # Draws the game ball
        if ((self.player1+self.player2)>2):
            self.powerup1.draw()   # Draws the power up
            if(self.powerup1.get_radius!=0):
                self.powerup_collison1()            
        
        if ((self.player1+self.player2)>5):
            self.powerup2.draw()   # Draws the power up
            if(self.powerup2.get_radius!=0):
                self.powerup_collison2()            
       
        if ((self.player1+self.player2)>8):
            self.powerup3.draw()   # Draws the power up
            if(self.powerup3.get_radius!=0):
                self.powerup_collison3()              
       
        if ((self.player1+self.player2)>9):
            self.powerup4.draw()   # Draws the power up
            if(self.powerup4.get_radius!=0):
                self.powerup_collison4()            
                      
        
        self.paddle.draw()  # Draws the paddle of player 1
        self.paddle2.draw()  # Draws the paddle of player 2
        self.score_print()  # Draws the scoreboard 
        pygame.display.update() # make the updated surface appear on the display
        

    def update(self):
        # Update the game objects for the next frame.
        # - self is the Game to update

        self.game_ball.move()  # Makes the ball move
        
        
        
        self.check_paddle_collision()  # Checks if the ball colides with the paddle
        self.count_score()  # Counts the score of each player
        self.paddle.move()   # Moves paddle of player 1
        self.paddle2.move()  # Moves paddle of player 1
        

    # This function counts the score of each player
    def count_score(self):
        size = self.surface.get_size()
        center_x = self.game_ball.get_center()  # Gets the center of the ball
        radius= self.game_ball.get_radius()  # Gets the radius of the ball
        
        if center_x[0] <= radius :  # Checks if the ball hits the left side of the screen 
            self.player1=self.player1+1  # If above condition is true then , adds 1 point againts player 1
            
        if center_x[0] + radius >= size[0] :  # Checks if the ball hits the right side of the screen 
            self.player2=self.player2+1  # If above condition is true then , adds 1 point againts player 2
   
    
    # This function checks if the ball colides with the paddles or not. If the ball collides with the paddles then the velocity of the 
    # ball is reversed.
    def check_paddle_collision(self):
        
        velocity=self.game_ball.get_velocity()  # Gets the velocity of the ball
        if self.paddle.collison_check(self.game_ball.center) == True :  # Checks if the ball colides with paddle 1
            if velocity[0]<0:  # Checks if the ball is moving from right to left (Avoids balls from bouncing from behind paddle)
                self.game_ball.set_velocity()  # Reverses velocity of ball
            
        if self.paddle2.collison_check(self.game_ball.center)==True:  # Checks if the ball colides with paddle 2
            if velocity[0]>0:  # Checks if the ball is moving from left to right (Avoids balls from bouncing from behind paddle)
                self.game_ball.set_velocity()  # Reverses velocity of ball   
                
    def powerup_collison1(self):
        
        distance=0
        temp=0
        powerup_r=self.powerup1.get_center()
        game_r=self.game_ball.get_center()
        a=(pow((powerup_r[0]-game_r[0]),2))
        b=(pow((powerup_r[1]-game_r[1]),2))
        temp=abs(a+b)
        
        distance= math.sqrt(temp)
        
        total_r=(self.game_ball.get_radius())+(self.powerup1.get_radius())
        
        if (self.powerup1.get_radius() != 0):
            if distance<(total_r):
                self.game_ball.dec_velocity()
                self.powerup1.set_radius(0)
                
    def powerup_collison2(self):
        
        distance=0
        temp=0
        powerup_r=self.powerup2.get_center()
        game_r=self.game_ball.get_center()
        a=(pow((powerup_r[0]-game_r[0]),2))
        b=(pow((powerup_r[1]-game_r[1]),2))
        temp=abs(a+b)
        
        distance= math.sqrt(temp)
        
        total_r=(self.game_ball.get_radius())+(self.powerup2.get_radius())
        
        if (self.powerup2.get_radius() != 0):
            if distance<(total_r):
                self.game_ball.inc_velocity()
                self.powerup2.set_radius(0)        
        
    def powerup_collison3(self):

        distance=0
        temp=0
        powerup_r=self.powerup3.get_center()
        game_r=self.game_ball.get_center()
        a=(pow((powerup_r[0]-game_r[0]),2))
        b=(pow((powerup_r[1]-game_r[1]),2))
        temp=abs(a+b)

        distance= math.sqrt(temp)

        total_r=(self.game_ball.get_radius())+(self.powerup3.get_radius())

        if (self.powerup3.get_radius() != 0):
            if distance<(total_r):
                self.game_ball.inc_size()
                self.powerup3.set_radius(0)  
                
    def powerup_collison4(self):

        distance=0
        temp=0
        powerup_r=self.powerup4.get_center()
        game_r=self.game_ball.get_center()
        a=(pow((powerup_r[0]-game_r[0]),2))
        b=(pow((powerup_r[1]-game_r[1]),2))
        temp=abs(a+b)

        distance= math.sqrt(temp)

        total_r=(self.game_ball.get_radius())+(self.powerup4.get_radius())

        if (self.powerup4.get_radius() != 0):
            if distance<(total_r):
                self.game_ball.dec_size()
                self.powerup4.set_radius(0)        
    
                      

    # This function prints the scores of player 1 and player 2 on the screen 
    def score_print(self):
        string1 = str(self.player2)
        string2= str(self.player1)
        font_size = 100
        fg_color = pygame.Color('white')
        bg_color = pygame.Color('black')
        font = pygame.font.SysFont('ariel',font_size)  # Create a font object
        text_box1 = font.render(string1,True,fg_color,bg_color)  # render the font object
        text_box2 = font.render(string2,True,fg_color,bg_color) 
        # self.surface is of type pygame.Surface
        # text_box is of type pygame.Surface
        w1 = self.surface.get_width()
        w2 = text_box2.get_width()
        location1 = (0,0)  # determine the location of the text_box
        location2=(w1-w2,0)
        self.surface.blit(text_box1,location1)  # blit or pin the text_box on the surface
        self.surface.blit(text_box2,location2)    

    # This function checks if one of the players have won or not if they have reached 11 points
    def game_win(self):

        if self.player1==11 or self.player2==11:
            self.continue_game=False

        

class Ball:
    # An object in this class represents a ba;; that moves 

    def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
        # Initialize a Ball.
        # - self is the Ball to initialize
        # - color is the pygame.Color of the ball
        # - center is a list containing the x and y int
        #   coords of the center of the ball
        # - radius is the int pixel radius of the ball
        # - velocity is a list containing the x and y components
        # - surface is the window's pygame.Surface object

        self.color = pygame.Color(ball_color)
        self.radius = ball_radius
        self.center = ball_center
        self.velocity = ball_velocity
        self.surface = surface
        
        
        

    def move(self):
        # Change the location of the ball by adding the corresponding 
        # speed values to the x and y coordinate of its center
        # - self is the ball
        size = self.surface.get_size()
        for i in range(0,2):
            self.center[i] = (self.center[i] + self.velocity[i])

            if self.center[i] <= self.radius :  # Hits the left side of the screen 
                self.velocity[i] = -self.velocity[i] 

            if self.center[i] + self.radius >= size[i]:  # Hits the right side of the screen
                self.velocity[i] = -self.velocity[i]


    def draw(self):
        # Draw the ball on the surface
        # - self is the ball

        pygame.draw.circle(self.surface, self.color, self.center, self.radius)
 
    # This function returns the center of the game ball    
    def get_center(self):
        return self.center
    
    # This function returns the radius of the game ball
    def get_radius(self):
        return self.radius
    
    def set_radius(self,size):
        self.radius=size
    
    # This function returns the velocity of the game ball
    def get_velocity(self):
        return self.velocity

    # This function sets the velocity reverse as the velocity reverses after the collision 
    def set_velocity(self):
        self.velocity[0]=-(self.velocity[0])
        
    def inc_velocity(self):
        self.velocity[0]=1.25*(self.velocity[0])
        
    def dec_velocity(self):
        self.velocity[0]=0.5*(self.velocity[0])
        
    def inc_size(self):
        self.radius=self.radius+3
        
    def dec_size(self):
        self.radius=self.radius-3

        


class Paddle:
    # An object in this class represents a Paddle that moves

    # This function initializes the paddle rectangle. Initializes the coordinates , the width and height and the color of the rectangle
    # along with the velocity of the paddle 
    def __init__(self,x,y,width,height,color,surface):
        self.rect = pygame.Rect(x,y,width,height)
        self.color = pygame.Color(color)
        self.surface = surface
        self.v_velocity = 0


    # This function draws the paddle on the screen 
    def draw(self):
        pygame.draw.rect(self.surface,self.color,self.rect)


    #This function takes the distance we want the paddle to move and sets the velocity it the distance 
    def set_velocity(self,v_distance):
        self.v_velocity = v_distance  # v_distance is the distance we want the paddle to move


    # This function moves the paddles.
    def move(self):
        self.rect.move_ip(0,self.v_velocity)  # moves the rectangle in place
        if self.rect.bottom >= self.surface.get_height():  # Checks if the bottom of the paddle leaves the screen by going too down 
            self.rect.bottom = self.surface.get_height()  # Sets the bottom of the paddle to bottom of screen if above conidition is true 
        if self.rect.top <= 0:  # Checks if the top of the paddle leaves the screen by going too up
            self.rect.top = 0  # Sets the top of the paddle to top of screen if above conidition is true 
    
    
    # This function checks if the ball collides with the paddle or not by checking if the center of the ball collides/ is inside the paddle or not
    # If it is true , the collision_check is true
    def collison_check(self,ball_point):
        self.rect.collidepoint(ball_point)
        
        return self.rect.collidepoint(ball_point)
    
    


main()
