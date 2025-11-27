import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")
sns.set_theme(style="whitegrid", palette="muted")

st.set_page_config(page_title="Customer Satisfaction Case Study", layout="wide")

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

        """
    )

if page == "Conclusion":
    st.title("Conclusion")
    st.markdown(
        """
### **🔍 Summarize Key Findings**

1. **App installs are extremely skewed**
    - Only a small percentage of apps achieve very high installs (10M+).
    -  Most apps remain in the low–to–mid install range (1K–100K).

2. **Reviews strongly correlate with installs**
    - Apps with more reviews consistently have higher installs.
    - Reviews are the strongest predictor of app popularity.

3. **Ratings show weak correlation with installs**
    - High or low ratings do not guarantee installs.
    - Users download apps based on need, not ratings alone.

4. **App size has little effect on installs**
    - Both small and large apps achieve high installs.
    - Size does not determine popularity; category and demand matter more.

5. **Free apps dominate the market**
    - Free apps massively outnumber paid apps.
    - Free apps get far higher installs; paid apps get fewer installs but slightly better ratings.

6. **Certain categories consistently show higher installs and ratings**
    - Categories with strong performance include:
    - Communication, Social, Video Players, Photography, Entertainment → high installs
    -  Books, Education, Tools, Productivity → high ratings


### **🧠Business Interpretation**

1. **Success depends more on visibility and engagement than on app rating**
    - Reviews drive installs → the app must focus on gathering reviews early.

2. **Choosing the right category is critical**
    - Some categories naturally have higher demand.
    - Entering a saturated category requires strong differentiation.

3. **APK size is not a major barrier**
    - Users install both small and large apps if value is clear.
    - Developers should prioritize functionality, not shrinking APK at the cost of features.

4. **Free or freemium is the best model for growth**
    - Paid apps struggle to gain installs unless they solve a niche, high-value problem.
    - Free model → faster traction and review generation.

### **🚀 Suggested Actions (Strategic Recommendations)**

1. **Launch the app as FREE first**
    - Maximizes downloads and visibility.
    - Consider monetization through ads or in-app purchases later.

2. **Implement a review-generation strategy**
    - In-app prompts after task completion
    - Reward-based review nudges
    - Email/notification reminders
    - This directly boosts install growth.

3. **Select the app category strategically**

    - Choose categories that offer:
        - High demand
        - High satisfaction (ratings)
        - Moderate competition
    - Consider Tools, Productivity, Education, Health, etc., depending on client goals.

4. **Optimize app size but don’t sacrifice functionality**
    - Target ~10–25 MB range when possible.
    - If building a heavy category (like gaming), focus on optimization instead of strict size constraints.




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
        st.stop()

    # Define numeric and categorical columns
    numeric_columns = data.select_dtypes(include="number").columns.tolist()
    categorical_columns = data.select_dtypes(include="object").columns.tolist()

    # Helper function to display plots
    def display_plot(fig):
        st.pyplot(fig)

# Univariate Analysis
if page == "Univariate Analysis":
    st.title("Univariate Analysis", anchor=False)
    st.header("Explore Single-Variable Trends")
    st.write("Explore univariate plots with dynamic column selection.")

    # Create a 2x2 subplot layout with increased figure width
    fig, axes = plt.subplots(2, 2, figsize=(22, 13))

    # Histogram
    hist_col = st.selectbox("Select column for Histogram:", numeric_columns, key="hist", index=0)
    sns.histplot(data[hist_col], kde=True, ax=axes[0, 0])
    axes[0, 0].set_title(f"Histogram of {hist_col}", fontsize=30, color="red", weight="bold")
    axes[0, 0].tick_params(axis='x', labelsize=15, rotation=90)




    # Countplot
    if categorical_columns:
        count_col = st.selectbox("Select column for Countplot (Categorical):", categorical_columns, key="countplot", index=0)
        sns.countplot(data=data, x=count_col, ax=axes[0, 1])
        axes[0, 1].set_title(f"Countplot of {count_col}", fontsize=30, color="red", weight="bold")
        axes[0, 1].tick_params(axis='x', labelsize=15, rotation=90)



    # Pie Chart
    if categorical_columns:
        pie_col = st.selectbox("Select column for Pie Chart:", categorical_columns, key="pie", index=0)
        top_categories = data[pie_col].value_counts().sort_values(ascending=False).head(5)
        top_categories.plot.pie(autopct='%1.1f%%', ax=axes[1, 0], textprops={'fontsize': 30})
        axes[1, 0].set_title(f"Pie Chart of Top 5 Categories in {pie_col}", fontsize=30, color="red", weight="bold")



    # Boxplot
    box_col = st.selectbox("Select column for Boxplot:", numeric_columns, key="box", index=0)
    sns.boxplot(data=data, x=box_col, ax=axes[1, 1])
    axes[1, 1].set_title(f"Boxplot of {box_col}", fontsize=30, color="red", weight="bold")
    axes[1, 1].tick_params(axis='x', labelsize=15, rotation=90)


    plt.tight_layout()
    display_plot(fig)


# Bivariate Analysis
elif page == "Bivariate Analysis":
    st.title("Bivariate Analysis", anchor=False)
    st.header("Explore Relationships Between Two Variables")
    st.write("Explore bivariate relationships with dynamic column selection.")

    # Create a 3x2 subplot layout with increased figure width
    fig, axes = plt.subplots(2, 1, figsize=(22, 13))

    if numeric_columns:
    
        # Scatter Plot
        scatter_x = st.selectbox("X for Scatter Plot:", numeric_columns, key="scatter_x", index=0)
        scatter_y = st.selectbox("Y for Scatter Plot:", numeric_columns, key="scatter_y", index=0)
        sns.scatterplot(data=data, x=scatter_x, y=scatter_y, ax=axes[0])
        axes[0, 1].set_title(f"Scatter Plot of {scatter_x} vs {scatter_y}", fontsize=30, color="red", weight="bold")
        axes[0, 1].tick_params(axis='x', labelsize=15, rotation=90)


    # Bar Plot
    if categorical_columns:
        bar_x = st.selectbox("X for Bar Plot (Categorical):", categorical_columns, key="bar_x", index=0)
        bar_y = st.selectbox("Y for Bar Plot (Numeric):", numeric_columns, key="bar_y", index=0)
        sns.barplot(data=data, x=bar_x, y=bar_y, ax=axes[1])
        axes[1, 0].set_title(f"Bar Plot of {bar_x} vs {bar_y}", fontsize=30, color="red", weight="bold")
        axes[1, 0].tick_params(axis='x', labelsize=15, rotation=90)

    
    plt.tight_layout()
    display_plot(fig)

# Multivariate Analysis
elif page == "Multivariate Analysis":
    st.title("Multivariate Analysis", anchor=False)
    st.header("Discover Patterns Across Multiple Variables")
    st.write("Generate Pairplot and Heatmap for multivariate analysis.")

    # Pairplot
    st.subheader("Pairplot")
    if numeric_columns:
        pairplot_cols = st.multiselect("Select columns for Pairplot:", numeric_columns, default=numeric_columns[:min(3, len(numeric_columns))])
        if pairplot_cols:
            pairplot_fig = sns.pairplot(data[pairplot_cols])
            st.pyplot(pairplot_fig)
        else:
            st.warning("Please select at least one column for the Pairplot.")
    else:
        st.error("No numeric columns available for Pairplot.")

    # Heatmap
    st.subheader("Heatmap")
    if numeric_columns:
        fig, ax = plt.subplots(figsize=(40, 30))
        sns.heatmap(data[numeric_columns].corr(), annot=True, cmap="coolwarm", ax=ax, annot_kws={"size": 30})
        ax.set_title("Correlation Heatmap", fontsize=40, color="red", weight="bold")
        ax.tick_params(axis='x', labelsize=40)
        ax.tick_params(axis='y', labelsize=40)
        display_plot(fig)
    else:

        st.error("No numeric columns available for Heatmap.")

