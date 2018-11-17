import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import urllib
import os

def mkdir(dirname=None, filename=None):
    """
    Make a directory structure
    Inputs:
        dirname: Make a directory with this name, or:
        filename: Make a directory for this file
    """
    if (dirname is None) and (filename is not None):
        dirname = os.path.dirname(filename)
    #fi
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    #fi
#edef

def download(url, filename, username=None, password=None, overwrite=False):
    """
    Download a file from the web using requests interface. Doesn't allow FTP.
    Inputs:
        url: String. Access this url
        filename: String. Where to store this file once it's downloaded
        username, password: authentication to use
        overwrite: If the file exists, re-download the file and overwrite it. (Default false)
    Output:
        True if file exists or download is successful
        False otherwise
    """
    if not(os.path.exists(filename)) or overwrite:
        #urllib.request.urlretrieve(urls[resolution], fileName)
        auth = HTTPBasicAuth(username, password) if not((username is None) and (password is None)) else None
        r = requests.get(url, auth=auth)

        if r.status_code == 200:
            with open(filename, 'wb') as out:
                for bits in r.iter_content():
                    out.write(bits)
                #efor
            #ewith
            return True # It worked
        #fi
        print(r)
        return False # We failed
    #fi
    return True # File exists
#edef

def download_ftp(url, filename, overwrite=False):
    """
    Download a file from the web, allows for FTP
    Inputs:
        url: String. Access this url
        filename: String. Where to store this file once it's downloaded
        overwrite: If the file exists, re-download the file and overwrite it. (Default false)
    Output:
        True if file exists or download is successful
        False otherwise
    """
    if not(os.path.exists(filename)) or overwrite:
        urllib.request.urlretrieve(url, filename)

        if not(os.path.exists(filename)):
            return False
        #fi
    #fi

    return True

#fi
