'''
Takes a given animation onto a 
given character and save the file via Python and PyMel
'''
import maya.cmds 
import pymel.core
import os 

def create_reference(file_path, ns):
    
    if not os.path.exists(file_path):
        
        pymel.core.error("File does not exist: {0}".format(file_path))
        return
    
    pymel.core.createReference(file_path, ns = ns)
 
    
    
def create_file_namespace(file_path):
    
     if not os.path.exists(file_path):
        
        pymel.core.error("File does not exist: {0}".format(file_path))
        return
        
     file_path_dir, file_path_fullname = os.path.split(file_path) 
    
     file_path_name, file_path_ext = os.path.splitext(file_path_fullname)
     
     ns_file_path_name = "ns_" + file_path_name
    
     return ns_file_path_name
    

def get_joints_from_namespace(ns):
    
    return maya.cmds.ls("{0}:*".format(ns), type = "joint") 
    #return pymel.core.ls("{0}:*".format(ns), type = "joint") 


def batchAnimation():

    path = os.getenv("ANIM_FILE_PATH")
    
    dirs = os.listdir(path)
    
    for file in dirs:
        
        run(file)

    
    
    
def run(fileName):
    
    print fileName
    
    # Creates a new scene
    pymel.core.newFile(force = True)
    
    # Create char and anim namespace
    char_path = "C:/Users/salem/Technical Art/sample_files/exercise/character.mb"
    anim_path = "C:/Users/salem/Technical Art/sample_files/exercise/animations/maya/" + fileName
    
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
    start_time = pymel.core.findKeyframe( anim_joints[0], which="first" )
    end_time = pymel.core.findKeyframe(anim_joints[0], which="last")  
    
    # Change the the current time to the start time
    pymel.core.currentTime(start_time)
    
    # Attach animation to character
    for anim_joint in anim_joints:
        for char_joint in char_joints:
            if(anim_joint.split(":")[-1] == char_joint.split(":")[-1] ):
               pymel.core.animation.parentConstraint( anim_joint, char_joint, mo = True )
               
    # Bake animation bones
    anim_joints = get_joints_from_namespace(anim_ns)
    
    maya.cmds.select(cl = True)
    maya.cmds.select(anim_joints)
    maya.cmds.select(char_joints)
    
    pymel.core.animation.bakeResults(simulation = True,
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
    #anim_reference.remove()
    
    # Save a file, figure out proper renaming (consider a helper function!!) 
    character_name = char_path.split("/")[-1][:-3]
    anim_file = anim_path.split("/")[-1][:-3]
    
    dir = "C:/Users/salem/Technical Art/sample_files/exercise/BakedAnim/"
    if not os.path.exists(dir):
        os.mkdir(dir)
    
    renamed_file = "C:/Users/salem/Technical Art/sample_files/exercise/BakedAnim/{0}_{1}".format(character_name,fileName)
    
    maya.cmds.file(rename = renamed_file)
    maya.cmds.file(save = True, f = True) 

animFile = "01_01.ma"
run(animFile)

#batchAnimation()