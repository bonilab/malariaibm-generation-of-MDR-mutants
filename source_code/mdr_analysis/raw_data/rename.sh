#!/bin/bash

mkdir monthly
mkdir mutpair
mkdir summary

SET_NUM="6c"

for i in {1..100} 
do
    mv set${SET_NUM}_${i}monthly_data_0.txt monthly/
    mv set${SET_NUM}_${i}mutpair_0.txt mutpair/
    mv set${SET_NUM}_${i}summary_0.txt summary/
done
