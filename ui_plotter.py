# ui_plotter.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


def animate_from_csv(
    csv_path: str,
    thin_step: int = 5000,
    interval_ms: int = 20,
    repeat: bool = False,
    show_orbits: bool = True,
    show: bool = True,
    title: str | None = None,
):
    """
    Animate a 2D trajectory from a CSV with columns: t,x,y (header allowed).

    Parameters
    ----------
    csv_path : str
        Path to CSV file (expects header row; uses skiprows=1).
    thin_step : int
        Plot every thin_step-th point for speed (1 = no thinning).
    interval_ms : int
        Animation interval in milliseconds.
    repeat : bool
        Repeat animation after finishing.
    show_orbits : bool
        Draw Earth/Mars circular reference orbits.
    show : bool
        Call plt.show().
    title : str | None
        Custom title. If None, uses filename.
    """

    # ------------------------
    # Load data
    # ------------------------
    data = np.loadtxt(csv_path, delimiter=",", skiprows=1)
    if data.ndim != 2 or data.shape[1] < 3:
        raise ValueError(f"{csv_path} must have columns: t,x,y")

    t = data[:, 0]
    x = data[:, 1]
    y = data[:, 2]

    # Constants (reference only)
    r_earth = 1.496e8  # km (1 AU)
    r_mars = 1.52 * r_earth
    AU = r_earth

    # ------------------------
    # Figure setup
    # ------------------------
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal", "box")

    # Sun
    ax.plot(0, 0, "yo", markersize=10, label="Sun")

    # Optional reference orbits
    if show_orbits:
        theta = np.linspace(0, 2 * np.pi, 400)
        ax.plot(r_earth * np.cos(theta), r_earth * np.sin(theta),
                "--", linewidth=0.5, label="Earth orbit")
        ax.plot(r_mars * np.cos(theta), r_mars * np.sin(theta),
                "--", linewidth=0.5, label="Mars orbit")

    # Trajectory artists
    traj_line, = ax.plot([], [], "-", linewidth=2, label="Spacecraft")
    sc_point,  = ax.plot([], [], "ro", markersize=4)

    ax.set_xlabel("x (km)")
    ax.set_ylabel("y (km)")

    if title is None:
        title = f"Trajectory: {csv_path}"
    ax.set_title(title)

    # Axis limits from data
    r = np.sqrt(x**2 + y**2)
    rmax = float(np.max(r))
    pad = 0.2 * rmax
    ax.set_xlim(-rmax - pad, rmax + pad)
    ax.set_ylim(-rmax - pad, rmax + pad)

    # Legend outside
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1.0), borderaxespad=0)

    # Telemetry text (figure coordinates, bordered)
    info_text = fig.text(
        0.80, 0.80, "",
        ha="left", va="top",
        bbox=dict(
            boxstyle="round,pad=0.4",
            edgecolor="grey",
            facecolor="white",
            linewidth=1
        )
    )

    plt.tight_layout(rect=[0, 0, 0.75, 1])

    # ------------------------
    # Thinned frame indices
    # ------------------------
    if thin_step < 1:
        thin_step = 1

    frame_indices = list(range(0, len(x), thin_step))
    if frame_indices[-1] != len(x) - 1:
        frame_indices.append(len(x) - 1)

    # ------------------------
    # Animation functions
    # ------------------------
    def init():
        traj_line.set_data([], [])
        sc_point.set_data([], [])
        info_text.set_text("")
        return traj_line, sc_point, info_text

    def update(k):
        idx = frame_indices[k]

        traj_line.set_data(x[:idx+1], y[:idx+1])
        sc_point.set_data([x[idx]], [y[idx]])

        time_s = t[idx]
        day = time_s / 86400.0
        year = time_s / (86400.0 * 365.25)
        rad_AU = np.sqrt(x[idx]**2 + y[idx]**2) / AU

        info_text.set_text(
            f"Day:  {day:7.0f}\n"
            f"Year: {year:7.2f}\n"
            f"r:    {rad_AU:7.3f} AU"
        )

        return traj_line, sc_point, info_text

    anim = FuncAnimation(
        fig,
        update,
        frames=len(frame_indices),
        init_func=init,
        interval=interval_ms,
        blit=True,
        repeat=repeat
    )

    if show:
        plt.show()

    return anim


# Optional CLI usage:
#   python ui_plotter.py trajectory_HPI.csv --thin 5000
if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument("csv", help="CSV path with columns t,x,y")
    p.add_argument("--thin", type=int, default=5000)
    p.add_argument("--interval", type=int, default=20)
    p.add_argument("--repeat", action="store_true")
    p.add_argument("--no-orbits", action="store_true")
    args = p.parse_args()

    animate_from_csv(
        csv_path=args.csv,
        thin_step=args.thin,
        interval_ms=args.interval,
        repeat=args.repeat,
        show_orbits=not args.no_orbits,
        show=True
    )
