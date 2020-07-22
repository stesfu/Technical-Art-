# Import statements
import maya.cmds
import random

cube = maya.cmds.polyCube()[0]
sphere = maya.cmds.polySphere()[0]
cone = maya.cmds.polyCone() [0]

# Grab time slider start and end
startTime = maya.cmds.playbackOptions(query = True, min = True)
endTime = maya.cmds.playbackOptions(query = True, max = True)

# Set current time to time slider start
maya.cmds.currentTime(startTime)

# Create list and set counter 
shapes = [cube, sphere, cone]
counter = 0

while counter < 5:

    for shape in shapes:
        
        # Select shape
        maya.cmds.select(shape, r = True)
        
        # Set the keyframe
        maya.cmds.setKeyframe(shape)
        
        # Edit the current time
        maya.cmds.currentTime(random.randint(startTime, endTime))
        
        # Move the shape 
        maya.cmds.setAttr(shape + ".translateX", random.randint(0,15))
        maya.cmds.setAttr(shape + ".translateY", random.randint(0,15))
        maya.cmds.setAttr(shape + ".translateZ", random.randint(0,15))
        
        # Set another keyframe
        maya.cmds.setKeyframe()
    counter += 1


