import numpy as np
import pandas as pd

from HertzsprungRussell import HertzsprungRussellDiagram, fitToIsochrone
import matplotlib.pyplot as plt

def darkkWrapper(f):
    def wrapper(*args, **kwargs):
        plt.style.use('dark_background')
        return f(*args, **kwargs)
    return wrapper


@darkkWrapper
def main():
    results = pd.read_csv(f"./ra_10.0_10.0_radius_20.0.csv")
    
    bp_rp, absolute_mag = HertzsprungRussellDiagram(results)
    
    filepath            = "/home/fredpl/Projekt/SkyCatalogue/SkyCatalogue/.cache/mist_isochrones/MIST_v1.2_feh_m3.50_afe_p0.0_vvcrit0.4_EEPS"
    target_age          = 5e6
    mass, Teff, L       = fitToIsochrone(filepath, target_age)
    
    
    mask  = np.isfinite(bp_rp) & np.isfinite(absolute_mag)
    stars = np.column_stack((bp_rp[mask], absolute_mag[mask])).astype('f4')
    
    fig, ax = plt.subplots(figsize=(12,8))
    ax.set_facecolor('#05050A')
    ax.scatter(stars[:,0], stars[:,1], s=0.5)
    ax.plot(Teff, L, '-o')
    
    ax.invert_yaxis()
    ax.set_xlim(-1, 4)
    ax.set_ylim(17, -7)
    plt.tight_layout()
    plt.show()


if __name__=="__main__":
    main()