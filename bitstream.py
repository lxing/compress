import struct

def start(infile_name, outfile_name):
  global infile, outfile
  infile = open(infile_name,'r')
  if outfile_name != None:
    outfile = open(outfile_name, 'w')
  
def read(n):
  bits = infile.read(n)
  return list(struct.unpack('{0}b'.format(len(bits)), bits))
  
def write(bits):
  for bit in bits:
    outfile.write(struct.pack('b',bit))
