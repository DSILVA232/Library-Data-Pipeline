# Data Creation

This folder contains the script used to generate the library dataset used throughout this pipeline.

## Overview

The script was written from scratch to generate four related CSV files — members, books, loans, and staff — using the [Faker](https://faker.readthedocs.io/en/master/) library. The data is intentionally dirty to simulate a real world dataset arriving from a source system with no quality guarantees.

By default the script targets a dirty data rate of **10–25% per table**, introducing issues such as:

- Inconsistent date formats across rows
- Mixed value representations for the same concept (e.g. `"Yes"`, `"1"`, `"TRUE"` for a boolean field)
- Intentionally misspelled column names
- Missing values across non-critical columns
- Duplicate records with slight variations (e.g. uppercased name)
- Phone numbers in multiple formats

The dirty data rate and the types of errors introduced can be customised by adjusting the logic embedded directly in the generation script.

## Dataset

The script is configured for an Australian library system by default — names, addresses, phone numbers, and postcodes are AU locale specific. The four tables are designed with relationships between them, making the dataset suitable for schema design, entity relationship diagrams, and dimensional modelling exercises.

| Table | Rows | Description |
|---|---|---|
| members | ~515 | library members with location and membership details |
| books | ~515 | book inventory with author, genre, and publisher |
| loans | 120 | loan transactions linking members to books |
| staff | 18 | library staff with branch and role assignments |

## Customisation

The script can be adapted for any theme or domain by:

- Swapping the Faker locale (`en_AU` → any supported locale)
- Replacing library specific fields with domain appropriate ones
- Adjusting the dirty data rate by modifying the probability thresholds in each generator function
- Changing row counts per table

For the full range of available data generators and locale options refer to the [Faker documentation](https://faker.readthedocs.io/en/master/).

## Usage

```bash
python data_creation/generate.py
```

Output CSVs are written to `data_raw/`. Re-running the script regenerates all four files.
