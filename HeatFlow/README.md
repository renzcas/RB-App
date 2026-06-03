# Heat Equation Demos

This folder contains self‑contained experiments showing both **classical PDE solvers** and **machine learning surrogates** for the heat equation. Each script can be run standalone with:

```bash
python demos/<filename>.py

Heat/
│
├── demos/                  # all your experiment scripts
│   ├── heat_fd.py          # finite-difference solver
│   ├── heat_pinn.py        # PINN training loop
│   ├── compare_fd_pinn.py  # comparison plot
│   ├── diffusion_anim.py   # multi-step diffusion + CNN animation
│   └── __init__.py         # makes demos importable as a package
│
├── notebooks/              # optional Jupyter notebooks for exploration
│
├── requirements.txt        # list of dependencies (torch, matplotlib, numpy, etc.)
└── README.md               # explain what each demo does

Contents
• 	
Classical finite‑difference solver for the 1D heat equation.
• 	Builds a Laplacian with Dirichlet boundaries.
• 	Evolves a spike initial condition over time.
• 	Plots diffusion at start and end.
• 	
Physics‑Informed Neural Network (PINN) in PyTorch.
• 	Maps .
• 	Loss = PDE residual + boundary + initial condition.
• 	Trains with Adam and saves a checkpoint.
• 	
Side‑by‑side comparison of FD vs PINN at the same time slice.
• 	Loads  if available.
• 	Plots both curves together.
• 	
2D multi‑step animation: diffusion vs CNN transformation.
• 	Left: Kronecker‑sum Laplacian diffusion.
• 	Right: CNN surrogate applying local transforms.
Dependencies
• 	Python 3.9+
• 	PyTorch
• 	NumPy
• 	Matplot

Notes
• 	For stability in explicit Euler, choose  in 1D.
• 	Train  first to produce  before running .
• 	Scripts are standalone; no external data required.
# Heat