'''
Created on 11.08.2016

@author: BuXXe
'''

import time

class OBJ(object):

    def __init__(self):
        '''
        Constructor
        '''
        # Format: Dictionary of meterialname -> filename
        self.materials = {}
        
        self.vertices = []
        self.vertexTexcoord = []
        # keys are material names and values are lists of face definitions
        self.faces = {}
        
        self.facecount = 0
        self.version = "2.2"
        self.name = "Unnamed Model"
        self.author = "Anonymous"
        self.creationDate = time.strftime("%d.%m.%Y") 
        self.lighting = 1
        self.transform = [[1,0,0,0],[0,1,0,0],[0,0,1,0]]
       
        # bounding data
        self.bspheres = []
        self.bboxes = []