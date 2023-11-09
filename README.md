# MaterialX JSON I/O

This is a Python package for reading and writing MaterialX files in JSON format.

## Installation

You can install the package via pip:

```bash
pip install materialxjson
``

## Usage
```python
import MaterialX as mx
from materialxjson import core

# Create an instance
mtlxjson = core.MaterialXJson()

# Load a MaterialX file
doc = mx.createDocument()
doc = mtlxjson.load('path_to_your_file.json')

# Manipulate the MaterialX data...

# Save the MaterialX file
mtlxjson.save(doc, 'path_to_your_file.json')
```
