import sys
sys.path.append("../../")

from appJar import gui
import os
import math

import numpy as np
import matplotlib.pyplot as plt

r11=-1
r22=-1
c11=-1
c22=-1
cs11=-1
cs22=-1
t_in_pri=-1
t_in_sec=-1
pvol=-1
leng  = -1
brea = -1
pr = -1
px = -1
rl= -1
zeq = -1
k = -1
class data:
    k = 0.00
    m = 0.00
    n = 0.00
    def __init__(self,f,s,t):
        print ("hey")
        self.k=f
        self.m=s
        self.n=t

dm14=data(0.005980,1.320,2.210)
dm16=data(0.001190,1.410,2.180)
dm60=data(0.000788,1.410,2.240)
dh14=data(4.8667e-7,1.26,2.52)
dh16=data(3.0702e-7,1.25,2.55)
dh60=data(2.0304e-7,1.23,2.56)
mpp={14:dm14,16:dm16,60:dm60}
hf={14:dh14,16:dh16,60:dh60}

def logoutFunction():
    return app.yesNoBox("Confirm Exit", "Are you sure you want to exit?")


def getting1 (btn):
    global leng
    global brea
    print (app.getEntry ("length"),app.getEntry ("breadth"))
    if (btn == "Set"):
        if (app.getEntry ("length")!=""):
            leng = (float) (app.getEntry ("length"))
        else:
            leng = -1
        if (app.getEntry ("breadth")!=""):
            brea = (float) (app.getEntry ("breadth"))
        else:
            brea = -1
        print (leng," ",brea)
    elif (btn == "Clear"):
        print ("working")
        brea = -1
        leng = -1
        print (leng," ",brea)

def getturns(btn):
    global t_in_pri
    global t_in_sec
    global pvol
    global rl
    if btn == "Clear ":
        app.clearEntry("turnsin1")
        app.clearEntry("turnsin2")
        app.clearEntry ("voltage")
        app.clearEntry ("load")
        t_in_pri=0.00
        t_in_sec=0.00
        pvol=0.00
        rl = 0
        print (t_in_pri,t_in_sec,pvol,rl)
        app.setEntryFocus("turnsin1")
    elif btn == "Enter ":
        if (app.getEntry("turnsin1")!=""):
            t_in_pri = float (app.getEntry ("turnsin1"))
        else:
            t_in_pri = 0;
        if (app.getEntry("turnsin2")!=""):
            t_in_sec = float (app.getEntry ("turnsin2"))
        else:
            t_in_sec = 0;
        if (app.getEntry ("voltage")!=""):
            pvol = float (app.getEntry ("voltage"))
        else:
            pvol =  0;
        if (app.getEntry ("load")!=""):
            rl = (float) (app.getEntry ("load"))
        else:
            rl = 0
        print (t_in_pri,t_in_sec,pvol,rl)

#app.infoBox("Success", "Successfully Entered\n Please Goto Next Tab :)")

def toolbar(btn):
    print(btn)
    if btn == "EXIT": app.stop()
    elif btn == "FILL": app.setTabBg("Tabs", app.getTabbedFrameSelectedTab("Tabs"), app.colourBox())
    elif btn == "FULL-SCREEN":
        if app.exitFullscreen():
            app.setToolbarIcon("FULL-SCREEN", "FULL-SCREEN")
        else:
            app.setGeometry("fullscreen")
            app.setToolbarIcon("FULL-SCREEN", "FULL-SCREEN-EXIT")

def changeTab(tabName):
    print("Changing to: ", tabName)
    app.setTabbedFrameSelectedTab("Tabs", tabName)
    print("done")

def func (tabName):
    if (tabName == "About"):
        new  = gui ("About ","300x200")
        new.setBg ("grey")
        new.addLabel ("def","EECE-270\n\nLab Project\n\nSEC-A GROUP-03\n\nMaj Arafat,FC Ashraf,Jim,\n\nShanto,Asif,Farhanaz :)")
        new.go()

def getoption (btn):
    if (app.getOptionBox ("Core Material")=="Solid Iron Core"):
        print ("Works")
    else:
        print ("works even more")
    print (app.getOptionBox ("Winding Material"))
    
def launch(win):
    app.showSubWindow(win)


def graph(formula, x_range):  
    x = np.array(x_range)  
    y = formula(x)
    plt.xlim(900, 2000)
    plt.ylim(0,1)
    plt.plot(x, y,color='#0066FF')  
    plt.show()  

def my_formula(x):
    global zeq
    global k
    return ((((x/(zeq+x)) * pvol)/k)/x)

def getresult (btn):
    global zeq
    global k
    if (btn == "Calculate"):
        print ("working")
        global t_in_pri
        global t_in_sec
        global pvol
        global leng
        global brea
        if (app.getOptionBox ("Winding Material    ")=="Copper(18 AWG)"):
            pr  = 0.021
            px = pr * (2 / 100)
        elif (app.getOptionBox ("Winding Material    ")=="Copper(10 AWG)"):
            pr =  0.00328
            px = pr * (2 / 100)
        print (t_in_pri,t_in_sec,pvol,leng,brea)
        peri = 2*leng + 2*brea;
        #peri = 4*leng
        ri = peri * pr * t_in_pri
        r2 = peri * pr * t_in_sec
        xi = peri * px * t_in_pri
        x2 = peri * px * t_in_sec
        k = t_in_pri/t_in_sec
        r1 = k * k * r2
        ro = ri - r1
        x1 = k * k* x2
        xo = xi - x1
        r2p = k * k * r2
        x2p = k * k * x2
        req = r1 + r2p
        xeq = x1 + x2p
        zeq = math.sqrt (req * req + xeq * xeq)
        v2p = (rl/(zeq+rl)) * pvol
        v2 = v2p / k
        i2 = v2 / rl
        i1 = i2 / k
        culoss = i1 * i1 * r1 + i2 * i2 * r2
        c = pvol * i1 - v2 * i2
        vol = leng * leng * brea *4
        
        coloss = 0
        permi = 4e-7*3.1416
        if (app.getOptionBox ("Select Permeability")=="14" and app.getOptionBox ("Core Material          ")=="Molypermalloy Powder Cores"):
            n = (14*permi*t_in_pri*i1)/(2*0.002)
            print ("flux density",n)
            coloss  = dm14.k * pow (50,dm14.m) * pow (n,dm14.n)
        elif (app.getOptionBox ("Select Permeability")=="16" and app.getOptionBox ("Core Material          ")=="Molypermalloy Powder Cores"):
            n = (16*permi*t_in_pri*i1)/(2*0.002)
            print ("flux density",n)
            coloss  = dm16.k * pow (50,dm16.m) * pow (n,dm16.n)
        elif (app.getOptionBox ("Select Permeability")=="60" and app.getOptionBox ("Core Material          ")=="Molypermalloy Powder Cores"):
            n = (60*permi*t_in_pri*i1)/(2*0.002)
            print ("flux density",n)
            coloss  = dm60.k * pow (50,dm60.m) * pow (n,dm60.n)
        if (app.getOptionBox ("Select Permeability")=="14" and app.getOptionBox ("Core Material          ")=="High Flux Powder Cores"):
            n = (14*permi*t_in_pri*i1)/(2*0.002)
            print ("flux density",n)
            coloss  = dh14.k * pow (50,dh14.m) * pow (n,dh14.n)
        elif (app.getOptionBox ("Select Permeability")=="16" and app.getOptionBox ("Core Material          ")=="High Flux Powder Cores"):
            n = (16*permi*t_in_pri*i1)/(2*0.002)
            print ("flux density",n)
            coloss  = dh16.k * pow (50,dh16.m) * pow (n,dh16.n)
        elif (app.getOptionBox ("Select Permeability")=="60" and app.getOptionBox ("Core Material          ")=="High Flux Powder Cores"):
            n = (60*permi*t_in_pri*i1)/(2*0.002)
            print ("flux density",n)
            coloss  = dh60.k * pow (50,dh60.m) * pow (n,dh60.n)
        #coloss = culoss * vol * 100
        v2 = round (v2,5)
        i2 = round (i2,5)
        i1 = round (i1,5)
        culoss = round (culoss,5)
        coloss = round (coloss,7)
        app.clearLabel("svoutp")
        app.clearLabel("pcoutp")
        app.clearLabel("scoutp")
        app.clearLabel("clossp")
        app.clearLabel ("corelp")
        print (v2,i2,i1,coloss)
        app.setLabel("svoutp",v2 )
        app.setLabel ("scoutp",i2)
        app.setLabel ("pcoutp",i1)
        app.setLabel ("clossp",culoss)
        app.setLabel ("corelp",coloss)
    elif (btn == "Graph"):
        print ("working More")
        x = np.arange(1600.0,1200.0,960.0)
        print ("rl",rl,"zeq",zeq,"k",k)
        t1= my_formula (rl)
        t2= my_formula (200.0)
        t3= my_formula (60.0)
        print (t3,t2,t1)
        plt.plot([60,200,400], [t3,t2,t1])
        plt.title ("Current vs. Load Resistance (Transformer)")
        plt.xlabel ("Load Resistance ->")
        plt.ylabel ("Current ->")
        plt.title ("Current vs. Load Resistance (Transformer)")
        plt.show()

#read from here :) :)
app = gui("Transformer Simulator","600x400")
app.setTransparency(200)
app.setIcon ("icon.ico")
app.showSplash("EECE-270 LAB PROJECT SEC-A GROUP-03\n MAJ ARAFAT,FC ASHRAF,JIM,\nSHANTO,ASIF,FARHANAZ",fill="red",stripe="black",fg="white",font=44)
app.setFont(12)
app.addToolbar(["EXIT","FILL","FULL-SCREEN"], toolbar, findIcon=True)
app.addMenuPreferences(toolbar)
app.addMenuItem("File", "EXIT", toolbar, shortcut="Control-x", underline=2)
app.addMenuItem("File", "FILL", toolbar, shortcut="Control-f", underline=2)
app.addMenuItem("File", "FULL-SCREEN", toolbar, shortcut="Control-m", underline=2)
app.addMenuItem ("Tabs","Core Windings",changeTab)
app.addMenuItem ("Tabs","Turns and Primary Voltage",changeTab)
app.addMenuItem ("Tabs","Outputs and Graph",changeTab)
app.addMenuItem ("Help","About",func)
app.addMenuItem ("Help","Git",func)
app.addMenuWindow()
app.addMenuHelp(toolbar)

#app.setMenuIcon ("File","EXIT","EXIT","right")
#app.setMenuIcon ("File","FILL","FILL","right")

app.startTabbedFrame ("Tabs")


#new tab
app.startTab ("Turns and Primary Voltage")
app.setBg ("brown")
app.setSticky ("New")
app.startLabelFrame ("Enter Data")
app.setSticky ("ew")
app.addLabel ("tt1","Primary Coil Turns",0,0)
app.addEntry ("turnsin1",0,1)
app.addLabel ("tt2","Secondary Coil Turns",1,0)
app.addEntry ("turnsin2",1,1)

app.addLabel ("pt","Primary Voltage",3,0)
app.addEntry ("voltage",3,1)
app.addLabel ("rrl","Load Resistance",4,0)
app.addEntry ("load",4,1)
app.setEntryFocus("turnsin1")
app.addButtons(["Enter ", "Clear "], getturns, 5, 1, 2)
app.stopLabelFrame()
app.stopTab()
#close tab



app.startTab ("Core Windings")
app.setBg ("salmon")
#app.setStretch("column")
#app.setPadding([10,10])
app.addLabel ("aaa","            Select Core Materials",0,0)
app.addLabelOptionBox("Core Material          ", ["Molypermalloy Powder Cores", "High Flux Powder Cores"],1,0)
app.addLabelOptionBox("Select Permeability", ["14", "16","60"],2,0)

app.addLabel ("em","",3,0)

app.addLabel ("aaaa","           Select Winding Materials",4,0)
app.addLabelOptionBox("Winding Material    ", ["Copper(18 AWG)", "Copper(10 AWG)"],6,0)
app.addLabel ("msg1","Enter Length of the Core",7,0,1)
app.addEntry ("length",7,1)
app.addLabel ("msg3","Enter breadth of the Core",9,0,1)
app.addEntry ("breadth",9,1)
app.addButtons (["Set","Clear"],getting1,11,1,2)
app.stopTab()



app.startTab ("Outputs and Graph")
app.setBg ("brown");
app.startLabelFrame ("Outputs")
app.addLabel ("svout","Secondary Voltage",1,0)
app.addLabel ("svoutp","0",1,1)
app.addLabel ("scout","Secondary Current",2,0)
app.addLabel ("scoutp","0",2,1)
app.addLabel ("pcout","Primary Current",3,0)
app.addLabel ("pcoutp","0",3,1)
app.addLabel ("closs","Copper loss",4,0)
app.addLabel ("clossp","0",4,1)
app.addLabel ("corel","Core Loss",5,0)
app.addLabel ("corelp","0",5,1)
app.stopLabelFrame()
app.addButtons(["Calculate","Graph"], getresult, 6, 0,2)
#stop tab



app.setStopFunction(logoutFunction)
app.go()
