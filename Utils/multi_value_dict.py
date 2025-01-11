class MultiValueDict:
    def __init__(self):
        self.data = {}

    def add(self, key, value):
        if key not in self.data:
            self.data[key] = []
        self.data[key].append(value)

    def get_and_pop(self, key):
        if key in self.data and self.data[key]:
            return self.data[key].pop(0)
<<<<<<< HEAD
        raise ValueError(f"Key not in dictionary")
=======
        raise ValueError("Key not in dictionary")
>>>>>>> 5bf4af3cabce276c9eab0587b04835f567ad043a
