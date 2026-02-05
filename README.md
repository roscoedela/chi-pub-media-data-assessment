# Data Engineer – Skill Assessment

## Overview
This project demonstrates how I clean and normalize a CSV file containing 5,000 unclean records.

I approached the problem by first addressing fields with simpler rules, followed by names and addresses, which require more parsing and effort. Breaking the work down by field made validation easier and allowed for clear before and after comparisons during development.

A Dockerfile is included to allow the pipeline to be run in a reproducible local environment.

The final output CSV matches the desired output. Tests and validations are handled in comments!  



## Requirements
- Python 3.11+
- Dependencies in `requirements.txt`
- (Bonus)Docker for containerized execution



## Setup (Local Environment)

### 1. Ensure Python 3.11 or higher is installed:

python --version

### 2. Create and activate a virtual environment

python -m venv .venv
source .venv/bin/activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Place the provided input file in the project root

skill-assessment-202511.csv


Run this command
python clean_csv.py

Which generates cleaned output

