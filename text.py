import pygame
import config
import mayhemfirst

guideText = config.font.render("Player 1 (left) use W to thrust, A and D to rotate and space to shoot.",1,config.white)
guideText2 = config.font.render("Player 2 (right) use UP to thrust, LEFT and RIGHT to rotate and RIGHT CTRL to shoot.",1,config.white)
guideText3 = config.font.render("You have each 5 lives, 100 health and infinite bullets.",1,config.white)
guideText4 = config.font.render("Thrusting costs fuel, refuel at the can. Watch out for walls and obstacles, ",1,config.white)
guideText5 = config.font.render("they are deadly! The floor is cushioned and will not kill you, unless you are out of fuel.",1,config.white)
guideText6 = config.font.render("Press F to start",1,config.white)