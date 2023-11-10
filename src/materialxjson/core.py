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
import os

# We use a colon to separate the category and name of an element in the JSON hierarchy
JSON_CATEGORY_NAME_SEPARATOR = ':'
# The root of the JSON hierarchy
MATERIALX_DOCUMENT_ROOT = 'materialx'

class MaterialXJson:
    '''
    Class for handling read and write of MaterialX from and to JSON
    '''

    def elementToJSON(self, elem: mx.Element, jsonParent: dict) -> dict:
        '''
        @brief Convert an MaterialX XML element to JSON.
        Will recursively traverse the parent/child Element hierarchy.
        @param elem The MaterialX element to convert
        @param jsonParent The JSON element append to
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

    def documentToJSON(self, doc: mx.Document) -> dict:
        '''
        Convert an MaterialX XML document to JSON
        @param doc The MaterialX document to convert
        @return The JSON document
        '''
        root = {}
        root["materialx"] = {}

        for attrName in doc.getAttributeNames():
            root[attrName] =  doc.getAttribute(attrName)

        for elem in doc.getChildren():
            self.elementToJSON(elem, root[MATERIALX_DOCUMENT_ROOT])

        return root
    
    def documentToJSONString(self, doc: mx.Document, indentation = 2) -> str:
        '''
        Convert an MaterialX XML document to JSON string
        @param doc The MaterialX document to convert
        @return The JSON string
        '''
        result = self.documentToJSON(doc)
        json_string = ''
        if result:
            json_string = json.dumps(result, indent=indentation)
        return json_string

    def elementFromJSON(self, node: dict, elem: mx.Element) -> None:
        '''
        @brief Convert an JSON element to MaterialX
        @param node The JSON element to read
        @param elem The MaterialX element to write to
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

    def documentFromJSON(self, jsonDoc: dict, doc: mx.Document):
        '''
        @brief Convert a JSON document to MaterialX
        @param jsonDoc The JSON document to read
        @param doc The MaterialX document to write to 
        '''
        self.elementFromJSON(jsonDoc, doc)

    def documentFromJSONString(self, jsonString: str, doc: mx.Document):
        '''
        @brief Convert a JSON document to MaterialX
        @param jsonString The JSON string to read
        @param doc The MaterialX document to write to 
        '''
        jsonDoc = json.loads(jsonString)
        if jsonDoc:
            self.elementFromJSON(jsonDoc, doc)   

class Util:
    '''
    Utility class for MaterialX JSON
    '''
    @staticmethod
    def readJson(fileName: str) -> dict:
        '''
        @brief Read a JSON file
        @param fileName The file name to read
        @return The JSON document
        '''
        jsonFile = open(fileName, 'r')
        if not jsonFile:
            return False

        jsonObject = json.load(jsonFile)
        if not jsonObject:
            return False

        return jsonObject
    
    @staticmethod
    def jsonStringToJson(jsonString: str) -> dict:
        '''
        @brief Convert a JSON string to a JSON document
        @param jsonString The JSON string to convert
        @return The JSON document
        '''
        return json.loads(jsonString)
    
    @staticmethod
    def jsonToJSONString(jsonObject: dict, indentation = 2) -> str:
        '''
        @brief Convert a JSON document to a JSON string
        @param jsonObject The JSON document to convert
        @return The JSON string
        '''
        return json.dumps(jsonObject, indent=indentation)
    
    @staticmethod
    def documentToXMLString(doc: mx.Document) -> str:
        '''
        @brief Convert a MaterialX document to XML string
        @param doc The MaterialX document to convert
        @return The XML string
        '''
        return mx.writeToXmlString(doc)
    
    @staticmethod
    def xmlStringToDocument(doc: mx.Document, xmlString: str) -> None:
        '''
        @brief Convert an XML string to a MaterialX document
        @param doc The MaterialX document to write to
        @param xmlString The XML string to convert
        '''
        mx.readFromXmlString(doc, xmlString)

    @staticmethod
    def writeJson(jsonObject: dict, fileName: str, indentation = 2) -> None:
        '''
        @brief Write a JSON document to file
        @param jsonObject The JSON document to write
        @param fileName The file name to write to
        '''
        with open(fileName, 'w') as outfile:
            json.dump(jsonObject, outfile, indent=indentation)

    @staticmethod
    def getFiles(rootPath: str, extension: str) -> list:
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
    def loadLibraries(searchPath: mx.FileSearchPath, libraryFolders: list) -> tuple:
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
    
    @staticmethod
    def jsonFileToXmlFile(fileName: str, outputFilename: str) -> bool:
        '''
        @brief Convert a JSON file to an XML file
        @param fileName The file name to read from
        @return True if successful, false otherwise
        '''
        mtlxjson = MaterialXJson()

        jsonFile = open(fileName, 'r')
        if not jsonFile:
            return ''
        jsonObject = json.load(jsonFile)
        if not jsonObject:
            return ''

        newDoc = mx.createDocument() 
        mtlxjson.documentFromJSON(jsonObject, newDoc)
        if newDoc.getChildren():

            mx.writeToXmlFile(newDoc, outputFilename)    

    @staticmethod
    def xmlFileToJsonFile(xmlFileName: str, jsonFileName: str) -> None:
        '''
        Convert an MaterialX XML file to a JSON file
        '''
        mtlxjson = MaterialXJson()

        doc = mx.createDocument()
        mx.readFromXmlFile(doc, xmlFileName)
        if doc:
            # Convert entire document to JSON
            doc_result = mtlxjson.documentToJSON(doc)

            # Write JSON to file
            with open(jsonFileName, 'w') as outfile:
                json.dump(doc_result, outfile, indent=2)

