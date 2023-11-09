#!/usr/bin/env python
'''
Utility to convert between XML and JSON representations of a MaterialX document
'''
import MaterialX as mx
from materialxjson import core
import json
import os, argparse

def main():
    '''
    Command to convert read / write from / to JSON representations of a MaterialX document
    '''
    parser = argparse.ArgumentParser(description="Utility to convert between XML and JSON representations of a MaterialX document")
    parser.add_argument('--outputPath', dest='outputPath', default='', help='File path to output results to.')
    parser.add_argument(dest="inputFileName", help="Filename of the input document or folder containing input documents")
    parser.add_argument('--fromJSON', dest='fromJSON', action='store_true', help='Convert from JSON to XML. Default is XML to JSON.')

    opts = parser.parse_args()

     # Get absolute path of opts.outputPath
    if opts.outputPath:    
        opts.outputPath = os.path.abspath(opts.outputPath)
    outputPath = mx.FilePath(opts.outputPath)
    # Check that output path exists
    if outputPath.size() > 0 and not os.path.isdir(outputPath.asString()):
        print('Output path "%s" does not exist.' % outputPath.asString())
        exit(-1)

    print('------------------------- outputPath'    + opts.outputPath)

    # Set extension to be 'json' if converting from JSON (opts.JSON) to XML
    extension = 'json' if opts.fromJSON else 'mtlx'   
    fileList = []
    if os.path.isdir(opts.inputFileName): 
        fileList = core.Util.getFiles(opts.inputFileName, extension)
    else:
        if opts.inputFileName.endswith(extension):
            fileList.append(opts.inputFileName)

    if not fileList:
        print('No files found with extension "%s"' % extension)
        exit(-1)

    libraries = []
    searchPath = mx.getDefaultDataSearchPath()
    libraryFolders = mx.getDefaultDataLibraryFolders()
    stdlib, status = mx.loadLibraries(searchPath, libraryFolders)
    if not stdlib:
        print('Error loading standard libraries: "%s"' % status)
        exit(-1)
    else:
        print(status)
    libraries.append(stdlib) 

    mtlxjson = core.MaterialXJson()

    for fileName in fileList:

        filePath = mx.FilePath(fileName)

        # Convert from JSON to XML
        if opts.fromJSON:
            jsonFile = open(fileName, 'r')
            if not jsonFile:
                continue
            jsonObject = json.load(jsonFile)
            if not jsonObject:
                continue

            newDoc = mx.createDocument() 
            #jsonObject = json.loads(doc_result)
            mtlxjson.documentFromJSON(jsonObject, newDoc)
            if newDoc.getChildren():

                if os.path.isdir(outputPath.asString()):
                    filePath = outputPath / filePath.getBaseName()

                print('Write to MaterialX file: ' + filePath.asString().replace('.json', '_json.mtlx'))
                mx.writeToXmlFile(newDoc, filePath.asString().replace('.json', '_json.mtlx'))
       
        # Convert from XML to JSON
        else:
            doc = mx.createDocument()
            mx.readFromXmlFile(doc, fileName)
            if doc:
                # Convert entire document to JSON
                doc_result = mtlxjson.documentToJSON(doc)

                if os.path.isdir(outputPath.asString()):
                    filePath = outputPath / filePath.getBaseName()

                # Write JSON to file
                with open(filePath.asString().replace('.mtlx', '_mtlx.json'), 'w') as outfile:
                    print('Write to JSON file: ' + filePath.asString().replace('.mtlx', '_mtlx.json'))
                    json.dump(doc_result, outfile, indent=2)
    
if __name__ == '__main__':
    main()
