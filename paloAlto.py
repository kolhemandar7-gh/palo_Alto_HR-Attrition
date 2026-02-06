import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="HR Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    return pd.read_csv("Palo Alto Networks.csv")

df = load_data()

# Convert Attrition to readable format
df["AttritionLabel"] = df["Attrition"].map({1: "Yes", 0: "No"})

# -------------------- HEADER WITH LOGO --------------------
col_logo, col_title = st.columns([1, 5])

with col_logo:
    st.image(
        "Palo-Alto-Networks-Logo-Pngsource-7CUZVIZ3 (2).png",
        width=150
    )

with col_title:
    st.title("Workforce Attrition Patterns & Risk Analysis")
    st.markdown(
        "**Analyzing employee attrition trends to identify risk factors and retention opportunities**"
    )
# ---------------- SIDEBAR ----------------
st.sidebar.header("Filters")

gender = st.sidebar.multiselect(
    "Gender",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

df = df[df["Gender"].isin(gender)]

# ---------------- TITLE ----------------
st.markdown(
    "<h1 style='text-align:center;'>HR Analytics Dashboard for Attrition</h1>",
    unsafe_allow_html=True
)

# ---------------- KPI CALCULATIONS ----------------
total_employees = len(df)
attrition_count = df[df["Attrition"] == 1].shape[0]
attrition_rate = (attrition_count / total_employees) * 100 if total_employees > 0 else 0

male_count = df[df["Gender"] == "Male"].shape[0]
female_count = df[df["Gender"] == "Female"].shape[0]

# ---------------- KPI SECTION ----------------
st.markdown("### 📌 Key Workforce Metrics")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

kpi1.metric(
    label="👥 Total Employees",
    value=total_employees
)

kpi2.metric(
    label="🚪 Attrition Count",
    value=attrition_count
)

kpi3.metric(
    label="📉 Attrition Rate",
    value=f"{attrition_rate:.2f}%"
)

kpi4.metric(
    label="👨 Male Employees",
    value=male_count
)

kpi5.metric(
    label="👩 Female Employees",
    value=female_count
)

# ===================== ROW 1 =====================
col1, col2 = st.columns(2)

# Attrition by Job Role
with col1:
    st.subheader("📌Attrition by Job Role")
    job_attr = (
        df[df["Attrition"] == 1]
        .groupby("JobRole")
        .size()
        .sort_values(ascending=False)
    )
    fig = px.bar(
        job_attr,
        labels={"value": "Employees", "index": "Job Role"}
    )
    st.plotly_chart(fig, use_container_width=True)

# Attrition by Department
with col2:
    st.subheader("📌Attrition by Department")
    dept_attr = (
        df[df["Attrition"] == 1]
        .groupby("Department")
        .size()
        .sort_values()
    )
    fig = px.bar(
        dept_attr,
        orientation="h",
        labels={"value": "Employees", "index": "Department"}
    )
    st.plotly_chart(fig, use_container_width=True)
#================ Row 2=======================

col3, col4 = st.columns(2)
# Attrition by Age Group (Donut)
with col3:
    st.subheader("📌Attrition by Age Group")
    df["AgeGroup"] = pd.cut(
        df["Age"],
        bins=[18, 25, 35, 45, 60],
        labels=["18-25", "26-35", "36-45", "46+"]
    )
    age_attr = df[df["Attrition"] == 1]["AgeGroup"].value_counts()
    fig = px.pie(
        values=age_attr.values,
        names=age_attr.index,
        hole=0.5
    )
    st.plotly_chart(fig, use_container_width=True)

# Attrition by OverTime
with col4:
    st.subheader("📌Attrition by OverTime")
    overtime_attr = (
        df.groupby("OverTime")["Attrition"]
        .sum()
    )
    fig = px.pie(
        values=overtime_attr.values,
        names=overtime_attr.index
    )
    st.plotly_chart(fig, use_container_width=True)
# ===================== ROW 2 =====================
col5, col6 = st.columns(2)

# Attrition by Years at Company
with col5:
    st.subheader("📌Attrition by Years at Company")
    years_attr = (
        df[df["Attrition"] == 1]
        .groupby("YearsAtCompany")
        .size()
    )
    fig = px.line(
        x=years_attr.index,
        y=years_attr.values,
        markers=True,
        labels={"x": "Years at Company", "y": "Attrition Count"}
    )
    st.plotly_chart(fig, use_container_width=True)

# Attrition by Business Travel
with col6:
    st.subheader("📌Attrition by Business Travel")
    travel_attr = (
        df[df["Attrition"] == 1]
        .groupby("BusinessTravel")
        .size()
    )
    fig = px.bar(
        travel_attr,
        labels={"value": "Employees", "index": "Business Travel"}
    )
    st.plotly_chart(fig, use_container_width=True)
