import xml.etree.ElementTree as ET
class XmlReader:
    ROOT_ELEMENT = ".//pmcId"
    NODE_ELEMENTS = [".//MedlineCitation/Article/Abstract/AbstractText"]
    # FIELDNAMES = {"ID" : "id", "COMPARISON" : "comparison", "INDICATION" : "indication", "FINDINGS" : "findings", "IMPRESSION" : "impression"}
    FIELDNAMES = {"ID" : "id", "FINDINGS" : "findings", "IMPRESSION" : "labels"}
    def __init__(self ):
        self.data = {}
        for fieldname in XmlReader.FIELDNAMES.keys():
            self.data[XmlReader.FIELDNAMES[fieldname]] = None

    def __read_id(self):
        pcm_code = self.root.find(XmlReader.ROOT_ELEMENT)
        if pcm_code is not None:
            self.data[XmlReader.FIELDNAMES["ID"]] = pcm_code.get("id").strip()
        else:
            self.data[XmlReader.FIELDNAMES["ID"]] = "ID NOT FOUND"
        return self.data.get(XmlReader.FIELDNAMES["ID"])
    
    def __read_abstract_text(self):
        for node_element in XmlReader.NODE_ELEMENTS:
            if self.root.findall(node_element) is not None:
                for innerchild in self.root.findall(node_element):
                    label = innerchild.get("Label")
                    value = innerchild.text
                    if label in XmlReader.FIELDNAMES.keys():
                        self.data[XmlReader.FIELDNAMES[label]] = value
        if self.data.get(XmlReader.FIELDNAMES["FINDINGS"]) is None:
            return None
        return self.data
    
    def read_file(self, file_path):
        self.file_path = file_path
        tree = ET.parse(self.file_path)
        self.root = tree.getroot()
        pcm_id = self.__read_id()
        if pcm_id is None:
            # write to log file
            return None
        data_dict = self.__read_abstract_text()
        return data_dict