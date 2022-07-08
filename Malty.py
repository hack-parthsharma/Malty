#!/usr/bin/python
# Simple tool to combine two Maltego configuration files (mtz)
import sys
import zipfile
from base64 import urlsafe_b64encode
import os
import shutil

def mergeFolders(root_src_dir, root_dst_dir):
    for src_dir, dirs, files in os.walk(root_src_dir):
        dst_dir = src_dir.replace(root_src_dir, root_dst_dir, 1)
        if not os.path.exists(dst_dir):
            os.makedirs(dst_dir)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            if os.path.exists(dst_file):
                os.remove(dst_file)
            shutil.move(src_file, dst_dir)

scratch = "/tmp/"
print "   _________________________________________________"
print " _/ Malty: Combine two Maltego .mtz files into one. \_ "
print "   \_______________________________________________/\n"

if len(sys.argv) < 3:
  print "Error: Please supply two .mtz files as parameters to combine."
  print "A third optional paramter for output name (Default: combined.mtz)"
  exit(-1)

fileA = sys.argv[1]
fileB = sys.argv[2]
outFile = "combined.mtz"
if len(sys.argv) == 4:
  outFile = sys.argv[3]

if fileA[-4:] != ".mtz" or fileB[-4:] != ".mtz":
  print "Error: Please supply two .mtz files as parameters to combine."
  print "A third optional paramter for output name (Default: combined.mtz)"
  exit(-1)

scratchA = scratch + urlsafe_b64encode(os.urandom(8))
scratchB = scratch + urlsafe_b64encode(os.urandom(8))
scratchO = scratch + urlsafe_b64encode(os.urandom(8))

os.makedirs(scratchA)
os.makedirs(scratchB)
os.makedirs(scratchO)

print "[+] Extracting %s" % fileA
zfileA = zipfile.ZipFile(fileA)
zfileA.extractall(scratchA)
print "[+] Extracting %s" % fileB
zfileB = zipfile.ZipFile(fileB)
zfileB.extractall(scratchB)

print "[+] Combining '%s' and '%s' into '%s'..." % (fileA, fileB, outFile)
mergeFolders(scratchA, scratchO)
mergeFolders(scratchB, scratchO)

shutil.make_archive(outFile, 'zip', scratchO)
os.rename(outFile + ".zip", outFile)
