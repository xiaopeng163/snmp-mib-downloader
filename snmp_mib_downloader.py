
import re
from urllib.parse import urljoin
from pathlib import Path

from bs4 import BeautifulSoup
import requests
import click
from rich import print



BASE_URL = "https://www.circitor.fr/Mibs/"
__version__ = 0.1


def http_get(path):
    """http get request"""
    url = urljoin(BASE_URL, path)
    return requests.get(url).text


def download_mib_from_circitor(name, download_path):
    name = name.upper()
    # check mib file exist or not
    if not Path(download_path / f'{name}.txt').is_file():
        # read file and check import
        url = f"http://www.circitor.fr/Mibs/Mib/{name[0]}/{name}.mib"
        with open(download_path / f"{name}.txt", 'w') as f:
            content = http_get(url)
            f.write(content)
            print(f"[bold magenta]{name}[/bold magenta] downloaded")
    with open(download_path / f"{name}.txt") as f:
        imported_mib = re.findall("\s+FROM ([a-zA-Z0-9-]*).*\n", f.read())
    
    for mib in imported_mib:
        download_mib_from_circitor(mib, download_path)
            



@click.group()
@click.version_option(prog_name='MIB Downloader', version=__version__)
def cli():
    """Command line tool for MIB file downloading"""
    pass


@cli.command()
@click.option("--name", required=True, help="MIB name")
def search(name):
    """search MIB file by name or oid"""
    path = "Mibs.php"
    name = name.upper()
    soup = BeautifulSoup(http_get(path), 'html.parser')
    results = soup.find_all("a", href=re.compile(rf'Html.*{name}.*'))
    for mib in results:
        print(mib.text.replace(name, f"[bold magenta]{name}[/bold magenta]"))

@cli.command()
@click.option("--name", required=True, help="the MIB file name")
def download(name):
    download_path = Path('./download')
    download_path.mkdir(parents=True, exist_ok=True)

    download_mib_from_circitor(name, download_path)

if __name__ == "__main__":
    try:
        cli()
    except Exception as err:
         print(err)
         print("There was an error. Retrying again!")
