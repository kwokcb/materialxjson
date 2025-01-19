cd docs
echo "Install Jupyter..."
pip install jupyter --quiet
echo "Build notebooks..."
python -m jupyter execute --inplace examples.ipynb > notebook_log.txt 2>&1
python -m jupyter nbconvert examples.ipynb --to html 
python -m jupyter nbconvert examples.ipynb --to python 
echo "Build Doxygen..."
doxygen Doxyfile > doxygen_log.txt 2>&1
cd ..