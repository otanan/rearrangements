#!/usr/bin/env python3
"""Takes user input for a "real" number and rearranges conditionally convergent series so that their partial sums converge to the provided number. Plots the convergence.

**Author: Jonathan Delgado**

Todo:
    * implement a Sequence object with methods such as "next" and "next_neg" etc.
    * request the desired sequence from the user.

"""
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
from matplotlib import gridspec

#------------- Matplotlib settings -------------#
# Place these settings at the end of all imports.
mpl.use('TKAgg')
# Reset any styles from imports
plt.style.use('default')
# Fonts
mpl.rcParams['font.family'] = 'serif'
# _FONT = 'cmunrm'
_FONT = 'STIX-regular'
mpl.rcParams['font.serif'] = [ mpl.font_manager.FontProperties(fname=mpl.get_data_path() + f'/fonts/ttf/{_FONT}.ttf').get_name() ]
mpl.rcParams['mathtext.fontset'] = 'cm'
# {100, 200, 300, normal, 500, 600, bold, 800, 900}
mpl.rcParams['font.weight']  = '500'
mpl.rcParams['font.size']    = 12.0 # 24.0 for papers
# Curves
mpl.rcParams['lines.linewidth'] = 1.7  # line width in points
mpl.rcParams['lines.linestyle'] = '--'
# Axis/Axes/Ticks
mpl.rcParams['axes.linewidth']  = 0.9 # line width of border
mpl.rcParams['xtick.minor.visible'] = mpl.rcParams['ytick.minor.visible'] = True
mpl.rcParams['xtick.direction'] = mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.top'] = mpl.rcParams['xtick.bottom'] = mpl.rcParams['ytick.left'] = mpl.rcParams['ytick.right'] = True
mpl.rcParams['xtick.major.size'] = mpl.rcParams['ytick.major.size'] = 7
mpl.rcParams['xtick.minor.size'] = mpl.rcParams['ytick.minor.size'] = 3
# Legend
plt.rcParams['legend.framealpha'] = 0.8 # legend transparency, range: [0,1]
#------------- End Matplotlib settings -------------#


def get_number():
    """ Request and gets a target number from user input.
    
        Returns:
            (float): the provided number.
    
    """
    x = float(input('Provide a real number:\n'))
    # x = 5.198
    print( f'Target number: {x}' )

    return x
    

def get_desired_precision():
    """ Requests the number of decimal places the rearrangement should aim to 
        agree with the target number to.
        
        Returns:
            (None): none
    
    """
    # Get the partial sums within x +- precision.
    p = int(input('Provide number of decimal points the partial sums should agree on:\n'))
    # p = 9
    print(f'Will rearrange partial sums to be within {p} decimal points of target number.')
    return 10**-p


###################### Conditionally Convergent Sequences ######################


def alternating_harmonic_sequence(n, choice=0):
    """ Provides terms of the alternating Harmonic sequence:
        (https://en.wikipedia.org/wiki/Harmonic_series_(mathematics)). Note that for this implementation all odd terms are negative.
        
        Args:
            n (int): the current index
    
        Kwargs:
            choice (0): positive choice grabs the nth positive term in the subsequence, negative choice grabs the nth negative term in the subsequence, choice of 0 grabs the nth term in the sequence.
    
        Returns:
            (float): the requested term.
    
    """
    if choice > 0:
        m = 2*n
    elif choice < 0:
        m = 2*n - 1
    else:
        m = n

    return 1/m


def alternating_log_sequence(n, choice=0):
    """ Provides terms of the logarithmic series
        (https://mathworld.wolfram.com/ConditionalConvergence.html).
        
        Args:
            n (int): the current index
    
        Kwargs:
            choice (0): positive choice grabs the nth positive term in the subsequence, negative choice grabs the nth negative term in the subsequence, choice of 0 grabs the nth term in the sequence.
    
        Returns:
            (float): the requested term.
    
    """
    if choice > 0:
        m = 2*n
    elif choice < 0:
        m = 2*n - 1
    else:
        m = n

    return np.log(m)/m
    

######################## Rearrangement body ########################


def get_partial_sums(x, sequence=alternating_harmonic_sequence, precision=10**-3):
    """ Gets the rearranged partial sums that converge to x up to the provided 
        precision.
        
        Args:
            x (float): the target number.
    
        Kwargs:
            sequence (function): the provided sequence.

            precision (float): the desired precision.
    
        Returns:
            (list): the sequence of partial sums.
    
    """
    # Tracks where we are in the subsequence of positive and negative terms
    pos_index = neg_index = 1

    # Holds the sequence of partial sums
    partial_sums = []

    # Do part of the while loop, get the last term of the sequence
    s = 0
    
    # While the partial sum has not converged to our desired degree of
        # precision
    while np.abs(s - x) > precision:

        if s < x:
            # We are underestimating the number so continue adding positive
                # terms
            s += sequence(pos_index, choice=1)
            pos_index += 1

        else:
            # We are overestimating
            s -= sequence(neg_index, choice=-1)
            neg_index += 1
            
        partial_sums.append(s)
    
    return partial_sums


#------------- Entry code -------------#


def main():
    x = get_number()
    precision = get_desired_precision()

    partial_sums = get_partial_sums(x, sequence=alternating_log_sequence, precision=precision)
    # partial_sums = get_partial_sums(x, sequence=alternating_harmonic_sequence, precision=precision)
    print('Sequence of partial sums has converged.')
    
    # Number of terms used in rearrangement
    n = len(partial_sums)
    
    print(f'There are {n} partial sums.') 
    ns = np.arange(1, n + 1)

    # Calculate the residual
    partial_sums = np.array(partial_sums)
    residual = np.abs(partial_sums - x)

    #------------- Plotting -------------#

    
    ### Subplot 1 ###

    fig = plt.figure(figsize=(12, 4)) 
    gs = gridspec.GridSpec(1, 2, figure=fig)

    ### Subplot 1 ###

    ax = fig.add_subplot(gs[0, :-1])
    # ax = fig.add_subplot(gs[0, 0])
    print('Plotting...')
    ax.plot(ns, np.full((n,), x), label='x', linestyle='-', zorder=9999)
    # Plot the partial sums
    ax.plot(ns, partial_sums, label='Rearrangement', linestyle='', marker='.', markersize=0.9)
    print('Plotting complete.')

    ax.legend(loc='lower right')
    # Technique for cutting off the left part of plot to where the partial
        # sums are closer to converging
    ax.set_xlim(left=3)
    ax.set_xscale('log')

    ### Subplot 2 ###

    ax2 = fig.add_subplot(gs[0, -1])

    print('Plotting residual.')
    ax2.plot(ns, residual, label=r'$|s_n - x|$', linestyle='', marker='.', markersize=0.6)
    ax2.set_xlim(left=3, right=n)
    ax2.set_yscale('log')
    ax2.legend(loc='upper right')
    
    plt.show()
    

if __name__ == '__main__':
    main()
