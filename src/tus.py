from tusclient import client
from time import sleep
from os.path import getsize
from math import floor, log10
from tusclient.storage import filestorage
from progress.bar import Bar
from time import time

def byteSI(inbytes):
    scale = {0:'', 1:'K', 2:'M', 3:'G'}
    exp = log10(inbytes)
    exp = int(exp/3)
    suf = scale[exp]
    rem = inbytes/(1024**exp)
    return f"{rem:.2f} {suf}"

filename = "archlinux-2023.10.14-x86_64.iso"

ourfile = open(filename, 'br')

filesize = getsize(filename) #filesize in bytes
chunksize = 1024*256 #chunksize in bytes
#URL='http://192.168.122.245:8080/files/e023c1e96008e86a36db4a8c2e27038c'

my_client = client.TusClient('http://192.168.122.245:8080/files/')

#my_client.set_headers({'Tus-Resumable': '1.0.0'})
storage = filestorage.FileStorage('storage_file')
uploader = my_client.uploader(filename, store_url=True,
                              url_storage=storage, chunk_size=chunksize)
if not uploader.url:
    print("Created URL")
    uploader.upload_chunk()
    uploader.create_url()

offset = uploader.get_offset()
uploader.offset = offset
print(offset)
print(filesize)
print(f"Uploading {filename}")

print("=================")

#exit()

bar = Bar("Uploading", max=floor(filesize/chunksize))
bar.suffix = '%(percent).1d%%'
bar.index=int(offset/chunksize)
bar.start()
bar.update()
acc=0
while offset < filesize:
    told = time()
    uploader.upload_chunk()
    tnew = time()
    rate = chunksize/(tnew-told)
    if(acc==0):
        bar.suffix = f'%(percent).1d%% | %(eta)ds remaining | {byteSI(rate)}B/s'
    acc = acc+1
    if acc==1000:
        bar.suffix = f'%(percent).1d%% | %(eta)ds remaining | {byteSI(rate)}B/s'
        acc=1
    #print(f"uploading at {rate}bytes per second")
    #exit()
    #uploader.offset = uploader.offset+chunksize
    offset = uploader.offset
    #print(f"{offset}/{filesize}")
    bar.next()
    #bar.update()

bar.finish()