import sys, math, string
from copy import deepcopy
# Erwarteter Input (stdin): Eine Liste mit "[(string)Name, (int)dauer]",
# das Paar ["maximal",(int)zeit] (optional) definiert die maximale Zeit, die das Wandern brauchen darf.
# das Schlüsselwort ["end",(int)egal was] bricht das einlesen ab. Groß/Kleinschreibung egal
# Namen dürfen nicht doppelt vergeben werden, sonst wird nur der spätere behalten und der frühere überschrieben


agenten=dict() # Globales Dictionary agenten "deklarieren"
status=[] #Eine Globale Liste status wird "deklariert"
maxval=2147483647
schnellster=1
zwschnellster=1

def main():
    global schnellster
    global zwschnellster
    einlesen() #stdin wird eingelesen.
    agl=sorted(agenten.values())
    schnellster=agl[0]
    zweitschnellster=agl[1]
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

    #Die Möglichkeit, der schnellste geht hin und her und nimmt alle mit, wird berechnet. Ist die Zeit kleiner maxval,
    #so wird maxval neu gesetzt.
    #Der Sinn ist, eine erste Abschätzung einer Obergrenze zu finden, falls keine sinnvolle angegeben.

    v=(len(agenten)-1)*schnellster
    for b in agenten.values():
        v+=b
    if v<maxval:
        maxval=v
        print "Berechnetes Maximum:" + str(v)

    #### HAUPTSCHLEIFE
    i=0
    while i<len(status):
        if status[i][0]%2==0:
            hingehen(i)
        else:
            if status[i][1]==[]:
                # Das Abbruchkriterium für ungünstige Pfade wird immer auf den aktuell günstigsten fertigen Pfad gesetzt.
                if status[i][3]<maxval:
                    maxval=status[i][3]
                    print str(status[i][3])+" Minuten:"
                    print status[i][4]
                    print "\n"
            else:
                zurueckgehen(i)
        i+=1;
    print "Anzahl ueberpruefter statusse:"
    print i
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
            #Nun wird abgeschätzt, wie lange man noch mindestens braucht.
            zuzeit=untere_schranke(neustat[1])
            #stimmt das folgende eh?
            if len(neustat[1])>0:
                zuzeit=zuzeit+schnellster #Der schnellste muss Taschenlampe nach links bringen, ehe untere Schranke gilt
            if neustat[3]+zuzeit<=maxval:
                status.append(neustat)
            else:
                pass
##                print "Ausgeschlossener Status:"
##                print neustat
##                print "Zuzeit:"
##                print zuzeit
##                print "\n"
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
        zuzeit=untere_schranke(neustat[1])
        if neustat[3]+zuzeit<=maxval:
            status.append(neustat)
        else:
            pass
##            print "Ausgeschlossener Status:"
##            print neustat
##            print "Zuzeit:"
##            print zuzeit
##            print "\n"
    return()

#Berechnet für den Status einen abgeschätzten Wert, der garantiert schneller ist
    # als alle möglichen Schrittkombinationen von dem Status aus zum Ziel.
    # Wenn gebrauchte Zeit plus diese Abschätzung schon zu langsam sind, dann muss dieser Zweig nicht weiter verfolgt werden.
def untere_schranke(leuteLi):
    #Jeder der links steht muss nach rechts. Da zwei zusammen gehen durch 2.
    # Die wahre Zeit ist immer größergleich der Durchschnitt der beiden
    #Außerdem müssen paarweise immer die nach rechts, die die Taschenlampe nach links gebracht haben
    #Schließlich muss einer die Taschenlampe nach links bringen
    z=0
    for agstr in leuteLi:
        z=z+agenten[agstr]
##    if len(leuteLi)==2:
##        print leuteLi
##        print "Summe ueber Leute= "+str(z)
    z=z/2
##    if len(leuteLi)==2:
##        print "Summe ueber Leute/2= "+str(z)
    z=z+zwschnellster*((len(leuteLi)-2)/2)
##    if len(leuteLi)==2:
##        print "zwei schnellste nach rechts= "+str(z)
    z=z+(len(leuteLi)-2)*schnellster
##    if len(leuteLi)==2:
##        print "ZuzeitGesamt= "+str(z)
    if z>0:
        return z #Frage: Rundet Python auf int automatisch ab?
    else:
        return 0


    

if __name__ == "__main__":
    main()
