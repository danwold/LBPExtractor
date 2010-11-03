import pickle
import datetime
import sys
import csv
import curses
from bottle import route, run, request, template, debug

##comment 222

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
                fleetfile = open('fleetfile','r')
                self.fleet = pickle.load(fleetfile)
                fleetfile.close 

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
 
def retclsmatch(match,entrlist):
	retlist = []
        if match != 'all':
                for f in entrlist:
                        if f.aircraft.cls == match:
                                retlist.append(f)
                return retlist
        if match == 'all':
                return entrlist

def rettypmatch(match,entrlist):
##return entries matching ac attributes in a list,
##first is attribute name (str)
##second is desired match (str)
##third is input list 
        retlist = []
        if match != 'all':
                for f in entrlist:
                        if f.aircraft.typ == match:
                                retlist.append(f)
                return retlist
        if match == 'all':
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
aclist = fl.fleetlist()


##read csv file into csv reader object
reader = csv.reader(open('log.csv','r'))

##iterate reader to create logbook - split to form dates, and pass into
##datetime, and use a fleet search to pass airplane instances in to entry
##from a string search
for r in reader:
      a=entry(int(r[0].split('/')[0]),int(r[0].split('/')[1]),int(r[0].split('/')[2]),\
              fl.search(r[1]),r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],\
              r[10],r[11],r[12],r[13],r[14],r[15],r[16],r[17],r[18],r[19],\
              r[20],r[21],r[22],r[23])
      logbook.append(a)


acs = ''
@route('/hello', method='GET')
def mainpage():
	text = ''
	if request.GET.get('save','').strip():
	
        	totalctl = 'duration'
        	tdctl = 'all'
		aircraftmatch='all'
		classmatch = 'all'
		
		
			
        	totalctl = request.GET.get('typetime', '')
		aircraftmatch = request.GET.get('acbox','')	
		if aircraftmatch == 'all':
			classmatch = request.GET.get('classbox','')
			

		
        	acs =''
		      	
		        
                disptuple = rettotal(totalctl,rettypmatch(aircraftmatch,retclsmatch(classmatch,rettimedelta(tdctl,logbook))))

		text = '{0} is {1}'.format(totalctl,disptuple)
			
		return template('hello.html',text=text,aclist=aclist,acs=acs)		

	else:
		acs = ''
		return template('hello.html',text=text,aclist=aclist,acs=acs)

debug()       
run(reloader=True)
fl.save()




