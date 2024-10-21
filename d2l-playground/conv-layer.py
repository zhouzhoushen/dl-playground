import torch
from torch import nn

def corr2d(X, K):
    h, w = K.shape
    Y = torch.zeros((X.shape[0] - h + 1, X.shape[1] - w + 1))
    for i in range(Y.shape[0]):
        for j in range(Y.shape[1]):
            Y[i, j] = (X[i:i + h, j:j + w] * K).sum()
    return Y

class Conv2D(nn.Module):
    def __init__(self, kernel_size):
        self.weight = nn.Parameter(torch.randn(kernel_size))
        self.bias = nn.Parameter(torch.zeros((1,)))
        
    def forward(self, X):
        return corr2d(X, self.weight) + self.bias
    
X = torch.ones((6, 8))
X[:, 2:6] = 0
K = torch.tensor([[1, -1]])
Y = corr2d(X, K)

conv2d = nn.Conv2d(1, 1, kernel_size = (1, 2), bias = False)
X = X.reshape((1, 1, 6, 8))
Y = Y.reshape((1, 1, 6, 7))
print(f"Initial kernel is {conv2d.weight.data.reshape((1, 2))}")
for i in range(20):
    Y_hat = conv2d(X)
    l = (Y_hat - Y) ** 2
    conv2d.zero_grad()
    l.sum().backward()
    conv2d.weight.data[:] -= 3e-2 * conv2d.weight.grad
    if i % 2 == 1:
        print(f"batch {i + 1}, loss {l.sum():.3f}")
print(f"After training, kernel becomes {conv2d.weight.data.reshape((1, 2))}")
