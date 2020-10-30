from src.define_net import Net
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.init as init
import torch.optim as optim
import torch
from torch.utils.data import DataLoader
import os
from src.my_transform import transform
from src.my_image_folder import ImageFolder


def testset_loss(dataset, network):
    loader = DataLoader(dataset, batch_size=1, num_workers=2)

    all_loss = 0.0
    for data in loader:
        inputs, labels = data
        inputs = Variable(inputs)

        outputs = network(inputs).squeeze(-1)
        all_loss = all_loss + abs(labels[0] - outputs.data[0])

    return all_loss / len(loader)


def train_net(path_):
    results_path = path_ + '/results'

    if not os.path.exists(results_path):
        os.mkdir(results_path)

    trainset = ImageFolder(path_ + '/train_set/', transform)
    trainloader = DataLoader(trainset, batch_size=8,
                             shuffle=True, num_workers=2)
    testset = ImageFolder(path_ + '/test_set/', transform)

    net = Net()
    init.xavier_uniform_(net.conv1.weight.data, gain=1)
    init.constant_(net.conv1.bias.data, 0.1)
    init.xavier_uniform_(net.conv2.weight.data, gain=1)
    init.constant_(net.conv2.bias.data, 0.1)
    # net.load_state_dict(torch.load(results_path+'/net_relu.pth'))
    print(net)

    criterion = nn.L1Loss()

    optimizer = optim.Adam(net.parameters(), lr=0.001)

    for epoch in range(10):

        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):

            inputs, labels = data
            inputs, labels = Variable(inputs), Variable(labels)

            optimizer.zero_grad()

            outputs = net(inputs).squeeze(-1)
            loss = criterion(outputs, labels.float())
            loss.backward()
            optimizer.step()

            running_loss += loss.item()
            if i % 200 == 199:
                print(('[%d, %5d] loss: %.3f' % (epoch + 1, i + 1, running_loss / 200)))
                running_loss = 0.0

        test_loss = testset_loss(testset, net)
        print(('[%d ] test loss: %.3f' % (epoch + 1, test_loss)))

    print('Finished Training')
    torch.save(net.state_dict(), results_path + '/net_relu.pth')
