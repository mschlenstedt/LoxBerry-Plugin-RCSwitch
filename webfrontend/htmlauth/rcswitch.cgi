#!/usr/bin/perl

# Copyright 2016 Michael Schlenstedt, michael@loxberry.de
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


##########################################################################
# Modules
##########################################################################

use CGI::Carp qw(fatalsToBrowser);
use CGI qw/:standard/;
use File::HomeDir;
use Cwd 'abs_path';
use Config::Simple;
#use warnings;
#use strict;
#no strict "refs"; # we need it for template system

##########################################################################
# Read Settings
##########################################################################

# Version of this script
our $version = "0.0.5";

# Figure out in which subfolder we are installed
our $psubfolder = abs_path($0);
$psubfolder =~ s/(.*)\/(.*)\/(.*)$/$2/g;

our $home = File::HomeDir->my_home;
our $cfg           = new Config::Simple("$home/config/system/general.cfg");
our $installfolder = $cfg->param("BASE.INSTALLFOLDER");
our $pcfg          = new Config::Simple("$home/config/plugins/$psubfolder/RCSwitch.cfg");
our $transPIN      = $pcfg->param("general.TransmissionPIN");

##########################################################################
# Main program
##########################################################################

print "Content-Type: text/plain\n\n";

# Everything from URL
foreach (split(/&/,$ENV{'QUERY_STRING'}))
{
  ($namef,$value) = split(/=/,$_,2);
  $namef =~ tr/+/ /;
  $namef =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $value =~ tr/+/ /;
  $value =~ s/%([a-fA-F0-9][a-fA-F0-9])/pack("C", hex($1))/eg;
  $query{$namef} = $value;
}

# Get parameters
if ( $query{'family'} ne "" ) {
  our $family = $query{'family'};
  $family = substr($family,0,1);
  $family =~ tr/A-Z/a-z/; # all lower case
  if ( $family !~ /[a-p]/ ) {
    $family = "";
  }
} else {
  our $family = "";
}

if ( $query{'group'} ne "" ) {
  our $group = $query{'group'};
  $group = substr($group,0,8);
  if ( $group !~ /[0-9]/ ) {
    print "Wrong group number. Giving up.";
    exit;
  }
} else {
  print "Missing group number. Giving up.";
  exit;
}

if ( $query{'unit'} ne "" ) {
  our $unit = $query{'unit'};
  $unit = substr($unit,0,5);
  $unit =~ tr/A-Z/a-z/; # all lower case
  if ( $unit eq "a") {$unit = "1";};
  if ( $unit eq "b") {$unit = "2";};
  if ( $unit eq "c") {$unit = "3";};
  if ( $unit eq "d") {$unit = "4";};
  if ( $unit eq "e") {$unit = "5";};
  if ( $unit !~ /[0-9]/ ) {
    print "Wrong unit number. Giving up.";
    exit;
  }
} else {
  print "Missing unit number. Giving up.";
  exit;
}

if ( $query{'command'} ne "" ) {
  our $command = $query{'command'};
  if ( $command eq "on" ) {
    $command = "1";
  }
  if ( $command eq "off" ) {
    $command = "0";
  }
  $command = substr($command,0,1);
  if ( $command !~ /[0-9]/ ) {
    print "Wrong command. Giving up.";
    exit;
  }
} else {
  print "Missing command. Giving up.";
  exit;
}

if ( $query{'all'} ne "" ) {
  our $all = $query{'all'};
  $all = substr($all,0,1);
  if ( $all !~ /[0-1]/ ) {
    print "Wrong parameter for 'all'. Giving up.";
    exit;
  }
} else {
   our $all = "0";
}

if ( $query{'protocol'} ne "" ) {
  our $protocol = $query{'protocol'};
  if ( $protocol !~ /[A-Za-z0-9]/ ) {
    print "Wrong protocol. Giving up.";
    exit;
  }
} else {
  #print "Missing protocol. Giving up.";
  #exit;
  # Backward compatibility for old versions prior 0.9 (no protocol parameter)
  our $protocol = "elro";
}

if ( $query{'pulselength'} ne "" ) {
  our $pulselength = $query{'pulselength'};
  if ( $pulselength !~ /[0-9]/ ) {
    print "Wrong pulse length. Giving up.";
    exit;
  }
  $pulselength = "-pl=" . $pulselength;
}

our $send = 0;

if ( $protocol eq "elro" ) {

  # Send command with rcswitch - do this 3 times to make sure the command could be received
  # Note: Family isn't needed for Elro, but is used here for backward compatibility for old version prior 0.9 (no protocol parameter and therefore
  # standard is "elro"
  print "/usr/bin/sudo $installfolder/data/plugins/$psubfolder/bin/send433 -p=$transPIN $pulselength $family $group $unit $command\n\n";
  our $output = qx(/usr/bin/sudo $installfolder/data/plugins/$psubfolder/bin/send433 -p=$transPIN $pulselength $family $group $unit $command 2>&1);
  if ( $? ne 0 ) {
    $send = 1;
    print "ERROR - Somehting went wrong. Could not send command. This is the error message: ";
  } else {
    $send = 1;
    print "OK:\n";
    our $output1 = qx(/usr/bin/sudo $installfolder/data/plugins/$psubfolder/bin/send433 -p=$transPIN $pulselength $family $group $unit $command 2>&1);
    our $output2 = qx(/usr/bin/sudo $installfolder/data/plugins/$psubfolder/bin/send433 -p=$transPIN $pulselength $family $group $unit $command 2>&1);
  }

}

if ( $protocol eq "arctechv1" ) {

  # Send command with rcswitch - do this 3 times to make sure the command could be received
  # Note: Family isn't needed for Elro, but is used here for backward compatibility for old version prior 0.9 (no protocol parameter and therefore
  # standard is "elro"
  print "/usr/bin/sudo $installfolder/data/plugins/$psubfolder/bin/send433 -p=$transPIN $pulselength $family $group $unit $command\n\n";
  our $output = qx(/usr/bin/sudo $installfolder/data/plugins/$psubfolder/bin/send433 -p=$transPIN $pulselength $family $group $unit $command 2>&1);
  if ( $? ne 0 ) {
    $send = 1;
    print "ERROR - Somehting went wrong. Could not send command. This is the error message: ";
  } else {
    $send = 1;
    print "OK:\n";
    our $output1 = qx(/usr/bin/sudo $installfolder/data/plugins/$psubfolder/bin/send433 -p=$transPIN $pulselength $family $group $unit $command 2>&1);
    our $output2 = qx(/usr/bin/sudo $installfolder/data/plugins/$psubfolder/bin/send433 -p=$transPIN $pulselength $family $group $unit $command 2>&1);
  }

}

if ( $protocol eq "arctechv2" ) {

  # Send command with rcswitch - do this 3 times to make sure the command could be received
  # Note: Family isn't needed for Elro, but is used here for backward compatibility for old version prior 0.9 (no protocol parameter and therefore
  # standard is "elro"
  print "/usr/bin/sudo $installfolder/data/plugins/$psubfolder/bin/send433 -p=$transPIN $pulselength $group $all $unit $command\n\n";
  our $output = qx(/usr/bin/sudo $installfolder/data/plugins/$psubfolder/bin/send433 -p=$transPIN $pulselength $group $all $unit $command 2>&1);
  if ( $? ne 0 ) {
    $send = 1;
    print "ERROR - Somehting went wrong. Could not send command. This is the error message: ";
  } else {
    $send = 1;
    print "OK:\n";
    our $output1 = qx(/usr/bin/sudo $installfolder/data/plugins/$psubfolder/bin/send433 -p=$transPIN $pulselength $group $all $unit $command 2>&1);
    our $output2 = qx(/usr/bin/sudo $installfolder/data/plugins/$psubfolder/bin/send433 -p=$transPIN $pulselength $group $all $unit $command 2>&1);
  }

}

if ( !$send ) {
  print "Unknown protocol. Giving up.";
  exit;
}

if ( !$output ) {
  $output = "Segmentation fault.";
}

print $output;

exit;
