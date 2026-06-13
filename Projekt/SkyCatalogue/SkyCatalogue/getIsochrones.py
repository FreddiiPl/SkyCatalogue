from urllib.parse import ParseResult, urlunparse
from pathlib import Path
import requests
import os
import tarfile



class MISTIsochroneEEPSData:
    SCHEME        = "https"
    NETWORK       = "waps.cfa.harvard.edu"
    BASE          = "/MIST/data/tarballs"
    
    base_feh_afe  = {
        "v1.2": {
            "m3.50": ["p0.0"], 
            "m4.0": ["p0.0"], 
            "m3.0": ["p0.0"], 
            "m2.50": ["p0.0"], 
            "m2.0": ["p0.0"], 
            "m1.75": ["p0.0"], 
            "m1.50": ["p0.0"], 
            "m1.25": ["p0.0"], 
            "m1.0": ["p0.0"], 
            "m0.75": ["p0.0"], 
            "m0.50": ["p0.0"], 
            "m0.25": ["p0.0"], 
            "p0.0": ["p0.0"], 
            "p0.25": ["p0.0"],
            "p0.50": ["p0.0"]
            },
        
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
        self.vvcrit  = kwargs.get("vvcrit", "0.4")
        
        self.feh     = kwargs.get("feh", list(self.base_feh_afe[f"v{self.version}"].keys())[0])    
        self.afe     = kwargs.get("afe", self.base_feh_afe[f"v{self.version}"][self.feh][0])
        
        
        print(f"Using version: v{self.version} with vvcrit = {self.vvcrit}, feh = {self.feh}, afe = {self.afe}")
                    
        if self.version == "1.2":
            self.base_path     = f"{MISTIsochroneEEPSData.BASE}_v{self.version}/"
        else:
            self.base_path     = f"{MISTIsochroneEEPSData.BASE}_v{self.version}/eeps"
        
        self.default_cache_dir()
        self.filename = f"MIST_v{self.version}_feh_{self.feh}_afe_{self.afe}_vvcrit{self.vvcrit}_EEPS.txz"
        
        
        self.filepath = Path(self.cache_dir) / self.filename



    def default_cache_dir(self,dir=None):
        if dir is None:
            dir = os.path.join(os.path.expanduser("."), ".cache", "mist_isochrones")
            
            
        
        self.cache_dir = Path(dir).expanduser().resolve().absolute()
        
        
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    
    def base_url(self):
        components = ParseResult(
            scheme=MISTIsochroneEEPSData.SCHEME,
            netloc=MISTIsochroneEEPSData.NETWORK,
            path=self.base_path,
            params="",
            query="",
            fragment="",
        )
        
        return urlunparse(components)
        

    def download(self,):
        if not hasattr(self, "url"):
            self.url = f"{self.base_url()}/{self.filename}"
        
        print(self.url)
        

        if self.filepath.is_file():
                print(f"File already exists: {self.filepath}")
                return self.filepath
            
        try:
            print("Fetching response...")
            response = requests.get(self.url, stream=True)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print("HTTP Error:", e)
            print("Response text:", response.text[:1000])
            
        
        total_bytes = int(response.headers.get("content-length", 0))
        chunk_size = 1024 * 1024  # 1 MB
        downloaded = 0
        
        
        with open(self.filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if total_bytes > 0:
                            percent = downloaded / total_bytes * 100
                            print(f"\rProgress: {percent:5.1f}% ({downloaded}/{total_bytes} bytes)", end="")
        
        
        print(f"\nDownload complete: {self.filepath}")
        return self.filepath
     
     
    def extract(self):
        with tarfile.open(self.filepath, "r:xz") as tar:
            tar.extractall(path=self.cache_dir)
       
    
    def available_feh_afe(self):
        keys = self.base_feh_afe[f"v{self.version}"].keys()
        vals = self.base_feh_afe[f"v{self.version}"].values()
        
        
        print(f"Available metallicities for v{self.version} are:\n {', '.join(keys)}\n")
        for key in keys:
            vals_for_feh = self.base_feh_afe[f"v{self.version}"][key]
            print(f"Available afe for v{self.version} and metallicity {key} are:\n {', '.join(vals_for_feh)}")
        

if __name__ == "__main__":
    mist = MISTIsochroneEEPSData()
    mist.download()
 
    
    
    