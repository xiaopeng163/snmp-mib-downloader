
import re
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import requests
from rich import inspect



BASE_URL = "https://www.circitor.fr/Mibs/"


class MIBRoot:

    def __init__(self):
        pass

    def _http_get(self, path):
        """http get request"""
        url = urljoin(BASE_URL, path)
        return requests.get(url).text
    
    def search_by_name(self, name):
        """search mib file by name"""
        path = "Mibs.php"
        soup = BeautifulSoup(self._http_get(path), 'html.parser')
        results = soup.find_all("a", href=re.compile(rf'Html.*{name}.*'))
        print(results)
        inspect(results[0])


if __name__ == "__main__":
    mib_root = MIBRoot()
    mib_root.search_by_name("CISCO-RTTMON-MIB")