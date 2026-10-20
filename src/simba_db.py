import pandas as pd

class Simba:
    def __init__(self, simba_csv_path):

        #cria o dataframe 
        df = pd.read_csv(simba_csv_path, 
                         sep=';', 
                         engine='python', 
                         on_bad_lines='skip', 
                         encoding = "ISO-8859-1")

        # Converter a coluna de datas para o formato datetime
        df['DATA_LANCAMENTO'] = pd.to_datetime(df['DATA_LANCAMENTO'], format='%d/%m/%Y')

        # Converter as colunas monetárias em formato float
        colunas_monetaria = ['VALOR_TRANSACAO', 'VALOR_SALDO']

        for col in colunas_monetaria:
            df[col] = df[col].str.replace(',','.')
            df[col] = pd.to_numeric(df[col], errors = 'coerce')
        
        # colunas como 'strings' exceto 'VALOR_TRANSACAO' e 'VALOR_SALDO'
        categorical_columns = [col for col in df.columns if col not in ['VALOR_TRANSACAO', 'VALOR_SALDO', 'DATA_LANCAMENTO']]
        for column in categorical_columns:
            df[column] = df[column].astype(str)
        
        self.simba_df = df

    def get_dataframe (self):
        df = self.simba_df
        return df

