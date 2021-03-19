import pandas as pd
from streamlit.proto.DataFrame_pb2 import DataFrame


def get_info_catalogo(PATH):
    df_catalogo = pd.read_excel(PATH)
    cursos = (df_catalogo['Cursos/Categoria'].drop_duplicates().str.split(';',
                                                                          expand=True))
    df_cursos = pd.Series(name='cursos')
    for column in cursos:
        df_edit = cursos[column].dropna().rename('cursos')
        df_cursos = pd.concat([df_cursos, df_edit], ignore_index=True).dropna()
    df_cursos_raw = (df_cursos.str.lstrip()).drop_duplicates().sort_values()
    df_cursos = (df_cursos.str.replace(r" \(.*?\)", "", regex=True).str.lstrip()
                 ).drop_duplicates().sort_values()
    return df_catalogo, list(df_cursos.values), list(df_cursos_raw.values)


def filter_subjects(df_catalogo, subject_values):
    df = pd.DataFrame()
    for subject_value in subject_values:
        if 'OBR' in subject_value:
            print(subject_value)
            df_edit = df_catalogo.loc[[((subject_value in x))
                                       for x in df_catalogo['Cursos/Categoria']]].reset_index(drop=True)
            df = df.append(df_edit)
    # print(df)
    # todo = todo[~todo['Sigla'].isin(df_personal['codigo'])]
    return df
