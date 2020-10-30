import torch
from src.my_image_folder import ImageFolder
from src.my_transform import transform
from src.define_net import Net
from torch.autograd import Variable


def test_net(path_):
    results_path = path_ + '/results'

    net = Net()

    if torch.cuda.is_available():
        net.cuda()

    net.load_state_dict(torch.load(results_path + '/net_relu.pth'))  # your net

    testset = ImageFolder(path_ + '/test_set/', transform)  # your test set

    tys = {}  # map typhoon to its max wind
    tys_time = {}  # map typhoon-time to wind

    for i in range(0, testset.__len__()):

        image, actual = testset.__getitem__(i)
        image = image.expand(1, image.size(0), image.size(1), image.size(2))  # a batch with 1 sample
        name = testset.__getitemName__(i)

        image = Variable(image)

        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        image = image.to(device)

        output = net(image).squeeze(-1)
        wind = output.data[0]
        wind = wind.item()  # Convert tensor to float data type

        name = name.split('_')

        tid = name[0]
        if tid in tys:
            if tys[tid] < wind:
                tys[tid] = wind
        else:
            tys[tid] = wind

        tid_time = name[0] + '_' + name[1] + '_' + name[2] + '_' + name[3]
        tys_time[tid_time] = wind

        if i % 100 == 99:
            print('have processed ', i + 1, ' samples.')

    tys = sorted(tys.items(), key=lambda asd: asd[1], reverse=True)
    for ty in tys:
        print(ty)  # show the sort of typhoons' wind

    tys_time = sorted(tys_time.items(), key=lambda asd: asd[0], reverse=False)

    # Write result to a csv file
    with open(results_path + '/result_relu.csv', 'w') as f:
        for ty in tys_time:
            f.write('%s,%f\n' % (ty[0], ty[1]))  # record all result by time
