import struct

class DistanceTable:
    def __init__(self, size):
        """
        Stores distance as a single byte (0-254).
        255 represents 'Unvisited'.
        """
        self.size = size
        self.data = bytearray([255] * size)

    def set(self, i, value):
        if i < 0 or i >= self.size:
            raise IndexError("Index out of range")
        self.data[i] = value

    def get(self, i):
        return self.data[i]

    def __len__(self):
        return self.size

    def to_file(self, filename):
        """Save: [4 bytes size] + [raw bytearray data]"""
        with open(filename, 'wb') as f:
            f.write(struct.pack('!I', self.size))
            f.write(self.data)

    @classmethod
    def from_file(cls, filename):
        """Load from binary file"""
        with open(filename, 'rb') as f:
            size_data = f.read(4)
            if not size_data:
                raise EOFError("File is empty")
            size = struct.unpack('!I', size_data)[0]
            instance = cls(size)
            instance.data = bytearray(f.read())
            return instance