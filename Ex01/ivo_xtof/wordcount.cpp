/*
  Last changed Time-stamp: <2008-03-26 20:58:04 xtof>
  $Id$

  compile with: g++ -Wall wordcount.cpp -o wordcount
  test with:    lynx -dump http://www.tbi.univie.ac.at/Origin/origin_1.html \
                | ./wordcount                                               \
		| less
*/
#include <algorithm>
#include <iostream>
#include <iterator>
#include <map>
#include <string>
#include <vector>

namespace std {
  // define outstream operator for pairs in namespace std this is a
  // trick to fix a know name lookup problem in STL

  ostream& operator<<(ostream& os, const std::pair<std::string,int>& p) {
    os << p.second << " " << p.first << endl;

    return (os);
  }

}

/*================================================*/
void split_at(const std::string& str,
	      std::vector<std::string>& tokens,
              const std::string& delimiters) {
  
  // skip delimiters at beginning of str
  std::string::size_type lastPos = str.find_first_not_of(delimiters, 0);
  // find first "non-delimiter" in str
  std::string::size_type pos     = str.find_first_of(delimiters, lastPos);

  while (std::string::npos != pos || std::string::npos != lastPos) {
    // found a token, add it to the vector
    tokens.push_back(str.substr(lastPos, pos - lastPos));
    // skip delimiters (note the "not_of")
    lastPos = str.find_first_not_of(delimiters, pos);
    // find next "non-delimiter"
    pos = str.find_first_of(delimiters, lastPos);
  }
}

/*=================================================*/
bool lt_pair(const std::pair<std::string,int>& lhs,
	     const std::pair<std::string,int>& rhs) {

  // (2) sort by word
  if (rhs.second == lhs.second) return (lhs.first < rhs.first);

  // (1) sort by frequency
  return (rhs.second < lhs.second);
}

/*============*/
int main(void) {
  std::string line;
  std::map<std::string,int> freqs;

  // read line from stream stdin
  while (getline(std::cin, line)) {
    const std::string digits("0123456789");
    const std::string spaces(" \f\n\r\t\v");
    const std::string special("-=~!@#$%^&*()_+[]\\{}|;':\",./<>?");
    const std::string non_word_chars = spaces + digits + special; 

    std::vector<std::string> words;
    
    words.clear();
    // split line to words
    split_at(line, words, non_word_chars);

    std::vector<std::string>::iterator w;
    // iterate over words
    for (w = words.begin(); w != words.end(); w++) {
      // inplace transform word to lowercase
      std::transform(w->begin(), w->end(), w->begin(), tolower);
      // memorize word
      freqs[*w]++;
    }
  }

  std::vector<std::pair<std::string,int> > wc;
  // make vector wc a copy of the content of map freqs
  wc.assign(freqs.begin(), freqs.end());

  // sort vector of pairs 1st by frequency and 2nd by word 
  sort(wc.begin(), wc.end(), lt_pair);

  std::ostream_iterator<std::pair<std::string,int> > out_it(std::cout, "");
  // print vector of pairs to stream stdout 
  copy(wc.begin(), wc.end(), out_it);
  
  return (0);
}

// End of file
