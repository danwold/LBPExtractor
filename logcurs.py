import pickle
import datetime
import sys
import csv
import curses



class airplane:
##Airplane Class, for holding aircraft variables
        def __init__(self,typ,eng,cplx,cls,hp):
                self.typ = typ
                self.eng = eng
                self.cplx = cplx
                self.cls = cls
                self.hp = hp
        

class fleet:
##Fleet Class, to persistently hold records of different aircraft types
##passes aircraft instances to the entry class when entrys are formed
        def __init__(self):
                try:
			fleetfile = open('fleetfile','r')
                	self.fleet = pickle.load(fleetfile)
                	fleetfile.close
		except:
			fleetfile = open('fleetfile','w')
			self.fleet = []
			pickle.dump(self.fleet,fleetfile)
                	fleetfile.close()
			 

        def add(self,typ,eng,cplx,cls,hp):        
        ##adds aircraft to fleet        
                ap = airplane(typ,eng,cplx,cls,hp)
                self.fleet.append(ap)

        
        def out(self,index):
                
                return self.fleet[index]

        def search(self,searchstr):
                ##returns aircraft instance, if search string matches
                for ind in self.fleet:
                        if ind.typ == searchstr:
                                return ind
                

        def fleetlist(self):
                self.flist = []
                for f in self.fleet:
                         self.flist.append(f.typ)
                return self.flist

        def rmfleet(self):

                self.fleet.pop()

        def save(self):
                fleetfile = open('fleetfile','w')
                pickle.dump(self.fleet,fleetfile)
                fleetfile.close()
                
        
class entry:
##Entry class for logbook entrys. Takes aircraft instances, times, and dates
##DATE,AIRCRAFT MAKE & MODEL,AIRCRAFT IDENT,LEGS,ROUTE OF FLIGHT,DURATION
##,POINT TO POINT,PATROL,LANDINGS DAY,LANDINGS NIGHT,INSTRUMENT,
##SIMULATED INSTRUMENT,APPROACHES & TYPE,NIGHT,SIMULATOR,CROSS COUNTRY,SOLO,
##PILOT IN COMMAND,SECOND IN COMMAND,DUAL,INSTRUCTOR,FLIGHT COST,EXPENSES,REMARKS
        def __init__(self,month,day,year,airc,ident,legs,route,duration,pp,\
                     patrol,dlandings,nlandings,instrument,sinstrument,app,\
                     night,sim,cc,solo,pic,sic,dual,instructor,cost,expense\
                     ,remarks):

                self.date = datetime.date(year,month,day)
                self.aircraft = airc
                self.ident = ident
                self.legs = legs
                self.route = route
                self.duration = duration
                self.pp = pp
                self.patrol = patrol
                self.dlandings = dlandings
                self.nlandings = nlandings
                self.instrument = instrument
                self.sinstrument = sinstrument
                self.app = app
                self.night = night
                self.sim = sim
                self.cc = cc
                self.solo = solo
                self.pic = pic
                self.sic = sic
                self.dual = dual
                self.instructor = instructor
                self.cost = cost
                self.expense = expense
                self.remarks = remarks
                self.night = night
                self.instrument = instrument
        def printlocals(self):
            return locals()

def flconv(string):
        
        if string == '':
                return 0.0
        if string == ' ':
                return 0.0
        else:
                return float(string)
        

def rettotal(attrib,entlist):
##returns time totals from a list containing entries
        total = 0.0
        for f in entlist:
                total = total + flconv(getattr(f,attrib))
        return total
 

def retacmatch(attribute,matchey,entrlist):
##return entries matching ac attributes in a list,
##first is attribute name (str)
##second is desired match (str)
##third is input list 
        retlist = []
        if attribute != 'all':
                for f in entrlist:
                        if getattr(f.aircraft,attribute) == matchey:
                                retlist.append(f)
                return retlist
        if attribute == 'all':
                return entrlist

def rettimedelta(tdelta,inlist):
##returns list of entries within the timedelta (days)
        retlist = []
        
        if type(tdelta) == int:
                for f in inlist:
                        if datetime.timedelta(tdelta * -1)+ datetime.date.today() < f.date:
                                retlist.append(f)
                return retlist
## if 'all' is passed in, returns the original list
        if tdelta == 'all':
                return inlist

def retentrystr(dt):
        for f in logbook:
                if f.date == dt:
                        entrylinereturn = []
                        entrylinereturn.append(f.duration)
                        entrylinereturn.append(f.aircraft.typ)
                        entrylinereturn.append(f.date)
                        return entrylinereturn
                if f.date !=dt:
                        return 'no date found'

logbook = []

fl = fleet()

##read csv file into csv reader object
try:
	reader = csv.reader(open('log.csv','r'))
except:
	filerr = raw_input('log.csv not found, please enter filename of LBP csv file : ')
	reader = csv.reader(open(filerr,'r'))

##iterate reader to create logbook - split to form dates, and pass into
##datetime, and use a fleet search to pass airplane instances in to entry
##from a string search
for r in reader:
      a=entry(int(r[0].split('/')[0]),int(r[0].split('/')[1]),int(r[0].split('/')[2]),\
              fl.search(r[1]),r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],\
              r[10],r[11],r[12],r[13],r[14],r[15],r[16],r[17],r[18],r[19],\
              r[20],r[21],r[22],r[23])
      logbook.append(a)
loopctl = ''

screen = curses.initscr()

while loopctl != 't':
        
        screen.clear()
        screen.border(0)
        screen.addstr(1,1,'h for help, enter selection:')
        screen.refresh()
        astring = screen.getstr()

        if astring == 'q':
                curses.endwin()                
                break
        if astring == 'h':
                screen.addstr(4,5, 'any unselected time groups will default to "all"')
                screen.addstr(5,5, '------------------------------------------------')
                screen.addstr(6,5, '-time _ attribute for different types of time')
                screen.addstr(7,5, '-aircraft _ aircaft type for type time')
                screen.addstr(8,5, '-class _ aircraft class for class time')
                screen.addstr(9,5, '-inlast _ days for time in last x days')
                screen.addstr(10,5,'aclist print list of available airplanes')
                screen.refresh()
                screen.getch()

        ##intercept before the string split for other functions
        if astring == 'aclist':
                acindex = 5                
                for f in fl.fleetlist():
                        screen.addstr(acindex,3,f)
                        acindex = acindex +1
                screen.addstr(acindex+1,3,'Press Enter To Continue')            
                screen.refresh()                
                screen.getch()
        
        ##aslist is split string for attribute input       
        aslist = astring.split(' ')

        ##default values for untouched parsing
        totalctl = 'duration'
        acactl = 'all'
        tdctl = 'all'
        acmctl = ''
        classctl = ''

        ##parse string, set non default values to index +1 entries
        if '-time' in aslist:
                totalctl = aslist[aslist.index('-time')+1]

        if '-aircraft' in aslist:
                acactl = 'typ'
                acmctl = aslist[aslist.index('-aircraft')+1]       

        if '-inlast' in aslist:
                tdctl = 'all'
        ##try section for time if loops
                try:
                    if aslist[aslist.index('-inlast')+2] == 'months':
                        tdctl = int(aslist[aslist.index('-inlast')+1])*30
                    if aslist[aslist.index('-inlast')+2] == 'years':
                        tdctl = int(aslist[aslist.index('-inlast')+1])*365
                    if aslist[aslist.index('-inlast')+2] == 'days':
                        tdctl = int(aslist[aslist.index('-inlast')+1])
                    
                except: 
                    print 'except'
                    
        if '-entry' in aslist:
                datestring = aslist[aslist.index('-entry')+1]
                selectdate = datetime.date(int(datestring.split('-')[2]),int(datestring\
                .split('-')[0]),int(datestring.split('-')[1]))
                
                screen.addstr(3,3,str(retentrystr(selectdate)))
                screen.refresh()
                screen.getch()
        
        if '-class' in aslist:
                acmctl = aslist[aslist.index('-class')+1]
                acactl = 'cls'
        ##final display string, if conditional is to prevent string from
        ##displaying while aslist is empty
        if len(aslist) > 1 and '-entry' not in aslist:        
                screen.addstr(5,5, 'total {0} is {1}'.format(totalctl,rettotal(totalctl,retacmatch(acactl,acmctl,\
                rettimedelta(tdctl,logbook)))))
                screen.refresh()
                screen.getch()


fl.save()




