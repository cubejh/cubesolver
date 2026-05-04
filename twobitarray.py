"""
not using this since change the idea of building table
"""

import struct

class BitArray2:
    def __init__(self, size):
        """
        initial 2-bit array
        every bit store 0~3
        """
        self.size = size
        self.byte_size = (size + 3) // 4  # 1 byte = 4 elements
        self.data = bytearray([0xFF] * self.byte_size)

    def _check_index(self, i):
        if i < 0 or i >= self.size:
            raise IndexError("Index out of range")

    def set(self, i, value):
        self._check_index(i)
        if value < 0 or value > 3:
            raise ValueError("Value must be between 0 and 3")

        byte_index = i // 4
        offset = (i % 4) * 2
        self.data[byte_index] &= ~(0b11 << offset)
        self.data[byte_index] |= (value << offset)

    def get(self, i):
        self._check_index(i)
        byte_index = i // 4
        offset = (i % 4) * 2
        return (self.data[byte_index] >> offset) & 0b11

    def clear(self, i):
        self.set(i, 3)

    def memory_usage(self):
        return len(self.data)

    def __len__(self):
        return self.size

    def to_file(self, filename):
        """
        save to data [4 bytes (size)] + [raw data]
        """
        with open(filename, 'wb') as f:
            f.write(struct.pack('!I', self.size))
            f.write(self.data)

    @classmethod
    def from_file(cls, filename):
        """
        read BitArray2
        """
        with open(filename, 'rb') as f:
            size_data = f.read(4)
            if not size_data:
                raise EOFError("File is empty")
            
            size = struct.unpack('!I', size_data)[0]
            
            instance = cls(size)
            instance.data = bytearray(f.read())
            
            return instance

"""
if __name__ == "__main__":

    ba = BitArray2(10)
    ba.set(0, 1)
    ba.set(1, 2)
    ba.set(9, 0)
    print(f"original : {[ba.get(i) for i in range(10)]}")

    filename = "test_bitarray.bin"
    ba.to_file(filename)
    print(f"save to {filename}")

    new_ba = BitArray2.from_file(filename)
    print(f"reade data: {[new_ba.get(i) for i in range(len(new_ba))]}")
    print(f"read size: {new_ba.size}")
    """