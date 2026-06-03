import torch

# Create two tensors
a = torch.tensor([2.0, 3.0], requires_grad=True)
b = torch.tensor([4.0, 5.0])

# Addition
c = a + b
print("Addition:", c)

# Elementwise multiplication
d = a * b
print("Multiplication:", d)

# Matrix product
M1 = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
M2 = torch.tensor([[2.0, 0.0], [1.0, 3.0]])
mat_prod = torch.matmul(M1, M2)
print("Matrix product:\n", mat_prod)