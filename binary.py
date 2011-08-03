# little-endian list of bits up to length
def binarize(n, length):
  bits = []
  for i in range(0, length):
    bits.append(n % 2)
    n = n/2
  return bits

# converts little-endian bit list into correspoding int
def numberize(bits):
  n = 0
  for bit in reversed(bits):
    n = 2*n + bit
  return n
