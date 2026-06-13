import numpy as np
from pathlib import Path



def computeAbsoluteMagnitude(g_mag, parallax):
    distance_pc = 1000.0 / parallax
    absolute_mag = g_mag - 5 * np.log10(distance_pc) + 5
    
    return absolute_mag


def filterByParallaxError(result, parallax_threshold=5):
    parallax = np.ma.filled(result["parallax"], np.nan)
    parallax_over_error = parallax / result["parallax_error"]
    valid_mask = (parallax > 0) & (parallax_over_error > parallax_threshold)

    return result[valid_mask]
    
    
def HertzsprungRussellDiagram(result):
    
    filtered_result = filterByParallaxError(result, parallax_threshold=5)
    
    g_mag       = np.ma.filled(filtered_result["phot_g_mean_mag"], 19.0)
    parallax    = np.ma.filled(filtered_result["parallax"], np.nan)
    
    
    bp_rp        = filtered_result["phot_bp_mean_mag"] - filtered_result["phot_rp_mean_mag"]
    absolute_mag = computeAbsoluteMagnitude(g_mag, parallax)
    
    
    return (bp_rp, absolute_mag)



def fitToIsochrone(filepath, target_age):
    '''
    Fits the Hertzsprung-Russell diagram to an isochrone.
    EEPS txz from mist has a bunch of files in it with data. Figure out how these work
    '''
    
    iso_points = []
    
    eeps_path = Path(filepath)
    for file in eeps_path.glob("*.track.eep"):
        data = read_eep(file)
        mass = float(file.name.split("M")[0]) / 100
        
        print(file.name, data.shape, mass)
        ages = data["star_age"]
        
        if target_age < ages.min() or target_age > ages.max():
                continue
        
        idx = np.argmin(np.abs(ages - target_age))
            
        iso_points.append((
                mass,
                data["log_Teff"][idx],
                data["log_L"][idx]
            ))
    
    
    iso_points.sort(key=lambda x: x[0])
    mass, logTeff, logL = zip(*iso_points)
    
    return (mass, logTeff, logL)



def read_eep(file):
    with open(file, "r") as f:
        lines = f.readlines()

    header_idx = None

    # Find the header with actual column names
    for i, line in enumerate(lines):
        if line.startswith("#") and "star_age" in line:
            header_idx = i
            break

    if header_idx is None:
        raise ValueError(f"Could not find header in {file}")

    # Clean column names (remove '#')
    header_line = lines[header_idx].replace("#", "").strip()

    col_names = header_line.split()

    data = np.genfromtxt(
        file,
        skip_header=header_idx + 1,
        names=col_names,
        dtype=None,
        encoding=None,
    )

    return data
    
    
    