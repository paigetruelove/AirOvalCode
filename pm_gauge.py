# Please note, this code has been adapted from: http://nicolasfauchereau.github.io/climatecode/posts/drawing-a-gauge-with-matplotlib/ 

import pandas as pd
import matplotlib
from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
import datetime
from matplotlib.patches import Circle, Wedge, Rectangle # Importing the individual shapes which are used to make the gauges 

plt.style.use('dark_background')

def degree_range(n): 
    """
    This function calculates basic trigonometry to draw the sectors of the gauges. 
    """
    
    start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
    end = np.linspace(0,180,n+1, endpoint=True)[1::]
    mid_points = start + ((end-start)/2.)
    return np.c_[start, end], mid_points

def rot_text(ang): 
    rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
    return rotation

def gauge(labels = ['V.LOW','LOW','AVERAGE','HIGH','V.HIGH'], \
          colors1= "Oranges_r", \
          colors2= "Blues_r", \
          title1 = 'PM 10', \
          title2 = 'PM 2.5', \
          arrow1=1, \
          arrow2=1, \
          fname="pmConcentrationIndex.png"): 
    """ 
    This function plots two gauges, one for PM 10 and PM 2.5; including labels, arrows, gauge titles, colors, sectors and so on. 
    """
    
    N = len(labels)
    
    # Gauge 1 
    if arrow1 > N: 
        raise Exception("\n\nThe category ({}) is greated than \
        the length\nof the labels ({})".format(arrow1, N))
        
    # Gauge 2    
    if arrow2 > N: 
        raise Exception("\n\nThe category ({}) is greated than \
        the length\nof the labels ({})".format(arrow2, N))
    
    # If colors is a string, we assume it's a matplotlib colormap. 
    # Else, if it's a list, this checks if the number of labels is equal to the number of colors
    # Gauge 1 
    if isinstance(colors1, str):
        cmap = cm.get_cmap(colors1, N)
        cmap = cmap(np.arange(N))
        colors1 = cmap[::-1,:].tolist()
    if isinstance(colors1, list): 
        if len(colors1) == N:
            colors1 = colors1[::-1]
        else: 
            raise Exception("\n\nnumber of colors {} not equal \
            to number of categories{}\n".format(len(colors1), N))       
    # Gauge 2
    if isinstance(colors2, str):
        cmap = cm.get_cmap(colors2, N)
        cmap = cmap(np.arange(N))
        colors2 = cmap[::-1,:].tolist()
    if isinstance(colors2, list): 
        if len(colors2) == N:
            colors2 = colors2[::-1]
        else: 
            raise Exception("\n\nnumber of colors {} not equal \
            to number of categories{}\n".format(len(colors2), N))

    # This plots the two gauges
    fig, ax = plt.subplots(1, 2)
    fig.suptitle("Daily PM Concentration Gauge", y=0.9, fontsize=14, fontweight='bold')
    fig.set_facecolor("white")
    ang_range, mid_points = degree_range(N)
    labels = labels[::-1]
    
    
    # This plots the sectors and the arcs
    patches = []
    for ang, c in zip(ang_range, colors1): 
        # sectors
        patches.append(Wedge((0.,0.), .4, *ang, facecolor='lightgray', lw=1, ec="black"))
        # arcs
        patches.append(Wedge((0.,0.), .4, *ang, width=0.10, facecolor=c, lw=1, ec="black", alpha=0.7))
    [ax[0].add_patch(p) for p in patches]
    
    patches = []
    for ang, c in zip(ang_range, colors2): 
        # sectors
        patches.append(Wedge((0.,0.), .4, *ang, facecolor='lightgray', lw=1, ec="black"))
        # arcs
        patches.append(Wedge((0.,0.), .4, *ang, width=0.10, facecolor=c, lw=1, ec="black", alpha=0.7))
    [ax[1].add_patch(p) for p in patches]

    
    # This sets the labels (e.g. 'V.LOW','LOW',...)
    for mid, lab in zip(mid_points, labels): 
        ax[0].text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab, \
            horizontalalignment='center', verticalalignment='center', color="black", fontsize=7, \
            fontweight='bold', rotation = rot_text(mid))
        
        ax[1].text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab, \
            horizontalalignment='center', verticalalignment='center', color="black", fontsize=7, \
            fontweight='bold', rotation = rot_text(mid))


    # This sets the bottom rectangles and the titles
    # Gauge 1 
    r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='lightgray', lw=1, ec="black")
    ax[0].add_patch(r)
    ax[0].text(0, -0.05, title1, horizontalalignment='center', \
         verticalalignment='center', fontsize=14, color="black", fontweight='bold')
    
    # Gauge 2
    r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='lightgray', lw=1, ec="black")
    ax[1].add_patch(r)
    ax[1].text(0, -0.05, title2, horizontalalignment='center', \
         verticalalignment='center', fontsize=14, color="black", fontweight='bold')


    # This plots the arrows
    # Gauge 1
    pos = mid_points[abs(arrow1 - N)]
    ax[0].arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                 width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')
    ax[0].add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
    ax[0].add_patch(Circle((0, 0), radius=0.01, facecolor='black', zorder=11))
    
    # Gauge 2
    pos = mid_points[abs(arrow2 - N)]
    ax[1].arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                 width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')
    ax[1].add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
    ax[1].add_patch(Circle((0, 0), radius=0.01, facecolor='black', zorder=11))

    
    # This removes the frame and ticks, and makes axis equal and tight
    # Gauge 1
    ax[0].set_frame_on(False)
    ax[0].axes.set_xticks([])
    ax[0].axes.set_yticks([])
    ax[0].axis('equal')
    
    # Guage 2 
    ax[1].set_frame_on(False)
    ax[1].axes.set_xticks([])
    ax[1].axes.set_yticks([])
    ax[1].axis('equal')
    plt.tight_layout()
    
    # If file name has been specified (which it is by default) then save gauges as image 
    if fname:
        fig.savefig(fname, dpi=200, facecolor="black")