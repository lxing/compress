import sys, bitstream

# returns number of bits written from buffer
def encode(pos, length, dic, buf, consts):
  if length < consts['min']: # not worth encoding, just dump the buffer
    bits = [consts['uncoded']]
    length = consts['max']
    bits.extend(buf[:consts['max']])
  else: # encode the buffer as a match
    bits = [consts['coded']]
    length = min(length, consts['max'])
    bits.extend(dic[pos:length])
  bitstream.write(bits)
  return length

#return (position, length) in dic of max matching substring between dic and buf
def match_buffers(dic, buf):
  bestpos = bestlength = 0  
  return (bestpos, bestlength)

def compress(dic, consts):
  bitstream.start(sys.argv[2], sys.argv[3])
  buf = bitstream.read(consts['max'])
  while buf != []:
    # find matches and encode
    match = match_buffers(dic, buf)
    length = encode(match[0], match[1], dic, buf, consts)
    # slide the window
    del dic[:length]
    dic.extend(buf[:length])
    del buf[:length]
    buf.extend(bitstream.read(length))

def decompress(dic, consts):
  bitstream.start(sys.argv[2], sys.argv[3])
  buf = ['filler']
  while buf != []:
    flag = bitstream.read(1)
    if flag == [47]: #unencoded
      buf = bitstream.read(consts['max'])
    else: # encoded
      break
    # slide the window
    del dic[:len(buf)]
    dic.extend(buf)
    bitstream.write(buf)

consts = {'min':16, # minimum match size; any less is not worth encoding
          'max':23, # maximum match size
          'dic':4096, # dictionary size
          'posbits':12, # number of bits to encode position
          'lenbits':3, # of bits to encode range
          'uncoded':47, # uncoded flag
          'coded':46,} # encoded flag
bitstream.start('dictionary', None)
dic = bitstream.read(consts['dic'])

if sys.argv[1] == '-c':
  compress(dic, consts)
elif sys.argv[1] == '-d':
  decompress(dic, consts)
else:
  print('Usage: {0} -(c/d) <infile> <outfile>'.format(sys.argv[0]))
