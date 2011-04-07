#! /usr/bin/perl -w
# Algorithmen und Programmentwicklung für Biologische Chemiker
# Working start at: March 28, 2011 3:05:53 PM GMT+02:00

use warnings;
use strict;

####################################################################################
# Four persons (fig1..fig2) want to cross a bridge, they all need different time to
# walk across, one always has to return and bring torch back. Which order should they
# go if the total time should be < 60min?
# Strategie: Try random combinations until one is below 60 min
# -> code doesn't exclude futile tries ->  would be nice if it does though
# the code should avoid failed attempts, but for that I have to rewrite a lot of it, 
# so this is just a first try
####################################################################################

my $fig1 = '5';                                         # figures assigned with their time
my $fig2 = '10';
my $fig3 = '20';                    
my $fig4 = '25';

my @arrayL = ("$fig1", "$fig2", "$fig3", "$fig4");      # arrayL = before crossing bridge
my @arrayR = ();                                        # arrayR = after crossing bridge
my @history = ();                                       # history of the moves

my ($a, $b, $number_of_tries_counter);
my $costs = 100;

while ($costs > 60)                                     # loop terminates if costs < 60 min
{
    while ($#arrayL >= 0)                               # terminates when nobody is in arrayL
    {
        $b = int(rand(($#arrayL + 1)));                 # pick randome guys for going
        $a = int(rand(($#arrayL + 1)));                 # together over bridge
                                       
        if ($a != $b )
        {
            my $tmp1 = splice(@arrayL, $a, 1);          # if not same guy -> remove toys
            my $tmp2 = splice(@arrayL, ($b-1), 1);      # from arrayL and assigne them
                                                        # variable tmp1 and tmp2
            push(@arrayR, $tmp1, $tmp2);                # push both guys at the end of
            push(@history, $tmp1, $tmp2);               # arrayR and history
                       
####################################################################################
# Just to print out the names of the persones
####################################################################################

                
                if ($tmp1 == 5)
                {
                    print "\n"."1. Person ist Buzz (t=5min). \n";
                }
                elsif ($tmp1 == 10)
                {
                    print "\n"."1. Person ist Woody (t=10min). \n";
                }
                elsif ($tmp1 == 20)
                {
                    print "\n"."1. Person ist Rex (t=20min). \n";
                }
                else
                {
                    print "\n"."1. Person ist Hamm (t=25min). \n";
                };
                
                 if ($tmp2 == 5)
                {
                    print "2. Person ist Buzz (t=5min). \n";
                }
                elsif ($tmp2 == 10)
                {
                    print "2. Person ist Woody (t=10min). \n";
                }
                elsif ($tmp2 == 20)
                {
                    print "2. Person ist Rex (t=20min). \n";
                }
                else
                {
                    print "2. Person ist Hamm (t=25min). \n";
                };
            
####################################################################################
                    
            if (defined($arrayR[3]))                    # if arrayR[position 3] is defined, then
            {                                           # all toys are over the bridge
                last;                                   # and loop should terminate
            }
            else
            {
                my $c = int(rand(($#arrayR +1)));       # random integer between amount of guys
                                                        # who are over the bridge and zero 
                
####################################################################################
# Just to print out the names of the persone - not very elegant, but it works
# just to remind myself: use reference in array and not variables!
####################################################################################       
                
                         if ($arrayR[$c] == 5)
                         {
                            print "\t --> Person die zurückgeht ist Buzz (t=5min). \n";
                         }
                         elsif ($arrayR[$c] == 10)
                         {
                           print "\t --> Person die zurückgeht ist Woody (t=10min). \n"
                         }
                         elsif ($arrayR[$c] == 20)
                         {
                             print "\t --> Person die zurückgeht ist Rex (t=20min). \n"
                         }
                         else
                         {
                              print "\t --> Person die zurückgeht ist Hamm (t=25min). \n"
                         };
                         
####################################################################################       

                 
                my $d = splice(@arrayR, $c , 1 );       # $d is now the toy which goes back
                push(@arrayL, $d);                      # 
                push(@history, $d);                     # delete guy who goes back from array
            };                                          # which represents "over bridge" state
        }                                               # push him back to "before bridge" and
        else                                            # write him in history 
        {
            next;                                       # out of loop, new randome numbers
        };                                              # this happens, when both randome numbers
                                                        # are the same $a == $b
    };                                                  
  
    my @all_history = @history;                         # rewrite all history!  -> to print it 
    for (my $counter = 0; $counter <=  5; )             # history used to calculate costs
    {
        if ($history[$counter] < $history[($counter +1)])
        {
            splice(@history, $counter, 1)               # delete always the faster guy of 
        }                                               # the two going together over bridge
        else                                            # 
        {                                               # 
            splice(@history, ($counter +1), 1)
        };
        
        $counter += 2;
    };
    
    $costs = $history[0]+$history[1]+$history[2]+$history[3]+$history[4];
    my %history_hash = ($costs => "@all_history");
    $number_of_tries_counter++;
    foreach my $key (keys(%history_hash)) 
    {
    print "\n -> Zeit: $key - Versuch Nummer: $number_of_tries_counter \n $history_hash{$key} \n\n";
    print "#"x50,"\n";
    };
    @history = ();                                      # now undo all changes made to 
    @arrayL = ("$fig1", "$fig2", "$fig3", "$fig4");     # states and start over again
    @arrayR = ();                                       # -> there might be a more graceful methode
};

