from bs4 import BeautifulSoup

def getBlurb(text):
  soup = BeautifulSoup(text, 'html.parser')
  
  return''.join(str(tag) for tag in soup.find_all(['p', 'ul'])[:4])