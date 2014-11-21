############################################################################
## Program: Fish Tank                                                     ##
## Programmers: John Groot, June Chew, Mitchell Vitez                     ##
## Purpose: Create the Fish Tank game as outlined in resources folder     ##
##                                                                        ##                                                                      
#  ERRORS:                                                                ##
##                                                                        ##
##                                                                        ##
##                                                                        ##
##                                                                        ##
##                                                                        ##
##                                                                        ##
############################################################################

from pandac.PandaModules import loadPrcFileData
from fish_tank_config import *
loadPrcFileData("", ORIGIN)
loadPrcFileData("", SIZE)
loadPrcFileData("", TITLE)

import sys
import random

import direct.directbase.DirectStart                                     
from direct.showbase.DirectObject import DirectObject
from pandac.PandaModules import *
from direct.task import Task
from direct.interval.IntervalGlobal import *
from direct.gui.DirectGui import *
from direct.ETCleveleditor import LevelLoader
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

import random

from collisions import *
## from joystick import *



class World(DirectObject):
    def __init__(self):
        self.startGame()
        
        ##base.camera = render.attachNewNode('camBase')  # control camera x,y ; ground collider attached
        self.camHigh = base.camera.attachNewNode('camBase')  # control camera Z
        self.right = base.camera.attachNewNode('right')
        self.right.setPos(.2, 0, 0)
        self.forward = base.camera.attachNewNode('forward')
        self.forward.setPos(0, .2, 0)
        
        # setup controls
        self.keys = {'w':False, 'a':False, 's':False, 'd':False, 'r':False, 'f':False, 
					'q':False, 'e':False, 't':False, 'g':False}
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
        
        taskMgr.add(self.controlTask, 'controlTask')
        # taskMgr.add(self.update, 'updateTask')
#######################  Keyboard Controls #################################### 
    def onKey(self, key, pressed): 
        self.keys[key] = pressed
        
    def controlTask(self, task):
        if self.keys['w']: base.camera.setPos( base.camera.getPos() + (self.forward.getPos(render) - base.camera.getPos(render)) * 1 )
        if self.keys['a']: base.camera.setPos( base.camera.getPos() + (self.right.getPos(render) - base.camera.getPos(render)) * -1 )
        if self.keys['s']: base.camera.setPos( base.camera.getPos() + (self.forward.getPos(render) - base.camera.getPos(render)) * -1 )
        if self.keys['d']: base.camera.setPos( base.camera.getPos() + (self.right.getPos(render) - base.camera.getPos(render)) * 1 )
        if self.keys['r']: base.camera.setZ( base.camera.getZ() + 0.2 )    
        if self.keys['f']: base.camera.setZ( base.camera.getZ() - 0.2 ) 
        if self.keys['q']: base.camera.setH( base.camera.getH() + 1 )
        if self.keys['e']: base.camera.setH( base.camera.getH() - 1 )
        if self.keys['t']: base.camera.setP( base.camera.getP() + 1 )
        if self.keys['g']: base.camera.setP( base.camera.getP() - 1 )
        ## print self.camBase.getH()    # testing


        return Task.cont
##############################################################################        
###################### JOYSTICKS #############################################

    def setJoysticks(self):
        #set up joysticks
        self.numSticks = 2              ## UPDATE THIS 
        self.events = []
        self.js = []
        self.js_axis = []
        for i in range(self.numSticks):
            self.events.append( self.setupButtonEvents(i))
            self.js.append(Joy(self.events[i],i))
            self.js_axis.append([0,0,0,0])
        # uncomment to poll the axis sticks
        ## taskMgr.doMethodLater(.1,self.pollAxis, 'pollAxisTask')
        
    def setupButtonEvents(self,num):
        # create button event handler conections
        events = {}
        self.accept(str(num) + "_joyButton0-up",self.ButtonHit, [num, 0, 1])                                                                                                                     
        self.accept(str(num) + "_joyButton0-down",self.ButtonHit, [num, 0, 0])
        events[0] = "joyButton0"
        self.accept(str(num) + "_joyButton1-up",self.ButtonHit, [num, 1, 1])
        self.accept(str(num) + "_joyButton1-down",self.ButtonHit, [num, 1, 0])
        events[1] = "joyButton1"
        self.accept(str(num) + "_joyButton2-up",self.ButtonHit, [num, 2, 1])
        self.accept(str(num) + "_joyButton2-down",self.ButtonHit, [num, 2, 0])
        events[2] = "joyButton2"
        self.accept(str(num) + "_joyButton3-up",self.ButtonHit, [num, 3, 1])
        self.accept(str(num) + "_joyButton3-down",self.ButtonHit, [num, 3, 0])
        events[3] = "joyButton3"
        self.accept(str(num) + "_joyButton4-up",self.ButtonHit, [num, 4, 1])
        self.accept(str(num) + "_joyButton4-down",self.ButtonHit, [num, 4, 0])
        events[4] = "joyButton4"
        self.accept(str(num) + "_joyButton5-up",self.ButtonHit, [num, 5, 1])
        self.accept("joyButton5-down",self.ButtonHit, [num, 5, 0])
        events[5] = "joyButton5"
        self.accept(str(num) + "_joyButton6-up",self.ButtonHit, [num, 6, 1])
        self.accept(str(num) + "_joyButton6-down",self.ButtonHit, [num, 6, 0])
        events[6] = "joyButton6"
        self.accept(str(num) + "_joyButton7-up",self.ButtonHit, [num, 7, 1])
        self.accept(str(num) + "_joyButton7-down",self.ButtonHit, [num, 7, 0])
        events[7] = "joyButton7"
        self.accept(str(num) + "_joyButton8-up",self.ButtonHit, [num, 8, 1])
        self.accept(str(num) + "_joyButton8-down",self.ButtonHit, [num, 8, 0])
        events[8] = "joyButton8"
        self.accept(str(num) + "_joyButton9-up",self.ButtonHit, [num, 9, 1])
        self.accept(str(num) + "_joyButton9-down",self.ButtonHit, [num, 9, 0])
        events[9] = "joyButton9"
        self.accept(str(num) + "_joyButton10-up",self.ButtonHit, [num, 10, 1])
        self.accept(str(num) + "_joyButton10-down",self.ButtonHit, [num, 10, 0])
        events[10] = "joyButton10"
        self.accept(str(num) + "_joyButton11-up",self.ButtonHit, [num, 11, 1])
        self.accept(str(num) + "_joyButton11-down",self.ButtonHit, [num, 11, 0])
        events[11] = "joyButton11"
        self.accept(str(num) + "_joyHatUp",self.ButtonHit, [num, 12, False])
        events[12] = "joyHatUp"
        self.accept(str(num) + "_joyHatDown",self.ButtonHit, [num, 13, False])
        events[13] = "joyHatDown"
        self.accept(str(num) + "_joyHatLeft",self.ButtonHit, [num, 14, False])
        events[14] = "joyHatLeft"
        self.accept(str(num) + "_joyHatRight",self.ButtonHit, [num, 15, False])
        events[15] = "joyHatRight"
        self.accept(str(num) + "_joyHatCenter",self.ButtonHit, [num, 16, False])
        events[16] = "joyHatCenter"
        return events
        
    def ButtonHit(self,control,button,up):
        # handle joystick button hits
        ## print button,up
        #Button 0 
        if (button == 0):
            if (up):  # UP
                print "button0 up for control", control
            else:     # DOWN
                print "button0 down for control", control
        #Button 1 
        elif (button == 1):
            if (up):  # UP
                print "button1 up for control", control
            else:     # DOWN
                print "button1 down for control", control
        #Button 2 
        elif (button == 2):
            if (up):  # UP
                print "button2 up for control", control
            else:     # DOWN
                print "button2 down for control", control
        #Button 3 
        elif (button == 3):
            if (up):  # UP
                print "button3 up for control", control
            else:     # DOWN
                print "button3 down for control", control
        #Button 4 
        elif (button == 4):
            if (up):  # UP
                print "button4 up for control", control
            else:     # DOWN
                print "button4 down for control", control
        #Button 5 
        elif (button == 5):
            if (up):  # UP
                print "button5 up for control", control
            else:     # DOWN
                print "button5 down for control", control
        #Button 6 
        elif (button == 6):
            if (up):  # UP
                print "button6 up for control", control
            else:     # DOWN
                print "button6 down for control", control
        #Button 7 
        elif (button == 7):
            if (up):  # UP
                print "button7 up for control", control
            else:     # DOWN
                print "button7 down for control", control
        #Button 8 
        elif (button == 8):
            if (up):  # UP
                print "button8 up for control", control
            else:     # DOWN
                print "button8 down for control", control
        #Button 9 
        elif (button == 9):
            if (up):  # UP
                print "button9 up for control", control
            else:     # DOWN
                print "button9 down for control", control
        #Button 10 
        elif (button == 10):
            if (up):  # UP
                print "button10 up for control", control
            else:     # DOWN
                print "button10 down for control", control
        #Button 11 
        elif (button == 11):
            if (up):  # UP
                print "button11 up for control", control
            else:     # DOWN
                print "button11 down for control", control
        
        
        #Button 12 - hat 
        elif (button == 12):
            print "button hat up for control", control
        #Button 13 - hat 
        elif (button == 13):
            print "button hat down for control", control
        #Button 14 - hat 
        elif (button == 14):
            print "button hat left for control", control
        #Button 15 - hat 
        elif (button == 15):
            print "button hat right for control", control
        #Button 16 - hat 
        elif (button == 16):
            print "button hat center for control", control
          

    def pollAxis(self,task):
        # poll the axis sticks on the joystick
        for i in range(4):
            for j in range(self.numSticks):
                ## # raw data - range -1to1
                ## self.js_axis[j][i] = self.js[j].getAxis(i)
                ## # inverted
                ## self.js_axis[j][i] = self.js[j].getAxis(i,True)
                ## # convert to range 0to2
                ## self.js_axis[j][i] = self.js[j].getAxis(i) + 1
                # rounded to two decimal places
                self.js_axis[j][i] = round(self.js[j].getAxis(i),2)
                print "joy", j,"axis", i, ":", self.js_axis[j][i]

        return task.again
    ## def axisCheck(self,task):
        ## if self.js_axis[0][0] > .2:
            ## self.cambase.getPos() +
         
    
##############################################################################        
    def startGame(self):
        self.createEnvironment()
        self.startTime()
        self.createUI()
        print "startGame"
        # Load models and player
 
    def createEnvironment(self):
        ## print "createEnvironment"
        # Loads aquarium and sets it so player is stuck in it.
        
        self.enviroNode = render.attachNewNode( "EnviroNode" )
        self.enviroNode.setScale(1)
        self.enviroNode.setPosHpr(0,0,-30,  0,0,0)
        # Load first fish example 
        self.fish1 = loader.loadModel("Models/flatYellowFishModel.egg")
        self.fish1 = Actor('Models/flatYellowFishModel.egg', {'swimming':'Models/flatYellowFishAnim.egg'})
        self.fish1.loop('swimming')
        self.fish1.reparentTo(self.enviroNode)
        ## self.fish1Tex = loader.loadTexture("Textures/pink.tif")
        ## self.fish1.setTexture(self.fish1Tex, 1)
        self.fish1.setScale(.5)
        self.fish1.setPos(100,100,10)
  
        # Load second fish example
        self.fish2 = loader.loadModel("Models/clownFishModel.egg")
        self.fish2 = Actor('Models/clownFishModel.egg', {'swimming':'Models/clownFishAnim.egg'})
        self.fish2.loop('swimming')
        self.fish2.reparentTo(self.enviroNode)
        ## self.fish2Tex = loader.loadTexture("Textures/red.tif")
        ## self.fish2.setTexture(self.fish2Tex, 1)
        self.fish2.setScale(.5)
        self.fish2.setPos(50,0,20)
       
        # Load third fish example
        self.fish3 = loader.loadModel("Models/smallSchoolFishModel.egg")
        self.fish3 = Actor('Models/smallSchoolFishModel.egg', {'swimming':'Models/smallSchoolFishAnim.egg'})
        self.fish3.loop('swimming')
        self.fish3.reparentTo(self.enviroNode)
        ## self.fish3Tex = loader.loadTexture("Textures/pink.tif")
        ## self.fish3.setTexture(self.fish3Tex, 1)
        self.fish3.setScale(.5)
        self.fish3.setPos(60,30,40)
        
        # Load fourth fish example
        self.fish4 = loader.loadModel("Models/lionFishModel.egg")
        self.fish4 = Actor('Models/lionFishModel.egg', {'swimming':'Models/lionFishAnim.egg'})
        self.fish4.loop('swimming')
        self.fish4.reparentTo(self.enviroNode)
        ## self.fish4Tex = loader.loadTexture("Textures/red.tiff")
        ## self.fish4.setTexture(self.fish4Tex, 1)
        self.fish4.setScale(.5)
        self.fish4.setPos(60,30,70)
        
        #Load Shrimp
        self.fish5 = loader.loadModel("Models/cleanerShrimpModel.egg")
        self.fish5 = Actor('Models/cleanerShrimpModel.egg', {'swimming':'Models/cleanerShrimpAnim.egg'})
        self.fish5.loop('swimming')
        self.fish5.reparentTo(self.enviroNode)
        ## self.fish5Tex = loader.loadTexture("Textures/red.tiff")
        ## self.fish5Tex.setTexture(self.fish5Tex, 1)
        self.fish5.setScale(.5)
        self.fish5.setPos(60, 30, 100)
        ## self.fish5.place()
        
        #Load Seahorse
        self.fish6 = loader.loadModel("Models/seaHorseModel.egg")
        self.fish6 = Actor('Models/seaHorseModel.egg', {'swimming':'Models/seaHorseAnim.egg'})
        self.fish6.loop('swimming')
        self.fish6.reparentTo(self.enviroNode)
        self.fish6.setScale(.5)
        self.fish6.setPos(60,30,50)
        
        # Loading in the first Toy Model
        self.toy1 = loader.loadModel("Models/car1.egg")
        self.toy1.reparentTo(self.enviroNode)
        ## self.toy1Tex = loader.loadTexture("Textures/red.tif")
        ## self.toy1.setTexture(self.toy1Tex, 1)
        self.toy1.setScale(.5)
        self.toy1.setPos(70,0,10)
        
        # Loading in the second Toy Model
        self.toy2 = loader.loadModel("Models/truck1.egg")
        self.toy2.reparentTo(self.enviroNode)
        ## self.toy2Tex = loader.loadTexture("Textures/red.tif")
        ## self.toy2.setTexture(self.toy1Tex, 1)
        self.toy2.setScale(.5)
        self.toy2.setPos(-30,0,10)
        
        
        # Load Aquarium Example
        self.aquarium = loader.loadModel("Models/aquarium_box.egg")
        self.aquarium.reparentTo(self.enviroNode)
        self.aquariumTex = loader.loadTexture("Textures/tank.png")
        self.aquarium.setTexture(self.aquariumTex, 1)
        self.aquarium.setScale(5)
        
        # Load Disk Plant
        self.diskPlant = loader.loadModel("Models/triDiskPlantModel.egg")
        self.diskPlant = Actor('Models/triDiskPlantModel.egg', {'swaying':'Models/triDiskPlantAnim.egg'})
        self.diskPlant.loop('swaying')
        self.diskPlant.reparentTo(self.enviroNode)
        ## self.diskPlantTex = loader.loadTexture("Textures/red.tif")
        ## self.diskPlant.setTexture(self.diskPlantTex, 1)
        self.diskPlant.setScale(.5)
        self.diskPlant.setPos(-100,-50,10)
        
        # Load Leafy Plant
        self.leafyPlant = loader.loadModel("Models/triLeafyPlantModel.egg")
        self.leafyPlant = Actor('Models/triLeafyPlantModel.egg', {'swaying':'Models/triLeafyPlantAnim.egg'})
        self.leafyPlant.loop('swaying')
        self.leafyPlant.reparentTo(self.enviroNode)
        ## self.leafyPlantTex = loader.loadTexture("Textures/red.tif")
        ## self.leafyPlant.setTexture(self.leafyPlantTex, 1)
        self.leafyPlant.setScale(.5)
        self.leafyPlant.setPos(70,0,10)
        
        #Load Coral
        self.coral = loader.loadModel("Models/coralStatic.egg")
        self.coral.reparentTo(self.enviroNode)
        self.coral.setScale(.5)
        self.coral.setPos(40,0,10)
        print "Load Coral"
        
        #Load Castle
        self.castle = loader.loadModel("Models/castleStatic.egg")
        self.castle.reparentTo(self.enviroNode)
        self.castle.setScale(.5)
        self.castle.setPos(-40,50,10)
        print "Load Castle"
        
        # Load Treasure Chest
        self.treasureChest = loader.loadModel("Models/treasureChestModel.egg")
        self.treasureChest = Actor('Models/treasureChestModel.egg', {'opening':'Models/treasureChestAnim.egg'})
        self.treasureChest.loop('opening')
        self.treasureChest.reparentTo(self.enviroNode)
        ## self.treasureChestTex = loader.loadTexture("Textures/red.tif")
        ## self.treasureChest.setTexture(self.treasureChestTex, 1)
        self.treasureChest.setScale(.5)
        self.treasureChest.setPos(0,70,10)
        
        
        # Test Load of Bubble
        self.bubble = loader.loadModel("Models/bubbleModel.egg")
        self.bubble = Actor('Models/bubbleModel.egg', {'floating':'Models/bubbleani.egg'})
        self.bubble.loop('floating')
        self.bubble.reparentTo(self.enviroNode)
        ## self.bubbleTex = loader.loadTexture("Textures/red.tif")
        ## self.bubble.setTexture(self.bubbleTex, 1)
        self.bubble.setScale(.5)
        self.bubble.setPos(0,70,30)
        
        # setup collisions - 
        # create the traverser and handler 
        base.cTrav = CollisionTraverser()
        if SHOW_C: base.cTrav.showCollisions(render)                          
        self.CollisionHandler = CollisionHandlerEvent()
        self.CollisionHandler.addInPattern('HitAnything')
        self.CollisionHandler.addAgainPattern('HitAnything')
        #add the player collider to the traverser 
        ########
        
    def hitSomething(self):
        print "hitSomething"
        # Checks for collisions between objects
        
    def createUI(self):
        self.ui = OnscreenImage(image = 'Textures/UIconcept1.png', pos = (0, 1, -.3), scale=1.35)
        self.ui.setTransparency(TransparencyAttrib.MAlpha)
        
        #Score
        self.score = 7
        self.scoreString = str(self.score)
        #Score Text
        self.scoreText= OnscreenText(text = '7', pos = (-.30, 0.5), scale = .35)
        print self.score
        self.score+= 0
        self.scoreString = str(self.score)
        self.scoreText['text']=self.scoreString
        
        #Bubbles
        self.bubbleMods = [None] * 5
        for i in range(5):
            self.bubbleMods = OnscreenImage(image = 'Textures/bubble.png', pos = (1, 2, .7), scale=.05)
            self.bubbleMods.setTransparency(TransparencyAttrib.MAlpha)
            self.bubbleMods2 = OnscreenImage(image = 'Textures/bubble.png', pos = (1.15, 2, .7), scale=.05)
            self.bubbleMods2.setTransparency(TransparencyAttrib.MAlpha)
            self.bubbleMods3 = OnscreenImage(image = 'Textures/bubble.png', pos = (1, 2, .58), scale=.05)
            self.bubbleMods3.setTransparency(TransparencyAttrib.MAlpha)
            self.bubbleMods4 = OnscreenImage(image = 'Textures/bubble.png', pos = (1.15, 2, .58), scale=.05)
            self.bubbleMods4.setTransparency(TransparencyAttrib.MAlpha)
            self.bubbleMods5 = OnscreenImage(image = 'Textures/bubble.png', pos = (1.075, 2, .46), scale=.05)
            self.bubbleMods5.setTransparency(TransparencyAttrib.MAlpha)
            
#Stopwatch
        self.secondsTime = 0
        self.minutesTime = 0
        self.time = self.formatTime(self.minutesTime, self.secondsTime)
        self.stopwatchText = OnscreenText(text=self.time, style = 1, fg =(.25, .2, .4, .5), pos = (-1.03, .5, 1), scale = .2)
        
    def startTime(self):
        self.firstPick = (-1, -1)
        f1 = Func(self.updateTime)
        print "Timer Started"
        self.s = Sequence(Wait(1), f1)
        self.s.loop()
        self.secondsTime = 0
        self.minutesTime = 0
    
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

        
    def update(self, task):
        # fish1AnimControl = self.fish1.getAnimControl('swimming')
        #self.fish1.loop('swimming')
        print "update"
        if self.score == 0:
            self.highScore()
        # Updates the game, should run as a task
        return task.cont
    
    def highScore(self):
        self.highScores = OnscreenImage(image = 'Textures/highscore.png', pos = (0, 1, -.3), scale=2)
        self.highScoreBackground.setTransparency(TransparencyAttrib.MAlpha)
        
    
    def bubbleShooter(self):
        print "bubbleShooter"
        #
class ToonMaker(DirectObject):
    def __init__(self):
        base.disableMouse()
        base.cam.node().getLens().setNear(10.0)
        base.cam.node().getLens().setFar(9999999)
        camera.setPos(0, -50, 0)
        
        # Check video card capabilities.
        
        if (base.win.getGsg().getSupportsBasicShaders() == 0):
            addTitle("Toon Shader: Video driver reports that shaders are not supported.")
            return
        
        # Enable a 'light ramp' - this discretizes the lighting,
        # which is half of what makes a model look like a cartoon.
        # Light ramps only work if shader generation is enabled,
        # so we call 'setShaderAuto'.

        tempnode = NodePath(PandaNode("temp node"))
        tempnode.setAttrib(LightRampAttrib.makeSingleThreshold(0.5, 0.4))
        tempnode.setShaderAuto()
        base.cam.node().setInitialState(tempnode.getState())
        
        # Use class 'CommonFilters' to enable a cartoon inking filter.
        # This can fail if the video card is not powerful enough, if so,
        # display an error and exit.
        
        self.separation = 1 # Pixels
        self.filters = CommonFilters(base.win, base.cam)
        filterok = self.filters.setCartoonInk(separation=self.separation)
        if (filterok == False):
            addTitle("Toon Shader: Video card not powerful enough to do image postprocessing")
            return
        
        # Create a non-attenuating point light and an ambient light.
        
        plightnode = PointLight("point light")
        plightnode.setAttenuation(Vec3(1,0,0))
        plight = render.attachNewNode(plightnode)
        plight.setPos(30,-50,0)
        alightnode = AmbientLight("ambient light")
        alightnode.setColor(Vec4(0.8,0.8,0.8,1))
        alight = render.attachNewNode(alightnode)
        render.setLight(alight)
        render.setLight(plight)
        
        # Panda contains a built-in viewer that lets you view the 
        # results of all render-to-texture operations.  This lets you
        # see what class CommonFilters is doing behind the scenes.
        
        self.accept("v", base.bufferViewer.toggleEnable)
        self.accept("V", base.bufferViewer.toggleEnable)
        base.bufferViewer.setPosition("llcorner")
        self.accept("s", self.filters.manager.resizeBuffers)
        
        # These allow you to change cartooning parameters in realtime
        
        self.accept("escape", sys.exit, [0])

t = ToonMaker()
w = World()
run()