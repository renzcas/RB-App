#!/usr/bin/env python3
"""
Basic tensor operations with PyTorch:
- Addition
- Multiplication
- Matrix product
- Gradient tracking
"""

import torch

def main():
    # Simple tensors
    a = torch.tensor([1.0, 2.0, 3.0])
    b = torch.tensor([4.0, 5.0, 6.0])

    print("a:", a)
    print("b:", b)

    # Addition
    print("a + b =", a + b)

    # Elementwise multiplication
    print("a * b =", a * b)

    # Matrix product
    A = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    B = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
    print("A @ B =", A @ B)

    # Gradient tracking
    x = torch.tensor(3.0, requires_grad=True)
    f = x**2 + 2*x + 1
    f.backward()
    print("f(x) =", f.item())
    print("df/dx at x=3 =", x.grad.item())

if __name__ == "__main__":
    main()