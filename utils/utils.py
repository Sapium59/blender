import os
import time

# import cv2
import bpy
import numpy as np


def rename_by_timestamp(src_name, is_file):
    timestamp = time.asctime()
    timestamp = " ".join(timestamp.split()[1:4])
    timestamp = "-".join(timestamp.split(r":"))
    
    if is_file:
        root_dir, file_name = src_name.rsplit(os.path.sep, maxsplit=1)
        file_name_main, file_name_apdx = file_name.rsplit(".", maxsplit=1)
        file_name = file_name_main + "-" + timestamp + "." + file_name_apdx
        dst_name = os.path.join(root_dir, file_name)
    else:
        root_dir, leaf_dir = src_name.rsplit(os.path.sep, maxsplit=1)
        leaf_dir = leaf_dir + "-" + timestamp
        dst_name = os.path.join(root_dir, leaf_dir)
    
    return dst_name



def compute_rgba_from_percentage(percentage):
    def _foo(pp, center):
        return np.clip(3 * (1-np.abs(2*(pp - center))) - 1, 0, 1)
    r = 0.8 * sum([_foo(percentage, 1/6 + period) for period in [-1, 0, 1]])
    g = 0.8 * sum([_foo(percentage, 3/6 + period) for period in [-1, 0, 1]])
    b = 0.8 * sum([_foo(percentage, 5/6 + period) for period in [-1, 0, 1]])
    a = 1
    return (r, g, b, a)

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    def plt_power_x_a(xx, a):
        plt.figure()
        yy = np.sin(xx * np.pi / 2)
        yy = np.power(yy, a)
        plt.plot(xx, yy)
        plt.show()


    xx = np.linspace(0,1,100)
    for a in np.linspace(0, 1, 10):
        plt_power_x_a(xx, a)

        plt.figure()


    pp = np.linspace(0, 1, 100)
    xx = np.cos(pp * 2 * np.pi)
    yy = np.sin(pp * 2 * np.pi)    
    r,g,b,_ = compute_rgba_from_percentage(pp)
    
    c = np.array([r,g,b]).T.tolist()
    for c in [r, g, b]:
        plt.plot(pp, c)
    for i in range(len(pp)):
        plt.scatter(xx[i], yy[i], color=[r[i], g[i], b[i]])
    # plt.plot(pp,r)
    plt.legend(["r", "g", "b"])
    plt.show()