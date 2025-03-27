import os
import requests
import zipfile
from datetime import datetime

def get_output_path():
    """
    Tomei a iniciativa de criar um caminho para o arquivo que funcione em diferentes sistemas operacionais,
      para evitar erros ao testar, pois não tenho conhecimento em qual sistema operacional ele sera testado
    """
    
    base_path = os.path.expanduser('~/Documentos/Downloads')
    
    # usar o diretório atual para o caminho
    if not os.path.exists(base_path):
        base_path = os.path.join(os.getcwd(), 'Downloads')
    
    
    os.makedirs(base_path, exist_ok=True)
    
    # Gerando data atual do download para melhor organização 
    data_atual = datetime.now().strftime('%Y-%m-%d')
    
    
    output_filename = f'ev_de_saude_{data_atual}.zip'
    output_path = os.path.join(base_path, output_filename)
    
    return output_path

def download_pdf(url, output_path):
   
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        #verificação de diretorio
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print(f"PDF baixado com sucesso: {output_path}")
        return output_path

    except requests.exceptions.RequestException as e:
        print(f"Erro ao baixar o PDF: {e}")
        return None

def download_and_compress_pdfs(pdf_urls, output_zip_path):
    
    # Criando diretório temporário 
    temp_dir = os.path.join(os.path.dirname(output_zip_path), 'temp_pdfs')
    os.makedirs(temp_dir, exist_ok=True)

    downloaded_pdfs = []

    try:
        for i, url in enumerate(pdf_urls, 1):
            pdf_path = download_pdf(url, os.path.join(temp_dir, f'documento_{i}.pdf'))
            if pdf_path:
                downloaded_pdfs.append(pdf_path)

        if not downloaded_pdfs:
            print("Nenhum PDF foi baixado.")
            return None

        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for pdf_path in downloaded_pdfs:
                zipf.write(pdf_path, os.path.basename(pdf_path))

        print(f"PDFs compactados com sucesso: {output_zip_path}")
        return output_zip_path

    finally:
        # Limpar arquivos temporários 
        for pdf_path in downloaded_pdfs:
            try:
                os.remove(pdf_path)
            except Exception as e:
                print(f"Erro ao remover arquivo temporário {pdf_path}: {e}")
        
        try:
            os.rmdir(temp_dir)
        except Exception as e:
            print(f"Erro ao remover diretório temporário: {e}")

def main():
    pdf_urls = [
        'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf',
        'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos/Anexo_II_DUT_2021_RN_465.2021_RN628.2025_RN629.2025.pdf'
    ]
    
    
    output_path = get_output_path()
    
    # baixar e compactar os pdfs
    download_and_compress_pdfs(pdf_urls, output_path)
    
    # imprimir o caminho completo para verificar onde o arquivo foi salvo
    print(f"Arquivo salvo em: {output_path}")

if __name__ == '__main__':
    main()