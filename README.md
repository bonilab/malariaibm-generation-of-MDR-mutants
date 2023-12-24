# Antimalarial Drug Resistance Simulation

This repository contains the figures output and source code for an individual-based
simulation that was a part of the scientific publication titled "Assessing
emergence risk of double-resistant and triple-resistant genotypes of Plasmodium falciparum"
published in Nature Communications in January 2024.

Authors: Eric Zhewen Li, Tran Dang Nguyen, Thu Nguyen-Anh Tran, Robert J Zupko,
Maciej F Boni

DOI: **TBD**

## Repository Structure

`figures`: Contains the figures generated from the simulation output.

`mdr_analysis`: Contains Python scripts for analyzing the simulation output.

`source_code`: Contains the source code for the individual-based simulation.

## How to Use

To reproduce or further explore the simulation described in the publication,
follow these steps:

Clone the repository to your local machine:

```sh
git clone https://github.com/bonilab/malariaibm-generation-of-MDR-mutants.git
```

The README file in the source_code/ directory contains detailed information on
how to build and run the simulation. If you require additional assistance or
have questions, please feel free to contact the corresponding author. Execute
the simulation code using your preferred environment or tools. Be sure to refer
to the publication and any additional documentation for specific instructions
on running the simulation.

## Citation

If you use or refer to the results, code, or data from this repository in your
research or work, please cite the original publication:

```text
**TBD**
```

For questions or inquiries, please contact the corresponding author or create
an issue in this repository.

## Notes about `mdr_analysis/` folder

Due to file size limit, the simulation output files are zipped under [GitHub release](https://github.com/bonilab/malariaibm-generation-of-MDR-mutants/releases/tag/v3.3_mdr.2). To generate the figures in our paper, please download `simulation_outputs.zip` file and upzip them to `mdr_analysis/simulation_outputs/`
