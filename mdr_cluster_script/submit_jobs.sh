#!/bin/bash

config="../input/mdr_input.yml"

for i in {1..100} 
do
	job_name="MaSimCycling_${i}"
	output_name="../mdr_output/Cycling_${i}"

	qsub -N $job_name -v input_files=$config,output_files=$output_name single_job.pbs

done
