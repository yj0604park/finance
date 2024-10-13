class BatchCreation:
    def __init__(self, file_path, delimiter):
        self.file_path = file_path
        self.delimiter = delimiter

    def load_file(self):
        with open(self.file_path) as file:
            header = file.readline().strip().split(self.delimiter)
            columns = len(header)
            for line in file:
                data = line.strip().split(self.delimiter)
                if len(data) != columns:
                    raise Exception(f"Invalid data: {data}")
                yield dict(zip(header, line.strip().split(self.delimiter)))
            data = file.read().split(self.delimiter)
        return data

    def create_batch(self):
        for data in self.load_file():
            print(data)
