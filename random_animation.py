# Import statements
import maya.cmds

import random

# Grab time slider start and end
startTime = maya.cmds.playbackOptions(query = True, min = True)
endTime = maya.cmds.playbackOptions(query = True, max = True)

# Set current time to time slider start
maya.cmds.currentTime(startTime)

# Create empty list 
shapes = []; 

# Set counter 
counter = 0

while counter < random.randint(5, 10):
    
    # Generate primitives and append to list
    shapes.append(maya.cmds.polyCube()[0])
    shapes.append(maya.cmds.polySphere()[0])
    shapes.append(maya.cmds.polyCone()[0])
    shapes.append(maya.cmds.polyTorus()[0])

    for shape in shapes:
        
        # Select shape
        maya.cmds.select(shape, r = True)
        
        # Set the keyframe
        maya.cmds.setKeyframe(shape)
        
        # Edit the current time
        maya.cmds.currentTime(random.randint(startTime, endTime))
        
        # Move the shape 
        maya.cmds.setAttr(shape + ".translateX", random.randint(0,25))
        maya.cmds.setAttr(shape + ".translateY", random.randint(0,25))
        maya.cmds.setAttr(shape + ".translateZ", random.randint(0,25))
        
        # Set another keyframe
        maya.cmds.setKeyframe()
    
    # Increment counter     
    counter += 1


