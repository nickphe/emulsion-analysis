#!/bin/bash

cd "/Users/nanostars/Desktop/emulsion-analysis-main/run ilastik"
python3 run_ilastik.py
echo Ilastik processing complete.

cd "/Users/nanostars/Desktop/emulsion-analysis-main/emulsion analysis"
python3 run.py
echo Fitting complete.

cd "/Users/nanostars/Desktop/emulsion-analysis-main/data analysis"
python3 analyze_data.py
echo Analysis complete.

