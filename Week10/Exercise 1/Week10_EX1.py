import requests
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
import os

class NotFoundException(Exception):
    
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Util():
    """A utility class that has a bunch of methods for downloading and looking through files"""

    def __init__(self, url_list=[]):
        """Initialize utility with a list of URLs"""
        self.url_list = url_list
        self.filenames = []
        self.current = 0

    def __repr__(self):
        return 'Util(%r)' % (self.url_list)
    
    def __str__(self):
        return 'Utility with given list of URLs:\n' + str(self.url_list)
    
    def download(self, url, filename):
        """Downloads file from given URL.\nReturns filepath.\nRaises NotFoundException when url returns 404. 
        Default save file path is: ./download_dumps/{filename}"""
        filepath = "./download_dumps/" + str(filename)
        r = requests.get(url)
        if r.status_code == 404:
            raise NotFoundException("No file found at given URL")
        with open(filepath, "wb", encoding=r.encoding) as f:
            f.write(r.content)

    def download_large_file(self, url, filename):
        """Downloads file from given URL - suited for large files.\nReturns filepath.\nRaises NotFoundException when url returns 404. 
        Default save file path is: ./download_dumps/{filename}"""
        filepath = "./download_dumps/" + str(filename)
        r = requests.get(url)
        if r.status_code == 404:
            raise NotFoundException("No file found at given URL")
        with open(filepath, 'wb') as fd:
            for chunk in r.iter_content(chunk_size=1024):
                fd.write(chunk)    

    def multi_download(self, url_list=[]):
        """Downloads a list of files to ./download_dumps.\nThe initial list of URLs will be used if no list is given to this method. 
        Uses threads to download multiple URLs as text and stores filenames as a property"""
        dl_list = url_list
        if len(url_list) == 0:
            dl_list = self.url_list
        if len(dl_list) == 0:
            return "Please provide a list of URLs"

        def save_file(url):
            r = requests.get(url)
            parsed_python_url = urlparse(url)
            filename = os.path.basename(parsed_python_url.path)
            filepath = "./download_dumps/" + filename
            with open(filepath, "w", encoding=r.encoding) as f:
                f.write(r.text)
            return filename
        if len(dl_list) == 1:
            self.filenames.append(save_file(dl_list[0]))
        else:
            with ThreadPoolExecutor(len(dl_list)) as ex:
                res = ex.map(save_file, dl_list)
                self.filenames.extend(list(res))
        return "Files saved"           
            
    def __iter__(self): 
        """Returns an iterator"""
        self.current = 0
        return self

    def __next__(self):
        """Returns each of the downloaded files"""     
        if self.current >= len(self.filenames):
            raise StopIteration()
        self.current += 1
        return "./download_dumps/" + self.filenames[self.current]

    def filelist_generator(self, url_list):
        """Returns a generator to loop through the filenames"""
        for url in url_list:
            parsed_python_url = urlparse(url)
            filename = os.path.basename(parsed_python_url.path)
            yield filename

    def urllist_generator(self):
        """Returns a generator to loop through the internal list of URLs"""
        for url in self.url_list:
            yield url

    def avg_vowels(self, text):
        """Gives a rough estimate on readability.\nReturns average number of vowels in the words of the text"""
        #Providing no seperator will remove all whitespace including newlines and tabs
        words = text.split()
        vowels = 0
        for word in words:
            for i in word:
                if(i=='a' or i=='e' or i=='i' or i=='o' or i=='u' or i=='A' or i=='E' or i=='I' or i=='O' or i=='U'):
                    vowels += 1
        avg = vowels / len(words)
        return avg

    def hardest_read(self):
        """Returns the filename of the text with the highest vowel score. Uses multiprocessing."""
        score_dict = {}
        for f in self.filenames:
            with open("./download_dumps/" + f, "r") as current_file:
                score_dict[f] = self.avg_vowels(current_file.read())
        res = {k: v for k, v in sorted(score_dict.items(), key=lambda item: item[1], reverse=True)}
        return "./download_dumps/" + list(res.keys())[0]
        #return {list(res.keys())[0] : list(res.values())[0]}
    

# Create a module containing a class with the following methods:

# init(self, url_list)
# download(url,filename) raises NotFoundException when url returns 404
# multi_download(url_list) uses threads to download multiple urls as text and stores filenames as a property
# iter() returns an iterator
# next() returns the next filename (and stops when there are no more)
# urllist_generator() returns a generator to loop through the urls
# avg_vowels(text) - a rough estimate on readability returns average number of vowels in the words of the text
# hardest_read() returns the filename of the text with the highest vowel score (use all the cpu cores on the computer for this work.
