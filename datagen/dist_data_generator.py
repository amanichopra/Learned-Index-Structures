import numpy as np
import random
import argparse
import pickle

def generate(dist, num_records, num_pages, std):
    if dist == 'random':
        data = np.array(random.sample(range(num_records*5), num_records))
    elif dist == 'binomial':
        data = np.random.binomial(500, 0.5, size=num_records)
    elif dist == 'poisson':
        data = np.random.poisson(8, size=num_records)
    elif dist == 'exponential':
        data = np.random.exponential(9, size=num_records)
    elif dist == 'lognormal':
        data = np.random.lognormal(5, 5, size=num_records)
    else:
        class InvalidDistributionArgumentException(Exception):
            pass
        raise InvalidDistributionArgumentException('Distribution must be one of the following: [random, binomial, poisson, exponential, lognormal]!')
    
    if std:
        data = (data - data.mean()) / data.std()
    
    data = np.array(sorted(data))
    
    memory = np.array([int(i / num_pages) for i in range(len(data))])
    
    return data, memory

def save_data(data, memory, savepath):
    with open(savepath, 'wb') as f:
        pickle.dump({'data': data, 'memory': memory}, f)
    
def main():
    parser = argparse.ArgumentParser(description='Script to generate datasets.')
    parser.add_argument('--save_path', type=str, default='../../Data', help='Path to save data.')
    parser.add_argument('--dist', type=str, default='random', help='Type of distribution to use to generate data.')
    parser.add_argument('--size', type=int, default=250000, help='Size of dataset to generate.')
    parser.add_argument('--num_pages', type=int, default=100, help='Number of pages in disk block.')
    parser.add_argument('--std', type=str, default='y', choices=['y', 'n'], help='Whether to standardize data.')
    
    args = parser.parse_args()
    if args.std == 'y':
        args.save_path += '/Standardized'
        std = True
    else:
        args.save_path += '/Unstandardized'
        std = False
    
    data, memory = generate(args.dist, args.size, args.num_pages, std)
    save_data(data, memory, f'{args.save_path}/{args.dist}.dat')

if __name__ == '__main__':
    main()