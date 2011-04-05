import sys, math, string
from copy import deepcopy
# Erwarteter Input (stdin): Eine Liste mit "[(string)Name, (int)dauer]",
# das Paar ["maximal",(int)zeit] (optional) definiert die maximale Zeit, die das Wandern brauchen darf.
# das Schlüsselwort ["end",(int)egal was] bricht das einlesen ab. Groß/Kleinschreibung egal
# Namen dürfen nicht doppelt vergeben werden, sonst wird nur der spätere behalten und der frühere überschrieben
# Mit ["printall",1] werden alle gleich schnellen Permutationen ausgedruckt, sonst nur eine willkürliche davon
# Alternativ kann ["flags",1] angegeben werden. Das spätere Argument überschreibt das vorherige!!!
# Mit ["movefastestback",1] oder  indem man flags angibt und 2 zum Wert dazuzählt,kann man einstellen, dass automatisch immer der schnellste von rechts zurück geht.
# Damit wird meistens trotzdem die beste Lösung gefunden. Ich glaube zwar, es wird immer die beste Lösung gefunden, kann es aber nicht beweisen, daher ist es optional


agenten=dict() # Globales Dictionary agenten "deklarieren"
status=[] #Eine Globale Liste status wird "deklariert"
maxval=2147483647
schnellster=1
zwschnellster=1
id_nr=dict()
numbered_status = dict()
flags=0
## flags%2=1: Printall


def main():
    global schnellster
    global zwschnellster
    global id_nr
    einlesen() #stdin wird eingelesen.
    agl=sorted(agenten.values())
    schnellster=agl[0]
    zweitschnellster=agl[1]
    id_nr=id_nummer() #Jedem Agenten wird eine Nummer der Form 2 hoch n zugewiesen
    grundstatus()
    schreiten()

def id_nummer():
    i=1
    ids=dict()
    for k in agenten.keys():
        ids[k]=2**i
        i=i+1
    return ids
    
def einlesen():
    global maxval
    global flags
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
            elif name.lower()=="printall":
                if dauer==1:
                    if flags%2==0:
                        flags=flags+1
                elif dauer==0:
                    if flags%2==1:
                        flags=flags-1
            elif name.lower()=="movefastestback":
                if dauer==1:
                    if flags%4<2:
                        flags=flags+2
                elif dauer==0:
                    if flags%4>=2:
                        flags=flags-2
            elif name.lower()=="flags":
                flags=dauer
            else:
                agenten[name]=dauer
    return()

#Der Grundstatus wird in die Liste Status geschrieben
# ein Status besteht aus Schrittzahl,[NamenLinkeSeite],[NamenRechteSeite],vergangeneZeit, [gemMoves]
def grundstatus():
    status.append([0,agenten.keys(),[],0,[]])
    numbered_status[statusnummer(0,agenten.keys())]=status[0]

def statusnummer(z,aglist):
    statnr=z%2
    for ag in aglist:
        statnr=statnr+id_nr[ag]
    return statnr

## Hier wird geprüft, ob der stat schon vorhanden
## ich wollte vermeiden, dazu über alle statusse zu loopen, daher hab ich das dictionary numbered_status eingeführt.
## Weiß nicht, ob das sinnvoll ist oder zu chaotisch wird...
def neuer_stat(test_status): 
    snr=statusnummer(test_status[0],test_status[1])
    if snr in numbered_status:
        if numbered_status[snr][3]>test_status[3]:
            numbered_status[snr][3]=test_status[3]
            numbered_status[snr][4]=test_status[4]   
        elif numbered_status[snr][3]==test_status[3]: 
            numbered_status[snr][4].append("oder:")
            numbered_status[snr][4].append(test_status[4])

    else:
        status.append(test_status)
        numbered_status[snr]=status[-1]


        

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
                    ausgeben(status[i][4])
                    print "\n"
            else:
                zurueckgehen(i)
        i+=1;
    print "Anzahl ueberpruefter statusse:"
    print str(i) 
    print "FERTIG"


## Schreibt den schnellsten Pfad auf.
def ausgeben(schrittliste):
    perm=0
    if flags%2==1:
        print schrittliste
    else:
        shortlist=[]
        i=0
        while i < len(schrittliste):
            if "oder:" in schrittliste[i]:
                i=i+2
            else:
                shortlist.append(schrittliste[i])
                i=i+1
        print shortlist






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
                neuer_stat(neustat)
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
    if flags%4<2:
        for ag in status[statind][2]:
            neustat=deepcopy(status[statind])
            neustat[0]+=1
            neustat[2].pop(neustat[2].index(ag))
            neustat[1].append(ag)
            neustat[3]+=agenten[ag]
            neustat[4].append("<"+ag)
            zuzeit=untere_schranke(neustat[1])
            if neustat[3]+zuzeit<=maxval:
                neuer_stat(neustat)
            else:
                pass
    else:
        time=2147483647
        schn=""
        for ag in status[statind][2]:
            if agenten[ag]<time:
                schn=ag
                time=agenten[ag]
        neustat=deepcopy(status[statind])
        neustat[0]+=1
        neustat[2].pop(neustat[2].index(schn))
        neustat[1].append(schn)
        neustat[3]+=agenten[schn]
        neustat[4].append("<"+schn)
        zuzeit=untere_schranke(neustat[1])
        if neustat[3]+zuzeit<=maxval:
            neuer_stat(neustat)
        else:
            pass



        

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
