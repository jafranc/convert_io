from typing import List
import numpy as np


class relperm:
    #
    corey_: (int, int, (float, float, float), (float, float, float), (float, float), (float, float))

    def __init__(self, krow=np.zeros((2, 3)), krog=np.zeros((2, 3)), pcow=np.zeros((2, 3)),
                 pcog=np.zeros((2, 3))):
        self.krow_ = krow
        self.krog_ = krog

        self.pcow_ = pcow
        self.pcog_ = pcog

    def import_txt(self, fow, fog, gow, gog):
        file_ow = np.loadtxt(fow)

    # TODO complete (bored)
    def __str__(self):
        return "kr(w) range: {smin}, {smax}".format(smin=self.krow_[0, 0], smax=self.krow_[0, -1])

    def define_corey(self, corey=(0, 0, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0), (0.0, 0.0))):
        self.corey_ = corey
        self.fill_corey()

    def plot(self):
        try:
            from matplotlib import pyplot as plt

            ax1 = plt.subplot(221)
            ax1.plot(self.krow_[:, 0], self.krow_[:, 1])
            ax1.plot(self.krow_[:, 0], self.krow_[:, 2])
            ax2 = plt.subplot(222)
            ax2.plot(1 + self.krog_[:, 0], self.krog_[:, 1])
            ax2.plot(1 + self.krog_[:, 0], self.krog_[:, 2])
            ax3 = plt.subplot(223)
            ax3.plot(self.pcow_[:, 0], self.pcow_[:, 1])
            ax4 = plt.subplot(224)
            ax4.plot(1 + self.pcog_[:, 0], self.pcog_[:, 1])
            plt.show()
        except:
            raise ModuleNotFoundError

    def fill_corey(self):
        npoint = 100
        sw = np.linspace(self.corey_[2][0], 1.0, npoint)
        self.krow_ = np.zeros((npoint, 3))
        self.krow_[:, 0] = sw
        self.krow_[:, 1] = self.corey_[2][1] * np.power(sw, self.corey_[0])
        self.krow_[:, 2] = self.corey_[2][2] * np.power(1.0 - sw, self.corey_[0])

        sg = np.linspace(self.corey_[3][0], 1.0, npoint)
        self.krog_ = np.zeros((npoint, 3))
        self.krog_[:, 0] = sg
        self.krog_[:, 1] = self.corey_[3][1] * np.power(sg, self.corey_[1])
        self.krog_[:, 2] = self.corey_[3][2] * np.power(1.0 - sg, self.corey_[1])

        spw = np.linspace(self.corey_[4][0], 1.0, npoint)
        self.pcow_ = np.zeros((npoint, 2))
        self.pcow_[:, 0] = spw
        self.pcow_[:, 1] = self.corey_[4][1] * np.power(spw, -1.0 / self.corey_[0])

        spg = np.linspace(self.corey_[5][0], 1.0, npoint)
        self.pcog_ = np.zeros((npoint, 2))
        self.pcog_[:, 0] = spg
        self.pcog_[:, 1] = self.corey_[5][1] * np.power(spg, -1.0 / self.corey_[1])

    def sum_check(self):
        print("scheck")

    def sanity_check(self):
        print("san check")


if __name__ == "__main__":
    sc = relperm()
    sc.define_corey((2, 2, (0.1, 1, 1), (0.5, 0.005, 1), (0, 0), (0, 0)))
    print(sc)
    sc.plot()
