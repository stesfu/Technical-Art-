'''
Takes a given animation onto a 
given character and save the file via Python
'''
import maya.cmds 

def connect_attr(src, dst, attr):
    
    # give a source and a destination 
    # give an attr
    
    srcString = "{0}.{1}".format(src, attr)
    dstString = "{0}.{1}".format(dst, attr)

    maya.cmds.connectAttr(srcString, dstString, f = True)


import os 

def create_reference(file_path, ns):
    
    if not os.path.exists(file_path):
        
        maya.cmds.error("File does not exist: {0}".format(file_path))
        return
    
    maya.cmds.file(file_path, r = True, ns = ns)
 
    
    
def create_file_namespace(file_path):
    
     if not os.path.exists(file_path):
        
        maya.cmds.error("File does not exist: {0}".format(file_path))
        return
        
     file_path_dir, file_path_fullname = os.path.split(file_path) 
    
     file_path_name, file_path_ext = os.path.splitext(file_path_fullname)
     
     ns_file_path_name = "ns_" + file_path_name
    
     return ns_file_path_name
    

def get_joints_from_namespace(ns):
    
    return maya.cmds.ls("{0}:*".format(ns), type = "joint") 
    
    
def run():
    
    # Creates a new scene
    maya.cmds.file(new = True, force = True)
    
    # Create char and anim namespace
    char_path = "C:/Users/salem/Technical Art/sample_files/exercise/character.mb"
    anim_path = "C:/Users/salem/Technical Art/sample_files/exercise/animations/maya/01_01.ma"
    
    char_ns = create_file_namespace(char_path)
    anim_ns = create_file_namespace(anim_path)

    # Bring in character 
    #char_path = "" already def 
    create_reference(char_path, char_ns)
    
    # Bring in the animation 
    #anim_path = "" already def
    create_reference(anim_path, anim_ns)
    
    # Get a list of joints of both the anim and char
    
    char_joints = get_joints_from_namespace(char_ns)
    anim_joints = get_joints_from_namespace(anim_ns)
        
    # Determine Start and End times 
    start_time = maya.cmds.findKeyframe( anim_joints[0], which="first" )
    end_time = maya.cmds.findKeyframe(anim_joints[0], which="last")  
    
    # Change the the current time to the start time
    maya.cmds.currentTime(start_time)
    
    # Attach animation to character
    for anim_joint in anim_joints:
        for char_joint in char_joints:
            if(anim_joint.split(":")[-1] == char_joint.split(":")[-1] ):
               maya.cmds.parentConstraint( anim_joint, char_joint, mo = True )
               
    # Bake animation bones
    anim_joints = get_joints_from_namespace(anim_ns)
    
    maya.cmds.select(cl = True)
    maya.cmds.select(anim_joints)
    
    maya.cmds.bakeResults(simulation = True,
                          time = (start_time, end_time),
                          sampleBy = 1,
                          oversamplingRate = 1,
                          disableImplicitControl = True,
                          preserveOutsideKeys = True,
                          sparseAnimCurveBake = False,
                          removeBakedAnimFromLayer = False,
                          bakeOnOverrideLayer = False,
                          minimizeRotation = True,
                          controlPoints = False,
                          shape = True
                         )
                       
    # Remove a reference
    maya.cmds.file(anim_path, rr = True)
    
    # Save a file, figure out proper renaming (consider a helper function!!) 
    character_name = char_path.split("/")[-1][:-3]
    anim_file = anim_path.split("/")[-1][:-3]
    
    dir = "C:/Users/salem/Technical Art/sample_files/exercise/BakedAnim/"
    if not os.path.exists(dir):
        os.mkdir(dir)
    
    renamed_file = "C:/Users/salem/Technical Art/sample_files/exercise/BakedAnim/{0}_{1}.ma".format(character_name,anim_file)
    
    maya.cmds.file(rename = renamed_file)
    maya.cmds.file(save = True, f = True) 
    
run()