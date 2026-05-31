# Python Data Analysis Project

This project is designed for **InternSpark Task 3: Data Analysis Project (Pandas)**.

## Objective
Load a CSV dataset, clean it, filter it, group it, and generate meaningful insights using Pandas.

## Features
- Loads CSV data using Pandas
- Cleans duplicates and invalid values
- Adds calculated `NetSales`
- Supports user input filters
- Generates grouped summaries by region, category, and product
- Saves an analysis report to `outputs/analysis_report.txt`
- Logs operations to `logs/operations.log`

## Files Included
- `main.py` - complete analysis script
- `data/sales_data.csv` - sample dataset
- `outputs/analysis_report.txt` - generated report
- `logs/operations.log` - log file
- `requirements.txt` - dependency list
- `sample_input_output.txt` - sample run format

## How to Run
1. Install Python 3.x
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the script:
   ```bash
   python main.py
   ```

## Sample Input
- Use sample dataset: `y`
- Filter choice: `3`
- Category: `Electronics`

## Output
The script prints:
- number of rows loaded
- cleaned row count
- filtered row count
- sales summary
- top products
- insights

## Submission Checklist
- GitHub source code link
- Screenshots of output
- Separate DOC/DOCX/PDF for the task
