#!/bin/bash
# Ali's path
FILES=/Users/alikazmi/Downloads/Minesweeper_starter_code/standard_boards/varied_size/* 

  # # Adrian's path
#FILES=/Users/adriannusalim/Desktop/Gatech/CS3510/minesweeper/standard_boards/varied_size/*

# #pass algoname to this file 
outputfilevaralgo1=varied_size_output_algo1.txt
outputfilevaralgo2=varied_size_output_algo2.txt
algoname=$1
rm $outputfilevaralgo1 
rm $outputfilevaralgo2

touch $outputfilevaralgo1
touch $outputfilevaralgo2
echo "numsquares dig_count bomb_count time" >> $outputfilevaralgo1
echo "numsquares dig_count bomb_count time" >> $outputfilevaralgo2 
for f in $FILES
do

  echo "Processing $f file..."
  # take action on each file. $f store current file name
  python ALGO1_safe_squares.py $f 0 >> $outputfilevaralgo1
  python ALGO2_bomb_blossom.py $f 0 >> $outputfilevaralgo2 
  # python $algoname $f 0 >> $outputfilevar
  printf "\n" >> $outputfilevaralgo1
  printf "\n" >> $outputfilevaralgo2
done



