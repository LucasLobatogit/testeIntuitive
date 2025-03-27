import os
import tabula
import pandas as pd
import zipfile


def extract_pdf_from_path(input_path):
 
    input_path = os.path.normpath(input_path)
    
    print(f"Caminho de entrada: {input_path}")
    print(f"Caminho existe: {os.path.exists(input_path)}")
    
    if input_path.lower().endswith('.zip'):
        try:
            with zipfile.ZipFile(input_path, 'r') as zip_ref:
                print("Arquivos no ZIP:")
                for nome in zip_ref.namelist():
                    print(f" - {nome}")
                
                pdfs = [
                    f for f in zip_ref.namelist() 
                    if f.lower().endswith('.pdf')
                ]
                
                if pdfs:
                    # extrair o primeiro pdf
                    pdf_nome = pdfs[0]
                    pdf_path = zip_ref.extract(pdf_nome)
                    print(f"PDF extraído: {pdf_path}")
                    return pdf_path
                else:
                    print("Nenhum PDF encontrado no ZIP.")
                    return None
        
        except Exception as e:
            print(f"Erro detalhado ao processar ZIP: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    elif os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for file in files:
                if file.lower().endswith('.pdf'):
                    return os.path.join(root, file)
    
    elif input_path.lower().endswith('.pdf'):
        return input_path
    
    print("Nenhum PDF encontrado.")
    return None

def extract_pdf_data(pdf_path):

    try:
       
        if not os.path.exists(pdf_path):
            print(f"Erro: O arquivo {pdf_path} não existe.")
            return None
        
        tables = tabula.read_pdf(pdf_path, pages='all', multiple_tables=True)
        
        # Concatena todas as tabelas em um unico
        df = pd.concat(tables, ignore_index=True)
        
        return df
    except Exception as e:
        print(f"Erro ao extrair tabelas: {e}")
        import traceback
        traceback.print_exc()
        return None

def clean_and_process_dataframe(df):
    # substituindo abreviações
    column_replacements = {
        'OD': 'Seg. Odontológica', 
        'AMB': 'Seg. Ambulatorial'
    }
    
    # Renomeia as colunas usando o dicionário de substituição
    df.rename(columns=column_replacements, inplace=True)
    
    
    return df

def save_to_csv_and_zip(df, output_filename='Teste_Lucas_Lobato.zip'):

    # nome temporário
    csv_filename = 'procedimentos_saude.csv'
    

    df.to_csv(csv_filename, index=False, encoding='utf-8')
    

    with zipfile.ZipFile(output_filename, 'w') as zipf:
        zipf.write(csv_filename)
    
    os.remove(csv_filename)
    
    print(f"Dados salvos em {output_filename}")

def main(input_path):
    
    pdf_path = extract_pdf_from_path(input_path)
    
    if pdf_path is not None:
        try:
            # extrair as tabelas
            df = extract_pdf_data(pdf_path)
            
            if df is not None:
                # processar o dataframe
                processed_df = clean_and_process_dataframe(df)
                
                # salvar em csv e compactar
                save_to_csv_and_zip(processed_df)
            else:
                print("Falha ao extrair dados do PDF")
        
        finally:
            
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
                print(f"Arquivo PDF temporário {pdf_path} removido.")
    else:
        print("Não foi possível encontrar o PDF")

zip_path = r'C:\Users\lucas\OneDrive\Documentos\TesteIntuitive\Downloads\ev_de_saude_2025-03-25.zip'

main(zip_path)