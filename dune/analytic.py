#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, np.pi, 100)
y = (1/(4*np.pi)) * (3/4) * (1 + np.cos(x)**2)

plt.plot(x, y)

plt.savefig("analytic.jpg", dpi=200)
