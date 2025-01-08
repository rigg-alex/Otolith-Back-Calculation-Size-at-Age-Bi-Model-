# Fish Size Back-Calculation Tool

A Python script for back-calculating fish sizes at different ages using the Biological Intercept (BI) model and otolith measurements.
![image](https://github.com/user-attachments/assets/329bcd95-49c6-4747-90a3-5ec430e7776b)


## Overview

This tool processes otolith measurement data to back-calculate fish sizes throughout their life history. It implements the Biological Intercept (BI) model, which uses the relationship between fish length and otolith size to estimate fish length at previous ages based on otolith growth rings.

## Requirements

- Python 3.x
- pandas
- numpy

Install required packages using:
```bash
pip install pandas numpy openpyxl
```

## Input Data Format

The script expects an Excel file with the following columns:
- `FishKey`: Unique identifier for each fish
- `L(CPT)_MM`: Capture length in millimeters
- `R(OP)_um`: Otolith radius at capture in micrometers
- `HATCH_UM`: Otolith size at hatch in micrometers
- Numbered columns (1-164): Otolith interval measurements

See the provided `Template for Size at Age Model.xlsx` for the expected format.

## Usage

1. Update the file path in the script:
```python
file_path = r"YOUR_FILE_PATH_HERE.xlsx"
```

2. Run the script:
```python
python back_calculate_size.py
```

The script will:
1. Load and clean the input data
2. Calculate initial length (L0) for each fish
3. Back-calculate lengths at each age using the BI model
4. Transform the data into a fish-by-age matrix
5. Save results to `OUTPUT FILE.csv`

## Output

The script generates a CSV file with:
- One row per fish (identified by FishKey)
- Columns for each age (Age_0, Age_1, etc.)
- Values representing back-calculated lengths in millimeters

## The BI Model

The Biological Intercept model uses the formula:

```
Lt = Lc - ((Rc - Rt) / Rc) * (Lc - L0)
```

Where:
- Lt = Length at age t
- Lc = Length at capture
- Rc = Otolith radius at capture
- Rt = Otolith radius at age t
- L0 = Length at hatch

## Example Data

The repository includes:
- `Template for Size at Age Model.xlsx`: Template showing required data format
- `output.csv`: Example output showing expected results

## Notes

- All measurements should be consistent in their units (mm or μm)
- This model was for daily growth increments
- The script automatically converts otolith measurements to micrometers
- Empty otolith intervals are handled automatically
- The output is formatted for easy import into statistical software

