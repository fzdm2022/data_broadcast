import random
import string


class RandomDataGenerator:
    def __init__(self, data_type='mixed', length=5):
        """
        Initialize the generator with the data type and the length of each data item.
        :param data_type: Type of data to generate ('numbers', 'letters', 'mixed').
        :param length: Length of each data item.
        """
        self.data_type = data_type
        self.length = length

    def generate_random_data(self, num_data):
        """
        Generate a line of random data.
        :param num_data: Number of data items to generate.
        :return: A string of random data items separated by commas.
        """
        data = []
        for _ in range(num_data):
            if self.data_type == 'numbers':
                random_data = ''.join(random.choices(string.digits, k=self.length))
            elif self.data_type == 'letters':
                random_data = ''.join(random.choices(string.ascii_letters, k=self.length))
            else:  # 'mixed'
                random_data = ''.join(random.choices(string.ascii_letters + string.digits, k=self.length))
            data.append(random_data)

        return ','.join(data)


# Example usage:
if __name__ == "__main__":
    num_data = int(input("Enter the number of data points: "))
    data_type = input("Enter the data type (numbers, letters, mixed): ")
    length = int(input("Enter the length of each data item: "))

    generator = RandomDataGenerator(data_type=data_type, length=length)
    random_data_line = generator.generate_random_data(num_data)
    print(random_data_line)
