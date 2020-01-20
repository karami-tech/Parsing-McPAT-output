import sys, os, sim, re, math
import random

def parse_power(self, fname):
# print "--------------------------------------------------------------In parse_power Function-----------------------------------------------------"
power_txt = file(fname)
self.power_dat = {}
components = power_txt.read().split('*'*89)[2:-1]#its a list: split() function returns a list of strings in ""
for component in components:
  lines = component.strip().split('\n')
  componentname = lines[0].strip().strip(':')
  values = {}
  prefix = []; spaces = []
  for line in lines[1:]:
    if not line.strip():
      continue
    elif '=' in line:
      res = re.match(' *([^=]+)= *([-+0-9.e]+)(nan)?', line)
      if res:
        name = ('/'.join(prefix + [res.group(1)])).strip()
        if res.groups()[-1] == 'nan':
          # Result is -nan. Happens for instance with 'Subthreshold Leakage with power gating'
          # on components with 0 area, such as the Instruction Scheduler for in-order cores
          value = 0.
        else:
          try:
            value = float(res.group(2))
          except:
            print >> sys.stderr, 'Invalid float:', line, res.groups()
            raise
        values[name] = value
    else:
      res = re.match('^( *)([^:(]*)', line)
      if res:
        j = len(res.group(1))
        while(spaces and j <= spaces[-1]):
          spaces = spaces[:-1]
          prefix = prefix[:-1]
        spaces.append(j)
        name = res.group(2).strip()
        prefix.append(name)
  if componentname in ('Core', 'L2', 'L3'):
    if componentname == 'L0' :        # WARNING: nuca_at_level omitted
      outputname = 'NUCA'
    else:
      outputname = componentname
    if outputname not in self.power_dat:
      self.power_dat[outputname] = []
    self.power_dat[outputname].append(values)
  else:
    assert componentname not in self.power_dat
    self.power_dat[componentname] = values
print "---------------------------------------------------Parsing The Power Output Of The McPAT Is Done----------------------------------------"
if not self.power_dat:
  raise ValueError('No valid McPAT output found')
return self.power_dat




