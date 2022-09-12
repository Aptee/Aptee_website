import urllib.request  
def generatekey(seed=0):
    for line in urllib.request.urlopen('https://drive.google.com/uc?export=veiw&id=1aDl21knHjUUVhrjBVb_os69SvskjXDo8'):
        if line.decode('utf-8')[0:2] == 'k@':
            return line.decode('utf-8')[2:]
