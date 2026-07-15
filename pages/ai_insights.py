"""
Insight AI Page.

Provides a premium ChatGPT-like assistant workspace.
Converses in natural, jargon-free English to explain data concepts.
Uses the active dataset in memory as context.
"""

import streamlit as st
import pandas as pd
import numpy as np

from components.section_header import render_section_header
from components.empty_state import render_empty_state
from components.glass_card import glass_card_panel


def generate_conversational_response(query: str, df: pd.DataFrame, filename: str) -> str:
    """
    Generate a dynamic, natural language explanation of the dataset based on query intent.
    Explains concepts in plain English, references columns, and avoids technical jargon.
    """
    # Extract dataset properties
    num_cols = list(df.select_dtypes(include=[np.number]).columns)
    cat_cols = list(df.select_dtypes(include=["object", "category", "bool"]).columns)
    all_cols = list(df.columns)
    total_rows = len(df)
    
    # Pre-calculate quality metrics to use in conversation
    missing_cells = int(df.isnull().sum().sum())
    missing_pct = (missing_cells / df.size * 100) if df.size > 0 else 0.0
    duplicate_rows = int(df.duplicated().sum())
    
    # Outliers count
    outliers_count = 0
    outlier_cols = {}
    for col in df.select_dtypes(include=[np.number]).columns:
        if df[col].notna().sum() > 3:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1
            if iqr > 0:
                lower = q1 - 1.5 * iqr
                upper = q3 + 1.5 * iqr
                mask = (df[col] < lower) | (df[col] > upper)
                cnt = int(mask.sum())
                if cnt > 0:
                    outlier_cols[col] = cnt
                    outliers_count += cnt

    q_lower = query.lower()

    # Detect if user is asking about a specific column in the dataset
    referenced_col = None
    for col in all_cols:
        if col.lower() in q_lower:
            referenced_col = col
            break

    # 1. Custom Column Query
    if referenced_col:
        col_type = "numerical" if referenced_col in num_cols else "categorical"
        null_count = int(df[referenced_col].isnull().sum())
        null_pct = (null_count / total_rows * 100) if total_rows > 0 else 0.0
        
        response = f"I see you are interested in the **{referenced_col}** column. Let's look at what the data tells us about it in plain terms.\n\n"
        
        if col_type == "numerical":
            mean_val = df[referenced_col].mean()
            min_val = df[referenced_col].min()
            max_val = df[referenced_col].max()
            response += (
                f"This is a numerical column, which means it tracks quantities or measurements. "
                f"On average, the values in **{referenced_col}** are around **{mean_val:,.2f}**. "
                f"The lowest value recorded is **{min_val:,.2f}**, and the highest is **{max_val:,.2f}**.\n\n"
            )
            if referenced_col in outlier_cols:
                response += (
                    f"I noticed that **{referenced_col}** has **{outlier_cols[referenced_col]} values** that are unusually high or low "
                    f"compared to the typical range. In statistics, we call these 'outliers.' They represent rare events or extreme values "
                    f"that might skew our calculations, like a single huge sales order in a month of typical smaller ones.\n\n"
                )
        else:
            uniq_cnt = df[referenced_col].nunique()
            top_vals = df[referenced_col].value_counts().head(3).index.tolist()
            response += (
                f"This is a categorical column, meaning it sorts data into labels, groups, or text categories. "
                f"There are **{uniq_cnt} unique groups** in this column. "
                f"The most common ones are: **{', '.join(map(str, top_vals))}**.\n\n"
            )
            
        if null_count > 0:
            response += (
                f"⚠️ Also, about **{null_pct:.1f}%** of the entries in this column are blank (missing data). "
                f"This means we don't have recorded values for **{null_count:,} rows**. Blank entries can create gaps in our analysis, "
                f"but we can handle them by filling them in with reasonable defaults during data cleaning.\n\n"
            )
        else:
            response += f"✓ Every single row has a value recorded for **{referenced_col}**, which is excellent for accuracy.\n\n"
            
        response += (
            f"**Here are a few questions we could explore next:**\n"
            f"1. Would you like to check if the unusual values (outliers) in **{referenced_col}** are skewing our averages?\n"
            f"2. Shall we examine how **{referenced_col}** behaves over time or correlates with other columns?\n"
            f"3. Do you want to see how to clean or impute the missing entries in this column?"
        )
        return response

    # 2. General Dataset Summary
    if "summarize" in q_lower or "summary" in q_lower or "overall" in q_lower:
        num_descr = f"**{len(num_cols)} columns with numbers** (like {', '.join(num_cols[:3])})" if num_cols else "no numerical columns"
        cat_descr = f"**{len(cat_cols)} columns with categories or text** (like {', '.join(cat_cols[:3])})" if cat_cols else "no text columns"
        
        response = (
            f"Let's break down what is in your dataset **{filename}** in simple terms.\n\n"
            f"Think of this dataset as a table of information containing **{total_rows:,} rows** (or entries) "
            f"and **{len(all_cols)} columns** (the characteristics we are measuring).\n\n"
            f"We have:\n"
            f"* {num_descr}\n"
            f"* {cat_descr}\n\n"
            f"In terms of data completeness, **{100.0 - missing_pct:.2f}% of all cells** contain data. "
            f"This is a solid start, but we have **{missing_cells:,} blank spots** across the dataset that we might want to fill. "
        )
        if duplicate_rows > 0:
            response += f"We also found **{duplicate_rows:,} duplicate rows** which are exact copies of other entries and can double-count statistics."
        else:
            response += "Fortunately, we didn't find any duplicate rows, so every entry is unique."
            
        response += (
            f"\n\n**What would you like to explore next?**\n"
            f"1. Should we look at the columns that contain missing values to see where the gaps are?\n"
            f"2. Would you like a list of strategic recommendations to improve this data's quality?\n"
            f"3. Shall we look at the relationships and correlations between the columns?"
        )
        return response

    # 3. Anomaly & Outlier Scan
    if "anomal" in q_lower or "outlier" in q_lower or "extreme" in q_lower or "bug" in q_lower:
        response = (
            f"Let's inspect the anomalies and unusual patterns in **{filename}**.\n\n"
            f"Anomalies are data points that don't fit the expected pattern. They are like grammatical errors in a book — they stand out and might cause confusion.\n\n"
        )
        if outliers_count > 0:
            response += (
                f"* **Unusual Values (Outliers)**: We detected **{outliers_count:,} values** that are significantly higher or lower than typical. "
                f"This occurs most notably in columns like: " + ", ".join([f"**{c}** ({cnt} unusual values)" for c, cnt in list(outlier_cols.items())[:3]]) + ". "
                f"For instance, if most entries are between 10 and 50, but one entry is 500, that is an outlier. We can 'clip' these to keep them within a normal range.\n"
            )
        else:
            response += "* **Unusual Values (Outliers)**: We didn't find any extreme numerical outliers. Your measurements look well-distributed.\n"
            
        if missing_cells > 0:
            response += (
                f"* **Gaps (Missing Data)**: There are **{missing_cells:,} empty entries** in the table. "
                f"Leaving these empty can cause charts to skip columns or calculations to return errors. We can fix this by replacing blanks with typical values (the middle or average value).\n"
            )
        else:
            response += "* **Gaps (Missing Data)**: The dataset is 100% complete with no empty cells.\n"
            
        if duplicate_rows > 0:
            response += (
                f"* **Duplicates**: Found **{duplicate_rows:,} exact copy rows**. "
                f"These can distort your calculations, making certain categories look twice as important as they actually are. We can drop these copies safely.\n"
            )
            
        response += (
            f"\n**Would you like to:**\n"
            f"1. Automatically clean these anomalies by replacing missing values with typical averages?\n"
            f"2. See a detailed list of which specific columns have the most outliers?\n"
            f"3. Learn how these anomalies might affect our business forecasts?"
        )
        return response

    # 4. Business Recommendations
    if "recommend" in q_lower or "business" in q_lower or "strategy" in q_lower or "action" in q_lower:
        col_names_lower = [c.lower() for c in all_cols]
        suggestions = []
        
        if any("revenue" in c or "sales" in c or "amount" in c or "price" in c for c in col_names_lower):
            suggestions.append(
                "💰 **Review pricing and transaction sizes**: Since you have sales/revenue columns, we should look at the distribution of transaction values. "
                "This helps identify if a few customers are driving most of the revenue, or if sales are evenly spread."
            )
        if any("customer" in c or "user" in c or "client" in c or "churn" in c for c in col_names_lower):
            suggestions.append(
                "👥 **Customer Segmentation**: We have customer identifiers. We can group rows by customer to identify your most active segments "
                "and spot clients whose activity has slowed down."
            )
        if any("date" in c or "time" in c or "year" in c or "month" in c for c in col_names_lower):
            suggestions.append(
                "📅 **Seasonality Planning**: Since date columns are present, we can look for seasonal peaks (like higher demand on weekends or specific months) "
                "to align your team's schedule and stock levels."
            )
            
        suggestions.append(
            "🧼 **Establish Data Quality Guidelines**: Since empty entries or outliers exist, creating a validation script will prevent "
            "corrupted or incomplete files from entering your dashboard in the future."
        )
        
        recs_str = "\n\n".join(suggestions)
        response = (
            f"Here are practical strategic recommendations based on the characteristics of **{filename}**:\n\n"
            f"{recs_str}\n\n"
            f"**What shall we focus on next?**\n"
            f"1. Would you like to segment your categorical columns to see which group has the highest values?\n"
            f"2. Should we check for seasonal timelines and trends?\n"
            f"3. Shall we clean the dataset to ensure these recommendations are backed by complete records?"
        )
        return response

    # 5. Predict Trends
    if "predict" in q_lower or "trend" in q_lower or "forecast" in q_lower or "future" in q_lower:
        date_cols = [c for c in all_cols if any(kw in c.lower() for kw in ["date", "time", "created", "updated"])]
        if date_cols and num_cols:
            response = (
                f"We can project trends in **{filename}** by tracking how **{num_cols[0]}** changes over the **{date_cols[0]}** timeline.\n\n"
                f"In data analysis, we do this by:\n"
                f"1. **Grouping by time period**: Summing or averaging our numbers (like `{num_cols[0]}`) daily, weekly, or monthly.\n"
                f"2. **Finding the trajectory**: Fitting a line to see if the overall direction is going up, down, or staying flat.\n"
                f"3. **Predicting the future**: Extending that line forward while adding a 'confidence band' (a shaded area showing our margin of error, which grows wider the further into the future we look).\n\n"
                f"If you go to the **Forecasting** tab, you can view this projection visually."
            )
        else:
            response = (
                f"To project future trends, we typically look for a column with dates or times, and a column with numbers.\n\n"
                f"In your dataset, we have numerical columns like `{', '.join(num_cols[:2])}`. "
                f"If you have date-like columns, we can match them together to look for cyclical patterns. "
                f"Even without dates, we can project values sequentially by row number to see if your metrics are growing or shrinking.\n\n"
            )
            
        response += (
            f"\n**Here is what we can do next:**\n"
            f"1. Would you like to run a trend projection on **{num_cols[0]}**?\n"
            f"2. Shall we look for correlations to see what factors are driving changes in our numbers?\n"
            f"3. Would you like me to explain how we calculate our margins of error (confidence intervals)?"
        )
        return response

    # 6. Default Conversational Fallback
    response = (
        f"Hello! I am your CLARIO conversational guide. I have loaded **{filename}** into my context.\n\n"
        f"Think of me as a translator between your raw table rows and practical business clarity. You don't need to know any programming or math to use me. "
        f"Your dataset has **{len(all_cols)} characteristics** (columns) and **{total_rows:,} entries** (rows).\n\n"
        f"**Here are some questions we can explore together:**\n"
        f"* *'Can you summarize the columns and tell me what types of data we have?'*\n"
        f"* *'Are there any blank entries or outliers that might skew our calculations?'*\n"
        f"* *'What strategic recommendations do you have for this kind of dataset?'*\n"
        f"* *'How can we project these numbers into the future?'*\n\n"
        f"Feel free to type any question in your own words, or click one of the quick actions on the left!"
    )
    return response


def render() -> None:
    """Render the Insight AI chatbot panel."""
    # Check dataset
    if "dataset" not in st.session_state:
        render_empty_state(
            title="No Dataset Selected",
            message="We couldn't locate an active dataset in memory. Please upload a dataset first.",
            action_label="Go to Upload Workspace",
            navigate_to="upload",
            navigate_label="Upload",
        )
        return

    df = st.session_state["dataset"]
    filename = st.session_state.get("dataset_filename", "dataset.csv")

    render_section_header(
        title="Insight AI Workspace",
        subtitle=f"Query machine learning insights and descriptive context for {filename}.",
        label="Insight AI Panel",
    )

    if st.session_state.get("cleaned_df") is not None:
        st.info("All insights and metrics are generated from the cleaned dataset.")

    # Initialize chat history
    if "ai_messages" not in st.session_state:
        st.session_state["ai_messages"] = [
            {
                "role": "assistant", 
                "content": (
                    f"Hello! I am **CLARIO Insight AI**. I have loaded your dataset **{filename}** into context. "
                    f"You don't need to be a data scientist to explore your data — simply ask me questions in plain English. "
                    f"What would you like to explore today?"
                )
            }
        ]

    # Two column layout: Left Quick Prompts, Right ChatGPT bubble feed
    col_prompts, col_chat = st.columns([1, 2.5])

    # Callback helper for preset buttons
    def trigger_preset_prompt(preset_text: str):
        st.session_state["ai_messages"].append({"role": "user", "content": preset_text})
        response = generate_conversational_response(preset_text, df, filename)
        st.session_state["ai_messages"].append({"role": "assistant", "content": response})
        # Add to dashboard activity log
        if "activity_log" in st.session_state:
            import datetime
            now_str = datetime.datetime.now().strftime("%I:%M %p")
            st.session_state["activity_log"].insert(0, {"time": now_str, "event": f"Query: '{preset_text[:25]}...'"})

    with col_prompts:
        st.markdown('<p style="font-size: 0.95rem; font-weight: 600; color: var(--text); margin-top: 0; margin-bottom: 0.75rem;">Workspace Actions</p>', unsafe_allow_html=True)
        
        with glass_card_panel():
            if st.button("Summarize Dataset", use_container_width=True, key="prompt_btn_summary"):
                trigger_preset_prompt("Summarize dataset")
                st.rerun()
            if st.button("Explain Charts", use_container_width=True, key="prompt_btn_charts"):
                trigger_preset_prompt("Explain charts")
                st.rerun()
            if st.button("Detect Anomalies", use_container_width=True, key="prompt_btn_anomalies"):
                trigger_preset_prompt("Detect anomalies")
                st.rerun()
            if st.button("Business Recommendations", use_container_width=True, key="prompt_btn_recs"):
                trigger_preset_prompt("Business recommendations")
                st.rerun()
            if st.button("Predict Trends", use_container_width=True, key="prompt_btn_predict"):
                trigger_preset_prompt("Predict trends")
                st.rerun()
            if st.button("Generate Insights", use_container_width=True, key="prompt_btn_insights"):
                trigger_preset_prompt("Generate insights")
                st.rerun()

    with col_chat:
        st.markdown('<p style="font-size: 0.95rem; font-weight: 600; color: var(--text); margin-top: 0; margin-bottom: 0.75rem;">Conversation</p>', unsafe_allow_html=True)
        
        # Chat container window
        chat_container = st.container(border=True)
        with chat_container:
            for msg in st.session_state["ai_messages"]:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

        # Chat Input at bottom
        user_query = st.chat_input("Ask a question about your data...")
        if user_query:
            st.session_state["ai_messages"].append({"role": "user", "content": user_query})
            response_content = generate_conversational_response(user_query, df, filename)
            st.session_state["ai_messages"].append({"role": "assistant", "content": response_content})
            # Add to dashboard activity log
            if "activity_log" in st.session_state:
                import datetime
                now_str = datetime.datetime.now().strftime("%I:%M %p")
                st.session_state["activity_log"].insert(0, {"time": now_str, "event": f"Query: '{user_query[:25]}...'"})
            st.rerun()


if __name__ == "__main__":
    render()
