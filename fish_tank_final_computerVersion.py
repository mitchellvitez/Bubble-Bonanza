############################################################################
## Program: Fish Tank                                                     
##
## Programmers: John Groot, June Chew, Mitchell Vitez
##             
## Artists: Lauren Breeding, Drew Blazewicz
##
## Purpose: Create the Fish Tank game as outlined in resources folder     
##
##                                                                                                                                              
#  ERRORS:  Multiple.                                                             
##                                                                        
##                                                                        
##                                                                        
##                                                                        
##                                                                        
##                                                                        
############################################################################

from pandac.PandaModules import loadPrcFileData
from fish_tank_config import *
loadPrcFileData("", ORIGIN)
loadPrcFileData("", SIZE)
loadPrcFileData("", TITLE)

import collisions

import sys
import random

import direct.directbase.DirectStart                                     
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.task import Task
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.actor.Actor import Actor

# Imports for Cartoon Lighting
from panda3d.core import PandaNode,LightNode,TextNode
from panda3d.core import Filename, NodePath
from panda3d.core import PointLight, AmbientLight
from panda3d.core import LightRampAttrib, AuxBitplaneAttrib
from panda3d.core import CardMaker
from panda3d.core import Shader, Texture
from panda3d.core import Point3,Vec4,Vec3
from direct.task.Task import Task
from direct.actor.Actor import Actor
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.showbase.BufferViewer import BufferViewer
from direct.filter.CommonFilters import CommonFilters
from direct.particles.ParticleEffect import ParticleEffect
import random


from operator import itemgetter


class World(DirectObject):
    def __init__(self):
        #self.accept('escape', self.endGame())
        
        #Turns on Frame Rate meter
        base.setFrameRateMeter(True)
        # Background Music
        ## backgroundMusic=base.loader.loadSfx("fishTankbgLighter.mp3")
        ## backgroundMusic.setLoop(True)                                    
        ## backgroundMusic.play()
        self.gameStarted = 0
        # Allows Joystick, disable if not in Cave
        ## self.setJoysticks()
        self.startScreen = OnscreenImage(image = 'Textures/titleScreen.png', pos = (0, 1, -.3), scale=1.35)
        self.startScreen.setTransparency(TransparencyAttrib.MAlpha)
        self.leftScreen = OnscreenImage(image = 'Textures/leftScreen.png', pos = (-2.7, 1, -.3), scale=1.35)
        self.leftScreen.setTransparency(TransparencyAttrib.MAlpha)
        self.rightScreen = OnscreenImage(image = 'Textures/rightScreen.png', pos = (2.7, 1, -.3), scale=1.35)
        self.rightScreen.setTransparency(TransparencyAttrib.MAlpha)
        
        base.disableMouse()
        base.cam.node().getLens().setNear(10.0)
        base.cam.node().getLens().setFar(9999)
        ## base.camnode().getLens().set
        camera.setPos(0, -50, 0)
        
        #Creates Environment
        self.createEnvironment()
        
        # Creates Camera
        self.camHigh = base.camera.attachNewNode('camBase')  # control camera Z
        base.camera.setPos(0,0,2)
        self.right = base.camera.attachNewNode('right')
        self.right.setPos(.2, 0, 0)
        self.forward = base.camera.attachNewNode('forward')
        self.forward.setPos(0, .2, 0)
        
        # setup controls
        self.keys = {'w':False, 'a':False, 's':False, 'd':False, 'r':False, 'f':False, 'q':False, 'e':False, 't':False, 'g':False, 'space':False}
        self.accept('w', self.onKey, ['w', True])
        self.accept('a', self.onKey, ['a', True])
        self.accept('s', self.onKey, ['s', True])
        self.accept('d', self.onKey, ['d', True])
        self.accept('r', self.onKey, ['r', True])
        self.accept('f', self.onKey, ['f', True])
        self.accept('q', self.onKey, ['q', True])
        self.accept('e', self.onKey, ['e', True])
        self.accept('t', self.onKey, ['t', True])
        self.accept('g', self.onKey, ['g', True])
        self.accept('space', self.onKey, ['space', True])
        self.accept('w-up', self.onKey, ['w', False])
        self.accept('a-up', self.onKey, ['a', False])
        self.accept('s-up', self.onKey, ['s', False])
        self.accept('d-up', self.onKey, ['d', False])
        self.accept('r-up', self.onKey, ['r', False])
        self.accept('f-up', self.onKey, ['f', False])
        self.accept('q-up', self.onKey, ['q', False])
        self.accept('e-up', self.onKey, ['e', False])
        self.accept('t-up', self.onKey, ['t', False])
        self.accept('g-up', self.onKey, ['g', False])
        self.accept('space-up', self.onKey, ['space', False])
        taskMgr.add(self.controlTask, 'controlTask')
        
        #######################  Keyboard Controls #################################### 
    def startScreen1(self):
        self.startScreen = OnscreenImage(image = 'Textures/instructionScreen.png', pos = (0, 1, -.3), scale=1.35)
        self.startScreen.setTransparency(TransparencyAttrib.MAlpha)
        self.gameStarted = 1
        
    def onKey(self, key, pressed): 
        self.keys[key] = pressed
        
    def controlTask(self, task):
        
        if self.keys['w']: base.camera.setPos( base.camera.getPos() + (self.forward.getPos(render) - base.camera.getPos(render)) * 5 )
        if self.keys['a']: base.camera.setPos( base.camera.getPos() + (self.right.getPos(render) - base.camera.getPos(render)) * -5 )
        if self.keys['s']: base.camera.setPos( base.camera.getPos() + (self.forward.getPos(render) - base.camera.getPos(render)) * -5 )
        if self.keys['d']: base.camera.setPos( base.camera.getPos() + (self.right.getPos(render) - base.camera.getPos(render)) * 5 )
        if self.keys['r']: base.camera.setZ( base.camera.getZ() + 0.2 )    
        if self.keys['f']: base.camera.setZ( base.camera.getZ() - 0.2 ) 
        if self.keys['q']: base.camera.setH( base.camera.getH() + 1 )
        if self.keys['e']: base.camera.setH( base.camera.getH() - 1 )
        if self.keys['t']: base.camera.setP( base.camera.getP() + 1 )
        if self.keys['g']: base.camera.setP( base.camera.getP() - 1 )

        if self.keys['space']: self.bubbleEmitter()
        


        return Task.cont
##############################################################################        
       
    def startGame(self):
        self.startScreen.destroy()
        self.rightScreen.destroy()
        self.leftScreen.destroy()
        self.startTime()
        self.createUI()
        self.gameStarted = 2
        # setup collisions - 
        # create the traverser and handler 
        base.cTrav = CollisionTraverser()
        if SHOW_C: base.cTrav.showCollisions(render)                          
        self.CollisionHandler = CollisionHandlerEvent()
        self.CollisionHandler.addInPattern('HitAnything')
        self.CollisionHandler.addAgainPattern('HitAnything')
        #add the player collider/model collider to the traverser 
        base.cTrav.addCollider(self.playerC, self.CollisionHandler)
        ##base.cTrav.addCollider(self.fish1C, self.CollisionHandler)
        ## base.cTrav.addCollider(self.fish2C, self.CollisionHandler)
        ## base.cTrav.addCollider(self.fish3C, self.CollisionHandler)
        ## base.cTrav.addCollider(self.fish4C, self.CollisionHandler)
        ## base.cTrav.addCollider(self.fish5C, self.CollisionHandler)
        base.cTrav.addCollider(self.treasureChestC, self.CollisionHandler)
        
        ## base.cTrav.addCollider(self.aquariumBottomC, self.CollisionHandler)
        ## base.cTrav.addCollider(self.aquariumTopC, self.CollisionHandler)
        ## base.cTrav.addCollider(self.aquariumRightC, self.CollisionHandler)
        ## base.cTrav.addCollider(self.aquariumLeftC, self.CollisionHandler)
        ## base.cTrav.addCollider(self.aquariumFrontC, self.CollisionHandler)
        ## base.cTrav.addCollider(self.aquariumBackC, self.CollisionHandler)                       
        
        
        self.accept('HitAnything', self.hitSomething)
        
        taskMgr.add(self.update, 'updateTask')
        ## p.place()
        print "startGame"
        # Load models and player
 
 
    def createCollider(self):
        # Setup Tank Collider
            # Bottom
        self.aquariumBottomC = createColTube(self.aquarium, "abC", 15, radius = 5, show = SHOW_C)
        setColMask(self.aquariumBottomC, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.aquariumBottomC, 0, type = 'Into' )
        self.aquariumBottomC.setScale(8, 15, .1)
        self.aquariumBottomC.setPos(-60, 0, 1.5)
        ## self.aquariumBottomC.place()
        
            # Top
        self.aquariumTopC = createColTube(self.aquarium, "atC", 15, radius = 5, show = SHOW_C)
        setColMask(self.aquariumTopC, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.aquariumTopC, 0, type = 'Into' )
        self.aquariumTopC.setScale(8, 15, .1)
        self.aquariumTopC.setPos(-60,0, 45)
        ## self.aquariumBottomC.place()
            # Right Side (from spawn)
        self.aquariumRightC = createColTube(self.aquarium, "arC", 15, radius = 5, show = SHOW_C)
        setColMask(self.aquariumRightC, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.aquariumRightC, 0, type = 'Into' )
        self.aquariumRightC.setScale(3, 15, .1)
        self.aquariumRightC.setPos(69,0,0)
        self.aquariumRightC.setHpr(0,0,-90)
        ## self.aquariumBottomC.place()
            # Left side (from spawn)
        self.aquariumLeftC = createColTube(self.aquarium, "alC", 15, radius = 5, show = SHOW_C)
        setColMask(self.aquariumLeftC, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.aquariumLeftC, 0, type = 'Into' )
        self.aquariumLeftC.setScale(3, 15, .1)
        self.aquariumLeftC.setPos(-68,0,50)
        self.aquariumLeftC.setHpr(0,0,90)
        ## self.aquariumBottomC.place()
            # Front side (from spawn)
        self.aquariumFrontC = createColTube(self.aquarium, "afC", 15, radius = 5, show = SHOW_C)
        setColMask(self.aquariumFrontC, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.aquariumFrontC, 0, type = 'Into' )
        self.aquariumFrontC.setScale(10, 6, .1)
        self.aquariumFrontC.setPos(-40,38,25)
        self.aquariumFrontC.setHpr(0,90,0)
        ## self.aquariumBottomC.place()
            # Back side (from spawn)
        self.aquariumBackC = createColTube(self.aquarium, "abaC", 15, radius = 5, show = SHOW_C)
        setColMask(self.aquariumBackC, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.aquariumBackC, 0, type = 'Into' )
        self.aquariumBackC.setScale(10, 6, .1)
        self.aquariumBackC.setPos(-40,-38,25)
        self.aquariumBackC.setHpr(0,90,0)
        ## self.aquariumBottomC.place()

        
        # Setup Player Collider 
        self.playerC = createColSphere(base.camera, "pC", 15, show = SHOW_C)
        setColMask(self.playerC, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.playerC, 0, type = 'Into' )
        
        ## ##self.fish1C = createColSphere(self.fish1, "f1C", 50, show = SHOW_C)
        ## ##self.fish1C.setPos(25, 5.15, 29.77)
        ## ##setColMask(self.fish1C, 0, type = 'From' )
        ## ##setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        ## ##setColMask(self.fish1C, 0, type = 'Into' ) 
        
           
        
        # Creates Toy Colliders  
        self.toy1C = createColSphere(self.toy1, "t1C", 50, show = SHOW_C)
        self.toy1C.setPos(30, -5, 5)
        setColMask(self.toy1C, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.toy1C, 0, type = 'Into' )
        
        self.toy2C = createColSphere(self.toy2, "t2C", 40, show = SHOW_C)
        self.toy2C.setPos(0, 0, 10)
        setColMask(self.toy2C, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.toy2C, 0, type = 'Into' )
        
        self.toy3C = createColSphere(self.toy3, "t3C", 38, show = SHOW_C)
        self.toy3C.setPos(0, 53, 0)
        setColMask(self.toy3C, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.toy3C, 0, type = 'Into' )
        
        self.toy4C = createColSphere(self.toy4, "t4C", 60, show = SHOW_C)
        self.toy4C.setPos(0, -10, 40)
        setColMask(self.toy4C, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.toy4C, 0, type = 'Into' )
        
        self.toy5C = createColSphere(self.toy5, "t5C", 35, show = SHOW_C)
        self.toy5C.setPos(0, 0, 0)
        setColMask(self.toy5C, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.toy5C, 0, type = 'Into' )
        
        self.toy6C = createColSphere(self.toy6, "t6C", 40, show = SHOW_C)
        self.toy6C.setPos(0, 0, 0)
        setColMask(self.toy6C, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.toy6C, 0, type = 'Into' )
        
        self.toy7C = createColSphere(self.toy7, "t7C", 35, show = SHOW_C)
        self.toy7C.setPos(0, -20,10)
        setColMask(self.toy7C, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.toy7C, 0, type = 'Into' )
        
        
        self.toy8C = createColSphere(self.toy8, "t8C", 35, show = SHOW_C)
        self.toy8C.setPos(-20, 0, 20)
        setColMask(self.toy8C, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.toy8C, 0, type = 'Into' )
        
        self.toy9C = createColSphere(self.toy9, "t9C", 80, show = SHOW_C)
        self.toy9C.setPos(0, 0, 32)
        setColMask(self.toy9C, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.toy9C, 0, type = 'Into' )
        
        # Treasure Chest Collider
        self.treasureChestC = createColSphere(self.treasureChest, "tcC", 45, show = SHOW_C)
        self.treasureChestC.setPos(15, 3, 32)
        setColMask(self.treasureChestC, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
        setColMask(self.treasureChestC, 0, type = 'Into' )
    
    def createEnvironment(self):
        # Loads aquarium and sets it so player is stuck in it.
        
        self.enviroNode = render.attachNewNode( "EnviroNode" )
        self.enviroNode.setScale(1)
        self.enviroNode.setPosHpr(0,0,-30,  0,0,0)
        # Load second fish example
        self.fish2 = loader.loadModel("Models/clownFishModel.egg")
        self.fish2 = Actor('Models/clownFishModel.egg', {'swimming':'Models/clownFishAnim.egg'})
        self.fish2.loop('swimming')
        self.fish2.reparentTo(self.enviroNode)
        ##self.fish2Tex = loader.loadTexture("Textures/red.tif")
        ##self.fish2.setTexture(self.fish2Tex, 1)
        self.fish2.setScale(.7)
        self.fish2.setPos(50, 164.8, 44.15)
        ## self.fish2.place()
        # Sequences for Fish2 movement
        self.fish2PosInterval1 = self.fish2.posInterval(10,Point3(-50, 0, 70),startPos=Point3(50,0, 70))
        self.fish2PosInterval2 = self.fish2.posInterval(10,Point3(50, 0, 70),startPos=Point3(-50, 0, 70))
        self.fish2HprInterval1 = self.fish2.hprInterval(3,Point3(180, 0, 0),startHpr=Point3(0, 0, 0))
        self.fish2HprInterval2 = self.fish2.hprInterval(3,Point3(0, 0, 0),startHpr=Point3(180, 0, 0))
        self.fish2move = Sequence(self.fish2PosInterval2, self.fish2HprInterval1, self.fish2PosInterval1, self.fish2HprInterval2, name="fish2move")        
        self.fish2move.loop()
        
        # Load third fish example
        self.fish3 = loader.loadModel("Models/smallSchoolFishModel.egg")
        self.fish3 = Actor('Models/smallSchoolFishModel.egg', {'swimming':'Models/smallSchoolFishAnim.egg'})
        self.fish3.loop('swimming')
        self.fish3.reparentTo(self.enviroNode)
        ## self.fish3Tex = loader.loadTexture("Textures/red.tif")
        ## self.fish3.setTexture(self.fish3Tex, 1)
        self.fish3.setScale(1.5)
        self.fish3.setPos(230, 50, 15)
        ## self.fish3.setHpr(0, 0, 0)
        ## self.fish3.place()
        # Sequences for Fish3 Movement
        self.fish3PosInterval1 = self.fish3.posInterval(10,Point3(230, 50, 25),startPos=Point3(150,50, 30))
        self.fish3PosInterval2 = self.fish3.posInterval(10,Point3(150, 50, 30),startPos=Point3(230, 50, 15))
        self.fish3HprInterval1 = self.fish3.hprInterval(3,Point3(180, 0, 0),startHpr=Point3(0, 0, 0))
        self.fish3HprInterval2 = self.fish3.hprInterval(3,Point3(0, 0, 0),startHpr=Point3(180, 0, 0))
        self.fish3move = Sequence(self.fish3PosInterval2, self.fish3HprInterval1, self.fish3PosInterval1, self.fish3HprInterval2, name="fish3move")        
        self.fish3move.loop()
        
        # Load fourth fish example
        self.fish4 = loader.loadModel("Models/lionFishModel.egg")
        self.fish4 = Actor('Models/lionFishModel.egg', {'swimming':'Models/lionFishAnim.egg'})
        self.fish4.loop('swimming')
        self.fish4.reparentTo(self.enviroNode)
        self.fish4Tex = loader.loadTexture("Textures/red.tif")
        self.fish4.setTexture(self.fish4Tex, 1)
        self.fish4.setScale(.8)
        self.fish4.setPos(55, -70, 135)
        ## self.fish4.place()
        # Sequence for fish4 Movement
        self.fish4PosInterval1 = self.fish4.posInterval(10,Point3(55, -70, 135),startPos=Point3(75, -30, 135))
        self.fish4PosInterval2 = self.fish4.posInterval(10,Point3(75, -30, 135),startPos=Point3(55, -70, 135))
        self.fish4HprInterval1 = self.fish4.hprInterval(3,Point3(180, 0, 0),startHpr=Point3(0, 0, 0))
        self.fish4HprInterval2 = self.fish4.hprInterval(3,Point3(0, 0, 0),startHpr=Point3(180, 0, 0))
        self.fish4move = Sequence(self.fish4PosInterval2, self.fish4HprInterval1, self.fish4PosInterval1, self.fish4HprInterval2, name="fish4move")        
        self.fish4move.loop()
        
        
        #Load Shrimp
        self.fish5 = loader.loadModel("Models/cleanerShrimpModel.egg")
        self.fish5 = Actor('Models/cleanerShrimpModel.egg', {'swimming':'Models/cleanerShrimpAnim.egg'})
        self.fish5.loop('swimming')
        self.fish5.reparentTo(self.enviroNode)
        ## self.fish5Tex = loader.loadTexture("Textures/red.tif")
        ## self.fish5.setTexture(self.fish5Tex, 1)
        self.fish5.setScale(.5)
        self.fish5.setPos(-230, -140, 4)
        ## self.fish5.setHpr(0, 0, 0)
        # Sequence for shrimp Movement
        self.fish5PosInterval1 = self.fish5.posInterval(10,Point3(-230, -140, 4),startPos=Point3(200, -140, 4))
        self.fish5PosInterval2 = self.fish5.posInterval(10,Point3(200, -140, 4),startPos=Point3(-230, -140, 4))
        self.fish5HprInterval1 = self.fish5.hprInterval(3,Point3(180, 0, 0),startHpr=Point3(0, 0, 0))
        self.fish5HprInterval2 = self.fish5.hprInterval(3,Point3(0, 0, 0),startHpr=Point3(-180, 0, 0))
        self.fish5move = Sequence(self.fish5PosInterval2, self.fish5HprInterval1, self.fish5PosInterval1, self.fish4HprInterval2, name="fish5move")        
        self.fish5move.loop()
        
        #Load Seahorse
        self.fish6 = loader.loadModel("Models/seaHorseModel.egg")
        self.fish6 = Actor('Models/seaHorseModel.egg', {'floating':'Models/seaHorseAnim.egg'})
        self.fish6.loop('floating')
        self.fish6.reparentTo(self.enviroNode)
        self.fish6.setScale(.9)
        self.fish6.setPos(282,160,58)
        self.fish6.setHpr(90, 0, 0)
        ## self.fish6.place()
        
        # Loading in the first Toy Model
        self.toy1 = loader.loadModel("Models/car1.egg")
        self.toy1.reparentTo(self.enviroNode)
        ## self.toy1Tex = loader.loadTexture("Textures/car1_unwrap.png")
        ## self.toy1.setTexture(self.toy1Tex, 1)
        self.toy1.setScale(.5)
        self.toy1.setPos(-286.7, -73.5,12)
        self.toy1.setHpr(90, 0, 0)
        ## self.toy1.place()
        
        # Loading in the second Toy Model
        self.toy2 = loader.loadModel("Models/truck1.egg")
        self.toy2.reparentTo(self.enviroNode)
        self.toy2Tex = loader.loadTexture("Textures/truck_unwrap.png")
        self.toy2.setTexture(self.toy2Tex, 1)
        self.toy2.setScale(1)
        self.toy2.setPos(265,150,7)
        self.toy2.setHpr(90,0,0)
        ## self.toy2.place()
        
        # Loading in the third Toy model
        self.toy3 = loader.loadModel("Models/car2.egg")
        self.toy3.reparentTo(self.enviroNode)
        self.toy3Tex = loader.loadTexture("Textures/car2_unwrap.png")
        self.toy3.setTexture(self.toy3Tex, 1)
        self.toy3.setScale(.5)
        self.toy3.setPos(-244.8, 35, 101.2)
        self.toy3.setHpr(273.5, 175.1, 344.7)
        ## self.toy3.place()
        
        #Load Diving Ring (Toy)
        self.toy4 = loader.loadModel("Models/divingRingModel.egg")
        self.toy4.reparentTo(self.enviroNode)
        self.toy4.setScale(.5)
        self.toy4.setPos(142.8, -23.5, 154)
        self.toy4.setHpr(104, 0, 0)
        ## self.divingRing.place()
        
        #loading in the 5th toy model
        self.toy5 = loader.loadModel("Models/crayonStatic.egg")
        self.toy5.reparentTo(self.enviroNode)
        self.toy5.setScale(.6)
        self.toy5.setPos(-303.9, -157, 9)
        ## self.toy5.place()
        
        #loading in the 6th toy model
        self.toy6 = loader.loadModel("Models/legoToyStatic.egg")
        self.toy6.reparentTo(self.enviroNode)
        self.toy6.setScale(.5)
        self.toy6.setPos(-26, 108, 7.5)
        ## self.toy6.place()
        
        #loading in the 7th toy model
        self.toy7 = loader.loadModel("Models/pokeballStatic.egg")
        self.toy7.reparentTo(self.enviroNode)
        self.toy7.setScale(.5)
        self.toy7.setPos(20, -116, 78)
        self.toy7.setHpr(9.9, 252.8, 1.1)
        ## self.toy7.place()
        
        #loading in the 8th toy model
        self.toy8 = loader.loadModel("Models/companionCubeStatic.egg")
        self.toy8.reparentTo(self.enviroNode)
        self.toy8.setScale(.5)
        self.toy8.setPos(-216, 178, 39)
        self.toy8.setHpr(0, 0, 0)
        ## self.toy8.place()
        
        #loading in the 9th toy model
        self.toy9 = loader.loadModel("Models/rubiksCubeStatic.egg")
        self.toy9.reparentTo(self.enviroNode)
        self.toy9.setScale(.5)
        self.toy9.setPos(310, -161, 7)
        ## self.toy9.place()
        
        
        # Load Aquarium
        self.aquarium = loader.loadModel("Models/tanktest.egg")
        self.aquarium.reparentTo(self.enviroNode)
        self.aquariumTex = loader.loadTexture("Textures/tank_unwrap.png")
        self.aquarium.setTexture(self.aquariumTex, 1)
        self.aquarium.setScale(5)
        
        self.aquariumTop = loader.loadModel("Models/tanktop.egg")
        self.aquariumTop.reparentTo(self.enviroNode)
        self.aquariumTopTex = loader.loadTexture("Textures/top_unwrap.png")
        self.aquariumTop.setTexture(self.aquariumTopTex, 1)
        self.aquariumTop.setScale(5)
        
        # Load Disk Plant
        self.diskPlant = loader.loadModel("Models/triDiskPlantStatic.egg")
        self.diskPlant = Actor('Models/triDiskPlantModel.egg', {'swaying':'Models/triDiskPlantAnim.egg'})
        self.diskPlant.loop('swaying')
        self.diskPlant.reparentTo(self.enviroNode)
        ## self.diskPlantTex = loader.loadTexture("Textures/red.tif")
        ## self.diskPlant.setTexture(self.diskPlantTex, 1)
        self.diskPlant.setScale(1.5)
        self.diskPlant.setPos(-280,-150,7)
        
        self.diskPlant2 = loader.loadModel("Models/triDiskPlantStatic.egg")
        self.diskPlant2 = Actor('Models/triDiskPlantModel.egg', {'swaying':'Models/triDiskPlantAnim.egg'})
        self.diskPlant2.loop('swaying')
        self.diskPlant2.reparentTo(self.enviroNode)
        ## self.diskPlant2Tex = loader.loadTexture("Textures/red.tif")
        ## self.diskPlant2.setTexture(self.diskPlantTex, 1)
        self.diskPlant2.setScale(1.5)
        self.diskPlant2.setPos(230,97,7)
        ## self.diskPlant2.place()
        
        self.diskPlant3 = loader.loadModel("Models/triDiskPlantStatic.egg")
        self.diskPlant3 = Actor('Models/triDiskPlantModel.egg', {'swaying':'Models/triDiskPlantAnim.egg'})
        self.diskPlant3.loop('swaying')
        self.diskPlant3.reparentTo(self.enviroNode)
        ## self.diskPlant3Tex = loader.loadTexture("Textures/red.tif")
        ## self.diskPlant3.setTexture(self.diskPlantTex, 1)
        self.diskPlant3.setScale(1.5)
        self.diskPlant3.setPos(244,100,7)
        self.diskPlant3.setHpr(90, 0, 0)
        ## self.diskPlant3.place()
        
        self.diskPlant4 = loader.loadModel("Models/triDiskPlantStatic.egg")
        self.diskPlant4 = Actor('Models/triDiskPlantModel.egg', {'swaying':'Models/triDiskPlantAnim.egg'})
        self.diskPlant.loop('swaying')
        self.diskPlant4.reparentTo(self.enviroNode)
        ## self.diskPlant4Tex = loader.loadTexture("Textures/red.tif")
        ## self.diskPlant4.setTexture(self.diskPlantTex, 1)
        self.diskPlant4.setScale(.5)
        self.diskPlant4.setPos(-220, -5.6, 40.6)
        ## self.diskPlant4.place()
        
        self.diskPlant5 = loader.loadModel("Models/triDiskPlantStatic.egg")
        self.diskPlant5 = Actor('Models/triDiskPlantModel.egg', {'swaying':'Models/triDiskPlantAnim.egg'})
        self.diskPlant5.loop('swaying')
        self.diskPlant5.reparentTo(self.enviroNode)
        ## self.diskPlant5Tex = loader.loadTexture("Textures/red.tif")
        ## self.diskPlant5.setTexture(self.diskPlantTex, 1)
        self.diskPlant5.setScale(1)
        self.diskPlant5.setPos(-243, -104, 7)
        self.diskPlant5.setHpr(90, 0, 0)
        ## self.diskPlant5.place()
        
        # Load Leafy Plant
        self.leafyPlant = loader.loadModel("Models/triLeafyPlantModel.egg")
        self.leafyPlant = Actor('Models/triLeafyPlantModel.egg', {'swaying':'Models/triLeafyPlantAnim.egg'})
        self.leafyPlant.loop('swaying')
        self.leafyPlant.reparentTo(self.enviroNode)
        ## self.leafyPlantTex = loader.loadTexture("Textures/red.tif")
        ## self.leafyPlant.setTexture(self.leafyPlantTex, 1)
        self.leafyPlant.setScale(1.3)
        self.leafyPlant.setPos(320,140,7)
        ## self.leafyPlant.place()
        
        self.leafyPlant2 = loader.loadModel("Models/triLeafyPlantModel.egg")
        self.leafyPlant2 = Actor('Models/triLeafyPlantModel.egg', {'swaying':'Models/triLeafyPlantAnim.egg'})
        self.leafyPlant2.loop('swaying')
        self.leafyPlant2.reparentTo(self.enviroNode)
        ## self.leafyPlant2Tex = loader.loadTexture("Textures/red.tif")
        ## self.leafyPlant2.setTexture(self.leafyPlantTex, 1)
        self.leafyPlant2.setScale(1.3)
        self.leafyPlant2.setPos(320,120,7)
        self.leafyPlant2.setHpr(90, 0, 0)
        
        self.leafyPlant3 = loader.loadModel("Models/triLeafyPlantModel.egg")
        self.leafyPlant3 = Actor('Models/triLeafyPlantModel.egg', {'swaying':'Models/triLeafyPlantAnim.egg'})
        self.leafyPlant3.loop('swaying')
        self.leafyPlant3.reparentTo(self.enviroNode)
        ## self.leafyPlant3Tex = loader.loadTexture("Textures/red.tif")
        ## self.leafyPlant3.setTexture(self.leafyPlantTex, 1)
        self.leafyPlant3.setScale(.35)
        self.leafyPlant3.setPos(5.4, 96.4, 7)
        ## self.leafyPlant3.place()
        
        self.leafyPlant4 = loader.loadModel("Models/triLeafyPlantModel.egg")
        self.leafyPlant4 = Actor('Models/triLeafyPlantModel.egg', {'swaying':'Models/triLeafyPlantAnim.egg'})
        self.leafyPlant4.loop('swaying')
        self.leafyPlant4.reparentTo(self.enviroNode)
        ## self.leafyPlant4Tex = loader.loadTexture("Textures/red.tif")
        ## self.leafyPlant4.setTexture(self.leafyPlantTex, 1)
        self.leafyPlant4.setScale(.5)
        self.leafyPlant4.setPos(-210, -5.6, 40.6)
        ## self.leafyPlant4.place()
        
        self.leafyPlant5 = loader.loadModel("Models/triLeafyPlantModel.egg")
        self.leafyPlant5 = Actor('Models/triLeafyPlantModel.egg', {'swaying':'Models/triLeafyPlantAnim.egg'})
        self.leafyPlant5.loop('swaying')
        self.leafyPlant5.reparentTo(self.enviroNode)
        ## self.leafyPlant5Tex = loader.loadTexture("Textures/red.tif")
        ## self.leafyPlant5.setTexture(self.leafyPlantTex, 1)
        self.leafyPlant5.setScale(.42)
        self.leafyPlant5.setPos(14.6, 108, 7)
        self.leafyPlant5.setHpr(90, 0, 0)
        ## self.leafyPlant5.place()
        
        #load small leafy plant
        self.smallLeafPlant = loader.loadModel("Models/smallLeafPlantModel.egg")
        self.smallLeafPlant.reparentTo(self.enviroNode)
        self.smallLeafPlant.setScale(.6)
        self.smallLeafPlant.setPos(-209, 138, 42)
        ## self.smallLeafPlant.place()
        
        self.smallLeafPlant2 = loader.loadModel("Models/smallLeafPlantModel.egg")
        self.smallLeafPlant2.reparentTo(self.enviroNode)
        self.smallLeafPlant2.setScale(.5)
        self.smallLeafPlant2.setPos(-200, 154, 42)
        self.smallLeafPlant2.setHpr(90, 0, 0)
        ## self.smallLeafPlant2.place()
        
        self.smallLeafPlant3 = loader.loadModel("Models/smallLeafPlantModel.egg")
        self.smallLeafPlant3.reparentTo(self.enviroNode)
        self.smallLeafPlant3.setScale(.5)
        self.smallLeafPlant3.setPos(-209, 151.38, 42)
        ## self.smallLeafPlant3.place()
        
        self.smallLeafPlant4 = loader.loadModel("Models/smallLeafPlantModel.egg")
        self.smallLeafPlant4.reparentTo(self.enviroNode)
        self.smallLeafPlant4.setScale(1.41)
        self.smallLeafPlant4.setPos(272.8, -181.6, 7)
        ## self.smallLeafPlant4.place()
        
        self.smallLeafPlant5 = loader.loadModel("Models/smallLeafPlantModel.egg")
        self.smallLeafPlant5.reparentTo(self.enviroNode)
        self.smallLeafPlant5.setScale(1.2)
        self.smallLeafPlant5.setPos(319.5, -142, 7)
        self.smallLeafPlant5.setHpr(90, 0, 0)
        ## self.smallLeafPlant5.place()
        
        #Load Spiral Shell
        self.spiralShell = loader.loadModel("Models/spiralShellStatic.egg")
        self.spiralShell.reparentTo(self.enviroNode)
        self.spiralShell.setScale(.5)
        self.spiralShell.setPos(-15.7, 54, 3.5)
        self.spiralShell.setHpr(294, 4, 0)
        ## self.spiralShell.place()
        
        self.spiralShell2 = loader.loadModel("Models/spiralShellStatic.egg")
        self.spiralShell2.reparentTo(self.enviroNode)
        self.spiralShell2.setScale(.6)
        self.spiralShell2.setPos(-42.24, 69, 3.5)
        self.spiralShell2.setHpr(37.4, 3, 0)
        ## self.spiralShell2.place()
        
        self.spiralShell3 = loader.loadModel("Models/spiralShellStatic.egg")
        self.spiralShell3.reparentTo(self.enviroNode)
        self.spiralShell3.setScale(3.52)
        self.spiralShell3.setPos(336.2, -163, 18)
        self.spiralShell3.setHpr(0, 296.57, 0)
        ## self.spiralShell3.place()
        
        
        
        # Load Treasure Chest
        self.treasureChest = loader.loadModel("Models/treasureChestModel.egg")
        self.treasureChest = Actor('Models/treasureChestModel.egg', {'opening':'Models/treasureChestAnim.egg'})
        self.treasureChest.loop('opening')
        self.treasureChest.reparentTo(self.enviroNode)
        ## self.treasureChestTex = loader.loadTexture("Textures/red.tif")
        ## self.treasureChest.setTexture(self.treasureChestTex, 1)
        self.treasureChest.setScale(.5)
        self.treasureChest.setPos(0,70,4)
        ## self.treasureChest.place()
        
        
        #Load Coral
        self.coral = loader.loadModel("Models/coralStatic.egg")
        self.coral.reparentTo(self.enviroNode)
        self.coral.setScale(1.9)
        self.coral.setPos(165,128,3.5)
        self.coral.setHpr(104.04, 0, 0)
        ## self.coral.place()
        
        self.coral2 = loader.loadModel("Models/coralStatic.egg")
        self.coral2.reparentTo(self.enviroNode)
        self.coral2.setScale(1.5)
        self.coral2.setPos(-28.8, 67.2, 3.5)
        self.coral2.setHpr(255.8, 0, 0)
        ## self.coral2.place()
        
        self.coral3 = loader.loadModel("Models/coralStatic.egg")
        self.coral3.reparentTo(self.enviroNode)
        self.coral3.setScale(2.19)
        self.coral3.setPos(0, -182.5, 3.5)
        self.coral3.setHpr(0, 0, 0)
        ## self.coral3.place()
        
        #Load Castle
        self.castle = loader.loadModel("Models/castleStatic.egg")
        self.castle.reparentTo(self.enviroNode)
        self.castle.setScale(1.7)
        self.castle.setPos(-250,130,-10)
        self.castle.setHpr(0, 0, 0)
        print "Load Castle"
        ## self.castle.place()
        # Starts the Game Fully
        self.createCollider()        
        self.startGame()
        #Enables Particles
        base.enableParticles()
        # Creates bubble particle
        pBubble = ParticleEffect()
        pBubble.loadConfig("bubbles_1.ptf")
        pBubble.start(parent = self.treasureChest, renderParent = self.treasureChest)
        pBubble.setPos(15,-26,45)
        pBubble.setScale(55, 50, 50)
        pBubble.setH(90)
        # Sets bubble able to be shot
        self.bubbleWasEmitted = 0
    def hitSomething(self, colEntry):
        # Collision between Player and Walls
        if (colEntry.getFromNode().getName()=='pC') and (colEntry.getIntoNode().getName()=='abC'):
            base.camera.setPos(0,0,2)
        if (colEntry.getFromNode().getName()=='pC') and (colEntry.getIntoNode().getName()=='atC'):
            base.camera.setPos( base.camera.getPos() + (self.forward.getPos(render) - base.camera.getPos(render)) * -7 )
        if (colEntry.getFromNode().getName()=='pC') and (colEntry.getIntoNode().getName()=='arC'):
            base.camera.setPos( base.camera.getPos() + (self.forward.getPos(render) - base.camera.getPos(render)) * -7 )
        if (colEntry.getFromNode().getName()=='pC') and (colEntry.getIntoNode().getName()=='alC'):
            base.camera.setPos( base.camera.getPos() + (self.forward.getPos(render) - base.camera.getPos(render)) * -7 )
        if (colEntry.getFromNode().getName()=='pC') and (colEntry.getIntoNode().getName()=='afC'):
            base.camera.setPos( base.camera.getPos() + (self.forward.getPos(render) - base.camera.getPos(render)) * -7 )
        if (colEntry.getFromNode().getName()=='pC') and (colEntry.getIntoNode().getName()=='abaC'):
            base.camera.setPos( base.camera.getPos() + (self.forward.getPos(render) - base.camera.getPos(render)) * -7 )
            
        
        # Collision between Player and Bubble
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='abC'):
            self.bubbleEmitted.removeNode()
            if self.bubbleWasEmitted == 1:
                self.bubbleWasEmitted = 0
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='atC'):
            self.bubbleEmitted.removeNode()
            if self.bubbleWasEmitted == 1:
                self.bubbleWasEmitted = 0
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='arc'):
            self.bubbleEmitted.removeNode()
            if self.bubbleWasEmitted == 1:
                self.bubbleWasEmitted = 0
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='alC'):
            self.bubbleEmitted.removeNode()
            if self.bubbleWasEmitted == 1:
                self.bubbleWasEmitted = 0
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='afC'):
            self.bubbleEmitted.removeNode()
            if self.bubbleWasEmitted == 1:
                self.bubbleWasEmitted = 0
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='abaC'):
            self.bubbleEmitted.removeNode()
            if self.bubbleWasEmitted == 1:
                self.bubbleWasEmitted = 0
            
        
        
        
        
        # Checks for collisions between bubble and toy
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='t1C'):
            self.bubbleEmitted.removeNode()
            l = LerpPosInterval(self.toy1, 5, (self.toy1.getX(), self.toy1.getY(), self.toy1.getZ()+500))
            s = Sequence(l, Wait(1)).start()
            if self.bubbleWasEmitted == 1:
                self.score -= 1
            self.bubbleWasEmitted = 0
            print self.score
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='t2C'):
            self.bubbleEmitted.removeNode()
            l = LerpPosInterval(self.toy2, 5, (self.toy2.getX(), self.toy2.getY(), self.toy2.getZ()+500))
            s = Sequence(l, Wait(1)).start()            
            if self.bubbleWasEmitted == 1:
                self.score -= 1
            self.bubbleWasEmitted = 0
            print self.score
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='t3C'):
            self.bubbleEmitted.removeNode()
            l = LerpPosInterval(self.toy3, 5, (self.toy3.getX(), self.toy3.getY(), self.toy3.getZ()+500))
            s = Sequence(l, Wait(1)).start() 
            if self.bubbleWasEmitted == 1:
                self.score -= 1
            self.bubbleWasEmitted = 0
            print self.score
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='t4C'):
            self.bubbleEmitted.removeNode()
            l = LerpPosInterval(self.toy4, 5, (self.toy4.getX(), self.toy4.getY(), self.toy4.getZ()+500))
            s = Sequence(l, Wait(1)).start()
            if self.bubbleWasEmitted == 1:
                self.score -= 1
            self.bubbleWasEmitted = 0
            print self.score
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='t5C'):
            self.bubbleEmitted.removeNode()
            l = LerpPosInterval(self.toy5, 5, (self.toy5.getX(), self.toy5.getY(), self.toy5.getZ()+500))
            s = Sequence(l, Wait(1)).start() 
            if self.bubbleWasEmitted == 1:
                self.score -= 1
            self.bubbleWasEmitted = 0
            print self.score
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='t6C'):
            self.bubbleEmitted.removeNode()
            l = LerpPosInterval(self.toy6, 5, (self.toy6.getX(), self.toy6.getY(), self.toy6.getZ()+500))
            s = Sequence(l, Wait(1)).start() 
            if self.bubbleWasEmitted == 1:
                self.score -= 1
            self.bubbleWasEmitted = 0
            print self.score
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='t7C'):
            self.bubbleEmitted.removeNode()
            l = LerpPosInterval(self.toy7, 5, (self.toy7.getX(), self.toy7.getY(), self.toy7.getZ()+500))
            s = Sequence(l, Wait(1)).start() 
            if self.bubbleWasEmitted == 1:
                self.score -= 1
            self.bubbleWasEmitted = 0
            print self.score
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='t8C'):
            self.bubbleEmitted.removeNode()
            l = LerpPosInterval(self.toy8, 5, (self.toy8.getX(), self.toy8.getY(), self.toy8.getZ()+500))
            s = Sequence(l, Wait(1)).start() 
            if self.bubbleWasEmitted == 1:
                self.score -= 1
            self.bubbleWasEmitted = 0
            print self.score
        if (colEntry.getFromNode().getName()=='bC') and (colEntry.getIntoNode().getName()=='t9C'):
            self.bubbleEmitted.removeNode()
            l = LerpPosInterval(self.toy9, 5, (self.toy9.getX(), self.toy9.getY(), self.toy9.getZ()+500))
            s = Sequence(l, Wait(1)).start() 
            if self.bubbleWasEmitted == 1:
                self.score -= 1   
            self.bubbleWasEmitted = 0
            print self.score 
            ## print "Got Toy!"
        # Makes the player reload bubbles when they collide with the treasure chest
        if (colEntry.getFromNode().getName()=='pC') and (colEntry.getIntoNode().getName()=='tcC'):
            self.bubblesLeft = 5
        self.scoreString = str(self.score)
        self.scoreText['text']=self.scoreString
        self.bubblesLeftString = str(self.bubblesLeft)
        self.bubblesLeftText['text']=self.bubblesLeftString
        
        
    def createUI(self):
        self.ui = OnscreenImage(image = 'Textures/subUI.png', pos = (0, 1, -.3), scale=1.35)
        self.ui.setTransparency(TransparencyAttrib.MAlpha)
        
        #Score
        self.score = 9
        self.scoreString = str(self.score)
        #Score Text
        self.scoreText= OnscreenText(text = self.scoreString, pos = (-.65, 0.83), scale = .15)
        print self.score
        self.scoreString = str(self.score)
        self.scoreText['text']=self.scoreString
        
        #Bubbles
        self.bubblesLeft = 5
        self.bubblesLeftString = str(self.bubblesLeft)
        #Bubble Text
        self.bubblesLeftText= OnscreenText(text = self.bubblesLeftString, pos = (.47, 0.81), scale = .15)
        print self.bubblesLeft
        self.bubblesLeftString = str(self.bubblesLeft)
        self.bubblesLeftText['text']=self.bubblesLeftString
            
#Stopwatch
        self.secondsTime = 0
        self.minutesTime = 0
        self.time = self.formatTime(self.minutesTime, self.secondsTime)
        self.stopwatchText = OnscreenText(text=self.time, style = 2, fg =(.25, .2, .4, .5), pos = (-.03, .85), scale = .13)
        
        self.crosshair = OnscreenImage(image = 'Textures/crosshair.png', pos = (0, 0, 0), scale = .10)
        self.crosshair.setTransparency(TransparencyAttrib.MAlpha)
    def startTime(self):
        self.firstPick = (-1, -1)
        f1 = Func(self.updateTime)
        print "Timer Started"
        self.s = Sequence(Wait(1), f1)
        self.s.loop()
        self.secondsTime = 0
        self.minutesTime = 0
        
    def bubbleEmitter(self):
        ## print "bubble emitted"
        if self.bubblesLeft == 0:
            return
        elif self.bubbleWasEmitted == 0:
            
            self.bubbleEmitted=loader.loadModel("Models/bubbleModel.egg")
            
            self.bubbleEmitted.setScale(.4)
            self.bubbleEmitted.reparentTo(render)
            ## self.bubbleEmitted.setScale(.2)
            self.bubbleForward = self.bubbleEmitted.attachNewNode('forward')
            self.bubbleForward.setPos(0, .2, 0)
            
        # Sets Bubble emission
            self.bubbleEmitted.setPos(base.camera.getPos())
            self.bubbleEmitted.setHpr(base.camera.getH(),base.camera.getP(),base.camera.getR())
        # Stops Other bubbles from Spawning
            self.bubbleWasEmitted=1
        # Creates Collider
            self.bubbleC = createColSphere(self.bubbleEmitted, "bC", 7, show = SHOW_C)
            self.bubbleC.setPos(0, 0, 3)
            setColMask(self.bubbleC, 0, type = 'From' )
        ## setColMask(self.playerC, -1, type = 'Into', allOff = True )  # disallow this type
            setColMask(self.bubbleC, 0, type = 'Into' )
            base.cTrav.addCollider(self.bubbleC, self.CollisionHandler)
        # Remove from bubble count
            self.bubblesLeft -= 1
            print self.bubblesLeft
        elif self.bubbleWasEmitted == 1:
            return
        self.bubblesLeftString = str(self.bubblesLeft)
        self.bubblesLeftText['text']=self.bubblesLeftString
        self.bubbleMover()
        
    def bubbleMover(self):
        self.bubbleEmitted.setPos( self.bubbleEmitted.getPos() + (self.bubbleForward.getPos(render) - self.bubbleEmitted.getPos(render)) * 20 )
        
    def formatTime(self, minutes, seconds):
        self.time = str(minutes) + ":"
        if self.secondsTime < 10:
            self.time += "0"
        self.time += str(self.secondsTime)
        return self.time
        
    def updateTime(self):
        if self.secondsTime == 0 and self.minutesTime == 59:
            print "Out of Time!"
            self.finish()
        else:
            self.secondsTime += 1
            if self.secondsTime > 59:
                self.secondsTime = 0 
                self.minutesTime += 1
            self.time = self.formatTime(self.minutesTime, self.secondsTime)        
            self.stopwatchText["text"] = self.time
        if self.score == 0:
            print "game over!  Congrats!"
        
    def update(self, task):
        # fish1AnimControl = self.fish1.getAnimControl('swimming')
        #self.fish1.loop('swimming')
        if self.bubbleWasEmitted==1:
            self.bubbleMover()
        # Updates the game, should run as a task
        return task.cont
    
w = World()
run()