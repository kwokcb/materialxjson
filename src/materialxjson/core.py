# core.py

'''
@file 
This module contains the core definitions and utilities for reading and wring MaterialX
in JSON format.
'''

# MaterialX support
import MaterialX as mx

# JSON support
import json

# Utilities
import os, argparse

# We use a colon to separate the category and name of an element in the JSON hierarchy
JSON_CATEGORY_NAME_SEPARATOR = ':'
# The root of the JSON hierarchy
MATERIALX_DOCUMENT_ROOT = 'materialx'

class MaterialXJson:
    '''
    Class for handling read and write of MaterialX from and to JSON
    '''

    def elementToJSON(self, elem, jsonParent):
        '''
        Convert an MaterialX XML element to JSON.
        Will recursively traverse the parent/child Element hierarchy.
        '''
        if (elem.getSourceUri() != ""):
            return
        
        # Create a new JSON element for the MaterialX element
        jsonElem = {}

        # Add attributes
        for attrName in elem.getAttributeNames():
            jsonElem[attrName] = elem.getAttribute(attrName)

        # Add children
        for child in elem.getChildren():
            jsonElem = self.elementToJSON(child, jsonElem)
        
        # Add element to parent
        jsonParent[elem.getCategory() + JSON_CATEGORY_NAME_SEPARATOR + elem.getName()] = jsonElem
        return jsonParent

    # Convert MaterialX document to JSON
    def documentToJSON(self, doc):
        '''Convert an MaterialX XML document to JSON'''
        root = {}
        root["materialx"] = {}

        for attrName in doc.getAttributeNames():
            root[attrName] =  doc.getAttribute(attrName)

        for elem in doc.getChildren():
            self.elementToJSON(elem, root[MATERIALX_DOCUMENT_ROOT])

        return root

    # Convert JSON element to MaterialX
    def elementFromJSON(self, node, elem):
        '''
        Convert an JSON element to MaterialX
        '''
        for key in node:
            value = node[key]

            # Set attributes            
            if isinstance(value, str):
                elem.setAttribute(key, str(value))

            # Traverse chilren
            else:
                # Traverse down from root
                if key == MATERIALX_DOCUMENT_ROOT:
                    self.elementFromJSON(value, elem)
                    continue

                # Split key name by ":" to get category and name
                category, name = key.split(JSON_CATEGORY_NAME_SEPARATOR, 1)
                if category and not elem.getChild(name):
                    child = elem.addChildOfCategory(category, name)
                    self.elementFromJSON(value, child)

    def documentFromJSON(self, jsonDoc, doc):
        '''
        @brief Convert a JSON document to MaterialX
        @param jsonDoc The JSON document to read
        @param doc The MaterialX document to write to 
        '''
        self.elementFromJSON(jsonDoc, doc)

    def load(self, fileName) -> mx.Document:
        '''
        @brief Load a JSON document into a MaterialX document
        @param fileName The file name to load from
        @return MaterialX document
        '''
        jsonFile = open(fileName, 'r')
        if not jsonFile:
            return False

        jsonObject = json.load(jsonFile)
        if not jsonObject:
            return False

        newDoc = mx.createDocument() 
        self.documentFromJSON(jsonObject, newDoc)

        return newDoc
    
    def save(self, doc, filePath, options) -> bool:
        '''
        @brief Save a MaterialX document to JSON
        @param doc The MaterialX document to save
        @param filePath The file path to save to
        @param options The options to use
        @return True if successful, otherwise False
        '''
        doc_result = self.documentToJSON(doc)
        if not doc_result:
            return False

        # Write JSON to file
        indentVal = options['indent']
        with open(filePath, 'w') as outfile:
            json.dump(doc_result, outfile, indent = indentVal)

        return True  

class Util:
    '''
    Utility class for MaterialX JSON
    '''

    @staticmethod
    def getFiles(rootPath, extension) -> list:
        '''
        @brief Get all files with the given extension from the given root path
        @param rootPath The root path to search from
        @param extension The extension to search for
        @return A list of file paths
        '''
        filelist = []
        exts = (extension, extension.upper() )
        for subdir, dirs, files in os.walk(rootPath):
            for file in files:
                if file.lower().endswith(exts):
                    filelist.append(os.path.join(subdir, file)) 
        return filelist

    @staticmethod
    def loadLibraries(searchPath, libraryFolders) -> tuple:
        '''
        @brief Load all libraries from the given search path and library folders
        @param searchPath The search path to use
        @param libraryFolders The library folders to use
        @return A tuple containing the library document and a status string
        '''
        status = ''
        lib = mx.createDocument()
        try:
            libFiles = mx.loadLibraries(libraryFolders, searchPath, lib)
            status = '- Loaded %d library definitions from %d files' % (len(lib.getNodeDefs()), len(libFiles))
        except mx.Exception as err:
            status = '- Failed to load library definitions: "%s"' % err

        return lib, status


