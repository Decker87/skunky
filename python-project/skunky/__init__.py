from time import sleep
from skunky import search
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

def main():
  print("Hello, world!")
  print(search.main())

def service_main():
  for i in range(10):
    open('/Users/adam/temp.txt', 'a').write("bla\n")
    sleep(1.0)
