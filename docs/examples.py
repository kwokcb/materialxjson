# %% [markdown]
# # MaterialXJSON Examples
# 
# ## Setup

# %%
from IPython.display import display_markdown

def displaySource(title, string, language='xml', open=True):
    text = '<details '
    text = text + (' open' if open else '') 
    text = text + '><summary><b>' + title + '</b></summary>\n\n' + '```' + language + '\n' + string + '\n```\n' + '</details>\n' 
    display_markdown(text, raw=True)

# %%
import MaterialX as mx
import materialxjson as mtlxjson
from materialxjson import core
import json, sys, io

buffer = io.StringIO()
sys.stdout = buffer
print("MaterialX version: " + mx.getVersionString())
print("JSON version: " + json.__version__)
print("MaterialXJSON version: " + mtlxjson.__version__)
help(core)
sys.stdout = sys.__stdout__
corehelp = buffer.getvalue()
displaySource('Core help', corehelp, 'text', False)

# %% [markdown]
# ## Package Resources

# %%
import pkg_resources

directory_name = "data"  
files = pkg_resources.resource_listdir('materialxjson', directory_name)
result = ''
for file in files:
    result = result + file + '\n'

displaySource('Available data files', result, 'text', True)

# %% [markdown]
# ## Writing MaterialX as JSON

# %%
import pkg_resources

mtlxFileName = pkg_resources.resource_filename('materialxjson', 'data/standard_surface_default.mtlx')
print('Using sample file: %s' % mx.FilePath(mtlxFileName).getBaseName())
doc = mx.createDocument()
mx.readFromXmlFile(doc, mtlxFileName)

mtlxjson = core.MaterialXJson()

doc_result = mtlxjson.documentToJSON(doc)
jsondump = json.dumps(doc_result, indent=2)
displaySource('Document to JSON', jsondump, 'json', True)

# Save the MaterialX file
options = {}
options['indent'] = 2
indentVal = options['indent']
#with open('test.json', 'w') as outfile:
#    print('Wrote json file: ' + outfile.name)
#    json.dump(doc_result, outfile, indent=indentVal)


# %% [markdown]
# ## Loading MaterialX Document From JSON

# %%
# Load a MaterialX JSON file
fromdoc = mx.createDocument()
mtlxjson.documentFromJSON(doc_result, fromdoc)

#fromdoc = mtlxjson.load('test.json')
docstring = mx.writeToXmlString(fromdoc)
displaySource('Document from JSON', docstring, 'xml', True)


