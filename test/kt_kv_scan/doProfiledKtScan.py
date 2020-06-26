import pickle
import matplotlib
import numpy as np
from scipy.interpolate import griddata
matplotlib.use('Qt4Agg')
import matplotlib.pyplot as plt

def print_header(axes, x_low, x_high, y_low, y_high, inside = False, logscale = False):
  y_val = y_high + 0.015 * (y_high - y_low)
  if inside:
    axes.text(x_low + abs(x_low) * 0.045, y_high - 0.46 * (y_high - y_low), 'CMS', style='normal', fontsize=15, fontweight='bold')
  else:
    axes.text(x_low, y_val, 'CMS', style='normal', fontsize=14, fontweight='bold') # 15 for a 6 X 6 figure                            
  #axes.text(x_low + (x_high - x_low) * 0.14, y_val, 'Preliminary', fontsize=15, style='italic') # for a 6 X 6 figure                 
  axes.text(x_low + (x_high - x_low) * 0.15, y_val, 'Preliminary', fontsize=14, style='italic') # for a 5 X 5 figure                  
  if logscale:
    axes.text(x_low + (x_high - x_low) * 0.67, y_high + 0.05 * (y_high - y_low), '137 fb$^{-1}$ (13 TeV)', fontsize=12)
  else:
    axes.text(x_low + (x_high - x_low) * 0.57+0.2, y_high + 0.01 * (y_high - y_low), '137 fb$^{-1}$ (13 TeV)', fontsize=12)


ct,cv,dnll=pickle.load(open('save.p','rb'))
x1 = np.linspace(-2, 2, 1000)
y1 = np.linspace(0.55, 2, 1000)

x2, y2 = np.meshgrid(x1, y1, sparse=False)
z2 = griddata((ct, cv), dnll, (x2, y2), method='cubic')
z2=np.nan_to_num(z2)


kt=x2.flatten()
kv=y2.flatten()
z2_flat=z2.flatten()
z2_constrain=np.copy(z2_flat)

# adding twice (kv-1.9)^2/sigma
correction=np.vectorize(lambda x : 2*(x-1.09)**2/0.17**2 if x < 1.09 else 2*(x-1.09)**2/0.12**2)
z2_constrain = (z2_constrain+correction(kv)).reshape(z2.shape)

#fig, axs = plt.subplots(1, 3)
#axs[1].pcolormesh( x2,y2, z2_constrain)
#axs[0].pcolormesh( x2,y2, z2)
#axs[2].plot( x1, np.amin(z2_constrain,0) )
#fig.tight_layout()
#plt.savefig('technical_plot.png',dpi=200)

kt_scan=np.amin(z2_constrain,0)
kt_scan=kt_scan-np.amin(kt_scan)



fig, ax = plt.subplots(figsize=(5,5))
fig.patch.set_facecolor('white')
ax.get_xaxis().set_major_locator(matplotlib.ticker.MultipleLocator(1.0))
ax.get_xaxis().set_minor_locator(matplotlib.ticker.MultipleLocator(0.10))
ax.get_yaxis().set_major_locator(matplotlib.ticker.MultipleLocator(10))
ax.get_yaxis().set_minor_locator(matplotlib.ticker.MultipleLocator(1))

line_obs, = ax.plot(x1, kt_scan, label='Observed',color='k')
ax.axhline(1.0, lw=0.5, ls='--', color='gray')
ax.axhline(4.0, lw=0.5, ls='--', color='gray')
ax.axhline(9.0, lw=0.5, ls='--', color='gray')
ax.axhline(16.0, lw=0.5, ls='--', color='gray')
ax.axhline(25.0, lw=0.5, ls='--', color='gray')

ax.text(2 + 0.02*2, 1.0-0.2, "1$\\sigma$", fontsize=14, color='gray')
ax.text(2 + 0.02*2, 4.0-0.2, "2$\\sigma$", fontsize=14, color='gray')
ax.text(2 + 0.02*2, 9.0-0.2, "3$\\sigma$", fontsize=14, color='gray')
ax.text(2 + 0.02*2, 16.0-0.2, "4$\\sigma$", fontsize=14, color='gray')
ax.text(2 + 0.02*2, 25.0-0.2, "5$\\sigma$", fontsize=14, color='gray')

y_low, y_high=0,50
x_low, x_high=-2,2
ax.set_ylim(y_low, y_high)
ax.set_xlim(x_low, x_high)
ax.set_xlabel("$\\kappa_\\mathrm{t}$" , fontsize=16, labelpad=5)
ax.set_ylabel("$-2\\Delta$ ln$(\\mathcal{L})$", fontsize=16, labelpad=5)


print_header(ax, x_low, x_high, y_low, y_high)

legend = plt.legend(handles=[line_obs], fontsize=12, loc='upper right', frameon=True)
legend.get_frame().set_facecolor('white')
legend.get_frame().set_linewidth(0)
ax.add_artist(legend)



legend.get_frame().set_facecolor('white')
legend.get_frame().set_linewidth(0)




plt.savefig('ktscan_profiled.pdf')

