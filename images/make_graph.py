import os
from math import pi

import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

sqrt_2pi = np.sqrt(2 * pi)


def gaussian(x, s, u=0):
    return (1 / (s * sqrt_2pi)) * np.exp(-0.5 * ((x - u) / s) ** 2)


def make_plot():
    max_users = 1e6
    font_size = 35

    users = np.arange(1, max_users, max(max_users // 1000, 1))
    feedback = gaussian(users, max_users / 3.5)
    ability_to_change = gaussian(users, max_users / 6)

    ability_to_change /= ability_to_change[0]
    feedback /= feedback[0]
    feedback = 1 - feedback

    cp = sns.color_palette()
    feedback_color = cp[2]
    change_color = cp[3]

    f = plt.figure(figsize=(18, 9))
    plt.plot(users, feedback, "-", color=feedback_color, lw=5)
    plt.plot(users, ability_to_change, "-", color=change_color, lw=5)

    plt.xticks([])
    plt.yticks([])

    plt.xlabel("Users", fontsize=font_size, fontweight="bold")

    plt.annotate(
        "Feedback",
        color=feedback_color,
        xy=(0.75, 0.85),
        xycoords="axes fraction",
        fontweight="bold",
        fontsize=font_size,
    )

    plt.annotate(
        "Ability to Change",
        color=change_color,
        xy=(0.70, 0.1),
        xycoords="axes fraction",
        fontsize=font_size,
        fontweight="bold",
    )

    plt.xlim(1, max_users)
    plt.tight_layout()

    return f


if __name__ == "__main__":
    f = make_plot()

    f.savefig(os.path.join(os.path.dirname(__file__), "stable-interface-graph.png"))
    plt.show()
