import zipfile
import pdfplumber
import pandas as pd
import os

def extrair_pdf_do_zip(zip_path, pdf_name, temp_pdf_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        with zip_ref.open(pdf_name) as pdf_file:
            with open(temp_pdf_path, 'wb') as f:
                f.write(pdf_file.read())

def extrair_tabelas_do_pdf(pdf_path):
    data = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_table()
            if tables:
                for row in tables:
                    if any(row):  
                        data.append(row)

    if not data:
        raise ValueError("Nenhuma tabela válida encontrada no PDF!")
    
    df = pd.DataFrame(data)
    header = df.iloc[0].tolist()  
    df = df[1:].reset_index(drop=True) 
    df.columns = header

    df.replace({'OD': 'Seg. Odontológica', 'AMB': 'Seg. Ambulatorial'}, inplace=True)
    
    return df

def salvar_csv_e_zip(df, csv_name, zip_name):
    df.to_csv(csv_name, sep=";", encoding="utf-8-sig", index=False, quotechar='"')

    with zipfile.ZipFile(zip_name, 'w') as zipf:
        zipf.write(csv_name, os.path.basename(csv_name))

    os.remove(csv_name)  

def main():
    ZIP_ORIGINAL = "Anexos_ANS.zip"
    PDF_NOME = "Anexo_I_Rol_2021RN_465.2021_RN627L.2024.pdf"
    TEMP_PDF = "temp_anexo.pdf"
    CSV_SAIDA = "Rol_de_Procedimentos.csv"
    ZIP_FINAL = "Teste_JoaoPedroNunesRamos.zip"
    
    try:
        print("Extraindo PDF do ZIP...")
        extrair_pdf_do_zip(ZIP_ORIGINAL, PDF_NOME, TEMP_PDF)
        
        print("Extraindo tabelas do PDF...")
        df = extrair_tabelas_do_pdf(TEMP_PDF)

        print("Salvando CSV e compactando...")
        salvar_csv_e_zip(df, CSV_SAIDA, ZIP_FINAL)

        os.remove(TEMP_PDF)  

        print(f"Processo concluído! {ZIP_FINAL}")

    except Exception as e:
        print(f" Erro: {str(e)}")

if __name__ == "__main__":
    main()
