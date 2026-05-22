from SkyQuery import queryData
from astropy.coordinates import SkyCoord
from astropy import units as u

def main():
    dr = "DR3"
    
    skycoord = SkyCoord(ra=10.0*u.deg, dec=10.0*u.deg, frame='icrs')
    radius   = 20.0 * u.deg
    
    query = queryData(dr=dr, sky_coord=skycoord, radius=radius, login=False)
    
    results = query.get_photometric_data_rgb(mags=True, errors=True)
    
    query.write_results_to_csv(results, f"./ra_10.0_10.0_radius_20.0.csv")
    


if __name__=="__main__":
    main() 