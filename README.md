# eCFR-analyzer
Public app: https://cfr-analyzer.streamlit.app/

To run locally, clone the repo and from the root directory run:
```bash
uv sync
```
(requires [`uv`](https://docs.astral.sh/uv/getting-started/installation/))

To download and process all the data run
```bash
./src/scripts/run_all.sh
```
This will download the eCFR data and process it into a format that can be used by the app. The processed data will be saved in the `data/` directory. It takes about 30 minutes to run (mostly hitting the eCFR API).


The `src/scripts` directory contains utility scripts for downloading and processing the eCFR data. 
The toplevel `src/` directory contains the Streamlit app code.

To run the app, after downloading the data, and with the .venv activated run:
```bash
 streamlit run src/app.py
 ```