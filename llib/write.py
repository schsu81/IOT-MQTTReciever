import os
_header = ['type','id','timestamp','station_mac','voltage','louver_mac','pm2p5','pm10','co2',
          'humidity','hdc1080_temperature','dsp310_temperature','airPressure',
          'windSpeed','windDirection','latitude','longitude','altitude']
#%%=======================================================================
def writeFile(fn,parsed_data,DATA_DIR='.',format='csv'):
  print(f"  Writting {DATA_DIR}/{fn}")
  if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
  fn = os.path.join(DATA_DIR,fn)
  if format=='csv':
    _write2csv(fn,parsed_data)
  elif format=='json':
    _write2json(fn,parsed_data)
#%%=======================================================================
def _write2csv(fn,parsed_data):
  import csv
  outdata = [ parsed_data[vn] for vn in _header ] 

  ofn = f'{fn}.csv'
  if os.path.isfile(ofn):
    with open(ofn,'a') as out:
      writer = csv.writer(out)
      writer.writerow(outdata)
  else:
    with open(ofn,'w') as out:
      writer = csv.writer(out)
      writer.writerow(_header) # Write header
      writer.writerow(outdata)
#%%=======================================================================
def _write2json(fn,parsed_data,DATA_DIR='.'):
  import json

  timestamp = int(parsed_data['timestamp'])
  outdata = {timestamp:{}}
  for key in parsed_data:
    if key == 'timestamp':
      continue
    outdata[timestamp][key] = parsed_data[key]

  ofn = f'{fn}.json'
  if os.path.isfile(ofn):
    with open(ofn,'r') as out:
      outdata = json.load(out)
    outdata[timestamp] = outdata[timestamp]
  else:
    outdata = outdata
  with open(ofn,'w') as out:
    json.dump(outdata,out,indent=2)
#%%=======================================================================