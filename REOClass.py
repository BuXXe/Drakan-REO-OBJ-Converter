'''
Created on 08.08.2016

@author: BuXXe
'''

import time

class REO(object):

    def __init__(self):
        '''
        Constructor
        '''
        self.version = "2.2"
        self.name = "Unnamed Model"
        self.author = "Anonymous"
        self.creationDate = time.strftime("%d.%m.%Y") 
        self.lighting = "1"
        self.transform = [[1,0,0,0],[0,1,0,0],[0,0,1,0]]
        
        # Format: List of Lists with each containing [Type, Filename]
        self.materials = []
        
        self.vertices = []
        self.faces = []
        self.vtentries = []
        
        # bounding data
        self.bspheres = []
        self.bboxes = []