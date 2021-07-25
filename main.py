# Imports everything from both model and graphics
from random import choice
from gamemodel import *
from gamegraphics import *


# Here is a nice little method you get for free
# It fires a shot for the current player and animates it until it stops
def graphicFire(game, graphics, angle, vel):
    player = game.getCurrentPlayer()
    # create a shot and track until it hits ground or leaves window
    proj = player.fire(angle, vel)
    while proj.isMoving():
        proj.update(1/50)
        graphics.sync() # This deals with all graphics-related issues
        update(50) # Waits for a short amount of time before the next iteration
    return proj

def graphicPlay():
    game = Game(10,3)
    graphics = GameGraphics(game)

    while True:
        choice = graphics.dialog.interact()
        if choice == "Fire!":
            #get angle and velocity from input
            angle, vel = graphicInput(graphics)
            proj = graphicFire(game, graphics, angle, vel)
            finishShot(game, graphics, proj)
        
        if choice == "Quit":
            break

def graphicInput(graphics):
    newAngle, newVel = graphics.dialog.getValues()
    return newAngle, newVel

def finishShot(game, graphics, proj):
    # The current player
    player = game.getCurrentPlayer()
    # The player opposing the current player
    other = game.getOtherPlayer()

    # Check if we won
    distance = other.projectileDistance(proj) 
    if distance == 0:
        player.increaseScore()
        
        # Start a new round
        game.newRound()
        graphics.sync()

    # Switch active player
    game.nextPlayer()


# Run the game with graphical interface
graphicPlay()
