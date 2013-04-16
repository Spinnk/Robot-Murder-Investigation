#mission.py
#this is the mission class, storing start and end flags, initialization information
#for item locations and NPC dialogue flags

class Mission:
    def __init__(self, mission_num):
        #self.mission_num stores which mission we are on, uses state
        self.mission_num = mission_num

        #load map items
        self.items = [] #[[x, y], item]
        if self.mission_num == 0:
            #tutorial mission, read in mission0.txt
            f = open("mission0.txt", 'rb')
        if self.mission_num == 1:
            #read mission1.txt
            f = open("mission1.txt", 'rb')
        if self.mission_num == 2:
            #read mission2.txt
            f = open("mission2.txt", 'rb')
        if self.mission_num == 3:
            #read mission3.txt
            f = open("mission3.txt", 'rb')
        #parse items
        #parse dialogue
        self.dialogue0 = [] #list of character0's dialogues. ["dialogue", [list of tags]]
        self.dialogue1 = []
        self.dialogue2 = []
        self.dialogue3 = []
        
        #parse ending trigger
        f.close()

    def getdialogue(self, npc):
        pass

    # function to create a journal entry based on a flag
    def createjournalentry(self, flag):
        pass
        




                           
        
        
