# TODO
Next concrete steps:
1. Check correctness of results.
    1a. Understand how does Yuki's code generate the method-level dependency graph.
    2a. Make inspections on the results of `commons-fileupload` and `commons-codec`.
        2aa. Bug in first commit SHA of both results -> All methods should be considered as impacted but they are not. Also impacted classes column are non-zero while changed classes column is zero.
        2ab. Bug in row 12 (commit: 7410e99) -> There are impacted classes but no impacted methods. Why? Could it be because fields have changed?
        2ac. Inspect all other non-zero rows in the results to make sure of correctness and find potential bugs.
2. Run the code on more projects.
3. Integrate STARTS method-level analysis with emop.


# Info
- Run `bash main_impacted.sh`. It will run the other scripts `helper_scripts/run_20_version.sh` and `helper_scripts/extract_data/extracted.py`. It will run STARTS impacted and method impacted mojo on 20 versions of projects given in `project_list.csv`.

- `extracted.py` will generate output.csv using the data in `logs/` that is generated by `run_20_version.py`.

- `CSVresultStartsmethods.csv`, `CSVresultStatrsImpacted.csv` and `graph.jpg` are the results Jiang obtained from his own version of evaluation with commons-codec.

