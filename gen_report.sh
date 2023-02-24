now=$(date +"%Y-%m-%d-%H-%M-%S")
#pytest --html=reports/report-$now.html --self-contained-html src
pytest --no-header --no-showlocals --html=reports/report.html --self-contained-html src
