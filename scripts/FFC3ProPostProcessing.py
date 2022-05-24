# By Tim Wiser, 2022, inspired by ArteFlux and the PostProcessingPlugin from Ruben Dulek but significantly expanded

import re 
from ..Script import Script


class FFC3ProPostProcessing(Script):
    """Performs a search-and-replace on all g-code.

    Due to technical limitations, the search can't cross the border between
    layers.
    """

    def getSettingDataString(self):
        return """{
            "name": "FFC3Pro Post Processing Script",
            "key": "FFC3ProPostProcessing",
            "metadata": {},
            "version": 2,
            "settings": {}
        }"""

    def execute(self, data):
        # Printer hangs if temperatures contain decimal points (really?)
        removeDecimal = re.compile(r"M(104|140) S([0-9]+)\.[0-9]+")
        removeDecimalSub = r"M\1 S\2"
        
        # Always need to specify which tool, even if in single-extruder mode
        addToolToTemp = re.compile("(M104 S[0-9]{1,3})([^T]*)$")
        def addToolToTempSub(tool):
            return "\\1 T" + tool + "\\2"
        
        # Also need to specify the tool on fan speed commands
        addToolToFan = re.compile("(M106 S[0-9.]+)([^T]*)$")
        
        # These don't seem to do anything
        commentUnnecessary = re.compile("(M10[59].*)$")
        commentUnnecessarySub = ";\\1"
        
        # Yes, the order of T and S matters to Flashforge
        rewriteTemp = re.compile("M104 (T[01]) (S[0-9]+)")
        rewriteTempSub = "M104 \\2 \\1"
        
        # Detect when tool is changed
        toolSwap = re.compile("^(M108 )?T([01])")
        
        activeTool = ""
        newData = []
        for layer_number, layer in enumerate(data):
            newLayer = []
            for line in layer.split('\n'):
                match = toolSwap.search(line)
                if match:
                    activeTool = match.group(2) # keep track of which tool is active for some substitutions
                newLine = removeDecimal.sub(removeDecimalSub, line)
                newLine = addToolToTemp.sub(addToolToTempSub(activeTool), newLine)
                newLine = addToolToFan.sub(addToolToTempSub(activeTool), newLine)
                newLine = commentUnnecessary.sub(commentUnnecessarySub, newLine)
                newLine = rewriteTemp.sub(rewriteTempSub, newLine)
                newLayer.append(newLine)
            newData.append('\n'.join(newLayer))
        return newData
