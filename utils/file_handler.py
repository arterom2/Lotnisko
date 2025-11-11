def load_data(file_path):
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split(';')
            data.append(parts)
    return data

def save_data(file_path, data_list):
    with open(file_path, 'w') as f:
        for row in data_list:
            f.write(';'.join(map(str, row)) + '\n')