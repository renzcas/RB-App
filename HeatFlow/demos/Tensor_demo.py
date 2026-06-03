import torch

# 1. Create a simple 1D tensor (vector)
x = torch.tensor([1, 2, 3, 4])
print("1D tensor:", x)

# 2. Create a 2D tensor (matrix)
y = torch.tensor([[1, 2], [3, 4]])
print("2D tensor:\n", y)

# 3. Create a tensor of zeros
z = torch.zeros((2, 3))
print("Zeros tensor:\n", z)

# 4. Create a tensor of random numbers
r = torch.rand((3, 3))
print("Random tensor:\n", r)

# 5. Check tensor shape and type
print("Shape:", r.shape)
print("Data type:", r.dtype)

# 6. Move tensor to GPU (if available)
if torch.cuda.is_available():
    r = r.to("cuda")
    print("Tensor on GPU:", r)