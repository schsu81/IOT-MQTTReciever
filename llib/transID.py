
#%%=======================================================================
def dec2base36(number,alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'):
  ID = ''
  div = number
  while div != 0:
    div, s = divmod(div,36)
    ID = alphabet[s]+ID
  return ID
#-----------------------------------------------------------------------
def base362dec(alpha):
  return int(alpha,36)
#%%=======================================================================