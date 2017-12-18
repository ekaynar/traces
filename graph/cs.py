
from matplotlib.ticker import StrMethodFormatter, NullFormatter
import sys
import numpy as np
import operator
from operator import itemgetter
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from collections import deque
from lru import LRU

from boltons.cacheutils import LRU as botlru
from boltons.cacheutils import LRI

def per(argv):
    fd = open(sys.argv[1], 'r')
    tot=0
    liste=[]
    for line in fd:
	value = line.split(" ")
	liste.append(value[0])
	tot+=float(value[0])
    fd.close()
    print tot
    fd = open(sys.argv[1]+".per", 'w')
    for item in liste:	
        per = float(item)/tot 
	out= item+ " "+str(per)+"\n"
	fd.write(out)
    fd.close()



def zipf(argv):
    liste=[]
    fd = open(sys.argv[1], 'r')
    for line in fd:
        value = line.split(" ")
        liste.append(int(value[0]))
    liste.sort(reverse=True)
    print len(liste)-1
    print (liste[0])
    print (liste[len(liste)-1])
    fig= plt.figure(figsize=(6,3))
    ax = plt.subplot(111)
    ax.plot(liste, color='b', linewidth=3.0,  label='Access_Freq')
    plt.grid()
    ax.set_ylabel('File Access Frequency', fontsize=14)
    ax.set_xlabel('Objects Rank By Descending \n Access Frequency', fontsize=14)
    #plt.yscale('log')
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_ylim(ymin=0.9)
    ax.set_xlim(xmin=0.9)
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
    axins = zoomed_inset_axes(ax, 2.5,  loc=4,
                     bbox_to_anchor=(0.93, 0.6),
                     bbox_transform=ax.figure.transFigure)
  #  axins = zoomed_inset_axes(ax, 2.5, loc=4, 
#			bbox_to_anchor=(0.95, 0.5)) 
    axins.plot(liste, color='b', linewidth=3.0)
    #x1, x2, y1, y2 = 600000, 1400000, 1, 5 # specify the limits
    axins.axis([1000000, 5000010, 0.9, 4])
    mark_inset(ax, axins, loc1=2, loc2=4, fc="none", ec="0.5")
    #plt.xscale('log')
    #plt.yscale('log')
#    labels = [item.get_text() for item in axins.get_xticklabels()]
#    print labels
#    plt.xticks([ ])
    #axins.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    #plt.xticklabels([600000,1400000], minor=False, rotation=45)
    plt.xticks(rotation=80,fontsize=14)
    plt.yticks(fontsize=14)
    #axins.xaxis.set_major_formatter(StrMethodFormatter('{x:.0f}'))
    #axins.xaxis.set_minor_formatter(NullFormatter())
#    plt.tick_params(axis='x', which='major')
    plt.xticks([1000000,2000000,3000000,4000000,5000000])
    plt.yticks([1,2,3,4])
    plt.minorticks_off()
#plt.xticks(visible=False) 
    #axins.set_xlim(x1, x2) # apply the x-limits
    #axins.set_ylim(y1, y2) # apply the y-limits
    plt.grid()
   



####################################3
    perc=[]
    fd2 = open(sys.argv[2], 'r')
    for line in fd2:
        value = line.split(" ")
        perc.append(float(value[1])*100)
    perc.sort(reverse=True)
    cumulative = np.cumsum(perc)
    fd2.close()
    df = pd.DataFrame({ "perc": cumulative})
    ax2 = ax.twinx()
    ax2.plot( cumulative, label='CDF', c='red', linewidth=2)
    #ax2.set_xticks(xticks_major)
    ax2.set_xscale('log')
    ax2.set_ylim(ymin=0.9)
    ax2.set_xlim(xmin=0.9)
    ax2.set_ylabel('Cummulative Percentage', fontsize=13)
    ax2 = plt.gca()
    ax2.set_ylim(0,1.05*df["perc"].max())
    lines1,l1=ax.get_legend_handles_labels()
    lines2, l2=ax2.get_legend_handles_labels()
    #ax2.legend(lines1 + lines2, l1 + l2, loc='upper center',bbox_to_anchor=(0.5, 1.2), ncol=2)
    ax2.legend(lines1 + lines2, l1 + l2, loc='lower left',ncol=1)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)
    plt.subplots_adjust(left=0.13, bottom=0.26, right=0.63, top=0.95,
                wspace=0.2, hspace=0.2)
    plt.savefig('allfreq.eps')
    plt.savefig('allfreq.pdf')
    plt.show()



if __name__ == "__main__":
    zipf(sys.argv[1:])
    #per(sys.argv[1:])
