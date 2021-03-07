import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def parser_data(data_json):
    df = pd.DataFrame(eval(data_json))
    return df


def get_credits(df):
    df_credit = df.groupby(['ano', 'periodo', 'situacao'], as_index=False)[
        'creditos'].sum()
    df_credit['position'] = df_credit['ano'].astype(
        str)+'.'+df_credit['periodo'].astype(str)
    return df_credit


def plot_credits(df):
    sns.set_theme(style="darkgrid")
    # fig, ax = plt.subplots(figsize=(20, 10))
    fig = sns.lineplot(x="position", y="creditos",
                       hue="situacao",
                       data=df)
    return fig.get_figure()


if __name__ == '__main__':
    st.title('Test')
    data = st.sidebar.text_input(
        'Insira seus dados no formato Json', [])
    df = parser_data(data)

    if df.shape[0] > 0:
        df_credit = get_credits(df)
        df_position_sum = df_credit.groupby(['position'], as_index=False)[
            'creditos'].sum()
        st.text(f'Máximo de créditos: {df_position_sum["creditos"].max()}')
        st.dataframe(df)
        st.dataframe(df_credit)
        st.pyplot(plot_credits(df_credit))
    else:
        st.text('Insira seus dados...')
