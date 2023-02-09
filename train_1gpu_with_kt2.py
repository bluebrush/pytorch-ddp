"""
Mostly based on the official pytorch tutorial
Link: https://pytorch.org/tutorials/beginner/blitz/cifar10_tutorial.html
Modified for educational purposes.
Nikolas, AI Summer 20222
"""
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
#from torchvision import transforms, datasets, models
import time


def create_data_loader_cifar10():
    transform = transforms.Compose(
        [
            transforms.RandomResizedCrop(224),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    
#    transforms.Compose(
#        [
#        transforms.RandomCrop(32),
#        transforms.RandomHorizontalFlip(),
##        transforms.ToTensor(),
#        transforms.Normalize((0.5, 0.5, 0.5), (0.5, 0.5, 0.5))])

    batch_size = 256
    print(F"batch_size: {batch_size}")

#    args.dataset = './dataset2/'
#
#    trainset = datasets.ImageFolder(
#        os.path.join(args.dataset, 'train'), transform=transform_train
#    )
#    testset = datasets.ImageFolder(
#        os.path.join(args.dataset, 'val'), transform=transform_val
#    )
#    trainloader = torch.utils.data.DataLoader(
#        dataset=trainset,
#        num_workers=args.num_workers,
#        shuffle=True,
#        pin_memory=True,
#        **kwargs,
#    )
#    testloader = torch.utils.data.DataLoader(
#        dataset=testset,
#        num_workers=args.num_workers,
#        shuffle=False,
#        pin_memory=True,
#        **kwargs,
#    )
#
#    num_classes = len(trainset.classes)
#    kwargs = {'num_classes': num_classes}
#    print(f'num_classes:{num_classes}')


    trainset = torchvision.datasets.ImageFolder(root='./dataset2/train',
                                           transform=transform)
    trainloader = torch.utils.data.DataLoader(
                                            trainset, 
                                            num_workers=16, 
                                            shuffle=True, 
                                            pin_memory=True,
                                            batch_size=batch_size,
                                            )

    testset = torchvision.datasets.ImageFolder(root='./dataset2/val', 
                                           transform=transform)
    testloader = torch.utils.data.DataLoader(
                                            testset, 
                                            num_workers=16,
                                            shuffle=False, 
                                            batch_size=batch_size
                                            )
    return trainloader, testloader
#
#    trainset = torchvision.datasets.CIFAR10(root='./data', train=True,
#                                            download=True, transform=transform)
#    trainloader = torch.utils.data.DataLoader(trainset, batch_size=batch_size,
#                                            shuffle=True, num_workers=10, pin_memory=True)
#
#    testset = torchvision.datasets.CIFAR10(root='./data', train=False,
#                                        download=True, transform=transform)
#    testloader = torch.utils.data.DataLoader(testset, batch_size=batch_size,
#                                            shuffle=False, num_workers=10)
#    return trainloader, testloader


def train(net, trainloader):
    print("Start training...")
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)
    epochs = 1
    num_of_batches = len(trainloader)
    for epoch in range(epochs):  # loop over the dataset multiple times

        running_loss = 0.0
        for i, data in enumerate(trainloader, 0):
            # get the inputs; data is a list of [inputs, labels]
            inputs, labels = data

            images, labels = inputs.cuda(), labels.cuda() 

            # zero the parameter gradients
            optimizer.zero_grad()

            # forward + backward + optimize
            outputs = net(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()

            # print statistics
            running_loss += loss.item()
        
        print(f'[Epoch {epoch + 1}/{epochs}] loss: {running_loss / num_of_batches:.3f}')
    
    print('Finished Training')


def test(net, PATH, testloader):
    net.load_state_dict(torch.load(PATH))

    correct = 0
    total = 0
    # since we're not training, we don't need to calculate the gradients for our outputs
    with torch.no_grad():
        for data in testloader:
            images, labels = data

            images, labels = images.cuda(), labels.cuda() 
            # calculate outputs by running images through the network
            outputs = net(images)
            # the class with the highest energy is what we choose as prediction
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    acc = 100 * correct // total
    print(f'Accuracy of the network on the 10000 test images: {acc} %')


if __name__ == '__main__':
    start = time.time()
    
    import torchvision
    
    PATH = './cifar_net.pth'
    trainloader, testloader = create_data_loader_cifar10()
    net = torchvision.models.resnet50(False).cuda()
    start_train = time.time()
    train(net, trainloader)
    end_train = time.time()
    # save
    torch.save(net.state_dict(), PATH)
    # test
    test(net, PATH, testloader)

    end = time.time()
    seconds = (end - start)
    seconds_train = (end_train - start_train)
    print(f"Total elapsed time: {seconds:.2f} seconds, \
     Train 1 epoch {seconds_train:.2f} seconds")


