import requests
from bs4 import BeautifulSoup
import zipfile
from urllib.parse import urljoin

def main():
    URL_BASE = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    NOME_ZIP = "Anexos_ANS.zip"
    
    print("Procurando anexos...")
    
    try:
        response = requests.get(URL_BASE, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links_anexos = []
        for link in soup.find_all('a', class_='internal-link'):
            href = link.get('href', '')
            if 'Anexo_I' in href or 'Anexo_II' in href:
                links_anexos.append(urljoin(URL_BASE, href))
        
        if not links_anexos:
            print("Nenhum anexo encontrado!")
            return
        
        with zipfile.ZipFile(NOME_ZIP, 'w') as zipf:
            for url in links_anexos:
                nome_arquivo = url.split('/')[-1] 
                print(f"Baixando {nome_arquivo}...")
                
                response_pdf = requests.get(url, stream=True, timeout=30)
                response_pdf.raise_for_status()
                
                zipf.writestr(nome_arquivo, response_pdf.content)
                print(f"{nome_arquivo} adicionado ao ZIP")
        
        print(f"\nConcluído! Arquivo ZIP gerado: '{NOME_ZIP}'")
    
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()