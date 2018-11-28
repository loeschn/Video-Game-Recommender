import os

def load_key(filename='igdb_key',
              location = os.environ['HOME']+'/.secrets'):
      pathname = os.path.join(location, filename)
      with open(pathname) as f:
        key = f.read().strip()
      return key
