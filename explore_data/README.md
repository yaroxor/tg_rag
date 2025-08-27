# Data Exploration for Telegram Chat Export Format

## Purpose
This directory contains exploratory analysis of Telegram's chat export format, as no official specification was available. The analysis focuses on identifying all possible keys and values within message objects.

## Methods
- **explore.jq**: JQ script for parsing and analyzing message structures
- **explore.py**: Python equivalent for comparative analysis
- **performance_results.txt**: Contains performance metrics comparing JQ and Python processing

## Notes
The initial performance comparison yielded unexpected results. It should be noted that the author is relatively new to both JQ and performance measurement methodologies. This inexperience may have contributed to these anomalous findings and should be considered when interpreting the results.
