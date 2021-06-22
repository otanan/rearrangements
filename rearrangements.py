#!/usr/bin/env python3
"""Takes user input for a "real" number and rearranges conditionally convergent series so that their partial sums converge to the provided number. Plots the convergence.

**Author: Jonathan Delgado**

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


# Get the partial sums within x +- precision.
PRECISION = 10E-8
POS_INDEX = NEG_INDEX = 1

def alternating_harmonic_sequence(n, pos=True):
    """ Provides terms of the alternating Harmonic sequence.
        
        Args:
            n (int): the current index
    
        Kwargs:
            pos (bool): True if the number should be mapped to an even term (corresponds to the positive terms of the Harmonic sequence) and False if it should be mapped to an odd term (corresponds to negative terms).
    
    
        Returns:
            (None): none
    
    """
    return 1/(2*n) if pos else 1/( 2*(n + 1) )
    

def get_number():
    # x = float(input('Provide a real number:\n'))
    # x = 0.5423
    x = 5.198
    print( f'x: {x}' )

    return x
    

def get_partial_sums(x, partial_sums=[0]):
    """ Recursive function to get partial sums by calling back on itself as the
        sequence converges more closely to requested real number.
        
        Args:
            arg1 (arg1 type): arg1 description.
    
        Kwargs:
            karg1 (arg1 type): arg1 description.
    
    
        Returns:
            (None): none
    
    """
    global POS_INDEX, NEG_INDEX

    while partial_sums[-1] <= x:
        # Check if we're within our desired precision
        if np.abs(partial_sums[-1] - x) < PRECISION:
            # Remove the leading zero
            return partial_sums[1:]
        
        s = partial_sums[-1] + alternating_harmonic_sequence(POS_INDEX, pos=True)

        print( f's: {s}. n: {POS_INDEX + NEG_INDEX}' )
        
        POS_INDEX += 1

        partial_sums.append(s)


    while partial_sums[-1] >= x:
        # Check if we're within our desired precision
        if np.abs(partial_sums[-1] - x) < PRECISION:
            return partial_sums[1:]


        s = partial_sums[-1] - alternating_harmonic_sequence(NEG_INDEX, pos=False)
        NEG_INDEX += 1
        
        partial_sums.append(s)

    # We aren't within our desired level of precision so go again
    try:
        return get_partial_sums(x, partial_sums=partial_sums)
    except RecursionError:
        print('Recursion error, returning partial sums as-is.')
        return partial_sums[1:]


#------------- Entry code -------------#

def main():
    print('rearrangements.py')

    x = get_number()

    partial_sums = get_partial_sums(x)
    print( f'partial_sums: {partial_sums}' )
    
    #------------- Plotting -------------#
    # Number of terms used in rearrangement
    n = len(partial_sums)
    ns = np.arange(1, n + 1)


    fig = plt.figure(figsize=(16, 4)) 
    gs = gridspec.GridSpec(1, 2, figure=fig)

    ax = fig.add_subplot(gs[0, :-1])
    ax.plot(ns, np.full((n,), x), label='x', linestyle='-', zorder=9999)
    # Plot the partial sums
    ax.plot(ns, partial_sums, label='Rearrangement', linestyle='', marker='.', markersize=0.9)

    ax.legend(loc='lower left')
    ax.set_xlim(left=3)
    ax.set_ylim(bottom=4.9, top=5.3)

    ax2 = fig.add_subplot(gs[0, -1])
    alternating_harmonic_sequence = np.array(
        [ (-1)**n * 1/n for n in range(1, n+1) ]
    )
    partial_sums = [
        alternating_harmonic_sequence[:i].sum()
        for i in range(1, n+1)
    ]

    ax2.plot(ns, partial_sums, label='Partial sums', linestyle='', marker='.', markersize=0.9)
    ax2.set_xlim(left=3)
    ax2.set_ylim(bottom=-0.75, top=-0.65)
    ax2.legend(loc='lower right')
    
    
    plt.show()
    

if __name__ == '__main__':
    main()
