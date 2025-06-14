import pandas as pd
from db_manager import DatabaseManager
from datetime import datetime
import plotly.express as px

def carregar_dados(db: DatabaseManager) -> pd.DataFrame:
    """
    Carrega dados do banco e retorna um DataFrame.
    Faz tratamento de erros na leitura e conversão.
    """
    try:
        leituras = db.buscar_leituras()
        df = pd.DataFrame(leituras, columns=[
            'id', 'codMaquina', 'ordemProducao', 'dataHora', 'distancia', 'folhas'
        ])
        df['dataHora'] = pd.to_datetime(df['dataHora'], errors='coerce')

        # Remove linhas com datas inválidas
        df = df.dropna(subset=['dataHora'])

        return df
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return pd.DataFrame()


def folhas_por_ordem(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o total de folhas produzidas por ordem de produção.
    """
    resumo = df.groupby(['ordemProducao', 'codMaquina']).agg({
        'dataHora': ['min', 'max'],
        'folhas': 'max'
    }).reset_index()

    resumo.columns = ['ordemProducao', 'codMaquina', 'inicio', 'fim', 'folhas']
    return resumo.sort_values(by='inicio')


def produtividade_por_maquina(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula a produtividade (folhas por hora) por máquina e ordem de produção.
    Remove leituras com tempo inferior a 1 minuto.
    """

    # Calcular duração por OP
    resumo = df.groupby(['ordemProducao', 'codMaquina']).agg({
        'dataHora': ['min', 'max'],
        'folhas': 'max'
    }).reset_index()

    resumo.columns = ['ordemProducao', 'codMaquina', 'inicio', 'fim', 'folhas']
    resumo['tempo_operacao_horas'] = (resumo['fim'] - resumo['inicio']).dt.total_seconds() / 3600

    # Eliminar leituras com tempo muito baixo (evita divisão por zero)
    resumo = resumo[resumo['tempo_operacao_horas'] >= (1 / 60)]  # mínimo de 1 minuto

    resumo['folhas_por_hora'] = resumo['folhas'] / resumo['tempo_operacao_horas']
    return resumo[['codMaquina', 'ordemProducao', 'tempo_operacao_horas', 'folhas', 'folhas_por_hora']].sort_values(by='codMaquina')


def folhas_por_dia(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula o total de folhas por dia, por máquina e por ordem de produção.
    """
    df['data'] = df['dataHora'].dt.date

    folhas_dia = df.groupby(['data', 'codMaquina', 'ordemProducao'])['folhas'].max().reset_index()
    return folhas_dia.sort_values(by=['data', 'codMaquina', 'ordemProducao'])

import os

def exportar_para_csv(df: pd.DataFrame, nome_arquivo: str):
    """
    Exporta o DataFrame para um arquivo CSV no diretório 'output/'.
    """
    os.makedirs('output', exist_ok=True)
    caminho = os.path.join('output', nome_arquivo)
    try:
        df.to_csv(caminho, index=False, sep=';', encoding='utf-8')
        print(f"CSV exportado com sucesso: {caminho}")
    except Exception as e:
        print(f"Erro ao exportar CSV: {e}")


def exportar_para_json(df: pd.DataFrame, nome_arquivo: str):
    """
    Exporta o DataFrame para um arquivo JSON no diretório 'output/'.
    """
    os.makedirs('output', exist_ok=True)
    caminho = os.path.join('output', nome_arquivo)
    try:
        df.to_json(caminho, orient='records', indent=4, date_format='iso')
        print(f"JSON exportado com sucesso: {caminho}")
    except Exception as e:
        print(f"Erro ao exportar JSON: {e}")

def plot_folhas_por_ordem_plotly(df: pd.DataFrame):
    """
    Gráfico de barras interativo: total de folhas por ordem de produção
    """
    fig = px.bar(
        df,
        x='ordemProducao',
        y='total_folhas',
        color='codMaquina',
        title='Total de Folhas por Ordem de Produção',
        labels={'ordemProducao': 'Ordem de Produção', 'total_folhas': 'Total de Folhas'},
        text='total_folhas'
    )
    fig.update_layout(xaxis_tickangle=-45)
    fig.show()


def plot_produtividade_maquina_plotly(df: pd.DataFrame):
    """
    Gráfico de linha interativo: produtividade por máquina (folhas/hora)
    """
    fig = px.line(
        df,
        x='codMaquina',
        y='folhas_por_hora',
        title='Produtividade por Máquina (Folhas por Hora)',
        labels={'codMaquina': 'Máquina', 'folhas_por_hora': 'Folhas/Hora'},
        markers=True
    )
    fig.show()


def plot_folhas_por_dia_plotly(df: pd.DataFrame):
    """
    Gráfico de linha interativo: evolução de folhas por dia por máquina
    """
    df_grouped = df.groupby(['data', 'codMaquina'])['folhas'].sum().reset_index()

    fig = px.line(
        df_grouped,
        x='data',
        y='folhas',
        color='codMaquina',
        title='Folhas por Dia por Máquina',
        labels={'data': 'Data', 'folhas': 'Folhas', 'codMaquina': 'Máquina'},
        markers=True
    )
    fig.update_xaxes(dtick="D", tickformat="%d/%m")
    fig.show()

