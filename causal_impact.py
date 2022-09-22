import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from causalimpact import CausalImpact

st.set_option('deprecation.showPyplotGlobalUse', False)

def input_to_df(input):
	df = pd.read_csv(uploaded_file)
	return df


def plot_raw_curves(df, kpi):
    plt.figure(figsize=(15, 8))
    df\
        .set_index(
            'Date', 
            inplace=True
        )
    df\
        .groupby('GROUP')[kpi]\
                            .plot(legend=True)
                        
    plt.axvline(
        pd.to_datetime(MEP_DATE), 
        color='r', 
        linestyle='--', 
        lw=2
    )
    plt.title(f"SEO {kpi.capitalize()} for pages of group Control (no change) vs Test (new feature applied)")
    
    
def plot_diff_curve(df, kpi):
    plt.figure(figsize=(15, 8))
    pivot_df = df\
        .reset_index()\
            .pivot_table(index="Date", columns="GROUP", values=kpi, aggfunc=np.sum)
    pivot_df["difference"] = pivot_df["TEST"] - pivot_df["CONTROL"]
    pivot_df = pivot_df.dropna()
    pivot_df['difference']\
        .plot(legend=True)
    plt.axvline(
        pd.to_datetime(MEP_DATE), 
        color='r', 
        linestyle='--', 
        lw=2
    )
    plt.title(f"Difference (Test - Control) of {kpi.capitalize()} between both Groups")
    return pivot_df


def compute_causal_impact(pivot_df):
    change_point = sum(pivot_df.index < pd.to_datetime(MEP_DATE)) - 1
    pre_period = [0, int(change_point)]
    post_period = [int(change_point) + 1, len(pivot_df.index) - 1]
    ci = CausalImpact(pivot_df[["difference"]].reset_index(drop=True), pre_period, post_period)
    ci.summary()
    ci.plot()
    #return ci
    #print(ci.summary(output='report'))

    
    
def perform_test_analysis(df, kpi='Clicks'):
    plot_raw_curves(df, kpi)
    pivot_df = plot_diff_curve(df, kpi)
    compute_causal_impact(pivot_df)



st.title("Causal impact tool")
form = st.form(key='my-form')
kpi = form.selectbox("KPI",("Clics","Impressions","CTR","Average Position"))
MEP_DATE = form.text_input("ex: 2022-02-09, please respect this format") 
Note = form.markdown("""**Requirements:** 
    * CSV file
    * Date DD/MM/YYYY 
    * KPI : Clics or Average Position or Impressions or CTR
    * GROUP : CONTROL & TEST
    """
uploaded_file = form.file_uploader("Upload your XLSX file")
submit = form.form_submit_button('Submit')
if submit:
    df = pd.read_csv(uploaded_file)
    df["Date"]= pd.to_datetime(df["Date"],format= "%d/%m/%Y")
    #df.rename(columns={"Date":"date"},inplace=True)
    curves = plot_raw_curves(df, kpi)
    st.pyplot(curves)
    pivot_df = plot_diff_curve(df, kpi)
    fig = compute_causal_impact(pivot_df)
    st.write(fig)
    st.pyplot(fig)
