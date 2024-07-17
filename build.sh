#!/bin/bash

buildDist=false

# Loop through command line arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        -dist) buildDist=true ;;
        *) echo "Unknown parameter passed: $1"; 
    esac
    shift
done

# Now use the useDist variable to conditionally execute code
if $buildDist; then
    echo "Building dist."
    py -m build
fi

echo "Installing package"
pip install .

echo "Building docs"
pushd docs
doxygen Doxyfile
popd

