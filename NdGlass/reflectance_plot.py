# coding:utf-8
#!/usr/bin/env python

from math import *

__author__ = 'XingHua'

"""

"""


def get_data(start, end, step):
    Ts1 = []
    Tp1 = []
    Rs2 = []
    Rp2 = []
    Rs3 = []
    Rp3 = []
    Ts4 = []
    Tp4 = []
    Ks1 = []
    Kp1 = []
    Ks1_Kp1 = []

    for i in range(start, end, step):
        #for i in range(0, 1):

        #    i = 45.0

        theta1 = i / 180.0 * pi

        n_air = 1.0
        n_nv = 1.5306

        theta2 = asin(n_air * sin(theta1) / n_nv)

        #absorption coefficiency......
        alpha = 0.0012
        l = 22.5 / cos(theta2) / 10
        print("l = ", l)

        # interface 1   transmission
        ts1 = n_nv * cos(theta2) / (n_air * cos(theta1)) * ((2 * sin(theta2) * cos(theta1) / sin(theta1 + theta2)) ** 2)
        tp1 = n_nv * cos(theta2) / (n_air * cos(theta1)) * (
            (2 * sin(theta2) * cos(theta1) / sin(theta1 + theta2) / cos(theta1 - theta2)) ** 2)

        print("input angle is ", i)
        print("ts1 = ", ts1)
        print("tp1 = ", tp1)
        print("\n")
        Ts1.append(ts1)
        Tp1.append(tp1)

        n_glue = 1.5312
        theta3 = pi / 2 - theta2
        theta4 = asin(n_nv * sin(theta3) / n_glue)

        # interface 2  reflectance
        rs2 = (sin(theta3 - theta4) / sin(theta3 + theta4)) ** 2
        rp2 = (tan(theta3 - theta4) / tan(theta3 + theta4)) ** 2
        print("rs2 = ", rs2)
        print("rp2 = ", rp2)
        print("\n")
        Rs2.append(rs2)
        Rp2.append(rp2)

        # interface 2 transmission (from n_nv to n_glue)
        ts21 = n_glue * cos(theta4) / (n_nv * cos(theta3)) * (
            (2 * sin(theta4) * cos(theta3) / sin(theta3 + theta4)) ** 2)
        tp21 = n_glue * cos(theta4) / (n_nv * cos(theta3)) * (
            (2 * sin(theta4) * cos(theta3) / sin(theta3 + theta4) / cos(theta3 - theta4)) ** 2)
        print("ts21 = ", ts21)
        print("tp21 = ", tp21)
        print("\n")

        # interface 2 transmission (from n_glue to n_nv)
        ts22 = n_nv * cos(theta3) / (n_glue * cos(theta4)) * (
            (2 * sin(theta3) * cos(theta4) / sin(theta3 + theta4)) ** 2)
        tp22 = n_nv * cos(theta3) / (n_glue * cos(theta4)) * (
            (2 * sin(theta3) * cos(theta4) / sin(theta3 + theta4) / cos(theta3 - theta4)) ** 2)

        print("ts22 = ", ts22)
        print("tp22 = ", tp22)
        print("\n")

        n_cu = 1.5336
        theta5 = theta4
        theta6 = asin(n_glue / n_cu * sin(theta4))

        # interface 3 reflectance
        rs3 = (sin(theta5 - theta6) / sin(theta5 + theta6)) ** 2
        rp3 = (tan(theta5 - theta6) / tan(theta5 + theta6)) ** 2

        print("rs3 = ", rs3)
        print("rp3 = ", rp3)
        print("\n")
        Rs3.append(rs3)
        Rp3.append(rp3)

        theta7 = theta2
        theta8 = theta1
        # interface 4 transmission
        ts4 = (n_air * cos(theta8)) / (n_nv * cos(theta7)) * (
            (2 * sin(theta8) * cos(theta7) / sin(theta7 + theta8)) ** 2)
        tp4 = (n_air * cos(theta8)) / (n_nv * cos(theta7)) * (
            (2 * sin(theta8) * cos(theta7) / sin(theta7 + theta8) / cos(theta7 - theta8)) ** 2)

        #print("theta7 = ", theta7)
        #print("theta8 = ", theta8)

        print("ts4 = ", ts4)
        print("tp4 = ", tp4)
        print("\n")
        Ts4.append(ts4)
        Tp4.append(tp4)

        #print("ts21*rs22*ts22 = ", ts21*rs22*ts22)
        #print("tp21*rp22*tp22 = ", tp21*rp22*tp22)
        #print("\n")

        Ks = ts1 * (rs2 + rs3) * ts4 * exp(-2 * alpha * l)
        Kp = tp1 * (rp2 + rp3) * tp4 * exp(-2 * alpha * l)

        Ks1.append(Ks)
        Kp1.append(Kp)
        Ks1_Kp1.append(Ks / Kp)

        print("Ks = ", Ks)
        print("Kp = ", Kp)
        print("Ks/Kp = ", Ks / Kp)
        print("\n")

    #    return Ts1, Tp1, Ts3, Tp3, Rs22, Rp22,Ks1, Kp1
    return {"Ts1": Ts1, "Tp1": Tp1, "Ts4": Ts4, "Tp4": Tp4, "Rs2": Rs2, "Rp2": Rp2, "Rs3": Rs3, "Rp3": Rp3, "Ks1": Ks1,
            "Kp1": Kp1}


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    x = range(10, 90, 10)
    i = 0
    label = ["Ts1", "Tp1", "Ts4", "Tp4", "Rs3", "Rp3", "Ks1", "Kp1"]
    #data_all=get_data(10,90,5)
    data_all = get_data(10, 90, 10)
    for key in data_all.keys():
        print data_all[key]

    #plt.semilogy(x,data_all["Rs2"],'-*',markersize=14, label="Rs2")


    font = {'family': 'serif',
            'color': 'darkred',
            'weight': 'normal',
            'size': 16,
    }

    # nnnn=plt.text(80, 0.65, r'$\cos(2 \pi t) \exp(-t)$', fontdict=font)

    # plt.semilogy(x,data_all["Rs2"],'-*',markersize=14, label="Rs2")
    plt.semilogy(x, data_all["Rs2"], '-*', markersize=14, label=r'$R_{s2}$')
    plt.semilogy(x, data_all["Rp2"], '-*', markersize=14, label="$R_{p2}$")
    plt.semilogy(x, data_all["Rs3"], '-*', markersize=14, label="$R_{s3}$")
    plt.semilogy(x, data_all["Rp3"], '-*', markersize=14, label="$R_{p3}$")
    plt.semilogy(x, data_all["Ks1"], '-*', markersize=14, label="$\eta_s$")
    plt.semilogy(x, data_all["Kp1"], '-*', markersize=14, label="$\eta_p$")

    plt.xlabel("Input angle (degree)")

    plt.legend()

    plt.show()
    

