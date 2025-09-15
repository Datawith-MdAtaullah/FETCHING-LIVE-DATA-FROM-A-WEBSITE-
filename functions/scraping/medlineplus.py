import concurrent.futures 
import json 
from bs4 import BeautifulSoup 
from utils.storage_utils import save_json 
import requests
 
bucketname = 'enigmagenomics-internship.firebasestorage.app' 
 
def scrape_and_save(): 
    url_main = 'https://medlineplus.gov/genetics/gene' 
    ses = requests.Session() 
    ses.headers.update({"User-Agent": "Mozilla/5.0"}) 
 
    letters = list("abcdefghijklmnopqrstuvwxyz") 
    all_links = [] 
 
    for i in letters: 
        url = url_main + '/' if i == 'a' else url_main + '-' + i + '/' 
        page = ses.get(url) 
        soup = BeautifulSoup(page.text, 'html.parser') 
        A = soup.find('ul', class_='withident breaklist') 
        if A: 
            L = A.find_all('a') 
            all_links.extend(L) 
 
    def process_link(x): 
        gene_name = x.text.strip() 
        link = x['href'] 
        page2 = ses.get(link) 
        soup = BeautifulSoup(page2.text, 'html.parser') 
        cond = soup.find_all('div', class_='mp-content mp-exp exp-full') 
        _conditions = [] 
        for j in cond: 
            z = j.find("h3") 
            if z: 
                z_text = z.text.strip() 
                if z_text: 
                    _conditions.append(z_text) 
        each_gene_data = {"gene": gene_name, "conditions": _conditions} 
 
        filename = f'genes/all_genes_separate_files/{gene_name}.json' 
        d = json.dumps(each_gene_data, ensure_ascii=False, indent=2) 
        save_json(d, bucketname, filename) 
 
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as e: 
        e.map(process_link, all_links) 
 
    return len(all_links), "Genes loaded successfully."