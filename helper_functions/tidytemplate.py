"""
Tidy Tuesday template utilities for Python/PyDyTuesday with Quarto
"""

from datetime import datetime, timedelta
import os
from pathlib import Path


def current_tuesday(refdate=None):
    """
    Get the date of Tuesday in the current week.
    
    Args:
        refdate (datetime, optional): Reference date (defaults to today)
        
    Returns:
        date: The date of Tuesday in the same week as refdate
    """
    if refdate is None:
        refdate = datetime.now().date()
    
    if hasattr(refdate, 'date'):
        refdate = refdate.date()
    
    # Find Tuesday of current week (Monday=0, Tuesday=1, etc.)
    days_to_tuesday = 1 - refdate.weekday()
    tuesday_date = refdate + timedelta(days=days_to_tuesday)
    return tuesday_date


def use_template(template_name, save_as, data, ignore=False, open_file=True):
    """
    Create a Quarto file from a template with data substitution.
    
    Args:
        template_name (str): Name of the template file
        save_as (str): Output filename
        data (dict): Data for template substitution
        ignore (bool): Whether to ignore existing files
        open_file (bool): Whether to open the file after creation
    """
    # Check if file exists and handle ignore flag
    if Path(save_as).exists() and not ignore:
        response = input(f"File {save_as} already exists. Overwrite? (y/n): ")
        if response.lower() != 'y':
            return
    
    # Quarto template content
    template_content = f'''---
title: "Tidy Tuesday - {data['call_tuesday']}"
author: "Your Name"
date: "{data['call_date']}"
format: 
  html:
    code-fold: false
    toc: true
    theme: cosmo
jupyter: python3
---

# Tidy Tuesday Analysis

Data from: {data['call_tuesday']}  
Created on: {data['call_date']}

## Setup

```{{python}}
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pydytuesday import PyDyTuesday

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

print("Tidy Tuesday Analysis")
print(f"Data from: {data['call_tuesday']}")
```

## Load Data

```{{python}}
# Load this week's data using PyDyTuesday
tt = PyDyTuesday()

# Get data for the specific Tuesday
tuesday_date = "{data['call_tuesday']}"
print(f"Loading data for {{tuesday_date}}...")

try:
    # Load the data (adjust this based on PyDyTuesday API)
    data_dict = tt.load_data(tuesday_date)
    
    print("Available datasets:")
    for key in data_dict.keys():
        print(f"  - {{key}}: {{data_dict[key].shape}}")
        
except Exception as e:
    print(f"Error loading data: {{e}}")
    print("You may need to check the date or data availability.")
```

## Data Exploration

```{{python}}
# Example analysis - customize based on your needs
for name, df in data_dict.items():
    print(f"\\n=== Analysis of {{name}} ===")
    print(f"Shape: {{df.shape}}")
    print("\\nFirst few rows:")
    display(df.head())
    
    print("\\nData info:")
    print(df.info())
```

## Visualizations

```{{python}}
#| fig-cap: "Overview visualizations"
#| fig-width: 12
#| fig-height: 8

# Example visualization - customize based on your data
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Data Overview', fontsize=16)

# Add your plots here based on the data structure
# Example:
# df.plot(kind='hist', ax=axes[0,0], title='Distribution')
# df.plot(kind='scatter', x='col1', y='col2', ax=axes[0,1])

plt.tight_layout()
plt.show()
```

## Analysis

Your analysis and insights here...

## Conclusions

What did you learn from this week's data?

## Session Info

```{{python}}
import sys
print(f"Python version: {{sys.version}}")
print(f"Pandas version: {{pd.__version__}}")
print(f"Matplotlib version: {{plt.matplotlib.__version__}}")
print(f"Seaborn version: {{sns.__version__}}")
```
'''
    
    # Write the file
    with open(save_as, 'w') as f:
        f.write(template_content)
    
    print(f"Created {save_as}")
    
    # Open file if requested
    if open_file:
        try:
            os.system(f"code {save_as}")  # VS Code
        except:
            try:
                os.system(f"open {save_as}")  # macOS
            except:
                try:
                    os.system(f"start {save_as}")  # Windows
                except:
                    print(f"File created: {save_as}")


def use_tidytemplate(name=None, open_file=True, refdate=None, ignore=False):
    """
    Create a Tidy Tuesday Quarto template file.
    
    Args:
        name (str, optional): Name for the output file
        open_file (bool): Whether to open the file after creation
        refdate (datetime, optional): Reference date (defaults to today)
        ignore (bool): Whether to ignore existing files
    """
    if refdate is None:
        refdate = datetime.now().date()
    
    if not isinstance(refdate, (datetime, type(refdate))):
        raise ValueError("Invalid date provided")
    
    # Get current Tuesday
    curr_tuesday = current_tuesday(refdate)
    
    # Generate default filename if not provided
    if name is None:
        name = f"{curr_tuesday.strftime('%Y_%m_%d')}_tidy_tuesday.qmd"
    
    # Template data
    template_data = {
        'call_date': datetime.now().date(),
        'call_tuesday': curr_tuesday.strftime('%Y-%m-%d')
    }
    
    # Create file from template
    use_template(
        template_name="tidytemplate.qmd",
        save_as=name,
        data=template_data,
        ignore=ignore,
        open_file=open_file
    )


# If you want to run the file directly for testing
if __name__ == "__main__":
    # Test the functions
    print("Current Tuesday:", current_tuesday())
    
    # Test creating a template
    # use_tidytemplate(open_file=False)  # Set to False to avoid opening file