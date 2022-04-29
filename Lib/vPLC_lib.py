
class Tag:
    def __init__(self, value=None, OPC=False, SQL=False):
        self.value = value
        self.OPC = OPC
        self.SQL = SQL

    def __setattr__(self, key, value):
        if value == "value":
            print(key, value)

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value

