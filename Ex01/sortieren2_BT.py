import sys, math, string
wortliste=dict()
o_list=[]
n_list=[]
# Liest die Namensliste ein
for line in sys.stdin:
    if line[len(line)-1]=="\n":
        line=line[0:len(line)-1]
    if line in wortliste:
        wortliste[line]+=1
    else:
        wortliste[line]=1
# fuegt Wort für Wort an der richtigen Position (nach frequenz) in eine neue Liste ein
for wortZ in wortliste.keys():
    for i in range(len(o_list)):
        if wortliste[wortZ] < n_list[i]:
            o_list.insert(i,wortZ)
            n_list.insert(i,wortliste[wortZ])
            break
    else:
        o_list.append(wortZ)
        n_list.append(wortliste[wortZ])
# druckt alle worte aus
for i in range(len(o_list)):
    print o_list[i]+": "+str(n_list[i])
    
