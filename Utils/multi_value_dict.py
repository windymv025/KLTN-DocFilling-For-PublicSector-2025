# Thêm loại dữ liệu MultiValueDict dict với key là list (Vì có thể có nhiều contextual trùng lặp).
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
        raise ValueError(f"Key not in dictionary: {key}")

    def get(self, key):
        """Retrieve the first value for the given key without removing it."""
        if key in self.data and self.data[key]:
            return self.data[key][0]  # Return first value without popping
        raise ValueError(f"Key not in dictionary: {key}")

    def pop(self, key):
        """Remove and return the first value for the given key."""
        if key in self.data and self.data[key]:
            return self.data[key].pop(0)  # Remove and return first value
        raise ValueError(f"Key not in dictionary: {key}")

    def print(self,size=None):
        for index,(key, values) in enumerate(self.data.items()):
            if size and index==size:
                break
            print(f"{key}: {values}")