import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid", palette="muted")


st.set_page_config(page_title="Play Store App Review Analysis", layout="wide")

st.sidebar.title("Navigation")
PAGES = [
    "Welcome",
    "Univariate Analysis",
    "Bivariate Analysis",
    "Multivariate Analysis",
    "Conclusion"
]
page = st.sidebar.radio("Select Page:", PAGES)


if page == "Welcome":
    st.title("🚀 Play Store App Review Analysis")
    st.markdown(
        """
### About the project...
This project focuses on analyzing a dataset of over 10,000 mobile applications from the Google Play Store to understand the key factors that drive app success. The analysis includes extensive data cleaning, handling missing values, converting textual data (e.g., "1,000+", "3.4M") into meaningful numeric formats, exploratory data analysis (EDA), and building a predictive model to estimate app installs.

The goal of the project is to provide data-driven insights for app developers and identify the elements that influence app installs, ratings, user engagement, and overall market competitiveness.

— **Objectives** —  
- To analyze the Google Play Store dataset to understand patterns in app popularity and user behavior.
- To identify the key factors that significantly impact the number of installs an app receives.
- To investigate category-wise performance to identify high-demand and high-potential app categories.
- To compare free vs paid apps in terms of installs, ratings, and market share.

- Data to Upload for Analysis → [link](https://drive.google.com/file/d/1Qr9ymoCWps9qpfwId51PvuIA_JWTKWK_/view?usp=drive_link)
        """
    )

if page == "Conclusion":
    st.title("Conclusion")
    st.markdown(
        """
### **🔍 Summarize Key Findings**

1. **App installs are extremely skewed**
    
2. **Reviews strongly correlate with installs**
    
3. **Ratings show weak correlation with installs**

4. **App size has little effect on installs**
    
6. **Certain categories consistently show higher installs and ratings**
   

### **🧠Business Interpretation**

1. **Success depends more on visibility and engagement than on app rating**
    
2. **Choosing the right category is critical**
    
3. **APK size is not a major barrier**

4. **Free or freemium is the best model for growth**

### **🚀 Suggested Actions (Strategic Recommendations)**

1. **Launch the app as FREE first**

2. **Implement a review-generation strategy**

3. **Select the app category strategically**

4. **Optimize app size but don’t sacrifice functionality**



        """
    )

if page != "Welcome":
    st.sidebar.title("Upload Dataset")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file here", type=["csv"], key="uploader")

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.sidebar.success("Dataset Loaded Successfully!")
    else:
        st.sidebar.info("Please upload a dataset to proceed.")
        data = None

    def display_plot(fig):
        st.pyplot(fig)


if page == "Univariate Analysis":
    st.title("Univariate Analysis")
    if data is None:
        st.warning("➡️  Please upload a dataset to view this analysis.")
        st.stop()

    st.markdown("### Distribution of App Installs")
    
    fig = px.histogram(data, x='log_Installs', nbins=50, title='Distribution of App Installs')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Distribution of App Ratings")
    
    fig = px.histogram(data, x='Rating', nbins=20, title='Distribution of App Ratings')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Distribution of App Sizes")
    
    fig = px.histogram(data, x='log_Size', nbins=50, title='Distribution of App Sizes')
    st.plotly_chart(fig, use_container_width=True)

    type_counts = data["Type"].value_counts().reset_index()
    type_counts.columns = ["Type", "Count"]

    st.markdown("### Distribution of App Types")
    fig = px.pie(type_counts, names="Type", values="Count", hole=0.35, title='Distribution of App Types')
    fig.update_traces(textinfo="percent+label", texttemplate="%{label}<br>%{percent:.0%}" )
    st.plotly_chart(fig, use_container_width=True)


if page == "Bivariate Analysis":
    st.title("Bivariate Analysis")
    if data is None:
        st.warning("➡️  Please upload a dataset to view this analysis.")
        st.stop()

    avg_installs = data.groupby("Type")["Installs"].mean()
    avg_ratings  = data.groupby("Type")["Rating"].mean()

    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    st.markdown("### Average Installs and Average Ratings by App Type")
    # Boxplot on the left
    sns.barplot(x=avg_installs.index, y=avg_installs.values, ax=axes[0])
    axes[0].set_title('Average Installs: Free vs Paid Apps', fontsize=18, fontweight='bold')
    axes[0].set_ylabel('Average Installs', fontsize=14)
    axes[0].set_xlabel('App Type', fontsize=14)
    axes[0].tick_params(axis='x', labelsize=12)
    axes[0].tick_params(axis='y', labelsize=12)
    axes[0].grid(visible=True, linestyle='--', alpha=0.7)

    # Barplot on the right
    sns.barplot(x=avg_ratings.index, y=avg_ratings.values, ax=axes[1])
    axes[1].set_title('Average Ratings: Free vs Paid Apps', fontsize=18, fontweight='bold')
    axes[1].set_ylabel('Average Ratings', fontsize=14)
    axes[1].set_xlabel('App type', fontsize=14)
    axes[1].tick_params(axis='x', labelsize=12)
    axes[1].tick_params(axis='y', labelsize=12)
    axes[1].grid(visible=True, linestyle='--', alpha=0.7)

    plt.tight_layout()
    display_plot(fig)


    top_20_installed_category =  data.groupby('Category')['Installs'].mean().reset_index().sort_values(by='Installs',ascending=False, ignore_index=True).head(20)
    st.markdown("### Top 20 most installed categories")

    fig = px.bar(top_20_installed_category, x="Category", y="Installs")
    fig.update_traces( textposition="outside", marker_color="indianred")
    fig.update_layout(
    title="Top 20 most installed categories",
    template="plotly_white",
    title_x=0.5

    )
    fig.update_yaxes(showgrid=True, title="Average Installs" )
    fig.update_xaxes(showgrid=False, title="Category" )
    st.plotly_chart(fig, use_container_width=True)
    
    
    st.markdown("### App Installs vs Reviews")
    
    fig = px.scatter(data, x='log_Reviews', y='log_Installs', trendline='ols', title='App Installs vs Reviews')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### App Installs vs Ratings")
    
    fig = px.scatter(data, x='Rating', y='log_Installs', trendline='ols', title='App Installs vs Ratings')
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### App Installs vs Size")
    
    fig = px.scatter(data, x='log_Size', y='log_Installs', trendline='ols', title='App Installs vs Size')
    st.plotly_chart(fig, use_container_width=True)


elif page == "Multivariate Analysis":
    st.title("Multivariate Analysis", anchor=False)
    if data is None:
        st.warning("➡️  Please upload a dataset to view this analysis.")
        st.stop()

    st.header("Discover Patterns Across Multiple Variables")
    st.write("Generate Pairplot and Heatmap for multivariate analysis.")

    # Pairplot
    st.subheader("Pairplot")
    fig, ax = plt.subplots(figsize=(20, 15))
    fig = sns.pairplot(data[["Rating","log_Installs","log_Reviews","log_Size"]], diag_kind='kde', plot_kws={'alpha':0.6})
    display_plot(fig)
    # Heatmap
    st.subheader("Heatmap")

    fig, ax = plt.subplots(figsize=(20, 15))
    sns.heatmap(data[['Rating', 'Installs', 'Reviews', 'Size']].corr(), annot=True, cmap="coolwarm", ax=ax, annot_kws={"size": 30})
    ax.set_title("Correlation Heatmap", fontsize=40, color="red", weight="bold")
    ax.tick_params(axis='x', labelsize=40)
    ax.tick_params(axis='y', labelsize=40)
    display_plot(fig)
    
