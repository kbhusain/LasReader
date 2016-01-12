# Author: Kamran Husain 
# LAS 2.0 file reader. 
import os, sys, re 
  
mrc = re.compile(r'^~(S+)') 
mr4 = re.compile(r'^(w+ *).(S*)s+(S*):(.*)$') 
  
class pLASfile: 
        def __init__(self): 
                self.thisSection = None 
                self.sections = { } 
                self.inAscii = False 
                self.inCurve = False 
                self.curves = { } 
                self.curveNames = []  # in the order read from file. 
                self.data = [ ] 
 
        def sectionNames(self): 
                skeys = self.sections.keys();  skeys.sort() 
                return skeys 
 
  
        def showSection(self,sn):            
                skeys = self.sections[sn]['constants'].keys(); skeys.sort() 
                for sk in skeys: 
                        print sk, self.sections[sn]['constants'][sk] ,  self.sections[sn]['units'][sk]; 
                if sn == 'ASCII': 
                        print self.curveNames 
                        print self.curves.keys() 
 
  
        def readfile(self, fn): 
                rlines = open(fn,'r').readlines() 
                for rl in rlines: 
                        match = mrc.match(rl) 
                        # --- Determine the section number. 
                        if match: 
                                sn = match.group(1) 
                                self.sections[sn] = { 'constants' : {} , 'units' : {} ,  
                                                'comments' : {} , 'data': [] } 
                                self.thisSection = self.sections[sn] 
                                self.inAscii = False 
                                self.inCurve = False 
                                if sn == 'ASCII': self.inAscii = True 
                                if sn == 'CURVE': self.inCurve = True 
                                continue 
                                        
                                if self.inAscii: 
                                        rawdata = map(float,rl.strip().split()) 
                                        self.thisSection['data'].extend(rawdata) 
                                else: 
                                        match = mr4.match(rl) 
                                        if match: 
                                                c = match.group(1).strip() 
                                                self.thisSection['constants'][c] = match.group(2); 
                                                self.thisSection['units'][c] = match.group(3); 
                                                self.thisSection['comments'][c] = match.group(4); 
                                                if self.inCurve: 
                                                        self.curveNames.append(c) 
                                                        self.curves[c] = [ ] 
                        # -------------------------------------------------------------- 
                        # Now create the curve vectors .. I miss panda and numarray 
                                # -------------------------------------------------------------- 
                        columns = len(self.curveNames) 
                        rawdata = self.sections['ASCII']['data'] 
                        datalen = len(rawdata) 
                        rows  = int(datalen/columns) 
                        k = 0       
                        for j in range(rows): 
                                for i in range(columns): 
                                        self.curves[self.curveNames[i]].append(rawdata[k]) 
                                        k = k + 1 
  
                def getCurve(self,cname): 
                        if cname in self.curveNames: return       self.curves[cname] 
                        return [ ] 
 
                def getCurveNames(self): return self.curveNames[:] 
                                
  
if __name__ == '__main__': 
        obj = pLASfile() 
        obj.readfile(sys.argv[1]) 
        print obj.sectionNames() 
        # Sample calls 
        obj.showSection('ASCII') 
        # or curves and their data 
        for i in obj.getCurveNames():  
                print obj.getCurve(i) 
        print obj.getCurve('DEPT') 
        # This returns an empty set.  
        print obj.getCurve('JUNK')
