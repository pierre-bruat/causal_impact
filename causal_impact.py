import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from causalimpact import CausalImpact
import openpyxl


def input_to_df(input):
	df = pd.read_csv(uploaded_file)
	return df


def plot_raw_curves(df, kpi):
    plt.figure(figsize=(15, 8))
    df\
        .set_index(
            'date', 
            inplace=True
        )
    df\
        .groupby('groups')[kpi]\
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
            .pivot_table(index="date", columns="groups", values=kpi, aggfunc=np.sum)
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
    plt.title(f"Difference (Test - Control) of {kpi.capitalize()} between both groups")
    return pivot_df


def compute_causal_impact(pivot_df):
    change_point = sum(pivot_df.index < pd.to_datetime(MEP_DATE)) - 1
    pre_period = [0, int(change_point)]
    post_period = [int(change_point) + 1, len(pivot_df.index) - 1]

    ci = CausalImpact(pivot_df[["difference"]].reset_index(drop=True), pre_period, post_period)
    print(ci.summary())
    print(ci.summary(output='report'))
    ci.plot()
    
    
def perform_test_analysis(df, kpi='impressions'):
    plot_raw_curves(df, kpi)
    pivot_df = plot_diff_curve(df, kpi)
    compute_causal_impact(pivot_df)



st.title("Causal impact launcher")
with st.expander("settings"):
	form = st.form(key='my-form')
	#st.markdown("What file do I need to upload ? Step #1: Export your data from Google Search for your test group and control group. ***** Step #2 Concatenate both files by respecting the following format CSV (;) with following header Date | Clicks | Impressions | CTR | Position | groups (CONTROL or TEST) ")
#image = Image.open(')
	#kpi = form.selectbox("KPI",("Clicks","Impressions","CTR","Position"))
	#MEP_DATE = form.text_input("ex: 2022-02-09, please respect this format") 
	uploaded_file = form.file_uploader("Upload your XLSX file")
	submit = form.form_submit_button('Submit')
	if submit:
		if uploaded_file is not None:
			df = pd.read_excel(uploaded_file)
			st.write(df)
		#df = input_to_df(uploaded_file)
		#df["Date"]= pd.to_datetime(df["Date"],format= "%d/%m/%Y")
		#df.rename(columns={"Date":"date"},inplace=True)
		#st.write(df)
		#causal_impact = perform_test_analysis(df, kpi)
		#st.write(causal_impact)





