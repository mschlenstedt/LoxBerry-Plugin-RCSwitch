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
#use File::HomeDir;
#use Cwd 'abs_path';
#use Config::Simple;
#use warnings;
#use strict;
#no strict "refs"; # we need it for template system

##########################################################################
# Read Settings
##########################################################################

# Version of this script
our $version = "0.0.3";

# Figure out in which subfolder we are installed
#our $psubfolder = abs_path($0);
#$psubfolder =~ s/(.*)\/(.*)\/(.*)$/$2/g;

#our $home = File::HomeDir->my_home;
#our $cfg           = new Config::Simple("$home/config/system/general.cfg");
#our $installfolder = $cfg->param("BASE.INSTALLFOLDER");
#our $pcfg          = new Config::Simple("$home/config/plugins/$psubfolder/RCSwitch.cfg");
#our $transPIN      = $pcfg->param("general.TransmissionPIN");

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
if ( $query{'id'} ne "" ) {
  our $id = $query{'id'};
  if ( $id !~ /[a-zA-Z0-9]/ ) {
    print "Wrong ID. Giving up.";
    exit;
  }
  $id = "-i $id";
} else {
  our $id = "";
}

if ( $query{'systemcode'} ne "" ) {
  our $systemcode = $query{'systemcode'};
  if ( $systemcode !~ /[a-zA-Z0-9]/ ) {
    print "Wrong Systemcode. Giving up.";
    exit;
  }
  $systemcode = "-s $systemcode";
} else {
  our $systemcode = "";
}

if ( $query{'unit'} ne "" ) {
  our $unit = $query{'unit'};
  if ( $unit !~ /[0-9]/ ) {
    print "Wrong unit number. Giving up.";
    exit;
  }
  our $unit = "-u $unit";
} else {
  print "Missing unit number. Giving up.";
  exit;
}

if ( $query{'command'} ne "" ) {
  our $command = $query{'command'};
  if ( $command eq "on" ) {
    $command = "-t";
  }
  if ( $command eq "off" ) {
    $command = "-f";
  }
  if ( $command !~ /[\-tf]/ ) {
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
  if ( $all eq 1 ) {
    $all = "-a"
  } else {
    $all = ""
  }
} else {
   our $all = "";
}

if ( $query{'protocol'} ne "" ) {
  our $protocol = $query{'protocol'};
  $protocol = "-p $protocol";
  if ( $protocol !~ /[A-Za-z0-9\_\-]/ ) {
    print "Wrong protocol. Giving up.";
    exit;
  }
} else {
  print "Missing protocol. Giving up.";
  exit;
}

  # Send command with rcswitch - do this 3 times to make sure the command could be received
  # Note: Family isn't needed for Elro, but is used here for backward compatibility for old version prior 0.9 (no protocol parameter and therefore
  # standard is "elro"
  print "/usr/local/bin/pilight-send -P 5000 -S 127.0.0.1 $protocol $id $systemcode $unit $all $command\n\n";
  our $output = qx(/usr/local/bin/pilight-send -P 5000 -S 127.0.0.1 $protocol $id $systemcode $unit $all $command 2>&1);
  #our $output1 = qx(/usr/local/bin/pilight-send -P 5000 -S 127.0.0.1 $protocol $id $systemcode $unit $all $command 2>&1); # send twice

if ( !$output ) { $output = "OK." }

print $output;

exit;
