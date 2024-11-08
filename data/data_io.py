import numpy as np
from game.board import create_data

def write_boards(boards, filename):
    np.savez_compressed(filename, *boards)
    print(f'Wrote dataset of size {len(boards)} to {filename}')

def load_boards(filename):
    with np.load(filename) as data:
        print(f'Loading dataset of size {len(data)} from {filename}')
        return [data[key] for key in data]

def create_dataset(size):
    data = create_data(30, 16, 99, size)
    dataset = [point[0] for point in data]
    labels = [point[1] for point in data]
    write_boards(dataset, 'board_dataset.npz')
    write_boards(labels, 'labels.npz')

def get_data_and_labels(xfile, yfile):
    data = load_boards(xfile)
    labels = load_boards(yfile)
    return [data, labels]

if __name__ == '__main__':
    create_dataset(3000)
    data, labels = get_data_and_labels('board_dataset.npz', 'labels.npz')
    # print(data)
    # print(labels)

