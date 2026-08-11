"""
PyCNC Studio
Toolpath Exporter

Converts CNC toolpaths into JSON.
"""

import json


class ToolpathExporter:

    def to_json(self, toolpath):

        return json.dumps(
            toolpath
        )
