import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# ------------------------
# 1. Load data from C++
# ------------------------
data = np.loadtxt("trajectory.csv", delimiter=",", skiprows=1)
t = data[:, 0]   # time (s) – optional for labels if you want
x = data[:, 1]   # km
y = data[:, 2]   # km

# If you want Earth/Mars radii for reference circles:
mu = 1.327e11      # km^3/s^2
r_earth = 1.496e8  # km
r_mars = 1.52 * r_earth

# ------------------------
# 2. Set up the figure
# ------------------------
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_aspect('equal', 'box')

# Plot Sun
ax.plot(0, 0, 'yo', markersize=10, label='Sun')

# Optional: Earth & Mars orbits
theta = np.linspace(0, 2*np.pi, 400)
ax.plot(r_earth * np.cos(theta), r_earth * np.sin(theta), '--', linewidth=0.5, label='Earth orbit')
ax.plot(r_mars * np.cos(theta), r_mars * np.sin(theta), '--', linewidth=0.5, label='Mars orbit')

# Spacecraft path + point
traj_line, = ax.plot([], [], '-', linewidth=2, label='Spacecraft')
sc_point, = ax.plot([], [], 'ro', markersize=4)

# Axis limits (pad a bit beyond Mars)
pad = 0.1 * r_mars
ax.set_xlim(-r_mars - pad, r_mars + pad)
ax.set_ylim(-r_mars - pad, r_mars + pad)
ax.set_xlabel('x (km)')
ax.set_ylabel('y (km)')
ax.set_title('Low-Thrust Transfer from Earth to Mars')
ax.legend(loc='upper right')

# ------------------------
# 3. Animation functions
# ------------------------
def init():
    traj_line.set_data([], [])
    sc_point.set_data([], [])
    return traj_line, sc_point

def update(frame):
    # Draw trajectory up to current frame
    traj_line.set_data(x[:frame+1], y[:frame+1])

    # Current spacecraft position: wrap in lists so they’re sequences
    sc_point.set_data([x[frame]], [y[frame]])

    return traj_line, sc_point


# You can thin frames if there are too many
frames = range(0, len(x), 5000)
#frames = len(x)

anim = FuncAnimation(
    fig,
    update,
    frames=frames,
    init_func=init,
    interval=20,   # ms per frame
    blit=True,
    repeat=False
)

plt.show()

# To save as a video (optional, needs ffmpeg installed):
# anim.save("earth_to_mars_trajectory.mp4", fps=30, dpi=150)
