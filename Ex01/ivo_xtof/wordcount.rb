#!/usr/bin/ruby
# Last changed Time-stamp: <2008-03-25 22:25:18 xtof>
# $Id$
#
# synopsis: counts word frequencies; reads from stdin, writes to stdout
#
# usage:
# lynx -dump http://www.tbi.univie.ac.at/Origin/origin_1.html \
# | ruby wordcount.rb                                         \
# | less
#

# create an empty hash, initialize default value to 0
freqs = Hash.new(0)

# read line-by-line from stdin
while line = gets
 # split line at non-alphabetic characters and filter out non-wordes
 words = line.chomp.split(/[^a-zA-Z]/).grep(/[a-zA-z]+/)
 # canonize words to lowercase and store them in hash
 words.each{|word| freqs[word.downcase] += 1}
end

# sort hash keys by frequency and output key-value pairs
freqs.sort_by{|x,y| y}.reverse.each{|word,freq| puts freq.to_s+' '+word}
