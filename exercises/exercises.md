# Exercises

## Lecture 1, Intro:
Generate barplots visualizing the rainfall from data in CSV file rainfall\_summer\_2014\_simple.csv

## Lecture 2, Acquisition:
Finish the lecture example. The Lotto numbers are also available in the JSON file lotto-2000.json.
Read the data in and explore the number frequencies (e.g. visually with histograms).

## Lecture 3, Wrangling 1:
Read in the data from https://github.com/WinVector/zmPDSwR/blob/master/Custdata/custdata.tsv 
and look for problems, explore the variables etc.

Also, try to read in the broken slurm data, pay attention to the error message,
get around the problem and see what's wrong

## Lecture 4, Wrangling 2:
Continue with custdata (or custdata2 from the same source, it is partially fixed):
- recode is.employed variable in to categories "employed", "not employed", "missing"
- bin the incomes in to income groups 
- bonus: using the first custdata data set, with missing values coded as a "no income" category

## Lecture 5, Wrangling 3:
roots data; find out the maximum growth of a single root in each measurement interval
one way:
- reshape to wide so that each row is a root, and lengths from different measurement events are in separate columns
- calculate the differences
- reshape back to long
- aggregate over measurement events

## Lecture 6, Visualization and analysis
Think up a question to explore using either custdata or any of the other data we have 
looked at, such as testing if income varies between different groups, 
predicting one weather variable with another etc.

## Lecture 7&8:
After everything has been said, either attack any of the data sets seen so far again,
or go find an interesting data set from e.g. Statistics Finland, City of Helsinki, 
"vaalikone" data etc. and play with it.

For the insane, raw roots data (that has everything wrong with it) to wrangle
