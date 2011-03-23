#include <iostream>
#include <string>
#include <fstream>
#include <map>

using namespace std;

//von Benedikt Weirich
//Programm zur Erstellung einer Hashtabelle

int main()
{
    //Grundlegende Deklarationen
    ifstream text;
    string puffer;
    string wort;
    size_t buchstabe;
    size_t anfang;
    map<string,int> tabelle;
    //Hier wird die Datei geöffnet!
    text.open ("test.txt", fstream::in|fstream::out);
    if(text.is_open())
    {
        cout<<"Öffnen erfolgreich!\n";
    }
    else
    {
        cout<<"Öffnen nicht erfolgreich!\n!";
    }
    //Bis hier hin die Öffnungsroutine!
    while (!text.eof())
    {
        //Ab hier wird Zeilenweise eingelesen.
       getline(text, puffer);
       puffer.insert (puffer.end(),1,' ');
       //Hier werden die Satzzeichen gelöscht.
       buchstabe=puffer.find_first_of(".:,;!?&()1234567890-");
       //Hier wird der String in Kleinbuchstaben umgeschrieben
       for (int i=0;i<puffer.length();i++)
       {
            puffer[i]=tolower (puffer[i]);
        }
       while (buchstabe!=puffer.npos)
       {
            puffer[buchstabe]=' ';
            buchstabe=puffer.find_first_of(".:,;!?&()1234567890-",buchstabe+1);
        }
        //Hier wird der String in Worte zerlegt
        anfang=puffer.find_first_not_of(" ");
        buchstabe=puffer.find_first_of(" ",anfang+1);
        while (anfang!=puffer.npos)
        {
            wort=puffer.substr (anfang, buchstabe-anfang);
            anfang=puffer.find_first_not_of(" ",buchstabe+1);
            buchstabe=puffer.find_first_of(" ",anfang+1);
            //Hier werden die Wörter in die Hashtabelle eingeschrieben
            if (tabelle.end()==tabelle.find(wort))
            {
                tabelle[wort]=1;
            }
            else
            {
                tabelle[wort]++;
            }
        }
    }
    //Hier wird die Tabelle wieder ausgegeben
    map<string,int>::iterator it;
    for ( it=tabelle.begin() ; it!=tabelle.end(); it++)
    {
        cout << (*it).first << " => " << (*it).second << endl;
    }
    //Die Datei wird geschlossen
    text.close ();
    return 0;
}
