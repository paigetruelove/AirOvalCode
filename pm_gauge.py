# Please note, this code has been adapted from: http://nicolasfauchereau.github.io/climatecode/posts/drawing-a-gauge-with-matplotlib/ 

import matplotlib
from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Wedge, Rectangle # Importing the individual shapes which are used to make the gauge 

def degree_range(n): 
    """
    This function calculates basic trigonometry to draw the sectors of the gauge. 
    """
    
    start = np.linspace(0,180,n+1, endpoint=True)[0:-1]
    end = np.linspace(0,180,n+1, endpoint=True)[1::]
    mid_points = start + ((end-start)/2.)
    return np.c_[start, end], mid_points

def rot_text(ang): 
    rotation = np.degrees(np.radians(ang) * np.pi / np.pi - np.radians(90))
    return rotation

def gauge(labels = ['V.LOW','LOW','MODERATE','HIGH','V.HIGH'], \
          colors = ['#33ccff','#00cc66','#fffc38','#ff8533','#ff3333'], \
          title = 'Oval PM Concentration Index', \
          arrow=1, \
          fname="pmConcentrationIndex.png"): 
    """ 
    This function plots the gauge; including labels, arrow, gauge title, colors, sectors and so on. 
    """
    
    N = len(labels)
    
    if arrow > N: 
        raise Exception("\n\nThe category ({}) is greated than \
        the length\nof the labels ({})".format(arrow, N))
    
    # If colors is a string, we assume it's a matplotlib colormap. 
    # Else, if it's a list, this checks if the number of labels is equal to the number of colors
    if isinstance(colors, str):
        cmap = cm.get_cmap(colors, N)
        cmap = cmap(np.arange(N))
        colors = cmap[::-1,:].tolist()
    if isinstance(colors, list): 
        if len(colors) == N:
            colors = colors[::-1]
        else: 
            raise Exception("\n\nnumber of colors {} not equal \
            to number of categories{}\n".format(len(colors), N))
  
    # This plots the gauge
    fig, ax = plt.subplots()
    fig.set_facecolor("black")
    ang_range, mid_points = degree_range(N)
    labels = labels[::-1]
    
    
    # This plots the sectors and the arcs
    patches = []
    for ang, c in zip(ang_range, colors): 
        # sectors
        patches.append(Wedge((0.,0.), .4, *ang, facecolor='lightgray', lw=1, ec="black"))
        # arcs
        patches.append(Wedge((0.,0.), .4, *ang, width=0.10, facecolor=c, lw=1, ec="black", alpha=1))
    [ax.add_patch(p) for p in patches]

    
    # This sets the labels (e.g. 'V.LOW','LOW',...)
    for mid, lab in zip(mid_points, labels): 
        ax.text(0.35 * np.cos(np.radians(mid)), 0.35 * np.sin(np.radians(mid)), lab, \
            horizontalalignment='center', verticalalignment='center', fontsize=14, \
            fontweight='bold', rotation = rot_text(mid))


    # This sets the bottom rectangle and the title
    r = Rectangle((-0.4,-0.1),0.8,0.1, facecolor='lightgray', lw=1, ec="black")
    ax.add_patch(r)
    ax.text(0, -0.05, title, horizontalalignment='center', \
         verticalalignment='center', fontsize=20, fontweight='bold')


    # This plots the arrow
    pos = mid_points[abs(arrow - N)]
    ax.arrow(0, 0, 0.225 * np.cos(np.radians(pos)), 0.225 * np.sin(np.radians(pos)), \
                 width=0.04, head_width=0.09, head_length=0.1, fc='k', ec='k')
    ax.add_patch(Circle((0, 0), radius=0.02, facecolor='k'))
    ax.add_patch(Circle((0, 0), radius=0.01, facecolor='black', zorder=11))

    
    # This removes the frame and ticks, and makes axis equal and tight
    ax.set_frame_on(False)
    ax.axes.set_xticks([])
    ax.axes.set_yticks([])
    ax.axis('equal')
    plt.tight_layout()
    
    # If file name has been specified (which it is by default) then save gauge as image 
    if fname:
        fig.savefig(fname, dpi=200, facecolor="white")


