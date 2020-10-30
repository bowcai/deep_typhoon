import torchvision.transforms as transforms


class DimensionReduce(object):
    def __call__(self, tensor):
        return tensor[0:2]  # only need Red and Green channel


transform = transforms.Compose([transforms.ToTensor(),
                                DimensionReduce(),
                                transforms.Normalize((0.5, 0.5), (0.5, 0.5))])
