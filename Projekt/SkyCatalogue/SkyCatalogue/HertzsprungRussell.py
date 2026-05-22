import numpy as np



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



def fitToIsochrone(bp_rp, absolute_mag):
    '''
    Fits the Hertzsprung-Russell diagram to an isochrone.
    '''
    
    
    
    