import random
from bb84.cascade.key import Key

class Shuffle:

    _random = random.Random()

    SHUFFLE_NONE = 0
    """Do not shuffle the bits in the key."""
    SHUFFLE_RANDOM = 1
    """Randomly shuffle the bits in the key."""

    def __init__(self, key, algorithm):
        """
        Create a shuffle, i.e. shuffle the bits of a key according to some algorithm.

        Args:
            key (Key): The key to be shuffled. The key itself is not modified in any way; all the
                bookkeeping to keep track of the shuffling is in the created Shuffle object.
            algorirthm (int): How to shuffle the bits in the key.
                SHUFFLE_NONE: Do not shuffle the key (keep the key bits in the original order).
                SHUFFLE_RANDOM: Randomly shuffle th key.
        """

        # Validate arguments.
        assert isinstance(key, Key)
        assert algorithm in [self.SHUFFLE_NONE, self.SHUFFLE_RANDOM]

        # The key underlying this block.
        self._key = key

        # Map the shuffle indexes to key indexes.
        self._shuffle_index_to_key_index = {}
        for index in range(0, key.size):
            self._shuffle_index_to_key_index[index] = index
        if algorithm == self.SHUFFLE_RANDOM:
            random.shuffle(self._shuffle_index_to_key_index, Shuffle._random.random)

    def __repr__(self):
        """
        Get the unambiguous string representation of the shuffle.

        Returns:
            The unambiguous string representation of the shuffle.
        """
        string = "Shuffle:"
        for shuffle_index in range(self.size):
            key_index = self._shuffle_index_to_key_index[shuffle_index]
            key_bit = self._key.get_bit(key_index)
            string += f" {shuffle_index}->{key_index}={key_bit}"
        return string

    def __str__(self):
        """
        Get the human-readable string representation of the shuffle.

        Returns:
            The human-readable string representation of the shuffle.
        """
        string = ""
        for i in range(self.size):
            string += str(self.get_bit(i))
        return string

    @staticmethod
    def set_random_seed(seed):
        """
        Set the seed for the isolated random number generated that is used only in the shuffle
        module and nowhere else. The application can set the seed to a specific value to make
        experimental results reproducable.

        Args:
            seed (int): The seed value for the random number generator which is isolated to the
                shuffle module.
        """
        Shuffle._random = random.Random(seed)

    @property
    def size(self):
        """
        Get the size of the shuffled key in bits.

        Returns:
            The size of the shuffled key in bits.
        """
        return self._key.size

    def get_bit(self, index):
        """
        Get the key bit value for the given shuffle index.

        Args:
            index (int): The shuffle index of the bit. Index must be in range [0, shuffle.size).

        Returns:
            The value (0 or 1) of the key bit at the given shuffle index.
        """

        # Validate arguments.
        assert isinstance(index, int)
        assert index in self._shuffle_index_to_key_index

        # Return the key bit.
        key_index = self._shuffle_index_to_key_index[index]
        return self._key.get_bit(key_index)

    def set_bit(self, index, value):
        """
        Set the key bit value for the given shuffle index.

        Args:
            index (int): The shuffle index of the bit. Index must be in range [0, shuffle.size).
            value (int): The new value of the bit. Must be 0 or 1.
        """

        # Validate arguments.
        assert isinstance(index, int)
        assert index in self._shuffle_index_to_key_index
        assert isinstance(value, int)
        assert value in [0, 1]

        # Return the key bit.
        key_index = self._shuffle_index_to_key_index[index]
        self._key.set_bit(key_index, value)

    def flip_bit(self, index):
        """
        Flip the value of the shuffle bit at a given shuffle index (0 to 1, and vice versa).

        Args:
            index (int): The shuffle index of the bit. Index must be in range [0, shuffle.size).
        """

        # Validate arguments.
        assert isinstance(index, int)
        assert 0 <= index < self.size

        # Flip the bit value.
        key_index = self._shuffle_index_to_key_index[index]
        self._key.flip_bit(key_index)

    def get_key_index(self, shuffle_index):
        """
        Get the key index that a given shuffle index is mapped to.

        Args:
            shuffle_index (int): The shuffle index of the bit. Index must be in range
                [0, shuffle.size).

        Returns:
            The key index.
        """

        # Validate arguments.
        assert isinstance(shuffle_index, int)
        assert shuffle_index in self._shuffle_index_to_key_index

        # Return the key index.
        return self._shuffle_index_to_key_index[shuffle_index]