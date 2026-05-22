from astroquery.gaia import Gaia
from dotenv          import load_dotenv
import astropy.units as u
import pandas as pd
import os




class queryData:
    
    DATA_RELEASE        = {"DR2": "gaiadr2", "DR3": "gaiadr3"}
    ASYNC_THRESHOLD_DEG = 2.0
    
    
    def __init__(self,dr,
                 sky_coord=None,
                 radius=None, 
                 login=False):
        
        dr = dr.upper()
        
        if dr not in self.DATA_RELEASE.keys():
            raise ValueError(f"Data release {dr} not supported. Supported releases: {self.DATA_RELEASE}")
        
        self.dr_src = self.DATA_RELEASE[dr]   
            
        if login:
            
            load_dotenv("../credentials.env")
            username = os.getenv('GAIA_USERNAME')
            password = os.getenv('GAIA_PASSWORD')
            
            
            Gaia.login(user=username, password=password)
        
        if sky_coord is not None:
            self.ra_deg  = sky_coord.ra.deg
            self.dec_deg = sky_coord.dec.deg
        
        if radius is not None:
            self.radius = radius.to(u.deg)
            
        
        if login:    
            Gaia.logout()
    
    
    def write_results_to_csv(self, results, filename):
        df = results.to_pandas()
        df.to_csv(filename, index=False)
        
    
    def _build_base_query(self,top=None,
                          errors=False, 
                          extra_columns=None):
        
        if top is not None:
            top_clause = f"TOP {top}"
        else:
            top_clause = ""
            
        
        columns = "source_id, ra, dec, parallax, pmra, pmdec"
        if extra_columns:
            columns += f", {extra_columns}"
        
        if errors:
            columns += ", ra_error, dec_error, parallax_error, pmra_error, pmdec_error"
        
        return f"""
        SELECT {top_clause} {columns}
        FROM {self.dr_src}.gaia_source
        WHERE CONTAINS (POINT('ICRS', ra, dec),
                        CIRCLE('ICRS', {self.ra_deg}, {self.dec_deg}, {self.radius.value})
                        ) = 1
        """
    
    
    def execute_query(self,top=None, extra_columns=None, errors=False):
        self.query = self._build_base_query(top=top, extra_columns=extra_columns, errors=errors)
        
        if self.radius.value > self.ASYNC_THRESHOLD_DEG:
            job = Gaia.launch_job_async(self.query)
            return job.get_results()
        else:
            return Gaia.launch_job(self.query).get_results()
        
        
    def get_photometric_data_rgb(self,top=None, mags=True, errors=False):
        '''
        rp: Integrated red-band photometer brightness.
        phot_g_mean_mag: G-band mean magnitude
        phot_bp_mean_mag: Integrated blue-band photometer brightness.
        '''
        
        if mags:
            extra = "phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag"
        else:
            extra = "phot_g_mean_flux, phot_bp_mean_flux, phot_rp_mean_flux"
        
        
        if errors:
            extra += ", phot_g_mean_mag_error, phot_bp_mean_mag_error, phot_rp_mean_mag_error"
        
        return self.execute_query(top=top, extra_columns=extra, errors=errors)