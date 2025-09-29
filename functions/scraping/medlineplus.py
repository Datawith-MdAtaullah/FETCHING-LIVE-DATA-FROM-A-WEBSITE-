from concurrent.futures import ThreadPoolExecutor 
import json 
from bs4 import BeautifulSoup 
from utils.storage_utils import save_json 
import requests
 
bucketname = 'enigmagenomics-internship.firebasestorage.app' 
 
def crawling_function(): 
    ses = requests.Session()
    ses.headers.update({"User-Agent": "Mozilla/5.0"})

    url_main = 'https://medlineplus.gov/genetics/gene'
    letters = list("abcdefghijklmnopqrstuvwxyz")

    all_links = []
    for i in letters:
        url = url_main + '/' if i == 'a' else url_main + '-' + i + '/'
        page = ses.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        A = soup.find('ul', class_='withident breaklist')
        if A:
            L = A.find_all('li')
            all_links.extend(L)

    def process_gene(i):
        name = i.text.strip()
        links = i.find('a')
        link = links['href']
        page2 = ses.get(link)
        soup1 = BeautifulSoup(page2.text, 'html.parser')
        
        divs = soup1.find_all('div' , class_ = 'mp-exp exp-full')

        function_div = None
        for z in divs:
            if z.get('data-bookmark') == 'function':
                function_div = z
                break
        function = ""
        if function_div:
            content = function_div.find('div', class_="mp-content")
            if content:
                function = content.text.strip()
    
  
        cond_div = None
        for y in divs:
            if y.get("data-bookmark") == "conditions":
                cond_div = y
                break
        conditions = []
        if cond_div:
            cond_blocks = cond_div.find_all("div", class_="mp-content")
            for k in cond_blocks:
                
                name_cond = k.find('h3')
                name_ = name_cond.text.strip() if name_cond else ""
        
                det = k.find_all('p')
                details = " ".join([j.text.strip() for j in det]) if det else ""
            
                lin = k.find('a')
                url = lin['href'] if lin else None
        
                conditions.append({
                    "name": name_,
                    "url": url,
                    "details": details
                })
                
                    
        syn_div = None
        for m in divs:
            if m.get("data-bookmark") == "synonyms":
                syn_div = m
                break
        synonyms = []
        if syn_div:
            ul = syn_div.find("ul", class_="bulletlist")
            if ul:
                other_n = ul.find_all("li")
                synonyms = [x.text.strip() for x in other_n]
                
                
        divs = soup1.find_all('div' , class_ = 'mp-exp exp-full')
        resources_div = None
        for n in divs:
                if n.get('data-bookmark') == 'resources':
                    resources_div = n
                    break
        resources = []           
        if resources_div:
            res =  resources_div.find_all('div', class_="mp-content")

            for q in res:
                name_resource = q.find('h2')
                name_res =  name_resource.text.strip() if name_resource else "No Title"

                a_all_tag = q.find_all('a', href=True)

                for a in a_all_tag:
                    resources.append({
                        "name": name_res,
                        "url": a['href'],
                        "details": a.text.strip()
                    })

        
        references_div = None
        for ln in divs:
            if ln.get("data-bookmark") == 'references':
                references_div = ln
                break
        references = []
        if references_div:
            li_items = references_div.find_all('li')
            
            for li in li_items:
                a_tags = li.find_all("a", href=True)
                
                citations = []
                urls = []
                for a in a_tags:
                    citations.append(a.text.strip())
                    urls.append(a['href'])
                    
                for p in a_tags:
                    p.extract()
                name_text = li.text.strip().replace('\n','')
            
                references.append({
                    "name": name_text,
                    "citation": " or ".join(citations),
                    "url": " or ".join(urls)
                })
                
        data_gene = {
            "gene_name": name,
            "details": {
                "function": function,
                "conditions": conditions,
                "synonyms": synonyms,
                "resources": resources,
                "references": references
            }
        }

        filename_ = name.split(':')[0].strip() 
        filename = f'genes/new_infos_added_to_gene/{filename_}.json' 
        d = json.dumps(data_gene, ensure_ascii=False, indent=2) 
        save_json(d, bucketname, filename) 

    with ThreadPoolExecutor(max_workers=15) as executor:
         executor.map(process_gene, all_links)

    return len(all_links), "Genes info added successfully."
