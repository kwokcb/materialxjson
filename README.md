# MaterialX JSON I/O

This is a Python package for reading and writing MaterialX files in JSON format.

## Installation

You can install the package via pip:

```bash
pip install materialxjson
```

## Usage

```python
import MaterialX as mx
from materialxjson import core
import json
```

```python
import pkg_resources

# Read in MaterialX file
mtlxFileName = pkg_resources.resource_filename('materialxjson', 'data/standard_surface_default.mtlx')
print('Using sample file: %s' % mx.FilePath(mtlxFileName).getBaseName())
doc = mx.createDocument()
mx.readFromXmlFile(doc, mtlxFileName)
```

```python
# Write to JSON format
mtlxjson = core.MaterialXJson()
doc_result = mtlxjson.documentToJSON(doc)
jsondump = json.dumps(doc_result, indent=2)

# Read from JSON format
fromdoc = mx.createDocument()
mtlxjson.documentFromJSON(doc_result, fromdoc)

# Write to XML string
docstring = mx.writeToXmlString(fromdoc)
```
