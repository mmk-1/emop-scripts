# Info
- Run `bash main_impacted.sh`. It will run the other scripts `helper_scripts/run_20_version.sh` and `helper_scripts/extract_data/extracted.py`. It will run STARTS impacted and method impacted mojo on 20 versions of projects given in `project_list.csv`.

- `extracted.py` will generate output.csv using the data in `logs/` that is generated by `run_20_version.py`.

- `CSVresultStartsmethods.csv`, `CSVresultStatrsImpacted.csv` and `graph.jpg` are the results Jiang obtained from his own version of evaluation with commons-codec.

