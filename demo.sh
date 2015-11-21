rm -rf tmp
mkdir tmp
cd tmp
set -ex

virtualenv tmpenv
. tmpenv/bin/activate
pip install coverage-enable-subprocess --extra-index-url https://testpypi.python.org/pypi
touch .coveragerc
export COVERAGE_PROCESS_START=$PWD/.coveragerc
echo 'print("oh, hi!")' > ohhi.py
python ohhi.py
coverage report
