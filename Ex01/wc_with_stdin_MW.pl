#! /usr/bin/perl -w

use strict;
use warnings;

my %hash =();
my @tmp;
my $i;
my $m = 0;
my @array;


while (<>) 
{
    while ( /(\w['\w-]*)/g ) 
    {
        $array[$m] = lc($1);
        $m++;
    }
};

@tmp = sort(@array);
chomp(@tmp);


for ( $i = 0; $i <= $#tmp -1; $i++)
{
    if  (($tmp[$i] ne $tmp[$i+1]) || ($tmp[$i] eq $tmp[$i+1]))
    {
        $hash{$tmp[$i]} += 1;
    }
};

foreach my $key(keys(%hash))
{
	print $key." = ".$hash{$key}."\n"
};

print $tmp[$#tmp]." = 1 \n";

