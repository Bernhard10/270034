// WordCount_BT.cpp: Hauptprojektdatei.

#include "stdafx.h"
#include<iostream>
#include<string>
#include <map>


using namespace std;
using namespace System;

int main()
{
	map<string,int> wortliste;
	multimap<int,string> geordnet;
	string w;
	int wmax=0;
	while (cin)
	{
		getline(cin,w);
		if (wortliste.find(w) == wortliste.end())
		{
			wortliste.insert(pair<string,int>(w, 1));
			if (wmax==0)
				wmax=1;
		}
		else
		{
			wortliste[w]+=1;
			if (wortliste[w]>wmax)
				wmax=wortliste[w];
		}
		if (w=="X")
			break;
	}
	for( map<string,int>::iterator ii=wortliste.begin(); ii!=wortliste.end(); ++ii)
	{
		geordnet.insert(pair<int,string>((*ii).second,(*ii).first));
	}
	pair<multimap<int, string>::iterator, multimap<int, string>::iterator> ppp;
	for (int z=wmax;z>0;z--)
	{
		ppp = geordnet.equal_range(z);
		for (multimap<int, string>::iterator it2 = ppp.first; it2 != ppp.second; ++it2)
		{
			cout <<  (*it2).second << ": " << (*it2).first <<"x"<< endl;
		}
	}
	system("pause");
    return 0;
}
