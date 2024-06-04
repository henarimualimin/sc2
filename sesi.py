import os
ab = os.listdir('session/')
for phone in ab:
 phone = phone.replace('.session','')
 try:
  fa = open('akun.txt', 'a')
  fa.write(phone+'\n')
  fa.close()
 except:pass
 