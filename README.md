# SEED ESPM Import Testing

This repo is for quickly testing the algorithm used for processing ESPM
import data.  This is an extremely heavy process in SEED, and I wanted a
standalone repo to do testing.

# Scope

This test really covers the steps _after_ the XML has been parsed into
a Python dictionary and the property objects have been collected into a
list.  Processing this list, along with all the keys, into a set of rows
to be written to a csv file is the really time-intensive step for some
reason.

# Steps

I've setup a few worker functions to easily "make" datasets of various
length. I then call the main function, which is the core of the import
function in SEED, and time the execution to evaluate whether the change
made a beneficial or detrimental change.
