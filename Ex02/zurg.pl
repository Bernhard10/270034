#!/usr/bin/perl
# -*-Perl-*-
# Last changed Time-stamp: <2008-05-09 14:37:30 xtof>
# $Id$

use Data::Dumper;
use Getopt::Long;
use Pod::Usage;
use strict;
use vars qw/$DEPTH $EXHAUSTIVE $MAXCOST %STATE %TOYS $VERBOSE/;
use warnings;

# defaults for global(s)
%TOYS = ( Buzz  =>  5,
	  Woody => 10,
	  Rex   => 20,
	  Hamm  => 25,
	  xtof  => 30,
	  ivo   =>  7 );

# initial state
%STATE = ( history  => [],
	   left     => [keys %TOYS],
	   right    => [],
	   cost     => 0,
	   lightpos => 'L' );

# initial maximal cost
$MAXCOST = 9999999;

# toggles
$EXHAUSTIVE = 0;
$VERBOSE = 0;

# process command-line
pod2usage(-verbose => 0)
    unless GetOptions(
      "toys=s"     => sub { %TOYS = split(':', $_[1]);
			    $STATE{left} = [keys %TOYS] },
      "exhaustive" => \$EXHAUSTIVE,
      "help"       => sub{pod2usage(-verbose => 1)},
      "man"        => sub{pod2usage(-verbose => 2)},      
      "maxcost=i"  => \$MAXCOST,
      "verbose"    => sub{ $VERBOSE++ }
      );

# main
print "Optimal cost is ", solve(\%STATE), "\n";
print Dumper(\%STATE);

#---
sub solve {
  my $s = shift;
  $DEPTH++;
  die if $DEPTH>20;
  print "$DEPTH: @{$s->{left}} | @{$s->{right}} $s->{cost}\n" if $VERBOSE >=2;

  $DEPTH--, return 0 unless @{$s->{left}};
  my $mvs = moves($s);
  my $best = 999999999;
  my $curr = $s->{cost};
  my %bstate;
  
  foreach my $m (@$mvs) {
    unless ($EXHAUSTIVE) {
      next if $m->[0] + $curr > $MAXCOST;
    }
    my %state = apply_move($s, $m);
    my $cost = $m->[0] + solve(\%state);
    print "$DEPTH: @$m + @{[$cost-$m->[0]]} = $cost\n" if $VERBOSE;
    $best = $cost, %bstate = %state if $cost<$best;
    $MAXCOST = $best + $curr if $MAXCOST > $best + $curr;
  }
  
  %$s = %bstate;
  $DEPTH--;
  return $best;
}

#---
# state, move -> updated_state
#---
sub apply_move {
  my %state =  %{shift()};
  my @m = @{shift()};
  my ($from, $to) = ($state{lightpos} eq 'L')
                  ? ('left','right')
		  : ('right','left');

  # update cost
  $state{cost} += shift @m;

  # update toys left/right of bridge according to move
  foreach my $t (@m) {
    $state{$from} = [ grep {! m/$t/} @{$state{$from}} ];
    $state{$to}   = [ @{$state{$to}}, $t ];
  }

  # update flashlight position
  $state{lightpos} = ($state{lightpos} eq 'L') ? 'R' : 'L';
  # update move history
  $state{history}  = [ @{$state{history}}, [ @m ] ];

  return %state;
}

#---
# state -> [move1, move2, ..., moveN]
#---
sub moves {
  my $state = shift();
  my @moves = ();

  if ($state->{'lightpos'} eq 'L') {
    # flashlight is on the left, therefore all subsets of cardinality
    # two of the set of toys left of the bridge form the legal moves.
    push @moves, all_pairs($state->{'left'});
  }
  else {
    # flashlight is on the right, therefore all subsets of cardinality
    # one of the set of toys right of the bridge form the legal moves.
    push @moves, map {[$TOYS{$_},$_]} @{$state->{right}};
  }

  return \@moves;
}

#---
# generates all combinations of 2 out of N array elements.
# ---
sub all_pairs {
  my $array = shift;
  my @combis = ();
  foreach my $idx1 (0 .. $#$array) {
    my $t1 = $array->[$idx1];
    foreach my $t2 (@{$array}[$idx1+1..$#$array]) {
      push @combis, [max($TOYS{$t1}, $TOYS{$t2}), $t1, $t2];
    }
  }

  return @combis;
}

#---
sub max {
  return ($_[0]>$_[1]) ? $_[0] : $_[1];
}

=pod

=head1 NAME

zurg.pl - solves "Escape from Zurg" problems

=head1 SYNOPSIS

zurg.pl [[-exhaustive] [-maxcost I<INT>] [-man] [-help] [-toys I<STRING>]]

=head1 OPTIONS

=over 4

=item B<-exhaustive>

Make search exhaustive.

=item B<-help>

Show synopsis.

=item B<-maxcost> I<INT>

Set maximal cost of solution to I<INT>.

=item B<-man>

Show man page.

=item B<-toys> I<STRING>

Set toys list. e.g.  -toys Buzz:5:Woody:10:Rex:20:Hamm:25

=item B<-verbose>

Toggle on verbose mode.
    
=back
    
=head1 DESCRIPTION

The "Escape from Zurg" problem reads as follows:

Buzz, Woody, Rex, and Hamm have to escape from Zurg.a They merely have
to cross one last bridge before they are free. However, the bridge is
fragile and can hold at most two of them at the same time. Moreover,
to cross the bridge a flashlight is needed to avoid traps and broken
parts. The problem is that our friends have only one flashlight with
one battery that lasts for only 60 minutes (this is not a typo:
sixty). The toys need different times to cross the bridge (in either
direction):

 +-------+------------+
 |  TOY  |    TIME    | 
 +=======+============+
 | Buzz  |  5 minutes |
 +-------+------------+
 | Woody | 10 minutes |
 +-------+------------+
 | Rex   | 20 minutes |
 +-------+------------+
 | Hamm  | 25 minutes |
 +-------+------------+
    
Since there can be only two toys on the bridge at the same time, they
cannot cross the bridge all at once. Since they need the flashlight to
cross the bridge, whenever two have crossed the bridge, somebody has
to go back and bring the flashlight to those toys on the other side
that still have to cross the bridge.  The problem now is: In which
order can the four toys cross the bridge in time (that is, in 60
minutes) to be saved from Zurg?

=head1 AUTHORS

Ivo Hofacker, Christoph Flamm
    
=head1 LITERATURE

 Martin Erwig "Escape from Zurg: an exercise in logic programming",
 J Func Prog, 14:(3) 253-261 (2004); doi: 10.1017/S0956796804005040

=cut

__END__
