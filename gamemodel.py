from math import dist, sin,cos,radians,copysign
import random

""" This is the model of the game"""
class Game:
    def __init__(self, cannonSize, ballSize):
        p1 = Player(self, "blue", -90)
        p2 = Player(self, "red", 90)
        self.players = [p1, p2]
        self.cannonSize = cannonSize
        self.ballSize = ballSize
        self.wind = 0
        self.currentPlayerIndex = 0

    """ A list containing both players """
    def getPlayers(self):
        return self.players 

    """ The current player, i.e. the player whose turn it is """
    def getCurrentPlayer(self):
        return self.players[self.currentPlayerIndex]

    """ The opponent of the current player """
    def getOtherPlayer(self):
        if self.currentPlayerIndex == 0:
            return self.players[1]
        else:
            return self.players[0]

    """ The number (0 or 1) of the current player. This should be the position of the current player in getPlayers(). """
    def getCurrentPlayerNumber(self):
        return self.currentPlayerIndex

    """ The height/width of the cannon """
    def getCannonSize(self):
        return self.cannonSize

    """ The radius of cannon balls """
    def getBallSize(self):
        return self.ballSize

    """ Set the current wind speed, only used for testing """
    def setCurrentWind(self, wind):
        self.wind = wind

    """ Get the current wind speed """
    def getCurrentWind(self):
        return self.wind

    """ Switch active player """
    def nextPlayer(self):
        if self.currentPlayerIndex == 0:
            self.currentPlayerIndex = 1
        else:
            self.currentPlayerIndex = 0
        
    """ Start a new round with a random wind value (-10 to +10) """
    def newRound(self):
        self.wind = random.random()*20-10


""" Models a player """
class Player:
    def __init__(self, game, color, position):
        self.color = color
        self.X = position
        self.score = 0
        self.game = game
        self.proj = None
        self.projAim = 45, 40

    """ Create and return a projectile starting at the centre of this players cannon. Replaces any previous projectile for this player. """
    def fire(self, angle, velocity):
        
        #when shooting to left (opposite direction)
        if self.getX() > 0:
            angle = 180-angle
        
        self.projAim = angle, velocity
        wind = self.game.getCurrentWind()
        xPos = self.X
        yPos = self.game.getCannonSize()/2
        xLower = -110
        xUpper = 110
        proj = Projectile(angle, velocity, wind, xPos, yPos, xLower, xUpper)
        self.proj = proj
        return proj

    """ Returns the current projectile of this player if there is one, otherwise None """
    def getProjectile(self):
        return self.proj

    """ Gives the x-distance from this players cannon to a projectile. If the cannon and the projectile touch 
    (assuming the projectile is on the ground and factoring in both cannon and projectile size) this method should return 0"""
    def projectileDistance(self, proj):
        ballX = proj.getX()
        cannonX = self.getX()
        # ballRadius = self.game.getBallSize()/2
        ballSize = self.game.getBallSize() 
        cannonRadius = self.game.getCannonSize() /2

        #the cannon range 
        min_cannonX = cannonX - cannonRadius
        max_cannonX = cannonX + cannonRadius
        
        #ball range
        minBallX = ballX - ballSize
        maxBallX = ballX + ballSize

        #ball to right side of cannon (positive value)
        if cannonX < ballX:
            distance = minBallX - max_cannonX
        
        #ball to left side of cannon (negative value)
        else:
            distance = maxBallX - min_cannonX
        
        #hit center of cannon
        if min_cannonX <= ballX <= max_cannonX:
            distance = 0

        #hit side of cannon 
        if minBallX <= max_cannonX <= maxBallX or minBallX <= min_cannonX <= maxBallX:
            distance = 0

        return distance

    """ The current score of this player """
    def getScore(self):
        return self.score

    """ Increase the score of this player by 1."""
    def increaseScore(self):
        self.score +=1

    """ Returns the color of this player (a string)"""
    def getColor(self):
        return self.color

    """ The x-position of the centre of this players cannon """
    def getX(self):
        return self.X

    """ The angle and velocity of the last projectile this player fired, initially (45, 40) """
    def getAim(self):
        return self.projAim



""" Models a projectile (a cannonball, but could be used more generally) """
class Projectile:
    """
        Constructor parameters:
        angle and velocity: the initial angle and velocity of the projectile 
            angle 0 means straight east (positive x-direction) and 90 straight up
        wind: The wind speed value affecting this projectile
        xPos and yPos: The initial position of this projectile
        xLower and xUpper: The lowest and highest x-positions allowed
    """
    def __init__(self, angle, velocity, wind, xPos, yPos, xLower, xUpper):
        self.yPos = yPos
        self.xPos = xPos
        self.xLower = xLower
        self.xUpper = xUpper
        theta = radians(angle)
        self.xvel = velocity*cos(theta)
        self.yvel = velocity*sin(theta)
        self.wind = wind

    """ 
        Advance time by a given number of seconds
        (typically, time is less than a second, 
         for large values the projectile may move erratically)
    """
    def update(self, time):
        # Compute new velocity based on acceleration from gravity/wind
        yvel1 = self.yvel - 9.8*time
        xvel1 = self.xvel + self.wind*time
        
        # Move based on the average velocity in the time period 
        self.xPos = self.xPos + time * (self.xvel + xvel1) / 2.0
        self.yPos = self.yPos + time * (self.yvel + yvel1) / 2.0
        
        # make sure yPos >= 0
        self.yPos = max(self.yPos, 0)
        
        # Make sure xLower <= xPos <= mUpper   
        self.xPos = max(self.xPos, self.xLower)
        self.xPos = min(self.xPos, self.xUpper)
        
        # Update velocities
        self.yvel = yvel1
        self.xvel = xvel1
        
    """ A projectile is moving as long as it has not hit the ground or moved outside the xLower and xUpper limits """
    def isMoving(self):
        return 0 < self.getY() and self.xLower < self.getX() < self.xUpper

    def getX(self):
        return self.xPos

    """ The current y-position (height) of the projectile". Should never be below 0. """
    def getY(self):
        return self.yPos
