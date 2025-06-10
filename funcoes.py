def calcular_tempo_injecao(qnt_pecas, cavidades, ciclo):
    tempo_injecao = ((qnt_pecas / cavidades) * ciclo)/3600
    
    return tempo_injecao.sum()

def calcular_material_necessario(qnt_pecas, cavidades, peso_galho):
    mat_necessario = ((qnt_pecas / cavidades) * peso_galho)/1000
        
    return mat_necessario.sum()

def calcular_tempo_limpeza(tempo_limp, quant_por_prod, quantidade_necessaria,quant_embalagem,func):
    
    tempo_limpeza = ((((tempo_limp* quant_por_prod )* quantidade_necessaria) *quant_embalagem)/func)/3600
    return tempo_limpeza.sum()

def calcular_montagem(montagem, quantidade_necessaria, quant_embalagem, func):
               
    montagem = (((montagem  * quantidade_necessaria) * quant_embalagem)/ func)/3600
    return montagem.sum()
def calcular_quant_por_prod(quant_embalagem, quant_por_prod, quantidade_necessaria):
            
    quant_pecas = (quant_embalagem *  quant_por_prod) * quantidade_necessaria
    return quant_pecas

def calcular_total_pecas(pecas, demanda_semanal, quant_embalagem):
    total_pecas = sum(pecas *  demanda_semanal / quant_embalagem)
    return total_pecas  

def calcular_total_por_produto(df_filtrada):
    df_filtrada = df_filtrada.copy()
    df_filtrada["Total de Peças"] = (
        df_filtrada["Qnt media semanal"] * df_filtrada["Qnt por produto"]
    ) * df_filtrada["Qnt por embalagem"]
    return df_filtrada