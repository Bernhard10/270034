#!/usr/bin/perl
# Last changed Time-stamp: <2008-04-03 21:58:07 xtof>
# $Id$
#
# synopsis: counts word frequencies; reads from stdin, writes to stdout
#
# usage:
# lynx -dump http://www.tbi.univie.ac.at/Origin/origin_1.html \
# | perl wordcount.pl                                         \
# | less
#

use strict;
use vars qw/%WC/;

# read line-by-line from stdin
while (<>) {
  # remove \n and canonicalize to lower case
  chomp; tr/A-Z/a-z/;
  # split at non-alphabetic characters filter out non-words and memorize words
  $WC{$_}++ for grep {length $_} split /[^a-zA-Z]/;
}

# sort hash keys by frequency and output key-value pairs
printf "%2d %s\n", $WC{$_}, $_  for sort {$WC{$b} <=> $WC{$a}
					  || $a cmp $b } keys %WC;
