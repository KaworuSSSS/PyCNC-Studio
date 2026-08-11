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


    def write_json(self, toolpath, filename):

        data = self.to_json(
            toolpath
        )

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(data)
