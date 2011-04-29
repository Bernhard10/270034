
import sys
import argparse
import string
import copy
_verbosity=5

def main(argv):
    global _verbosity
    
## Comandline optionen verarbeiten
    parser=argparse.ArgumentParser(description="Loest das Manhattan tourist problem. Die Strassen werden von stdin gelesen.")
    parser.add_argument("-v", nargs=1, type=int , help="Setzt den Verbositylevel zur angegebenen Zahl default=5, maximum=12, minimum=1. Fuer große Inputfils wird maximal 6, eventuell 7 empfohlen. ")
    args=parser.parse_args()
    if args.v!=None:
        _verbosity=args.v[0]


## StdIn auslesen
    p("Lese von stdin...",6)
    mode=-1
    streets=[[],[]] #0 für E-->W, 1 für N-->S
    # Straßen einlesen
    for line in sys.stdin:
        p("Neue Zeile wird von stdin gelesen...",8)
        if "# west-east streets" in line:
            mode=0
        elif "# north-south streets" in line:
            mode=1
        else:
            zeile=[]
            stri=""
            for ch in line:
                if ch in "0123456789":
                    stri += ch
                elif ch in string.whitespace:
                    if stri!="":
                        zeile.append(int(stri))
                        stri=""
            if zeile !=[]:
                streets[mode].append(zeile)
    if _verbosity>=9:
        for i in range(0,len(streets)):
            print i
            print streets[i]
    p("Einlesen von stdin beendet",6)

    #Angabe ueberpruefen


    

    # Initialisieren einer leeren Ecken-Liste der richtigen Größe
    ecke=leereEckenListe(streets, [None,""])
    p("Eckenarray initialisiert",7)
    p("Anzahl Zeilen: "+ str(len(ecke)),8)
    p("Anzahl Spalten: "+ str(len(ecke[1])),8)
    p("Ecken:",9)
    pe(ecke,9)

    # Setzte die Ecke links oben gleich null.
    ecke[0][0][0]=0
    #linker Rand
    for i in range (1,len(ecke)):
        p("Linker Rand: i= " + str(i),10)
        p("Streets[0][i-1][0]="+str(streets[1][i-1][0]),11)
        p("Ecke[i]="+str(ecke[i]),12)
        p("Ecke[i][0]="+str(ecke[i][0]),12)
        p("Ecke[i][0][0]="+str(ecke[i][0][0]),12)
        ecke[i][0][0]=ecke[i-1][0][0]+streets[1][i-1][0]
        ecke[i][0][1]=ecke[i-1][0][1]+"V"
        p("ecke=",11)
        pe(ecke,11)
    #oberer Rand
    for i in range (1,len(ecke[0])):
        p("oberer Rand: i= " + str(i),10)
        ecke[0][i][0]=ecke[0][i-1][0]+streets[0][0][i-1]
        ecke[0][i][1]=ecke[0][i-1][1]+">"
        p("ecke=",11)
        pe(ecke,11)
    p("Ausgangslage hergestellt: Eckenliste mit Rand links und oben erledigt.",6)
    p("Ecken:",9)
    pe(ecke,9)

    p("Fuelle das Gitter Zeilenweise, linksoben beginnend auf.",6)
    for i in range(1,len(ecke)):
        for j in range (1, len(ecke[i])):
            p("Berechne horizontalen und vertikalen Weg zur Ecke ["+str(i)+","+str(j)+"]",7)
            p("hor=Ecke[i][j-1]: "+str(ecke[i][j-1][0])+" + strasse[0][i][j-1]: "+str(streets[0][i][j-1]),10)
            hor=ecke[i][j-1][0]+streets[0][i][j-1]
            p(hor,8)
            p("ver=Ecke[i-1][j]: "+str(ecke[i-1][j][0])+" + strasse[1][i-1][j]: "+str(streets[1][i-1][j]),10)
            ver=ecke[i-1][j][0]+streets[1][i-1][j]
            p(ver,8)
            if hor>ver:
                p("Horizontal gewinnt",7)
                ecke[i][j][0]=hor
                ecke[i][j][1]=ecke[i][j-1][1]+">"
            elif ver>hor:
                p("Vertikal gewinnt",7)
                ecke[i][j][0]=ver
                ecke[i][j][1]=ecke[i-1][j][1]+"V"
            else:
                p("beide egal",7)
                ecke[i][j][0]=hor
                ecke[i][j][1]="entw: ("+ecke[i][j-1][1]+"> oder: "+ecke[i-1][j][1]+"V)"
            p("Pfad zur Ecke ["+str(i)+","+str(j)+"]: " +str(ecke[i][j][1]),11)
            p("Alle Ecken",11)
            pe(ecke,11)
    p("Alle Ecken" + str(ecke),9)
    p("FERTIG",6)
    p("Beste Wege:",6)
    p(ecke[len(ecke)-1][len(ecke[0])-1][1],6)
    p("Gewicht des besten Weges:",5)
    p(ecke[len(ecke)-1][len(ecke[0])-1][0],5)
    Pfadausgabe(ecke[len(ecke)-1][len(ecke[0])-1][1], streets)
        
def leereEckenListe(streets, w):
    ecke=[]
    for i in range(0,len(streets[0])):
        ecke.append([])
        for j in range(0, len(streets[0][0])+1):
            ecke[i].append(copy.copy(w))
    return ecke


def Pfadausgabe(stri, streets):
    p(stri,8)
    kurzstri=""
    if _verbosity>=3:
        ecken=leereEckenListe(streets,".")
        i=0
        j=0
        status=0
        ecken[0][0]="*"
        for ch in stri:
            if ch==">":
                j=j+1
                p("Bereite Ecke "+str(i)+","+str(j)+"vor...",10)
                ecken[i][j]="*"
                if status==0:
                    kurzstri=kurzstri+ch
            elif ch=="V":
                i=i+1
                p("Bereite Ecke "+str(i)+","+str(j)+"vor...",10)
                ecken[i][j]="*"
                if status==0:
                    kurzstri=kurzstri+ch
            elif ch=="e":
                i=0
                j=0
            elif ch=="o":
                i=0
                j=0
                status=status+1
            elif ch==")":
                status=status-1
        p("Fuer graphische Darstellung vorbereitete Matrix:"+str(ecken),9)
        print("\n\n")
        for i in range(0,len(ecken)):
            for j in range(0,len(ecken[0])):
                print(ecken[i][j]),
            print
        p("\n\nFERTIG",6)
    else:
        status=0
        i=0
        j=0
        for ch in stri:
            if ch==">":
                j=j+1
                if status==0:
                    kurzstri=kurzstri+ch
            elif ch=="V":
                i=i+1
                if status==0:
                    kurzstri=kurzstri+ch
            elif ch=="e":
                i=0
                j=0
            elif ch=="o":
                i=0
                j=0
                status=status+1
            elif ch==")":
                status=status-1
    print("\n Empfohlener Weg: " + kurzstri)

    
        
                
def pe(li,lev):
    if _verbosity>=lev:
        print("\n")
        for i in range(0,len(li)):
            for j in range(0,len(li[0])):
                print(li[i][j][0]),
            print
        print "\n\n"





    
    
## VerbosityLevels:
##        0=nur 1 Zeile
##        5=default
##        6= Fortschrittsmeldungen
##        7=Detaillierte Fortschrittsmeldungen
##        8=Debug
##        9=Detaillierte Daten u Listen ausgeben
##        10=jede Kleinigkeit
def p(obj,lev):
    if _verbosity>=lev:
        print obj














if __name__ == "__main__":
    main(sys.argv[1:])
