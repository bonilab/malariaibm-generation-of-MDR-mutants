import os

for setnum in range(1,13):
  for sp_dir in ['']:
    for stgy in ['ac', 'c', 'm']:
      for ftype in ['monthly', 'mutpair', 'summary']:
        if sp_dir != '': sp_dir += '/'
        fdir = f'simulation_outputs/{sp_dir}set{setnum}_{stgy}/{ftype}/'
        files = os.listdir(fdir)
        for f in files:
          if f == '.DS_Store': continue
          numonly = ''.join(filter(str.isdigit, f.split('_')[1])) + '.txt'
          os.rename(fdir+f, fdir+numonly)