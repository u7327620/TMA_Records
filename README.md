# TMA_Records
A collection of statistics from TMA events, courtesy of Yahummy, and data analysis scripts, courtesy of Lostmail.

# Project Structure
- **`Data/`** TFC match statistics.
  - `Fighters/` Data grouped by fighter. Python generated files denoted by `_database`.
  - `Records/` Collection of notable statistics.
  - `Replays/` Match replays from TFC_1 to TFC_22.
  - `Stats/` Raw match analysis from TFC_1 to TFC_23.
- **`toribash_records/`** Python scripts.
  - `objects/` Data classes used by the scripts.
  - `tests/` minimalist test suite.
  - `util/` Helpers.
  - `player_records.py` Main script which generates records.
- **`README.md`** This file.
- **`requirements.txt`** Python dependencies.


Note: **TFC_23 stats don't record any match data**. They exist solely for win/loss tracking.
If you're doing data analysis on stats like 'strikes landed', ONLY use TFC_1 to TFC_22.


# Installation
Developed using python 3.14.2

1. **Clone the repository**
    ```bash
   git clone https://github.com/u7327620/TMA_Records.git
   cd TMA_Records
   ```

2. **Make a virtual environemnt (Optional):**
    ```bash
    python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

# Usage
To get all TFC W-L-D: `python toribash_records/player_records.py`

### Updating Records:
Each match needs to be recorded in a `Data/Stats/TFC/TFC_<x>/<name>_vs_<name>.json` file.

For backwards compatibility, I recommend making a `<name>_vs_<name>.txt` file for each match 
and using `python toribash_records/util/txt_to_json.py` to create the json file.
