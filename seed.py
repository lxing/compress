import random, struct, sys

outfile = open(sys.argv[1],'w')
for i in range(0, int(sys.argv[2])):
  outfile.write(struct.pack('b', random.randint(48,49)))
