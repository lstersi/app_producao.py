
import streamlit as st
import pandas as pd
from funcoes import *

tab1, tab2 = st.tabs(['Previsão', 'Planejamento'])

# Carregar planilha com múltiplas abas
arquivo = "estrutura_producao.xlsx"
df_produtos = pd.read_excel(arquivo, sheet_name="Produtos")
df_pecas = pd.read_excel(arquivo, sheet_name="Pecas")
df_infos = pd.read_excel(arquivo, sheet_name="Infos")


with tab1:
    st.title("Média de Embalagens Por Produto")

    # Selecionar produto
    produto_selecionado = st.selectbox("Selecione o produto:", df_produtos["Produto"].unique())
    quantidade_necessaria = st.number_input("Digite a quantidade de Embalagens")
  
    # Filtrar dados
    pecas_produto = df_pecas[df_pecas["Produto"] == produto_selecionado][["Molde", "Qnt por produto", "Pais", "Tempo Limpeza (seg)"] ]
    df_coluns = df_produtos[df_produtos["Produto"] == produto_selecionado]
    if pecas_produto.empty or df_coluns.empty:
        st.write("Produto não encontrado")
    else:
    #variavel
        quant_por_prod = pecas_produto["Qnt por produto"]
        quant_embalagem = df_coluns["Qnt por embalagem"].values[0]
        func = df_coluns["Qnt Funcionario"].values[0]
        tempo_limp = pecas_produto["Tempo Limpeza (seg)"]
        tempo_mont = df_coluns["Tempo Montagem (seg)"].values[0]
        pais = pecas_produto["Pais"]
      
    # Calcular tempos
        pecas_produto["Quantidade Total"] = calcular_quant_por_prod(quant_embalagem, quant_por_prod, quantidade_necessaria)
  
        montagem = calcular_montagem(tempo_mont, quantidade_necessaria, quant_embalagem, func)
        limpeza = calcular_tempo_limpeza(tempo_limp, quant_por_prod, quantidade_necessaria,quant_embalagem,func)


        tempo_total =  (limpeza + montagem).sum()

    #Considerar transporte de 4 semanas (fixo)
        pecas_produto["Dias Transporte"] = pais.apply(lambda x: 4 if x == "PY" else 1)
    
    #Previsão estoque baseado no tempo de transporte e tempo de quantidade necessaria
        pecas_produto["Qnt por País"] = pecas_produto["Quantidade Total"] * pecas_produto["Dias Transporte"]
      
    #Exibir resultados
        st.subheader("Resumo do Tempo de Produção")
        st.write(f"🧼 Tempo total de limpeza:{limpeza:.2f} Horas")
        st.write(f"🔧 Tempo de montagem: {montagem:.2f} Horas")
        st.write(f"⏱️ Tempo total estimado: {tempo_total:.2f} Horas")

    #Mostrar peças
        st.subheader("Quantidade de Peças")
        st.dataframe(pecas_produto[["Molde", "Quantidade Total"]])
        st.subheader("Estoque Mínimo por Peça ")
        st.dataframe(pecas_produto[["Molde", "Qnt por País", "Pais"]])

with tab2:
    #selecionar molde
    molde = st.text_input("Digite o Molde", key= "input_molde").strip().upper()
    qnt_pecas = st.number_input("Digite a quantidade de peças necessárias")
    
    #filtros
    df_coluns = df_pecas[df_pecas["Molde"] == molde][["Produto", "Peso Galho(g)", "Cavidades(n)", "Tempo Injeção (seg)"]]
    infos = df_infos[df_infos["Molde"] == molde]["Infos"]
        

    if df_coluns.empty or infos.empty:
        st.write("Produto não encontrado")
    else:
    
        cavidades = df_coluns["Cavidades(n)"]
        ciclo = df_coluns["Tempo Injeção (seg)"]
        peso_galho = df_coluns["Peso Galho(g)"]
              
        
   
#calculos
    if not df_coluns.empty:       
        if qnt_pecas > 0:
            tempo_injecao = calcular_tempo_injecao(qnt_pecas, cavidades, ciclo)
            mat_necessario = calcular_material_necessario(qnt_pecas, cavidades, peso_galho)
            
            st.subheader(" Dados previsto para Produção")
            st.write(f"⚖ Mistura de material: {mat_necessario:.2f} Kg")
            st.write(f"⏱️ Tempo de injeção: {tempo_injecao:.2f} Horas ou {tempo_injecao/4:.2f} Turnos")
            st.subheader(f"Informações do molde")
            st.write(f" {infos.values[0]}")
        else:
            st.write("Quantidade de peças necessárias deve ser maior que 0")
        #mostrar dados    
    else:
        st.write("Molde não encontrado, digite outra vez")
    df = pd.merge(df_produtos,df_pecas, on = "Produto")

       
    
    if molde:
        df_filtrada = df[df["Molde"].str.upper() == molde]
        if df_filtrada.empty:
            st.error("nenhum  dado encontrado para esse molde")
        else:
            df_resultado = calcular_total_por_produto(df_filtrada)    
            
            soma_total = df_resultado["Total de Peças"].sum()

            st.subheader("Detalhamento por Produto")
            st.dataframe(df_resultado[[
                "Produto",
                "Qnt media semanal",
                "Qnt por produto",
                "Qnt por embalagem",
                "Total de Peças"
            ]])
            
        st.subheader("🔩 Total geral de peças")
        st.write(f"Para o molde **{molde}** a quantidade de peças prevista por semana: **{round(soma_total)}**")
    else:
        st.info("Digite o nome do molde para visualizar os dados")