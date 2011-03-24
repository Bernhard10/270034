import sys, math, string
from copy import deepcopy
# Erwarteter Input (stdin): Eine Liste mit "[(string)Name, (int)dauer]",
# das Paar ["maximal",(int)zeit] (optional) definiert die maximale Zeit, die das Wandern brauchen darf.
# das Schlüsselwort ["end",(int)egal was] bricht das einlesen ab. Groß/Kleinschreibung egal
# Namen dürfen nicht doppelt vergeben werden, sonst wird nur der spätere behalten und der frühere überschrieben


agenten=dict() # Globales Dictionary agenten "deklarieren"
status=[] #Eine Globale Liste status wird "deklariert"
maxval=2147483647

def main():
    einlesen() #stdin wird eingelesen.
    grundstatus()
    schreiten()

def einlesen():
    global maxval
    for line in sys.stdin:
        position=0
        while position>=0:
            position=int(string.find(line,"[",position, len(line)-1))
            if position<0:
                break
            pos2=int(string.find(line,",",position,len(line)-1))
            name=line[position+1:pos2]
            position=int(string.find(line,"]",pos2,len(line)-1))
            dauer=int(line[pos2+1:position])
            if name.lower()=="end":
                return() #Bricht aus beiden Schleifen aus
            elif name.lower()=="maximal":
                maxval=dauer
            else:
                agenten[name]=dauer
    return()

#Der Grundstatus wird in die Liste Status geschrieben
# ein Status besteht aus Schrittzahl,[NamenLinkeSeite],[NamenRechteSeite],vergangeneZeit, [gemMoves]
def grundstatus():
    status.append([0,agenten.keys(),[],0,[]])


def schreiten():
    global maxval
    i=0
    while i<len(status):
        if status[i][0]%2==0:
            hingehen(i)
        else:
            if status[i][1]==[]:
                print str(status[i][3])+" Minuten:"
                print status[i][4]
                print "\n"
            else:
                zurueckgehen(i)
        i+=1;
    print "FERTIG"



#Fuehrt alle möglichen Schritt vom status[statind] aus und erzeugt dadurch neue statusse.
#Geht von links nach rechts!
def hingehen(statind):
    for ag in status[statind][1]:
        for ak in status[statind][1][status[statind][1].index(ag)+1:]: #für alle paare von 2 Agenten von der linken Seite
            neustat=deepcopy(status[statind])
            neustat[0]+=1
            neustat[1].pop(neustat[1].index(ag))
            neustat[1].pop(neustat[1].index(ak))
            neustat[2].append(ag)
            neustat[2].append(ak)
            if agenten[ag]<agenten[ak]:
                neustat[3]+=agenten[ak]
            else:
                neustat[3]+=agenten[ag]
            neustat[4].append(">"+ag)
            neustat[4].append(">"+ak)
            if neustat[3]<=maxval:
                status.append(neustat)
    return()


#Fuehrt alle möglichen Schritt vom status[statind] aus und erzeugt dadurch neue statusse.
#Geht von rechts nach links!
def zurueckgehen(statind):
    for ag in status[statind][2]:
        neustat=deepcopy(status[statind])
        neustat[0]+=1
        neustat[2].pop(neustat[2].index(ag))
        neustat[1].append(ag)
        neustat[3]+=agenten[ag]
        neustat[4].append("<"+ag)
        if neustat[3]<=maxval:
            status.append(neustat)
    return()

if __name__ == "__main__":
    main()
