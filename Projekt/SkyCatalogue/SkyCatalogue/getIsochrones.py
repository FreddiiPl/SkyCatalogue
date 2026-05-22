from urllib.parse import ParseResult, urlencode, urlunparse
import requests
import os


class MISTIsochroneEEPSData:
    SCHEME        = "http"
    NETWORK       = "waps.cfa.harvard.edu"
    BASE          = "/MIST/data/tarballs"
    
    base_feh      = {
        "v1.2": ["m4.0", "m3.50", "m3.0", "m2.50", "m2.0", "m1.75", "m1.50", "m1.25", "m1.0", "m0.75", "m0.50", "m0.25", "p0.0", "p0.25", "p0.50"],
        
        "v2.5": {
            "m400": ["m2", "p0", "p2", "p4", "p6"],
            "m350": ["m2", "p0", "p2", "p4", "p6"],
            "m300": ["m2", "p0", "p2", "p4", "p6"],
            "m250": ["m2", "p0", "p2", "p4", "p6"],
            "m200": ["m2", "p0", "p2", "p4", "p6"],
            "m175": ["m2", "p0", "p2", "p4", "p6"],
            "m150": ["m2", "p0", "p2", "p4", "p6"],
            "m125": ["m2", "p0", "p2", "p4", "p6"],
            "m100": ["m2", "p0", "p2", "p4", "p6"],
            "m075": ["m2", "p0", "p2", "p4", "p6"],
            "m050": ["m2", "p0", "p2", "p4", "p6"],
            "m025": ["m2", "p0", "p2", "p4", "p6"],
            "p000": ["m2", "p0", "p2", "p4", "p6"],
            "p025": ["m2", "p0", "p2", "p4", "p6"],
            "p050": ["m2", "p0", "p2", "p4"],
        }
        }
    
     
    def __init__(self, **kwargs):
        
        
        
        # Default values for optional parameters -> version 1.2, vvcrit 0.4
        self.version = kwargs.get("version", "1.2")
        self.vvcrit  = kwargs.get("vvcrit", 0.4)

            
        if not kwargs:
            print(f"Using default values - version: {self.version}, vvcrit: {self.vvcrit}")
                    
        
        self.base_version = f"{MISTIsochroneEEPSData.BASE}_v{self.version}" 
        self.urlparams    = f"MIST_v{self.version}_vvcrit{self.vvcrit}"
        self.path         = self.base_version + "/" + self.urlparams
        
        
    def base_filename(self):
        '''
        MIST Filenames for eeps are discrete
        '''
        pass


    def default_cache_dir(self):
        cache_dir = os.path.join(os.path.expanduser("."), ".cache", "mist_isochrones")
        os.makedirs(cache_dir, exist_ok=True)
        
        return cache_dir
    
    
    def base_url(self):
        components = ParseResult(
            scheme=MISTIsochroneEEPSData.SCHEME,
            netloc=MISTIsochroneEEPSData.NETWORK,
            path=self.path,
            params="",
            query="",
            fragment="",
        )
        
        return urlunparse(components)


if __name__ == "__main__":
    mass, age, feh = (1.03, 9.72, -0.11)
    mist_data = MISTIsochroneEEPSData(mass, age, feh)
    
    cache_dir = mist_data.default_cache_dir()
    url       = mist_data.base_url()
    
    base = mist_data.base_filename()
    
    print(base)
    
    
    
    