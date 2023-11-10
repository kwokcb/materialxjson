#!/usr/bin/env python
'''
Command to convert between XML and JSON representations of a MaterialX document
'''
import MaterialX as mx
from materialxjson import core
import json
import os, argparse

def main():
    '''
    Command to convert between XML and JSON representations of a MaterialX document
    '''
    parser = argparse.ArgumentParser(description="Utility to convert between XML and JSON representations of a MaterialX document")
    parser.add_argument('--outputPath', dest='outputPath', default='', help='File path to output results to.')
    parser.add_argument(dest="inputFileName", help="Filename of the input document or folder containing input documents")
    parser.add_argument('--fromJSON', dest='fromJSON', action='store_true', help='Convert files in folder from JSON to XML if a folder is specified as input. Default is XML to JSON.')

    opts = parser.parse_args()

     # Get absolute path of opts.outputPath
    if opts.outputPath:    
        opts.outputPath = os.path.abspath(opts.outputPath)
    outputPath = mx.FilePath(opts.outputPath)
    # Check that output path exists
    if outputPath.size() > 0:
        if os.path.isdir(outputPath.asString()):
            print('Output path "%s" does not exist.' % outputPath.asString())
            exit(-1)
        else:
            print('- Write files to outputPath: '+ opts.outputPath)

    # Set extension to be 'json' if converting from JSON (opts.JSON) to XML
    fileList = []
    extension = 'mtlx'
    if os.path.isdir(opts.inputFileName): 
        extension = 'json' if opts.fromJSON else 'mtlx'   
        fileList = core.Util.getFiles(opts.inputFileName, extension)
    else:
        extension = mx.FilePath(opts.inputFileName).getExtension()
        if extension in ['mtlx', 'json']:
            fileList.append(opts.inputFileName)

    if not fileList:
        print('No files found with extension "%s"' % extension)
        exit(-1)

    ## Create I/O handler
    mtlxjson = core.MaterialXJson()
    
    for fileName in fileList:

        # Convert from JSON to XML
        if extension == 'json':
            outputFilePath = outputPath / mx.FilePath(fileName.replace('.json', '_json.mtlx'))
            outputFileName = outputFilePath.asString()
            core.Util.jsonFileToXmlFile(fileName, outputFileName)
            print('Convert JSON file "%s" -> XML file "%s"' % (fileName, outputFileName))
       
        # Convert from XML to JSON
        else:
            outputFilePath = outputPath / mx.FilePath(fileName.replace('.mtlx', '_mtlx.json'))
            outputFileName = outputFilePath.asString()
            core.Util.xmlFileToJsonFile(fileName, outputFileName)
            print('Convert XML file %s -> JSON file %s' % (fileName, outputFileName))
    
if __name__ == '__main__':
    main()
