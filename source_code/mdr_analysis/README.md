# Multiple-Drug-Resistance Analysis & Visualization

This repo contains all the Python codes used to categorize, visualize, and analyze multiple-drug-resistance (MDR) evolution trends.

The Python files (end in `.py`) contain all the plotting functions (for visualizations) and their supporting functions. The Jupyter Notebook files (end in `.ipynb`) are showing the outcome measure calculation functions and evolution trend visualizations for the Multiple-Drug-Resistance (MDR) Analysis, focusing on comparing the Multiple-Firstline-Therapy (MFT) with other strategies.

This program is open-sourced under MIT License. There is much freedom with MIT License, but you must include the original license here and properly cite this as your source.

## Plotting Scripts (Updated Dec 2020)

For ease of generating both Fig. 1 and Fig. 2 for all 12 settings of different prevalence and coverage, several Python scripts are also provided in this folder. Refer to `script_run_for_all_sets.ipynb` notebook for more details and how to use.

## Legend Coloring

For the genotype evolution trend plots, there are two options of calculating drug-resistance strength -

- Option 1: summarizes / categorizes by each genotype's drug resistance. This options uses `resistant_strength_calc` function and the resistance is formatted as `a-b`, where `a` being  how many drugs the genotype is resistant to, and `b` being how many mutation events occurred with the genotype. Refer to the function def for more info
- Option 2: summarizes by each genotype's drug efficacy

| Resistance Strength        | Drug Efficacy | Legend Color            |
| -------------------------- | ------------- | ----------------------- |
| 0-0                        | [90,∞)        | \#32cd32, green         |
| *N/A*                      | [80,90)       | \#636363, grey          |
| 1-1                        | *N/A*         | \#b0ebf7, light blue    |
| 1-2                        | [70,80)       | \#74a9cf, medium blue   |
| 1-3                        | *N/A*         | \#045a8d, dark blue     |
| 2-2                        | [60,70)       | \#fc9272, light red     |
| 2-3                        | [0,60)        | \#ef3b2c, medium red    |
| 2-4, most dangerous double | *N/A*         | \#99000d, dark red      |
| 3-5, most dangerous triple | *N/A*         | \#800080, purple        |
