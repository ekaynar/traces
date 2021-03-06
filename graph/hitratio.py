import numpy as np
import matplotlib.pyplot as plt
import time
import sys
import pandas as pd

def draw(argv):

    data = np.genfromtxt(sys.argv[1], delimiter=',' ,skip_header=0, names=['x', 'y'])
    data2 = np.genfromtxt(sys.argv[2], delimiter=',' ,skip_header=0, names=['x','y'])
    data3 = np.genfromtxt(sys.argv[3], delimiter=',' ,skip_header=0, names=['x','y'])
    data4 = np.genfromtxt(sys.argv[4], delimiter=',' ,skip_header=0, names=['x','y'])


    fig = plt.figure(figsize=(12,6))
    ax1 = fig.add_subplot(111)   
    ax1.plot( data['x']/148017203512793*100, label='FIFO',marker='^',markersize=10,markeredgecolor='none', c='green', linewidth=2)
    ax1.plot( data2['x']/148017203512793*100, label='LRU',marker='s',markersize=10,markeredgecolor='none', c='blue', linewidth=2)
    ax1.plot( data3['x']/148017203512793*100, label='LFU',marker='o',markersize=10,markeredgecolor='none', c='magenta', linewidth=2)
    ax1.plot( data4['x']/148017203512793*100, label='Infinite',marker='o',markersize=10,markeredgecolor='none', c='red', linewidth=2)


    plt.ylabel('Hit Ratio (%)',  fontsize=20)
    plt.xlabel('Cache Size (%)',  fontsize=20)
    ax1.grid(True)

    #ax1.set_ylim(60,100)
    xlabels=["1 (125GB)" , "2", "3", "4","5", "6","7","8","9","10" ]
    xticks_major = np.arange(len(data['y']))
    ax1.set_xticks(xticks_major)
    ax1.set_xticklabels(xlabels,minor=False)
    plt.yticks(np.arange(0, 100, 10))
    ax1.tick_params(axis='both', which='major', labelsize=18 , top='off')
    ax1.legend( loc=4,fontsize=18)

    plt.subplots_adjust(left=0.12, bottom=0.21, right=0.90, top=0.90 , wspace=0.2 ,hspace=0.2 )
    plt.savefig("Hitratio.pdf",bbox_inches='tight')
    plt.savefig("hitratio.eps",bbox_inches='tight')
    plt.show()


if __name__ == "__main__":
    draw(sys.argv[1:])

