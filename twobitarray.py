class BitArray2:
    def __init__(self, size):
        """
        initial 2-bit array
        every bit store 0~3
        """
        if size <= 0:
            raise ValueError("Size must be positive")

        self.size = size
        self.byte_size = (size + 3) // 4  # 1 byte = 4 elements
        self.data = bytearray([0xFF] * self.byte_size)

    def _check_index(self, i):
        if i < 0 or i >= self.size:
            raise IndexError("Index out of range")

    def set(self, i, value):
        """
        set i val
        """
        self._check_index(i)

        if value < 0 or value > 3:
            raise ValueError("Value must be between 0 and 3")

        byte_index = i // 4
        offset = (i % 4) * 2

        self.data[byte_index] &= ~(0b11 << offset)

        self.data[byte_index] |= (value << offset)

    def get(self, i):
        """
        get ith val
        """
        self._check_index(i)

        byte_index = i // 4
        offset = (i % 4) * 2

        return (self.data[byte_index] >> offset) & 0b11

    def clear(self, i):
        """set to 3(not check)"""
        self.set(i, 3)

    def memory_usage(self):
        return len(self.data)

    def __len__(self):
        return self.size

"""

if __name__ == "__main__":
    N = 2217093120  # 約 22 億個「2-bit 元素」

    print("Initializing 2-bit array...")
    arr = BitArray2(N)

    print(f"Total elements: {len(arr)}")
    print(f"Memory usage: {arr.memory_usage() / (1024**2):.2f} MB")

    i = 1_000_000_000

    print(f"\nSetting index {i} to value 3")
    arr.set(i, 3)

    print("Value:", arr.get(i))        # 3
    print("Next value:", arr.get(i+1)) # 0

    print("\nSetting more values...")
    arr.set(123, 1)
    arr.set(456, 2)
    arr.set(789, 3)

    print(arr.get(123), arr.get(456), arr.get(789))
"""