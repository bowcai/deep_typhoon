import os
from src.download_agora import download_agora
from src.create_samples import create_samples
from src.train_net import train_net
from src.test_net import test_net

if __name__ == '__main__':
    path_ = os.path.abspath('.')
    # download_agora(path_)
    # create_samples(path_)
    train_net(path_)
    # test_net(path_)
