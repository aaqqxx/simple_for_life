__author__ = 'XingHua'


import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import derivative

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.itervalues():
        sp.set_visible(False)


def get_vel(pos,time_inteval=1):
    vel=[]
    for index,each in enumerate(pos):
        if index<pos.size-1:
            vel.append((pos[index+1]-pos[index])/time_inteval)
    return vel
    pass

if __name__ == '__main__':
    filename = "GatherFile.txt"
    data = np.loadtxt(filename)
    print data.shape
    # plt.plot(data[:,1])
    fig, host = plt.subplots()
    # host.plot(data[:,1])
    # fig.subplots_adjust(right=0.75)

    par1 = host.twinx()

    # par2 = host.twinx()
    # par2.spines["right"].set_position(("axes", 1.2))
    # make_patch_spines_invisible(par2)
    # par2.spines["right"].set_visible(True)

    host.plot(data[:,1],label="act_pos")
    host.plot(data[:,2],label="cmd_pos")
    par1.plot(data[:,1]-data[:,2],label="fe")

    host.set_xlim(0,1000)
    plt.show()
    plt.plot(get_vel(data[:,2]))
    plt.plot(get_vel(data[:,1]))
    plt.show()
    pass