#!/usr/bin/python3

# Python version, V.Zavjalov, 2023.01.29

##################################################

# Filter for skipping points.
# Arguments:
#   t,v  - data point: time, value
#   storage - Internal storge. Initially should be {}
#   col  - Data column to use for filtering.
#   maxn - Upper limit for buffer size (0 for no limit).
#   maxt - Upper limit for buffer time span (0 for no limit).
#   minn - Lower limit for buffer size (0 for no limit).
#   mint - Lower limit for buffer time span (0 for no limit).
#   noise - Noise level. Max difference between original and filtered data.
#   auto_noise - calibrate noise level automatically, using factor from the argument.
#                Default value 1, use 0 to switch off.
#                if both auto_noise and noise parameters are non-zero, maximum of
#                automatically found and manually set values is used.
#
# Filter function uses three global variables: time, data, storage.
# It can be installed as an input filters in graphene database
#   https://github.com/slazav/graphene
#
# V.Zavjalov, 2021.03.06

def flt_skip(t,v, storage, maxn=100, maxt=0, minn=0, mint=0, noise=0, auto_noise=1):

  if "buf"  not in storage: storage["buf"] = []
  if "sbuf" not in storage: storage["sbuf"] = []
  if "tv" not in storage: storage["tv"] = ()

  n = len(storage["buf"])

  ret = ()

  # If data is NaN or Inf
  # reset buffers and return 0.
  if v!=v:
    storage["buf"] = []
    storage["sbuf"] = []
    storage["tv"] = ()
    return 0

  # Noise level finder
  if auto_noise>0:

    # To calibrate noise we want to use noise_n points
    # at the beginning of the main buffer. If the buffer is shorter,
    # we use a separate sliding buffer of noise_n length.
    noise_n = 30

    # Add new point to the sliding buffer
    storage["sbuf"].append((t,v))
    ns = len(storage["sbuf"])

    # Remove old points
    if ns > noise_n:
      del storage["sbuf"][0:ns - noise_n]
      ns = len(storage["sbuf"])

    # In the beginning the sliding buffer can be shorter
    # then noise_n. We should use ns below.

    # Collect squares of deviations of points from
    # their two neighbours.
    dev = []
    # use main buffer if possible
    if n >= ns: b='buf'
    else: b = 'sbuf'
    for i in range(1,ns-1):
      vm = storage[b][i-1][1]
      vp = storage[b][i+1][1]
      v0 = storage[b][i][1]
      dev.append((v0 - (vp-vm)/2.0)**2)

    # Skip three lagrest
    # values to reduce effect of steps and pikes.
    # Do not skip values if buffer is small
    dev.sort()
    if ns == noise_n: del dev[-3:]

    # Calculate RMS deviation
    if len(dev):
      mean = sum(dev)
      rdev = (sum((x-mean)**2 for x in dev)/len(dev))**0.5

      # Compensate removed points. Theory?!
      rdev *= 1.2

      anoise = auto_noise*3*rdev
      if anoise>noise: noise = anoise


  # If we have previous point:
  if len(storage["tv"])==2:

    # If the buffer contains 3 or more points
    # and we can do 2-segment fit:
    if n>2:

      # extract v-v0, t-t0 lists
      dts=[]
      dvs=[]
      for tv in storage["buf"]:
        dts.append( tv[0] - storage["tv"][0] )
        dvs.append( tv[1] - storage["tv"][1] )

      # 2-segment fit: we want to find an internal point 0<j<n
      # with best RMS deviation from 2-segment line (t0,d0)-(tj,dj)-(tn,dn).
      # The only free parameter is index j.
      # The line formula:
      #    t<=tj: A*t,            A=$dj/$tj
      #    t>=tj: B*(t-tj) + dj,  B=($dn-dj)/($tn-$tj)
      # We will check all possible values of j and choose the best one.

      # best values:
      opt_j = 0
      opt_D = float("inf")
      opt_A = None
      opt_B = None

      # Last point
      tn = dts[n-1]
      vn = dvs[n-1]

      for j in range(1,n-1):
        tj = dts[j]
        vj = dvs[j]
        A = vj/tj
        B = (vn-vj)/(tn-tj)

        # RMS deviation from the fit:
        D = 0.0
        for k in range(n):
          if dts[k] <= tj:
            D += (A*dts[k] - dvs[k])**2
          else:
            D += (B*(dts[k]-tj) - (dvs[k]-vj))**2

        D = (D/(n-1))**0.5

        # If we have flat noisy data than simple 2-segment fit
        # will give almost random position of the central point.
        # Without a good reason we do not want to have it close
        # to the beginning (to avoid too short segments), or to the end
        # (to avoid random slope of the second segment and bad evaluation
        # of the stopping condition).
        # I will multiply D by function f(j) = 1 + 2j(j-n-1)/(n-1)^2
        # (quadratic function with f(0) = f(n-1) = 1, f((n-1)/2) = 1/2 )
        D *= 1 + 2.0*j*(j-n-1)/(n-1)**2

        if D <= opt_D: # "=" is important if you have many points with same values!
          opt_j = j
          opt_D = D
          opt_A = A
          opt_B = B

      j = opt_j
      tj = dts[j]
      vj = dvs[j]

      # Now we have a 2-segment fit with best RMS deviation.
      # We can reset buffer and send central point
      # to the output if some "stopping condition" is met.

      # There are a few stopping conditions
      # - too long buffer
      # - new point is too far from the fit
      # - max deviation in the fit is more then noise level

      # There is one more stopping condition: 4*$j < ($n-1-$j)
      # If first segment become very short it means there is
      # a feature there. No need to add more points and make
      # the second segment longer. This works after sharp steps or peaks.

      # Deviation of the new point (which is not in the buffer yet)
      tx = t - storage["tv"][0]
      vx = v - storage["tv"][1]
      Q1 = abs(vj + opt_B*(tx-tj) - vx)

      # Max absolute deviation of buffer points:
      Q2 = 0
      for k in range(n):
        if dts[k] <= tj:
          vv = abs(A*dts[k] - dvs[k])
        else:
          vv = abs(B*(dts[k]-tj) - (dvs[k]-vj))
        if Q2 < vv: Q2 = vv

      # Calculate stopping condition:
      stop = 0
      if (noise>0 and Q1 > 2*noise) or\
         (noise>0 and Q2 > noise) or\
         (4*j < (n-1-j)) or\
         (maxn>0 and n > maxn) or\
         (maxt>0 and tn > maxt): stop = 1

      # Clear stopping condition if buffer is too short (--minn, --mint parameters)
      if (minn>0 and n < minn) or\
         (mint>0 and tn < mint): stop = 0

      # let's send the point to output!
      if stop:
        ret = storage["buf"][j]
        # Crop beginning of the buffer, it should start with the sent point!
        del storage["buf"][0:j]

  else:
    # no previous point, 1st point ever
    ret = (t,v)

  # Add new point to the buffer
  storage["buf"].append((t,v))

  # Update data
  if len(ret):
    storage["tv"] = ret

  return ret

##################################################

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--maxn', type=int, default=100)
parser.add_argument('--minn', type=int, default=0)
parser.add_argument('--maxt', type=float, default=0)
parser.add_argument('--mint', type=float, default=0)
parser.add_argument('--noise', type=float, default=0)
parser.add_argument('--auto_noise', type=float, default=1)
args = parser.parse_args()
####

import sys
import re

####

storage = {}
while 1:
  line = sys.stdin.readline()
  if not line: break

  if re.match(r'^\s*$', line) or re.match(r'^#.*', line):
    print(line, end='')
    continue

  d = re.findall(r'\S+', line)
  if len(d) < 2: continue

  d = flt_skip(float(d[0]), float(d[1]), storage,
    maxn=args.maxn, maxt=args.maxt,
    minn=args.minn, mint=args.mint,
    noise=args.noise, auto_noise=args.auto_noise)

  if len(d)<2: continue
  print(d[0], " ", d[1])
