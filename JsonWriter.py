import json

class JsonWriter():
    def __init__(self):
         pass
    def write_file(self, d):
        with open("output_file.json", "w") as final:
            json.dump(d, final, indent=2, default=lambda x: list(x) if isinstance(x, tuple) else str(x))