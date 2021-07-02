import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from parser_catalogo import get_info_catalogo, filter_subjects


def parser_data(data_json):
    df = pd.DataFrame(eval(data_json))
    return df


def get_credits(df):
    df_credit = df.groupby(['ano', 'periodo', 'situacao'], as_index=False)[
        'creditos'].sum()
    df_credit['position'] = df_credit['ano'].astype(
        str)+'-'+df_credit['periodo'].astype(str).str.zfill(2)
    return df_credit


def calculator_cr(df):
    notes = {}


def plot_credits(df):
    sns.set_theme(style="darkgrid")

    fig = px.bar(
        df,
        x="position",
        y="creditos",
        color="situacao",
        category_orders={
            "situacao": ["Aprovado", "Apr.S.Nota", "Disc.Equiv", "Reprovado", "Repr.Freq'"]
        },
        color_discrete_map={
            'Apr.S.Nota': 'green',
            'Reprovado': 'red',
            'Disc.Equiv': 'green', 'Aprovado': 'green', 'Repr.Freq': 'red'},
        title="Test"
    )
    return fig


def discipline_reproved(df):
    df_reproveded = df[df['situacao'] == 'Reprovado']
    df_reproveded = df_reproveded.groupby(
        ['disciplina'], as_index=False).count()
    df_reproveded['reprovacoes'] = df_reproveded['periodo']
    return df_reproveded[['disciplina', 'reprovacoes']]


if __name__ == '__main__':
    st.title('Test')
    data = st.sidebar.text_input(
        'Insira seus dados no formato Json', [])

    df_catalogo, courses, courses_raw = get_info_catalogo(
        'data/catalogo_disciplinas_graduacao_2019_2020_categorias.xlsx')
    course_value = st.sidebar.selectbox(
        'Selecione o curso que deseja cursar',
        courses, index=2
    )
    st.sidebar.text(
        f'Curso {course_value} selecionado.'
    )
    print(courses_raw)
    print(course_value)
    print([x for x in courses_raw if x in course_value])
    df_subjects = filter_subjects(
        df_catalogo, [x for x in courses_raw if course_value in x])

    df_user = parser_data(data)

    if df_user.shape[0] > 0:
        df_credit = get_credits(df_user)
        df_position_sum = df_credit.groupby(['position'], as_index=False)[
            'creditos'].sum()
        df_position_sum.sort_values(by='position', inplace=True)
        st.dataframe(discipline_reproved(df_user))
        st.text(f'Máximo de créditos: {df_position_sum["creditos"].max()}')
        st.plotly_chart(plot_credits(df_credit), use_container_width=True)
        st.dataframe(
            df_subjects[~df_subjects['Sigla'].isin(df_user.loc[~df_user['situacao'].isin(['Repr.Freq', 'Reprovado'])]['codigo'])][['Disciplina', 'TPI']].reset_index(drop=True))
    else:
        st.text('Insira seus dados...')
        st.dataframe(df_subjects[['Disciplina']], width=1200)
