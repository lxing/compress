# buf: the lookahead buffer
# dic: the dictionary buffer
# limits: min/max match lengths, uncoded bits to copy each time
# bufsize: size of dic/buf

# coded/uncoded flag takes 1 bits to encode
# buffer position takes log(4096) = 12 bits to encode
# match length takes 3 bits to encode (range of 8)
# uncoded bits copy 15 at a time
# net uncoded/coded bits required: 16/16
# min/max match length: 17-24 (anything less should be uncoded for efficiency)

import sys, bitstream

# returns number of bits written from buffer
def encode(pos, length, dic, buf, limits):
  if length < limits[0]: # unencoded
    bits = [47]
    bits.extend(buf[0:limits[2]])
  else: # encoded
    bits = [49]
    bits.extend(dic[pos:min(length, limits[1])])
  bitstream.write(bits)
  return len(bits) - 1

#return (position, length) in dic of max matching substring between dic and buf
def match_buffers(dic, buf):
  bestpos = bestlength = 0  
  return (bestpos, bestlength)

def compress(dic, bufsize, limits):
  bitstream.start(sys.argv[2], sys.argv[3])
  buf = bitstream.read(bufsize)
  while len(buf) > 0:
    # find matches and encode
    match = match_buffers(dic, buf)
    length = encode(match[0], match[1], dic, buf, limits)
    # slide the window
    dic = dic[length:]
    dic.extend(buf[0:length])
    buf = buf[length:]
    buf.extend(bitstream.read(length))

def decompress(dic, limits):
  bitstream.start(sys.argv[2], sys.argv[3])
  buf = []
  length = 1
  while length > 0:
    flag = bitstream.read(1)
    if flag == [47]:
      buf = bitstream.read(limits[2])
    else:
      break
    length = len(buf)
    dic = dic[length:]
    dic.extend(buf)
    bitstream.write(buf)

bufsize = 4096
limits = (17, 24, 15)
bitstream.start('dictionary', None)
dic = bitstream.read(bufsize)

if sys.argv[1] == '-c':
  compress(dic, bufsize, limits)
elif sys.argv[1] == '-d':
  decompress(dic, limits)
else:
  print('Usage: {0} -(c/d) <infile> <outfile>'.format(sys.argv[0]))
