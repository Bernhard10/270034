# -*- coding: utf-8 -*-
#"""
#Created on Sun Mar 20 22:28:30 2011

#@author: Benedikt
#"""
#Hier den Dateipfad eingeben!
file = open ('/Vorlesung/Test.txt','r')
#Hier wird die Datei eingelesen
puffer = file.read()
#Hier werden alle Buchstaben in Kleinbuchstaben geändert
puffer = puffer.lower()
#Diese Schleife entfernt alle Satzzeichen
case={'.',',','!','?',';','&','\'','(',')','-'}
for i in case:
    puffer=puffer.replace(i,"")
#Hier wird der String in einzelne Wörter zerlegt
puffer= puffer.split()
#Hier wird die Hashtabelle angelegt
hash={}
#Hier wird die Hashtabelle gefüllt
for x in puffer:
    if not(hash.has_key(x)):
        k=1
    if hash.has_key(x):
        k=k+1
    hash[x]=k
#Ausgabe der Hashtabelle
print hash.items()
file.close()
