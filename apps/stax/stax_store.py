class StaxStore:
    variables = {}

    @staticmethod
    def keys():
        return StaxStore.variables.keys()

    @staticmethod
    def set(key, value):
        StaxStore.variables[key] = value

    @staticmethod
    def get(key, default=None):
        return StaxStore.variables.get(key, default)

    @staticmethod
    def clear():
        StaxStore.variables.clear()
