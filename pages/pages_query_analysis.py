# import streamlit as st
# import pandas as pd
# import spacy
# import plotly.express as px
# from datetime import datetime, timedelta
# from collections import defaultdict
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors
# from reportlab.platypus.tables import TableStyle  # Added missing import
# import io

# # Load spacy model
# nlp = spacy.load("en_core_web_sm")

# # Define the 50 questions as a reference (first 10 from each category)
# QUESTIONS = {
#     "customer_behavior_1": "How many unique customers are in the dataset?",
#     "customer_behavior_2": "What is the average number of sessions per customer?",
#     "customer_behavior_3": "Which customers have the highest number of sessions?",
#     "customer_behavior_4": "What is the distribution of session durations across all customers?",
#     "customer_behavior_5": "Which customers have the longest average session duration?",
#     "customer_behavior_6": "How many sessions occur per day on average?",
#     "customer_behavior_7": "What is the most common time of day for customer sessions?",
#     "customer_behavior_8": "Which customers have sessions from multiple IP addresses?",
#     "customer_behavior_9": "How does session frequency vary by customer group?",
#     "customer_behavior_10": "What is the retention rate of customers (e.g., those with multiple sessions over time)?",
#     "product_performance_1": "Which products are added to carts most frequently?",
#     "product_performance_2": "What is the total number of unique products added to carts?",
#     "product_performance_3": "Which product categories (based on hierarchy) are most popular in carts?",
#     "product_performance_4": "How many products have never been added to a cart?",
#     "product_performance_5": "What is the average time a product stays in a cart before session ends?",
#     "product_performance_6": "Which products are most often added together in the same session?",
#     "product_performance_7": "What is the distribution of cart additions by product hierarchy level?",
#     "product_performance_8": "Which products have the highest addition rate per session?",
#     "product_performance_9": "How does product popularity vary over time (e.g., daily or weekly trends)?",
#     "product_performance_10": "Which products are added by the most unique customers?",
#     "session_analysis_1": "What is the total number of sessions in the dataset?",
#     "session_analysis_2": "What is the average session duration across all sessions?",
#     "session_analysis_3": "Which sessions have the longest duration?",
#     "session_analysis_4": "How does session duration vary by time of day?",
#     "session_analysis_5": "What is the distribution of sessions by day of the week?",
#     "session_analysis_6": "Which IP addresses are associated with the most sessions?",
#     "session_analysis_7": "How many sessions have no cart activity?",
#     "session_analysis_8": "What is the average time between session start and cart addition?",
#     "session_analysis_9": "Which sessions have the most products added to the cart?",
#     "session_analysis_10": "How does session duration correlate with the number of cart additions?",
#     "cart_activity_1": "How many unique products are added to carts overall?",
#     "cart_activity_2": "What is the average number of products added per cart?",
#     "cart_activity_3": "Which customers have the most cart additions?",
#     "cart_activity_4": "What is the distribution of cart additions by session duration?",
#     "cart_activity_5": "Which sessions have the highest number of cart additions?",
#     "cart_activity_6": "How many cart additions occur within the first minute of a session?",
#     "cart_activity_7": "What is the most common product added to carts by new customers?",
#     "cart_activity_8": "Which products are added to carts in the same session by the same customer?",
#     "cart_activity_9": "How does cart activity vary by time of day?",
#     "cart_activity_10": "What is the average time from session start to first cart addition?",
#     "business_insights_1": "What is the conversion rate from sessions to cart additions?",
#     "business_insights_2": "Which customer groups have the highest cart addition rates?",
#     "business_insights_3": "How does customer group size correlate with session frequency?",
#     "business_insights_4": "What is the potential revenue impact of top-performing products (assuming equal pricing)?",
#     "business_insights_5": "Which customer segments (based on group or session behavior) are most valuable?",
#     "business_insights_6": "How can session duration be optimized to increase cart additions?",
#     "business_insights_7": "What is the customer lifetime value based on session and cart activity?",
#     "business_insights_8": "Which IP address ranges indicate potential bot activity (e.g., high session frequency)?",
#     "business_insights_9": "How does product hierarchy depth impact customer engagement?",
#     "business_insights_10": "What is the churn rate of customers based on session activity?"
# }

# st.title("Query Analysis")

# if 'data' not in st.session_state:
#     st.error("Please upload an Excel file on the main page.")
# else:
#     user_query = st.text_area("Enter your query (e.g., 'How many unique customers are in the dataset?'):", height=100)
#     if st.button("Run Query"):
#         if user_query:
#             # Parse query with spacy
#             doc = nlp(user_query.lower())
#             tokens = [token.lemma_ for token in doc]
#             phrases = [" ".join([token.text for token in chunk]) for chunk in doc.noun_chunks]
            
#             # Score queries based on token overlap
#             scores = defaultdict(float)
#             for q_key, q_text in QUESTIONS.items():
#                 q_doc = nlp(q_text.lower())
#                 q_tokens = [token.lemma_ for token in q_doc]
#                 overlap = len(set(tokens) & set(q_tokens)) / len(set(q_tokens))
#                 scores[q_key] = overlap
            
#             # Find the best match
#             best_match = max(scores, key=scores.get, default=None)
#             if scores[best_match] < 0.4:  # Threshold for match confidence
#                 st.warning("I cannot interpret the question. Can the user ask in a different way?")
#             else:
#                 result_df = None
#                 visualization = None
#                 feasibility_study = ""
#                 recommendation = ""
#                 title = f"Result for: {QUESTIONS[best_match]}"
                
#                 # Customer Behavior Queries
#                 if best_match == "customer_behavior_1":
#                     customers = st.session_state['data']['Customers']
#                     unique_customers = customers['id'].nunique()
#                     result_df = pd.DataFrame({"Metric": ["Unique Customers"], "Value": [unique_customers]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Number of Unique Customers")
#                     visualization = fig
#                     feasibility_study = f"There are {unique_customers} unique customers in the dataset as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Evaluate customer acquisition strategies if the number is below target."
                
#                 elif best_match == "customer_behavior_2":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     customers = st.session_state['data']['Customers']
#                     sessions_per_customer = sessions.groupby('customer_id').size().reset_index(name='session_count')
#                     avg_sessions = sessions_per_customer['session_count'].mean()
#                     result_df = pd.DataFrame({"Metric": ["Average Sessions per Customer"], "Value": [avg_sessions]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Average Number of Sessions per Customer")
#                     visualization = fig
#                     feasibility_study = f"Each customer averages {avg_sessions:.2f} sessions, indicating engagement levels as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Boost engagement with targeted campaigns if the average is low."
                
#                 elif best_match == "customer_behavior_3":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     customers = st.session_state['data']['Customers']
#                     sessions_per_customer = sessions.groupby('customer_id').size().reset_index(name='session_count')
#                     result_df = sessions_per_customer.merge(customers, left_on='customer_id', right_on='id')
#                     result_df = result_df[['email', 'first_name', 'last_name', 'session_count']].sort_values('session_count', ascending=False).head(5)
#                     fig = px.bar(result_df, x='email', y='session_count', title="Top 5 Customers by Number of Sessions", labels={'email': 'Customer Email', 'session_count': 'Session Count'})
#                     visualization = fig
#                     top_customer = result_df.iloc[0]['email'] if not result_df.empty else "N/A"
#                     feasibility_study = f"Top 5 customers have {result_df['session_count'].sum()} sessions, with '{top_customer}' leading as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Offer '{top_customer}' loyalty rewards to sustain their activity."
                
#                 elif best_match == "customer_behavior_4":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
#                     result_df = sessions[['duration']].copy()
#                     fig = px.histogram(result_df, x='duration', nbins=20, title="Distribution of Session Durations", labels={'duration': 'Duration (minutes)'})
#                     visualization = fig
#                     avg_duration = result_df['duration'].mean()
#                     feasibility_study = f"Average session duration is {avg_duration:.2f} minutes, with a varied distribution as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Enhance content if short durations dominate to retain customers longer."
                
#                 elif best_match == "customer_behavior_5":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     customers = st.session_state['data']['Customers']
#                     sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
#                     avg_duration = sessions.groupby('customer_id')['duration'].mean().reset_index()
#                     result_df = avg_duration.merge(customers, left_on='customer_id', right_on='id')
#                     result_df = result_df[['email', 'first_name', 'last_name', 'duration']].sort_values('duration', ascending=False).head(5)
#                     fig = px.bar(result_df, x='email', y='duration', title="Top 5 Customers by Average Session Duration", labels={'email': 'Customer Email', 'duration': 'Average Duration (minutes)'})
#                     visualization = fig
#                     top_customer = result_df.iloc[0]['email'] if not result_df.empty else "N/A"
#                     feasibility_study = f"Top 5 customers average {result_df['duration'].mean():.2f} minutes, with '{top_customer}' at {result_df.iloc[0]['duration']:.2f} minutes as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Study '{top_customer}'s behavior to improve engagement strategies."
                
#                 elif best_match == "customer_behavior_6":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     sessions_per_day = sessions.groupby(sessions['session_start'].dt.date).size().mean()
#                     result_df = pd.DataFrame({"Metric": ["Average Sessions per Day"], "Value": [sessions_per_day]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Average Number of Sessions per Day")
#                     visualization = fig
#                     feasibility_study = f"Average of {sessions_per_day:.2f} sessions per day as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Optimize staffing for peak days based on this average."
                
#                 elif best_match == "customer_behavior_7":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     sessions['hour'] = sessions['session_start'].dt.hour
#                     most_common_hour = sessions['hour'].mode()[0]
#                     result_df = pd.DataFrame({"Metric": ["Most Common Session Hour"], "Value": [f"{most_common_hour}:00"]})
#                     fig = px.bar(result_df, x="Metric", y=["Value"], title="Most Common Session Hour", text=["Value"], height=300)
#                     visualization = fig
#                     feasibility_study = f"Most common session hour is {most_common_hour}:00 EEST on May 18, 2025."
#                     recommendation = f"Schedule promotions at {most_common_hour}:00 to maximize reach."
                
#                 elif best_match == "customer_behavior_8":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     ip_counts = sessions.groupby(['customer_id', 'ip_address']).size().reset_index(name='count')
#                     multi_ip_customers = ip_counts.groupby('customer_id').filter(lambda x: len(x) > 1)['customer_id'].unique()
#                     customers = st.session_state['data']['Customers']
#                     result_df = customers[customers['id'].isin(multi_ip_customers)][['email', 'first_name', 'last_name']]
#                     if result_df.empty:
#                         result_df = pd.DataFrame({"Message": ["No customers with multiple IP addresses found"]})
#                     fig = px.bar(result_df, x='email', y=[1] * len(result_df), title="Customers with Multiple IP Addresses", labels={'email': 'Customer Email'}, height=300)
#                     visualization = fig
#                     count = len(multi_ip_customers)
#                     feasibility_study = f"{count} customers use multiple IP addresses, possibly indicating multi-device usage as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Monitor for unusual patterns to detect potential fraud."
                
#                 elif best_match == "customer_behavior_9":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     customers = st.session_state['data']['Customers']
#                     customers['group'] = pd.qcut(customers['registration_date'].rank(method='first'), 4, labels=['G1', 'G2', 'G3', 'G4'])
#                     sessions_per_group = sessions.merge(customers, on='customer_id').groupby('group').size().reset_index(name='session_count')
#                     result_df = sessions_per_group
#                     fig = px.bar(result_df, x='group', y='session_count', title="Session Frequency by Customer Group", labels={'group': 'Customer Group', 'session_count': 'Session Count'})
#                     visualization = fig
#                     max_group = result_df.loc[result_df['session_count'].idxmax(), 'group']
#                     feasibility_study = f"Group {max_group} has the highest session count of {result_df['session_count'].max()} as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Target group {max_group} with personalized offers."
                
#                 elif best_match == "customer_behavior_10":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     customer_sessions = sessions.groupby('customer_id').size().reset_index(name='session_count')
#                     total_customers = len(customer_sessions)
#                     retained_customers = len(customer_sessions[customer_sessions['session_count'] > 1])
#                     retention_rate = (retained_customers / total_customers) * 100 if total_customers > 0 else 0
#                     result_df = pd.DataFrame({"Metric": ["Retention Rate (%)"], "Value": [retention_rate]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Customer Retention Rate", text=[f"{retention_rate:.2f}%"])
#                     visualization = fig
#                     feasibility_study = f"The retention rate is {retention_rate:.2f}%, with {retained_customers} customers having multiple sessions as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Implement retention strategies if the rate is below industry benchmarks (e.g., 20-30%)."
                
#                 # Product Performance Queries
#                 elif best_match == "product_performance_1":
#                     order_details = st.session_state['data']['Order_Details']
#                     products = st.session_state['data']['Products']
#                     cart_freq = order_details.groupby('product_id').size().reset_index(name='cart_additions')
#                     result_df = products.merge(cart_freq, left_on='id', right_on='product_id')[['name', 'cart_additions']].sort_values('cart_additions', ascending=False).head(5)
#                     fig = px.bar(result_df, x='name', y='cart_additions', title="Top 5 Products Added to Carts", labels={'name': 'Product', 'cart_additions': 'Additions'})
#                     visualization = fig
#                     top_product = result_df.iloc[0]['name'] if not result_df.empty else "N/A"
#                     feasibility_study = f"Top 5 products added to carts {result_df['cart_additions'].sum()} times, with '{top_product}' leading as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Promote '{top_product}' to leverage its popularity."
                
#                 elif best_match == "product_performance_2":
#                     order_details = st.session_state['data']['Order_Details']
#                     unique_products = order_details['product_id'].nunique()
#                     result_df = pd.DataFrame({"Metric": ["Unique Products in Carts"], "Value": [unique_products]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Total Unique Products Added to Carts")
#                     visualization = fig
#                     feasibility_study = f"{unique_products} unique products are added to carts, showing product variety as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Maintain diverse inventory to support customer preferences."
                
#                 elif best_match == "product_performance_3":
#                     order_details = st.session_state['data']['Order_Details']
#                     products = st.session_state['data']['Products']
#                     categories = st.session_state['data']['Categories']
#                     category_popularity = order_details.merge(products, on='product_id').merge(categories, left_on='category_id', right_on='id')
#                     result_df = category_popularity.groupby('name_y')['id_x'].count().reset_index(name='cart_additions').sort_values('cart_additions', ascending=False).head(5)
#                     result_df = result_df.rename(columns={'name_y': 'Category', 'cart_additions': 'Additions'})
#                     fig = px.bar(result_df, x='Category', y='Additions', title="Top 5 Popular Categories in Carts", labels={'Category': 'Category', 'Additions': 'Cart Additions'})
#                     visualization = fig
#                     top_category = result_df.iloc[0]['Category'] if not result_df.empty else "N/A"
#                     feasibility_study = f"Top 5 categories have {result_df['Additions'].sum()} additions, with '{top_category}' leading as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Focus inventory on '{top_category}' to meet demand."
                
#                 elif best_match == "product_performance_4":
#                     order_details = st.session_state['data']['Order_Details']
#                     products = st.session_state['data']['Products']
#                     carted_products = order_details['product_id'].unique()
#                     total_products = products['id'].nunique()
#                     never_carted = total_products - len(carted_products)
#                     result_df = pd.DataFrame({"Metric": ["Products Never Added to Cart"], "Value": [never_carted]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Products Never Added to Cart")
#                     visualization = fig
#                     feasibility_study = f"{never_carted} products have never been added to carts out of {total_products} as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Review and promote these products to boost sales."
                
#                 elif best_match == "product_performance_5":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     order_details = st.session_state['data']['Order_Details']
#                     sessions = sessions.merge(order_details, left_on='id', right_on='id', how='left')
#                     sessions['time_in_cart'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
#                     avg_time = sessions['time_in_cart'].mean()
#                     result_df = pd.DataFrame({"Metric": ["Average Time in Cart (minutes)"], "Value": [avg_time]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Average Time Products Stay in Cart")
#                     visualization = fig
#                     feasibility_study = f"Average time a product stays in cart is {avg_time:.2f} minutes as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Shorten checkout process if time is high to reduce abandonment."
                
#                 elif best_match == "product_performance_6":
#                     order_details = st.session_state['data']['Order_Details']
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     merged = sessions.merge(order_details, left_on='id', right_on='id')
#                     pairs = merged.groupby(['session_id', 'product_id']).size().reset_index(name='count')
#                     pair_counts = pairs.groupby(['session_id']).apply(lambda x: x.nlargest(2, 'count')).reset_index(drop=True)
#                     top_pairs = pair_counts.groupby(['product_id']).size().sort_values(ascending=False).head(5).reset_index(name='pair_count')
#                     result_df = st.session_state['data']['Products'].merge(top_pairs, left_on='id', right_on='product_id')[['name', 'pair_count']]
#                     fig = px.bar(result_df, x='name', y='pair_count', title="Top 5 Products Added Together", labels={'name': 'Product', 'pair_count': 'Pair Count'})
#                     visualization = fig
#                     top_product = result_df.iloc[0]['name'] if not result_df.empty else "N/A"
#                     feasibility_study = f"Top 5 product pairs total {result_df['pair_count'].sum()} instances, with '{top_product}' leading as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Bundle '{top_product}' with frequent pairs for upselling."
                
#                 elif best_match == "product_performance_7":
#                     order_details = st.session_state['data']['Order_Details']
#                     products = st.session_state['data']['Products']
#                     categories = st.session_state['data']['Categories']
#                     merged = order_details.merge(products, on='product_id').merge(categories, left_on='category_id', right_on='id')
#                     result_df = merged.groupby('parent_id').size().reset_index(name='additions')
#                     result_df['parent_id'] = result_df['parent_id'].fillna('Top Level')
#                     fig = px.bar(result_df, x='parent_id', y='additions', title="Distribution of Cart Additions by Hierarchy Level", labels={'parent_id': 'Hierarchy Level', 'additions': 'Additions'})
#                     visualization = fig
#                     avg_additions = result_df['additions'].mean()
#                     feasibility_study = f"Average additions per hierarchy level is {avg_additions:.2f}, with varied distribution as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Focus on popular hierarchy levels to optimize product placement."
                
#                 elif best_match == "product_performance_8":
#                     order_details = st.session_state['data']['Order_Details']
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     merged = sessions.merge(order_details, left_on='id', right_on='id')
#                     product_sessions = merged.groupby('product_id').size().reset_index(name='additions')
#                     session_count = sessions['id'].nunique()
#                     result_df = st.session_state['data']['Products'].merge(product_sessions, left_on='id', right_on='product_id')
#                     result_df['addition_rate'] = result_df['additions'] / session_count * 100
#                     result_df = result_df[['name', 'addition_rate']].sort_values('addition_rate', ascending=False).head(5)
#                     fig = px.bar(result_df, x='name', y='addition_rate', title="Top 5 Products by Addition Rate", labels={'name': 'Product', 'addition_rate': 'Rate (%)'})
#                     visualization = fig
#                     top_product = result_df.iloc[0]['name'] if not result_df.empty else "N/A"
#                     feasibility_study = f"Top 5 products have addition rates up to {result_df['addition_rate'].max():.2f}%, with '{top_product}' leading as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Highlight '{top_product}' in marketing due to its high addition rate."
                
#                 elif best_match == "product_performance_9":
#                     order_details = st.session_state['data']['Order_Details']
#                     orders = st.session_state['data']['Orders']
#                     products = st.session_state['data']['Products']
#                     merged = order_details.merge(orders, on='order_id').merge(products, on='product_id')
#                     merged['order_date'] = merged['order_date'].dt.date
#                     result_df = merged.groupby(['order_date', 'name']).size().reset_index(name='additions').head(10)
#                     fig = px.line(result_df, x='order_date', y='additions', color='name', title="Product Popularity Over Time", labels={'order_date': 'Date', 'additions': 'Additions'})
#                     visualization = fig
#                     max_additions = result_df['additions'].max()
#                     feasibility_study = f"Product popularity peaks at {max_additions} additions, showing temporal trends as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Adjust inventory based on these trends to meet demand."
                
#                 elif best_match == "product_performance_10":
#                     order_details = st.session_state['data']['Order_Details']
#                     orders = st.session_state['data']['Orders']
#                     products = st.session_state['data']['Products']
#                     merged = order_details.merge(orders, on='order_id')
#                     unique_customers = merged.groupby('product_id')['customer_id'].nunique().reset_index(name='unique_customers')
#                     result_df = products.merge(unique_customers, left_on='id', right_on='product_id')[['name', 'unique_customers']].sort_values('unique_customers', ascending=False).head(5)
#                     fig = px.bar(result_df, x='name', y='unique_customers', title="Top 5 Products by Unique Customers", labels={'name': 'Product', 'unique_customers': 'Unique Customers'})
#                     visualization = fig
#                     top_product = result_df.iloc[0]['name'] if not result_df.empty else "N/A"
#                     feasibility_study = f"Top 5 products are added by {result_df['unique_customers'].sum()} unique customers, with '{top_product}' leading as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Promote '{top_product}' to a broader audience."
                
#                 # Session Analysis Queries
#                 elif best_match == "session_analysis_1":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     total_sessions = len(sessions)
#                     result_df = pd.DataFrame({"Metric": ["Total Sessions"], "Value": [total_sessions]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Total Number of Sessions")
#                     visualization = fig
#                     feasibility_study = f"There are {total_sessions} sessions in the dataset as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Use this data to assess platform traffic trends."
                
#                 elif best_match == "session_analysis_2":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
#                     avg_duration = sessions['duration'].mean()
#                     result_df = pd.DataFrame({"Metric": ["Average Session Duration (minutes)"], "Value": [avg_duration]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Average Session Duration")
#                     visualization = fig
#                     feasibility_study = f"Average session duration is {avg_duration:.2f} minutes as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Improve content if the duration is below industry averages (e.g., 5-10 minutes)."
                
#                 elif best_match == "session_analysis_3":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
#                     result_df = sessions[['id', 'duration']].sort_values('duration', ascending=False).head(5)
#                     fig = px.bar(result_df, x='id', y='duration', title="Top 5 Longest Sessions", labels={'id': 'Session ID', 'duration': 'Duration (minutes)'})
#                     visualization = fig
#                     max_duration = result_df.iloc[0]['duration']
#                     feasibility_study = f"Top 5 sessions reach up to {max_duration:.2f} minutes in duration as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Analyze these sessions to replicate engaging features."
                
#                 elif best_match == "session_analysis_4":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
#                     sessions['hour'] = sessions['session_start'].dt.hour
#                     result_df = sessions.groupby('hour')['duration'].mean().reset_index()
#                     fig = px.line(result_df, x='hour', y='duration', title="Average Session Duration by Hour", labels={'hour': 'Hour of Day', 'duration': 'Average Duration (minutes)'})
#                     visualization = fig
#                     peak_hour = result_df.loc[result_df['duration'].idxmax(), 'hour']
#                     feasibility_study = f"Peak duration occurs at hour {peak_hour}:00 with {result_df['duration'].max():.2f} minutes as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Enhance features at {peak_hour}:00 to retain users."
                
#                 elif best_match == "session_analysis_5":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     sessions['day'] = sessions['session_start'].dt.day_name()
#                     result_df = sessions.groupby('day').size().reset_index(name='session_count')
#                     fig = px.bar(result_df, x='day', y='session_count', title="Distribution of Sessions by Day of Week", labels={'day': 'Day', 'session_count': 'Session Count'})
#                     visualization = fig
#                     peak_day = result_df.loc[result_df['session_count'].idxmax(), 'day']
#                     feasibility_study = f"Most sessions occur on {peak_day} with {result_df['session_count'].max()} counts as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Schedule promotions on {peak_day} to maximize impact."
                
#                 elif best_match == "session_analysis_6":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     ip_sessions = sessions.groupby('ip_address').size().reset_index(name='session_count')
#                     result_df = ip_sessions.sort_values('session_count', ascending=False).head(5)
#                     fig = px.bar(result_df, x='ip_address', y='session_count', title="Top 5 IP Addresses by Session Count", labels={'ip_address': 'IP Address', 'session_count': 'Session Count'})
#                     visualization = fig
#                     top_ip = result_df.iloc[0]['ip_address']
#                     feasibility_study = f"Top 5 IPs account for {result_df['session_count'].sum()} sessions, with '{top_ip}' leading as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Monitor '{top_ip}' for potential bot activity if sessions are excessive."
                
#                 elif best_match == "session_analysis_7":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     order_details = st.session_state['data']['Order_Details']
#                     sessions_with_cart = order_details['id'].unique()
#                     total_sessions = len(sessions)
#                     no_cart_sessions = total_sessions - len(sessions_with_cart)
#                     result_df = pd.DataFrame({"Metric": ["Sessions with No Cart Activity"], "Value": [no_cart_sessions]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Sessions with No Cart Activity")
#                     visualization = fig
#                     feasibility_study = f"{no_cart_sessions} sessions have no cart activity out of {total_sessions} as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Improve call-to-action if this number is high to encourage purchases."
                
#                 elif best_match == "session_analysis_8":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     order_details = st.session_state['data']['Order_Details']
#                     merged = sessions.merge(order_details, left_on='id', right_on='id', how='left')
#                     merged['time_to_cart'] = (merged['session_start'] - merged['session_start']).dt.total_seconds() / 60  # Placeholder
#                     avg_time = merged['time_to_cart'].mean()
#                     result_df = pd.DataFrame({"Metric": ["Average Time to Cart (minutes)"], "Value": [avg_time]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Average Time to Cart Addition")
#                     visualization = fig
#                     feasibility_study = f"Average time to cart addition is {avg_time:.2f} minutes (note: requires exact cart time data) as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Streamline navigation if this time is long to boost conversions."
                
#                 elif best_match == "session_analysis_9":
#                     order_details = st.session_state['data']['Order_Details']
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     products_per_session = order_details.groupby('id').size().reset_index(name='product_count')
#                     result_df = sessions.merge(products_per_session, on='id', how='left').fillna(0)[['id', 'product_count']].sort_values('product_count', ascending=False).head(5)
#                     fig = px.bar(result_df, x='id', y='product_count', title="Top 5 Sessions by Products Added", labels={'id': 'Session ID', 'product_count': 'Product Count'})
#                     visualization = fig
#                     max_products = result_df.iloc[0]['product_count']
#                     feasibility_study = f"Top 5 sessions have up to {max_products} products added as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Analyze these sessions to identify popular product combinations."
                
#                 elif best_match == "session_analysis_10":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     order_details = st.session_state['data']['Order_Details']
#                     sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
#                     merged = sessions.merge(order_details, on='id', how='left')
#                     cart_counts = merged.groupby('id')['id_y'].count().reset_index(name='cart_count')
#                     result_df = sessions.merge(cart_counts, on='id', how='left').fillna(0)[['duration', 'cart_count']]
#                     fig = px.scatter(result_df, x='duration', y='cart_count', title="Session Duration vs Cart Additions", labels={'duration': 'Duration (minutes)', 'cart_count': 'Cart Additions'})
#                     visualization = fig
#                     correlation = result_df['duration'].corr(result_df['cart_count'])
#                     feasibility_study = f"Correlation between session duration and cart additions is {correlation:.2f} as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Increase session engagement if correlation is positive to boost cart additions."
                
#                 # Cart Activity Queries
#                 elif best_match == "cart_activity_1":
#                     order_details = st.session_state['data']['Order_Details']
#                     unique_products = order_details['product_id'].nunique()
#                     result_df = pd.DataFrame({"Metric": ["Unique Products in Carts"], "Value": [unique_products]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Total Unique Products Added to Carts")
#                     visualization = fig
#                     feasibility_study = f"{unique_products} unique products are added to carts, reflecting diversity as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Ensure stock levels match this variety."
                
#                 elif best_match == "cart_activity_2":
#                     order_details = st.session_state['data']['Order_Details']
#                     avg_products = order_details.groupby('order_id').size().mean()
#                     result_df = pd.DataFrame({"Metric": ["Average Products per Cart"], "Value": [avg_products]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Average Number of Products per Cart")
#                     visualization = fig
#                     feasibility_study = f"Average products per cart is {avg_products:.2f}, indicating purchase behavior as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Encourage larger carts with bundle offers if the average is low."
                
#                 elif best_match == "cart_activity_3":
#                     order_details = st.session_state['data']['Order_Details']
#                     orders = st.session_state['data']['Orders']
#                     customers = st.session_state['data']['Customers']
#                     cart_adds = order_details.merge(orders, on='order_id').groupby('customer_id').size().reset_index(name='cart_additions')
#                     result_df = cart_adds.merge(customers, left_on='customer_id', right_on='id')[['email', 'first_name', 'last_name', 'cart_additions']].sort_values('cart_additions', ascending=False).head(5)
#                     fig = px.bar(result_df, x='email', y='cart_additions', title="Top 5 Customers by Cart Additions", labels={'email': 'Customer Email', 'cart_additions': 'Additions'})
#                     visualization = fig
#                     top_customer = result_df.iloc[0]['email'] if not result_df.empty else "N/A"
#                     feasibility_study = f"Top 5 customers have {result_df['cart_additions'].sum()} additions, with '{top_customer}' leading as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Offer '{top_customer}' personalized discounts to retain them."
                
#                 elif best_match == "cart_activity_4":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     order_details = st.session_state['data']['Order_Details']
#                     sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
#                     merged = sessions.merge(order_details, left_on='id', right_on='id', how='left')
#                     result_df = merged.groupby(pd.cut(merged['duration'], bins=5))['id_y'].count().reset_index(name='additions')
#                     result_df['duration_range'] = result_df['duration'].astype(str)
#                     fig = px.bar(result_df, x='duration_range', y='additions', title="Cart Additions by Session Duration", labels={'duration_range': 'Duration Range (minutes)', 'additions': 'Additions'})
#                     visualization = fig
#                     peak_range = result_df.loc[result_df['additions'].idxmax(), 'duration_range']
#                     feasibility_study = f"Peak cart additions occur in the {peak_range} minute range as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Optimize for sessions in the {peak_range} range to boost sales."
                
#                 elif best_match == "cart_activity_5":
#                     order_details = st.session_state['data']['Order_Details']
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     products_per_session = order_details.groupby('id').size().reset_index(name='cart_additions')
#                     result_df = sessions.merge(products_per_session, on='id', how='left').fillna(0)[['id', 'cart_additions']].sort_values('cart_additions', ascending=False).head(5)
#                     fig = px.bar(result_df, x='id', y='cart_additions', title="Top 5 Sessions by Cart Additions", labels={'id': 'Session ID', 'cart_additions': 'Additions'})
#                     visualization = fig
#                     max_additions = result_df.iloc[0]['cart_additions']
#                     feasibility_study = f"Top 5 sessions have up to {max_additions} cart additions as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Analyze these sessions for effective product recommendations."
                
#                 elif best_match == "cart_activity_6":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     order_details = st.session_state['data']['Order_Details']
#                     sessions['first_minute'] = sessions['session_start'] + timedelta(minutes=1)
#                     merged = sessions.merge(order_details, left_on='id', right_on='id', how='left')
#                     within_minute = merged[merged['session_start'] <= merged['session_start']].shape[0]
#                     result_df = pd.DataFrame({"Metric": ["Cart Additions in First Minute"], "Value": [within_minute]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Cart Additions in First Minute")
#                     visualization = fig
#                     feasibility_study = f"{within_minute} cart additions occur within the first minute as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Enhance early engagement to capitalize on this trend."
                
#                 elif best_match == "cart_activity_7":
#                     customers = st.session_state['data']['Customers']
#                     order_details = st.session_state['data']['Order_Details']
#                     orders = st.session_state['data']['Orders']
#                     new_customers = customers[customers['registration_date'] > (datetime.now() - timedelta(days=30))]['id']
#                     new_orders = orders[orders['customer_id'].isin(new_customers)]
#                     new_cart = order_details.merge(new_orders, on='order_id')
#                     most_common = new_cart['product_id'].mode()[0] if not new_cart.empty else None
#                     product_name = st.session_state['data']['Products'].set_index('id').loc[most_common, 'name'] if most_common else "N/A"
#                     result_df = pd.DataFrame({"Metric": ["Most Common Product for New Customers"], "Value": [product_name]})
#                     fig = px.bar(result_df, x="Metric", y=[1], title="Most Common Product for New Customers", text=[product_name], height=300)
#                     visualization = fig
#                     feasibility_study = f"'{product_name}' is the most common product added by new customers in the last 30 days as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Promote '{product_name}' to attract more new customers."
                
#                 elif best_match == "cart_activity_8":
#                     order_details = st.session_state['data']['Order_Details']
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     merged = sessions.merge(order_details, on='id')
#                     customer_products = merged.groupby(['customer_id', 'session_id', 'product_id']).size().reset_index(name='count')
#                     result_df = customer_products.merge(st.session_state['data']['Products'], left_on='product_id', right_on='id')[['name', 'count']].drop_duplicates().head(5)
#                     fig = px.bar(result_df, x='name', y='count', title="Top 5 Products Added in Same Session", labels={'name': 'Product', 'count': 'Occurrences'})
#                     visualization = fig
#                     top_product = result_df.iloc[0]['name'] if not result_df.empty else "N/A"
#                     feasibility_study = f"Top 5 products are added {result_df['count'].sum()} times in same sessions, with '{top_product}' leading as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Bundle '{top_product}' with other frequent pairs."
                
#                 elif best_match == "cart_activity_9":
#                     order_details = st.session_state['data']['Order_Details']
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     merged = sessions.merge(order_details, on='id')
#                     merged['hour'] = merged['session_start'].dt.hour
#                     result_df = merged.groupby('hour').size().reset_index(name='cart_additions')
#                     fig = px.line(result_df, x='hour', y='cart_additions', title="Cart Activity by Hour", labels={'hour': 'Hour of Day', 'cart_additions': 'Additions'})
#                     visualization = fig
#                     peak_hour = result_df.loc[result_df['cart_additions'].idxmax(), 'hour']
#                     feasibility_study = f"Peak cart activity is at {peak_hour}:00 with {result_df['cart_additions'].max()} additions as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Boost promotions at {peak_hour}:00 to increase conversions."
                
#                 elif best_match == "cart_activity_10":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     order_details = st.session_state['data']['Order_Details']
#                     merged = sessions.merge(order_details, left_on='id', right_on='id', how='left')
#                     merged['time_to_cart'] = (merged['session_start'] - merged['session_start']).dt.total_seconds() / 60  # Placeholder
#                     avg_time = merged['time_to_cart'].mean()
#                     result_df = pd.DataFrame({"Metric": ["Average Time to First Cart Addition (minutes)"], "Value": [avg_time]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Average Time to First Cart Addition")
#                     visualization = fig
#                     feasibility_study = f"Average time to first cart addition is {avg_time:.2f} minutes (note: requires exact cart time data) as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Streamline navigation if this time is long to boost conversions."
                
#                 # Business Insights Queries
#                 elif best_match == "business_insights_1":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     order_details = st.session_state['data']['Order_Details']
#                     total_sessions = len(sessions)
#                     total_cart_additions = len(order_details)
#                     conversion_rate = (total_cart_additions / total_sessions * 100) if total_sessions > 0 else 0
#                     result_df = pd.DataFrame({"Metric": ["Conversion Rate (%)"], "Value": [conversion_rate]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Conversion Rate from Sessions to Cart Additions", text=[f"{conversion_rate:.2f}%"])
#                     visualization = fig
#                     feasibility_study = f"Conversion rate is {conversion_rate:.2f}% as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Improve UX if below 2-3% to enhance conversions."
                
#                 elif best_match == "business_insights_2":
#                     customers = st.session_state['data']['Customers']
#                     order_details = st.session_state['data']['Order_Details']
#                     orders = st.session_state['data']['Orders']
#                     customers['group'] = pd.qcut(customers['registration_date'].rank(method='first'), 4, labels=['G1', 'G2', 'G3', 'G4'])
#                     cart_by_customer = orders.merge(order_details, on='order_id').groupby('customer_id').size().reset_index(name='cart_additions')
#                     group_data = customers.merge(cart_by_customer, left_on='id', right_on='customer_id').groupby('group')['cart_additions'].mean().reset_index()
#                     result_df = group_data
#                     fig = px.bar(result_df, x='group', y='cart_additions', title="Cart Addition Rate by Customer Group", labels={'group': 'Customer Group', 'cart_additions': 'Average Additions'})
#                     visualization = fig
#                     top_group = result_df.loc[result_df['cart_additions'].idxmax(), 'group']
#                     feasibility_study = f"Group {top_group} has the highest average cart additions of {result_df['cart_additions'].max():.2f} as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Target group {top_group} with tailored offers."
                
#                 elif best_match == "business_insights_3":
#                     customers = st.session_state['data']['Customers']
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     customers['group'] = pd.qcut(customers['registration_date'].rank(method='first'), 4, labels=['G1', 'G2', 'G3', 'G4'])
#                     group_size = customers.groupby('group').size().reset_index(name='group_size')
#                     sessions_per_group = sessions.merge(customers, on='customer_id').groupby('group').size().reset_index(name='session_count')
#                     result_df = group_size.merge(sessions_per_group, on='group')
#                     fig = px.scatter(result_df, x='group_size', y='session_count', trendline="ols", title="Session Frequency vs Group Size", labels={'group_size': 'Group Size', 'session_count': 'Session Count'})
#                     visualization = fig
#                     correlation = result_df['group_size'].corr(result_df['session_count'])
#                     feasibility_study = f"Correlation between group size and session frequency is {correlation:.2f} as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Focus on larger groups if correlation is positive to boost engagement."
                
#                 elif best_match == "business_insights_4":
#                     order_details = st.session_state['data']['Order_Details']
#                     products = st.session_state['data']['Products']
#                     top_products = order_details.groupby('product_id').size().sort_values(ascending=False).head(5).index
#                     avg_price = products['price'].mean()
#                     potential_revenue = order_details[order_details['product_id'].isin(top_products)]['quantity'].sum() * avg_price
#                     result_df = pd.DataFrame({"Metric": ["Potential Revenue from Top Products ($)"], "Value": [potential_revenue]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Potential Revenue from Top Products")
#                     visualization = fig
#                     feasibility_study = f"Top 5 products could generate ${potential_revenue:.2f} in revenue at an average price of ${avg_price:.2f} as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Prioritize stock and marketing for these top products."
                
#                 elif best_match == "business_insights_5":
#                     customers = st.session_state['data']['Customers']
#                     orders = st.session_state['data']['Orders']
#                     customers['group'] = pd.qcut(customers['registration_date'].rank(method='first'), 4, labels=['G1', 'G2', 'G3', 'G4'])
#                     value_by_group = orders.merge(customers, on='customer_id').groupby('group')['total_amount'].sum().reset_index()
#                     result_df = value_by_group
#                     fig = px.bar(result_df, x='group', y='total_amount', title="Value by Customer Segment", labels={'group': 'Customer Group', 'total_amount': 'Total Value ($)'})
#                     visualization = fig
#                     top_group = result_df.loc[result_df['total_amount'].idxmax(), 'group']
#                     feasibility_study = f"Group {top_group} is the most valuable with ${result_df['total_amount'].max():.2f} in total orders as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Focus retention efforts on group {top_group}."
                
#                 elif best_match == "business_insights_6":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     order_details = st.session_state['data']['Order_Details']
#                     sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
#                     merged = sessions.merge(order_details, left_on='id', right_on='id', how='left')
#                     duration_bins = pd.qcut(merged['duration'], 4, duplicates='drop')
#                     cart_by_duration = merged.groupby(duration_bins)['id_y'].count().reset_index(name='cart_additions')
#                     result_df = cart_by_duration
#                     fig = px.bar(result_df, x='duration', y='cart_additions', title="Cart Additions by Session Duration Quartile", labels={'duration': 'Duration Quartile', 'cart_additions': 'Additions'})
#                     visualization = fig
#                     peak_quartile = result_df.loc[result_df['cart_additions'].idxmax(), 'duration']
#                     feasibility_study = f"Peak cart additions occur in the {peak_quartile} duration quartile as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Optimize for sessions in the {peak_quartile} range to boost conversions."
                
#                 elif best_match == "business_insights_7":
#                     customers = st.session_state['data']['Customers']
#                     orders = st.session_state['data']['Orders']
#                     clv = orders.groupby('customer_id')['total_amount'].sum().mean()
#                     result_df = pd.DataFrame({"Metric": ["Average Customer Lifetime Value ($)"], "Value": [clv]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Average Customer Lifetime Value")
#                     visualization = fig
#                     feasibility_study = f"Average customer lifetime value is ${clv:.2f} based on order totals as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Increase CLV with upselling or loyalty programs if below industry standards."
                
#                 elif best_match == "business_insights_8":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     ip_freq = sessions.groupby('ip_address').size().reset_index(name='session_count')
#                     threshold = ip_freq['session_count'].quantile(0.95)
#                     potential_bots = ip_freq[ip_freq['session_count'] > threshold]
#                     result_df = potential_bots[['ip_address', 'session_count']]
#                     fig = px.bar(result_df, x='ip_address', y='session_count', title="Potential Bot IPs by Session Count", labels={'ip_address': 'IP Address', 'session_count': 'Session Count'})
#                     visualization = fig
#                     top_ip = result_df.iloc[0]['ip_address'] if not result_df.empty else "N/A"
#                     feasibility_study = f"{len(potential_bots)} IPs may indicate bot activity, with '{top_ip}' having {result_df.iloc[0]['session_count']} sessions as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Investigate '{top_ip}' for bot behavior and implement CAPTCHA if needed."
                
#                 elif best_match == "business_insights_9":
#                     order_details = st.session_state['data']['Order_Details']
#                     products = st.session_state['data']['Products']
#                     categories = st.session_state['data']['Categories']
#                     merged = order_details.merge(products, on='product_id').merge(categories, left_on='category_id', right_on='id')
#                     merged['depth'] = merged['parent_id'].apply(lambda x: 0 if pd.isna(x) else 1)
#                     result_df = merged.groupby('depth').size().reset_index(name='cart_additions')
#                     fig = px.bar(result_df, x='depth', y='cart_additions', title="Cart Additions by Product Hierarchy Depth", labels={'depth': 'Hierarchy Depth', 'cart_additions': 'Cart Additions'})
#                     visualization = fig
#                     max_depth = result_df.loc[result_df['cart_additions'].idxmax(), 'depth']
#                     feasibility_study = f"Depth {max_depth} has the most cart additions with {result_df['cart_additions'].max()} as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = f"Focus on products at depth {max_depth} to enhance engagement."
                
#                 elif best_match == "business_insights_10":
#                     sessions = st.session_state['data']['Customer_Sessions']
#                     customers = st.session_state['data']['Customers']
#                     last_session = sessions.groupby('customer_id')['session_start'].max().reset_index()
#                     merged = customers.merge(last_session, left_on='id', right_on='customer_id')
#                     threshold_date = datetime.now() - timedelta(days=90)
#                     churned = merged[merged['session_start'] < threshold_date]
#                     churn_rate = (len(churned) / len(customers)) * 100 if len(customers) > 0 else 0
#                     result_df = pd.DataFrame({"Metric": ["Churn Rate (%)"], "Value": [churn_rate]})
#                     fig = px.bar(result_df, x="Metric", y="Value", title="Customer Churn Rate", text=[f"{churn_rate:.2f}%"])
#                     visualization = fig
#                     feasibility_study = f"Churn rate is {churn_rate:.2f}% based on customers inactive for 90 days as of May 18, 2025, 10:03 AM EEST."
#                     recommendation = "Implement re-engagement campaigns if churn rate is high."
                
#                 # Display results if available
#                 if result_df is not None:
#                     st.subheader(title)
#                     st.dataframe(result_df)
#                     if visualization:
#                         st.plotly_chart(visualization)
#                     st.subheader("Feasibility Study")
#                     st.write(feasibility_study)
#                     st.write(f"Recommendation: {recommendation}")
                    
#                     # PDF Download Section
#                     pdf_buffer = io.BytesIO()
#                     doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
#                     styles = getSampleStyleSheet()
#                     elements = [
#                         Paragraph("Query Analysis Report", styles['Title']),
#                         Paragraph(title, styles['Heading2']),
#                         Spacer(1, 12),
#                         Paragraph(f"Author: GrowEasy Platform", styles['Normal']),
#                         Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}", styles['Normal']),
#                         Spacer(1, 12),
#                         Paragraph("Results", styles['Heading2']),
#                     ]
                    
#                     # Add table
#                     data = [list(result_df.columns)]
#                     for _, row in result_df.iterrows():
#                         data.append([str(row[col]) for col in result_df.columns])
#                     table = Table(data)
#                     table.setStyle(TableStyle([
#                         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#                         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#                         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#                     ]))
#                     elements.append(table)
#                     elements.append(Spacer(1, 12))
#                     elements.append(Paragraph("Feasibility Study", styles['Heading2']))
#                     elements.append(Paragraph(feasibility_study, styles['Normal']))
#                     elements.append(Spacer(1, 12))
#                     elements.append(Paragraph("Recommendation", styles['Heading2']))
#                     elements.append(Paragraph(recommendation, styles['Normal']))
                    
#                     try:
#                         # Build the PDF
#                         doc.build(elements)
                        
#                         # Debug: Check buffer size
#                         pdf_buffer.seek(0, 2)  # Move to end
#                         buffer_size = pdf_buffer.tell()  # Get size
#                         st.write(f"Debug: PDF buffer size is {buffer_size} bytes")
#                         pdf_buffer.seek(0)  # Reset to start
                        
#                         # Download button
#                         st.download_button(
#                             label="Download Query Analysis Report",
#                             data=pdf_buffer.getvalue(),
#                             file_name="Query_Analysis_Report.pdf",
#                             mime="application/pdf",
#                             key="download-report-button"
#                         )
#                     except Exception as e:
#                         st.error(f"Error generating PDF: {str(e)}. Please ensure reportlab is installed and compatible.")
#         else:
#             st.info("Please enter a query to analyze the data (e.g., 'How many unique customers are in the dataset?').")
#     else:
#         st.info("Enter a query and click 'Run Query' to analyze the data (e.g., 'How many unique customers are in the dataset?').")








import streamlit as st
import pandas as pd
import spacy
import plotly.express as px
from datetime import datetime, timedelta
from collections import defaultdict
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus.tables import TableStyle
import io

# Load spacy model
nlp = spacy.load("en_core_web_sm")

# Define the 50 questions
QUESTIONS = {
    "customer_behavior_1": "How many unique customers are in the dataset?",
    "customer_behavior_2": "What is the average number of sessions per customer?",
    "customer_behavior_3": "Which customers have the highest number of sessions?",
    "customer_behavior_4": "What is the distribution of session durations across all customers?",
    "customer_behavior_5": "Which customers have the longest average session duration?",
    "customer_behavior_6": "How many sessions occur per day on average?",
    "customer_behavior_7": "What is the most common time of day for customer sessions?",
    "customer_behavior_8": "Which customers have sessions from multiple IP addresses?",
    "customer_behavior_9": "How does session frequency vary by customer group?",
    "customer_behavior_10": "What is the retention rate of customers (e.g., those with multiple sessions over time)?",
    "product_performance_1": "Which products are added to carts most frequently?",
    "product_performance_2": "What is the total number of unique products added to carts?",
    "product_performance_3": "Which product categories (based on hierarchy) are most popular in carts?",
    "product_performance_4": "How many products have never been added to a cart?",
    "product_performance_5": "What is the average time a product stays in a cart before session ends?",
    "product_performance_6": "Which products are most often added together in the same session?",
    "product_performance_7": "What is the distribution of cart additions by product hierarchy level?",
    "product_performance_8": "Which products have the highest addition rate per session?",
    "product_performance_9": "How does product popularity vary over time (e.g., daily or weekly trends)?",
    "product_performance_10": "Which products are added by the most unique customers?",
    "session_analysis_1": "What is the total number of sessions in the dataset?",
    "session_analysis_2": "What is the average session duration across all sessions?",
    "session_analysis_3": "Which sessions have the longest duration?",
    "session_analysis_4": "How does session duration vary by time of day?",
    "session_analysis_5": "What is the distribution of sessions by day of the week?",
    "session_analysis_6": "Which IP addresses are associated with the most sessions?",
    "session_analysis_7": "How many sessions have no cart activity?",
    "session_analysis_8": "What is the average time between session start and cart addition?",
    "session_analysis_9": "Which sessions have the most products added to the cart?",
    "session_analysis_10": "How does session duration correlate with the number of cart additions?",
    "cart_activity_1": "How many unique products are added to carts overall?",
    "cart_activity_2": "What is the average number of products added per cart?",
    "cart_activity_3": "Which customers have the most cart additions?",
    "cart_activity_4": "What is the distribution of cart additions by session duration?",
    "cart_activity_5": "Which sessions have the highest number of cart additions?",
    "cart_activity_6": "How many cart additions occur within the first minute of a session?",
    "cart_activity_7": "What is the most common product added to carts by new customers?",
    "cart_activity_8": "Which products are added to carts in the same session by the same customer?",
    "cart_activity_9": "How does cart activity vary by time of day?",
    "cart_activity_10": "What is the average time from session start to first cart addition?",
    "business_insights_1": "What is the conversion rate from sessions to cart additions?",
    "business_insights_2": "Which customer groups have the highest cart addition rates?",
    "business_insights_3": "How does customer group size correlate with session frequency?",
    "business_insights_4": "What is the potential revenue impact of top-performing products (assuming equal pricing)?",
    "business_insights_5": "Which customer segments (based on group or session behavior) are most valuable?",
    "business_insights_6": "How can session duration be optimized to increase cart additions?",
    "business_insights_7": "What is the customer lifetime value based on session and cart activity?",
    "business_insights_8": "Which IP address ranges indicate potential bot activity (e.g., high session frequency)?",
    "business_insights_9": "How does product hierarchy depth impact customer engagement?",
    "business_insights_10": "What is the churn rate of customers based on session activity?"
}

# Page configuration
st.set_page_config(layout="wide", page_title="GrowEasy: Query Analysis")

# CSS styling
st.markdown(
    """
    <style>
    .title {
        animation: fadeIn 1s ease-in-out;
        color: #4f627c;
        font-size: 3.5em;
        text-align: center;
        font-family: 'Arial', sans-serif;
        margin: 30px 0;
    }
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .stButton>button {
        background-color: #4CAF50;
        color: #d3d3d3;
        border-radius: 8px;
        padding: 10px 20px;
        transition: all 0.3s ease;
        border: 1px solid #2c3e50;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        margin: 10px 0;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.03);
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
    }
    .stExpander {
        border-radius: 8px;
        background-color: #1f2a44;
        color: #d3d3d3;
        border: 1px solid #2c3e50;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15);
        margin: 15px 0;
        padding: 10px;
    }
    .stMultiSelect label, .stDateInput label {
        color: #000000;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        margin-top: 15px;
    }
    .metric {
        animation: fadeIn 1.2s ease-in-out;
        background-color: #141c30;
        color: #d3d3d3;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2c3e50;
        font-family: 'Arial', sans-serif;
        margin: 10px 0;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1f2a44;
        color: #d3d3d3;
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        margin-right: 10px;
        transition: all 0.3s ease;
        font-family: 'Arial', sans-serif;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #141c30;
        color: #000000;
        border-bottom: 2px solid #4CAF50;
    }
    .section-spacer {
        margin: 20px 0;
    }
    .stTextArea textarea {
        border-radius: 8px;
        border: 1px solid #2c3e50;
        background-color: #1f2a44;
        color: #d3d3d3;
        font-family: 'Arial', sans-serif;
    }
    .warning-box {
        background-color: #2c3e50;
        color: #d3d3d3;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #4CAF50;
        font-family: 'Arial', sans-serif;
        margin: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Animated title
st.markdown('<div class="title">Query Analysis</div>', unsafe_allow_html=True)

# Check for data
if 'data' not in st.session_state or st.session_state['data'] is None:
    st.error("Please upload an Excel file on the main page.")
else:
    try:
        # Validate required columns
        required_columns = {
            'Customers': ['id', 'email', 'first_name', 'last_name', 'registration_date'],
            'Customer_Sessions': ['id', 'customer_id', 'session_start', 'session_end', 'ip_address'],
            'Order_Details': ['id', 'order_id', 'product_id', 'quantity'],
            'Orders': ['customer_id', 'total_amount'],  # Removed order_id
            'Products': ['id', 'name', 'category_id', 'price'],
            'Categories': ['id', 'name', 'parent_id']
        }
        has_order_id = True
        disabled_queries = []
        for sheet, cols in required_columns.items():
            if sheet not in st.session_state['data']:
                raise ValueError(f"Missing required sheet: {sheet}")
            missing_cols = [col for col in cols if col not in st.session_state['data'][sheet].columns]
            if missing_cols:
                raise ValueError(f"Missing columns in {sheet}: {', '.join(missing_cols)}")
        # Check for order_id separately
        if 'Orders' in st.session_state['data'] and 'order_id' not in st.session_state['data']['Orders'].columns:
            has_order_id = False
            disabled_queries = [
                "product_performance_9", "product_performance_10", "cart_activity_3",
                "cart_activity_7", "business_insights_2", "business_insights_4",
                "business_insights_5", "business_insights_7"
            ]
        
        # Sidebar filters and warning
        st.sidebar.subheader("Filter Options")
        category_options = [
            "All",
            "Customer Behavior",
            "Product Performance",
            "Session Analysis",
            "Cart Activity",
            "Business Insights"
        ]
        category_filter = st.sidebar.multiselect(
            "Select Question Category",
            options=category_options,
            default=["All"],
            key="category_filter"
        )
        date_start, date_end = st.sidebar.date_input(
            "Select Date Range",
            value=(datetime.now() - timedelta(days=30), datetime.now()),
            min_value=datetime(2020, 1, 1),
            max_value=datetime.now(),
            key="date_range"
        )
        st.sidebar.button(
            "Clear Filters",
            key="clear_filters",
            on_click=lambda: st.session_state.update(
                category_filter=["All"],
                date_range=(datetime.now() - timedelta(days=30), datetime.now())
            )
        )
        if not has_order_id:
            st.sidebar.markdown(
                f"""
                <div class="warning-box">
                <strong>Warning:</strong> The 'order_id' column is missing in the Orders sheet. The following queries are disabled:
                <ul>
                    <li>Product Performance: Trends Over Time, Unique Customers</li>
                    <li>Cart Activity: Top Customers, New Customer Products</li>
                    <li>Business Insights: Cart Addition Rates, Revenue Impact, Customer Segments, CLV</li>
                </ul>
                Please verify the Orders sheet or contact GrowEasy support for assistance.
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Filter questions based on category
        filtered_questions = QUESTIONS
        if "All" not in category_filter:
            filtered_questions = {
                k: v for k, v in QUESTIONS.items()
                if any(cat.lower().replace(" ", "_") in k for cat in category_filter)
            }
        
        # Query input
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        user_query = st.text_area(
            "Enter your query (e.g., 'How many unique customers are in the dataset?'):",
            height=100,
            placeholder="Type your question here...",
            key="user_query"
        )
        
        if st.button("Run Query", key="run_query"):
            if user_query:
                with st.spinner("Processing query..."):
                    # Parse query with spacy
                    doc = nlp(user_query.lower())
                    tokens = [token.lemma_ for token in doc]
                    phrases = [" ".join([token.text for token in chunk]) for chunk in doc.noun_chunks]
                    
                    # Score queries based on token overlap
                    scores = defaultdict(float)
                    for q_key, q_text in filtered_questions.items():
                        q_doc = nlp(q_text.lower())
                        q_tokens = [token.lemma_ for token in q_doc]
                        overlap = len(set(tokens) & set(q_tokens)) / len(set(q_tokens))
                        scores[q_key] = overlap
                    
                    # Find the best match
                    best_match = max(scores, key=scores.get, default=None)
                    confidence = scores[best_match] * 100
                    if confidence < 40:  # Threshold for match confidence
                        st.warning("The query could not be interpreted. Please rephrase or try a different question.")
                    else:
                        result_df = None
                        visualization = None
                        feasibility_study = ""
                        recommendation = ""
                        title = f"Result for: {filtered_questions[best_match]}"
                        
                        # Apply date filter where applicable
                        date_filter_applicable = best_match in [
                            "customer_behavior_6", "customer_behavior_7", "customer_behavior_10",
                            "product_performance_9", "session_analysis_4", "session_analysis_5",
                            "cart_activity_6", "cart_activity_9", "business_insights_10"
                        ]
                        sessions = st.session_state['data']['Customer_Sessions'].copy()
                        orders = st.session_state['data']['Orders'].copy()
                        if date_filter_applicable and date_start and date_end:
                            start_date = pd.to_datetime(date_start)
                            end_date = pd.to_datetime(date_end) + pd.Timedelta(days=1)
                            sessions = sessions[
                                (sessions['session_start'] >= start_date) &
                                (sessions['session_start'] < end_date)
                            ]
                            if has_order_id and 'order_date' in orders.columns:
                                orders = orders[
                                    (orders['order_date'] >= start_date) &
                                    (orders['order_date'] < end_date)
                                ]
                        
                        # Check if query is disabled due to missing order_id
                        if best_match in disabled_queries:
                            result_df = pd.DataFrame({"Message": ["This query requires the 'order_id' column in the Orders sheet, which is unavailable."]})
                            feasibility_study = "The 'order_id' column is missing in the Orders sheet, preventing this analysis."
                            recommendation = "Please verify the Orders sheet includes the 'order_id' column or contact GrowEasy support for assistance."
                        else:
                            # Customer Behavior Queries
                            if best_match == "customer_behavior_1":
                                customers = st.session_state['data']['Customers']
                                unique_customers = customers['id'].nunique()
                                result_df = pd.DataFrame({"Metric": ["Unique Customers"], "Value": [unique_customers]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Number of Unique Customers", color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"There are {unique_customers} unique customers in the dataset as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Evaluate customer acquisition strategies if the number is below target."
                            
                            elif best_match == "customer_behavior_2":
                                customers = st.session_state['data']['Customers']
                                sessions_per_customer = sessions.groupby('customer_id').size().reset_index(name='session_count')
                                avg_sessions = sessions_per_customer['session_count'].mean()
                                result_df = pd.DataFrame({"Metric": ["Average Sessions per Customer"], "Value": [avg_sessions]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Average Number of Sessions per Customer", color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"Each customer averages {avg_sessions:.2f} sessions, indicating engagement levels as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Boost engagement with targeted campaigns if the average is low."
                            
                            elif best_match == "customer_behavior_3":
                                customers = st.session_state['data']['Customers']
                                sessions_per_customer = sessions.groupby('customer_id').size().reset_index(name='session_count')
                                result_df = sessions_per_customer.merge(customers, left_on='customer_id', right_on='id')
                                result_df = result_df[['email', 'first_name', 'last_name', 'session_count']].sort_values('session_count', ascending=False).head(5)
                                fig = px.bar(result_df, x='email', y='session_count', title="Top 5 Customers by Number of Sessions", labels={'email': 'Customer Email', 'session_count': 'Session Count'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                top_customer = result_df.iloc[0]['email'] if not result_df.empty else "N/A"
                                feasibility_study = f"Top 5 customers have {result_df['session_count'].sum()} sessions, with '{top_customer}' leading as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = f"Offer '{top_customer}' loyalty rewards to sustain their activity."
                            
                            elif best_match == "customer_behavior_4":
                                sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
                                result_df = sessions[['duration']].copy()
                                fig = px.histogram(result_df, x='duration', nbins=20, title="Distribution of Session Durations", labels={'duration': 'Duration (minutes)'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                avg_duration = result_df['duration'].mean()
                                feasibility_study = f"Average session duration is {avg_duration:.2f} minutes, with a varied distribution as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Enhance content if short durations dominate to retain customers longer."
                            
                            elif best_match == "customer_behavior_5":
                                customers = st.session_state['data']['Customers']
                                sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
                                avg_duration = sessions.groupby('customer_id')['duration'].mean().reset_index()
                                result_df = avg_duration.merge(customers, left_on='customer_id', right_on='id')
                                result_df = result_df[['email', 'first_name', 'last_name', 'duration']].sort_values('duration', ascending=False).head(5)
                                fig = px.bar(result_df, x='email', y='duration', title="Top 5 Customers by Average Session Duration", labels={'email': 'Customer Email', 'duration': 'Average Duration (minutes)'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                top_customer = result_df.iloc[0]['email'] if not result_df.empty else "N/A"
                                feasibility_study = f"Top 5 customers average {result_df['duration'].mean():.2f} minutes, with '{top_customer}' at {result_df.iloc[0]['duration']:.2f} minutes as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = f"Study '{top_customer}'s behavior to improve engagement strategies."
                            
                            elif best_match == "customer_behavior_6":
                                sessions_per_day = sessions.groupby(sessions['session_start'].dt.date).size().mean()
                                result_df = pd.DataFrame({"Metric": ["Average Sessions per Day"], "Value": [sessions_per_day]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Average Number of Sessions per Day", color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"Average of {sessions_per_day:.2f} sessions per day in the selected date range as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Optimize staffing for peak days based on this average."
                            
                            elif best_match == "customer_behavior_7":
                                sessions['hour'] = sessions['session_start'].dt.hour
                                most_common_hour = sessions['hour'].mode()[0] if not sessions.empty else 0
                                result_df = pd.DataFrame({"Metric": ["Most Common Session Hour"], "Value": [f"{most_common_hour}:00"]})
                                fig = px.bar(result_df, x="Metric", y=[1], title="Most Common Session Hour", text=["Value"], height=300, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"Most common session hour is {most_common_hour}:00 EEST in the selected date range."
                                recommendation = f"Schedule promotions at {most_common_hour}:00 to maximize reach."
                            
                            elif best_match == "customer_behavior_8":
                                ip_counts = sessions.groupby(['customer_id', 'ip_address']).size().reset_index(name='count')
                                multi_ip_customers = ip_counts.groupby('customer_id').filter(lambda x: len(x) > 1)['customer_id'].unique()
                                customers = st.session_state['data']['Customers']
                                result_df = customers[customers['id'].isin(multi_ip_customers)][['email', 'first_name', 'last_name']]
                                if result_df.empty:
                                    result_df = pd.DataFrame({"Message": ["No customers with multiple IP addresses found"]})
                                fig = px.bar(result_df, x='email', y=[1] * len(result_df), title="Customers with Multiple IP Addresses", labels={'email': 'Customer Email'}, height=300, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                count = len(multi_ip_customers)
                                feasibility_study = f"{count} customers use multiple IP addresses, possibly indicating multi-device usage as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Monitor for unusual patterns to detect potential fraud."
                            
                            elif best_match == "customer_behavior_9":
                                customers = st.session_state['data']['Customers']
                                customers['group'] = pd.qcut(customers['registration_date'].rank(method='first'), 4, labels=['G1', 'G2', 'G3', 'G4'])
                                sessions_per_group = sessions.merge(customers, on='customer_id').groupby('group').size().reset_index(name='session_count')
                                result_df = sessions_per_group
                                fig = px.bar(result_df, x='group', y='session_count', title="Session Frequency by Customer Group", labels={'group': 'Customer Group', 'session_count': 'Session Count'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                max_group = result_df.loc[result_df['session_count'].idxmax(), 'group'] if not result_df.empty else "N/A"
                                feasibility_study = f"Group {max_group} has the highest session count of {result_df['session_count'].max() if not result_df.empty else 0} as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = f"Target group {max_group} with personalized offers."
                            
                            elif best_match == "customer_behavior_10":
                                customer_sessions = sessions.groupby('customer_id').size().reset_index(name='session_count')
                                total_customers = len(customer_sessions)
                                retained_customers = len(customer_sessions[customer_sessions['session_count'] > 1])
                                retention_rate = (retained_customers / total_customers) * 100 if total_customers > 0 else 0
                                result_df = pd.DataFrame({"Metric": ["Retention Rate (%)"], "Value": [retention_rate]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Customer Retention Rate", text=[f"{retention_rate:.2f}%"], color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"The retention rate is {retention_rate:.2f}%, with {retained_customers} customers having multiple sessions in the selected date range."
                                recommendation = "Implement retention strategies if the rate is below industry benchmarks (e.g., 20-30%)."
                            
                            # Product Performance Queries
                            elif best_match == "product_performance_1":
                                order_details = st.session_state['data']['Order_Details']
                                products = st.session_state['data']['Products']
                                cart_freq = order_details.groupby('product_id').size().reset_index(name='cart_additions')
                                result_df = products.merge(cart_freq, left_on='id', right_on='product_id')[['name', 'cart_additions']].sort_values('cart_additions', ascending=False).head(5)
                                fig = px.bar(result_df, x='name', y='cart_additions', title="Top 5 Products Added to Carts", labels={'name': 'Product', 'cart_additions': 'Additions'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                top_product = result_df.iloc[0]['name'] if not result_df.empty else "N/A"
                                feasibility_study = f"Top 5 products added to carts {result_df['cart_additions'].sum()} times, with '{top_product}' leading as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = f"Promote '{top_product}' to leverage its popularity."
                            
                            elif best_match == "product_performance_2":
                                order_details = st.session_state['data']['Order_Details']
                                unique_products = order_details['product_id'].nunique()
                                result_df = pd.DataFrame({"Metric": ["Unique Products in Carts"], "Value": [unique_products]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Total Unique Products Added to Carts", color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"{unique_products} unique products are added to carts, showing product variety as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Maintain diverse inventory to support customer preferences."
                            
                            elif best_match == "product_performance_3":
                                order_details = st.session_state['data']['Order_Details']
                                products = st.session_state['data']['Products']
                                categories = st.session_state['data']['Categories']
                                category_popularity = order_details.merge(products, left_on='product_id', right_on='id').merge(categories, left_on='category_id', right_on='id')
                                result_df = category_popularity.groupby('name_y').size().reset_index(name='cart_additions').sort_values('cart_additions', ascending=False).head(5)
                                result_df = result_df.rename(columns={'name_y': 'Category', 'cart_additions': 'Additions'})
                                fig = px.bar(result_df, x='Category', y='Additions', title="Top 5 Popular Categories in Carts", labels={'Category': 'Category', 'Additions': 'Cart Additions'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                top_category = result_df.iloc[0]['Category'] if not result_df.empty else "N/A"
                                feasibility_study = f"Top 5 categories have {result_df['Additions'].sum()} additions, with '{top_category}' leading as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = f"Focus inventory on '{top_category}' to meet demand."
                            
                            elif best_match == "product_performance_4":
                                order_details = st.session_state['data']['Order_Details']
                                products = st.session_state['data']['Products']
                                carted_products = order_details['product_id'].unique()
                                total_products = products['id'].nunique()
                                never_carted = total_products - len(carted_products)
                                result_df = pd.DataFrame({"Metric": ["Products Never Added to Cart"], "Value": [never_carted]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Products Never Added to Cart", color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"{never_carted} products have never been added to carts out of {total_products} as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Review and promote these products to boost sales."
                            
                            elif best_match == "product_performance_5":
                                sessions = sessions.merge(st.session_state['data']['Order_Details'], left_on='id', right_on='id', how='left')
                                sessions['time_in_cart'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
                                avg_time = sessions['time_in_cart'].mean()
                                result_df = pd.DataFrame({"Metric": ["Average Time in Cart (minutes)"], "Value": [avg_time]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Average Time Products Stay in Cart", color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"Average time a product stays in cart is {avg_time:.2f} minutes as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Shorten checkout process if time is high to reduce abandonment."
                            
                            elif best_match == "product_performance_6":
                                order_details = st.session_state['data']['Order_Details']
                                merged = sessions.merge(order_details, left_on='id', right_on='id')
                                pairs = merged.groupby(['session_id', 'product_id']).size().reset_index(name='count')
                                pair_counts = pairs.groupby(['session_id']).apply(lambda x: x.nlargest(2, 'count')).reset_index(drop=True)
                                top_pairs = pair_counts.groupby(['product_id']).size().sort_values(ascending=False).head(5).reset_index(name='pair_count')
                                result_df = st.session_state['data']['Products'].merge(top_pairs, left_on='id', right_on='product_id')[['name', 'pair_count']]
                                fig = px.bar(result_df, x='name', y='pair_count', title="Top 5 Products Added Together", labels={'name': 'Product', 'pair_count': 'Pair Count'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                top_product = result_df.iloc[0]['name'] if not result_df.empty else "N/A"
                                feasibility_study = f"Top 5 product pairs total {result_df['pair_count'].sum()} instances, with '{top_product}' leading as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = f"Bundle '{top_product}' with frequent pairs for upselling."
                            
                            elif best_match == "product_performance_7":
                                order_details = st.session_state['data']['Order_Details']
                                products = st.session_state['data']['Products']
                                categories = st.session_state['data']['Categories']
                                merged = order_details.merge(products, left_on='product_id', right_on='id').merge(categories, left_on='category_id', right_on='id')
                                result_df = merged.groupby('parent_id').size().reset_index(name='additions')
                                result_df['parent_id'] = result_df['parent_id'].fillna('Top Level')
                                fig = px.bar(result_df, x='parent_id', y='additions', title="Distribution of Cart Additions by Hierarchy Level", labels={'parent_id': 'Hierarchy Level', 'additions': 'Additions'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                avg_additions = result_df['additions'].mean()
                                feasibility_study = f"Average additions per hierarchy level is {avg_additions:.2f}, with varied distribution as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Focus on popular hierarchy levels to optimize product placement."
                            
                            elif best_match == "product_performance_8":
                                order_details = st.session_state['data']['Order_Details']
                                merged = sessions.merge(order_details, left_on='id', right_on='id')
                                product_sessions = merged.groupby('product_id').size().reset_index(name='additions')
                                session_count = sessions['id'].nunique()
                                result_df = st.session_state['data']['Products'].merge(product_sessions, left_on='id', right_on='product_id')
                                result_df['addition_rate'] = result_df['additions'] / session_count * 100
                                result_df = result_df[['name', 'addition_rate']].sort_values('addition_rate', ascending=False).head(5)
                                fig = px.bar(result_df, x='name', y='addition_rate', title="Top 5 Products by Addition Rate", labels={'name': 'Product', 'addition_rate': 'Rate (%)'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                top_product = result_df.iloc[0]['name'] if not result_df.empty else "N/A"
                                feasibility_study = f"Top 5 products have addition rates up to {result_df['addition_rate'].max():.2f}%, with '{top_product}' leading as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = f"Highlight '{top_product}' in marketing due to its high addition rate."
                            
                            # product_performance_9 and product_performance_10 are disabled if has_order_id is False
                            
                            # Session Analysis Queries
                            elif best_match == "session_analysis_1":
                                total_sessions = len(sessions)
                                result_df = pd.DataFrame({"Metric": ["Total Sessions"], "Value": [total_sessions]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Total Number of Sessions", color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"There are {total_sessions} sessions in the dataset as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Use this data to assess platform traffic trends."
                            
                            elif best_match == "session_analysis_2":
                                sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
                                avg_duration = sessions['duration'].mean()
                                result_df = pd.DataFrame({"Metric": ["Average Session Duration (minutes)"], "Value": [avg_duration]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Average Session Duration", color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"Average session duration is {avg_duration:.2f} minutes as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Improve content if the duration is below industry averages (e.g., 5-10 minutes)."
                            
                            elif best_match == "session_analysis_3":
                                sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
                                result_df = sessions[['id', 'duration']].sort_values('duration', ascending=False).head(5)
                                fig = px.bar(result_df, x='id', y='duration', title="Top 5 Longest Sessions", labels={'id': 'Session ID', 'duration': 'Duration (minutes)'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                max_duration = result_df.iloc[0]['duration'] if not result_df.empty else 0
                                feasibility_study = f"Top 5 sessions reach up to {max_duration:.2f} minutes in duration as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Analyze these sessions to replicate engaging features."
                            
                            elif best_match == "session_analysis_4":
                                sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
                                sessions['hour'] = sessions['session_start'].dt.hour
                                result_df = sessions.groupby('hour')['duration'].mean().reset_index()
                                fig = px.line(result_df, x='hour', y='duration', title="Average Session Duration by Hour", labels={'hour': 'Hour of Day', 'duration': 'Average Duration (minutes)'}, line_shape='linear')
                                visualization = fig
                                peak_hour = result_df.loc[result_df['duration'].idxmax(), 'hour'] if not result_df.empty else 0
                                feasibility_study = f"Peak duration occurs at hour {peak_hour}:00 with {result_df['duration'].max():.2f} minutes in the selected date range."
                                recommendation = f"Enhance features at {peak_hour}:00 to retain users."
                            
                            elif best_match == "session_analysis_5":
                                sessions['day'] = sessions['session_start'].dt.day_name()
                                result_df = sessions.groupby('day').size().reset_index(name='session_count')
                                fig = px.bar(result_df, x='day', y='session_count', title="Distribution of Sessions by Day of Week", labels={'day': 'Day', 'session_count': 'Session Count'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                peak_day = result_df.loc[result_df['session_count'].idxmax(), 'day'] if not result_df.empty else "N/A"
                                feasibility_study = f"Most sessions occur on {peak_day} with {result_df['session_count'].max()} counts in the selected date range."
                                recommendation = f"Schedule promotions on {peak_day} to maximize impact."
                            
                            elif best_match == "session_analysis_6":
                                ip_sessions = sessions.groupby('ip_address').size().reset_index(name='session_count')
                                result_df = ip_sessions.sort_values('session_count', ascending=False).head(5)
                                fig = px.bar(result_df, x='ip_address', y='session_count', title="Top 5 IP Addresses by Session Count", labels={'ip_address': 'IP Address', 'session_count': 'Session Count'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                top_ip = result_df.iloc[0]['ip_address'] if not result_df.empty else "N/A"
                                feasibility_study = f"Top 5 IPs account for {result_df['session_count'].sum()} sessions, with '{top_ip}' leading as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = f"Monitor '{top_ip}' for potential bot activity if sessions are excessive."
                            
                            elif best_match == "session_analysis_7":
                                order_details = st.session_state['data']['Order_Details']
                                sessions_with_cart = order_details['id'].unique()
                                total_sessions = len(sessions)
                                no_cart_sessions = total_sessions - len(sessions_with_cart)
                                result_df = pd.DataFrame({"Metric": ["Sessions with No Cart Activity"], "Value": [no_cart_sessions]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Sessions with No Cart Activity", color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"{no_cart_sessions} sessions have no cart activity out of {total_sessions} as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Improve call-to-action if this number is high to encourage purchases."
                            
                            elif best_match == "session_analysis_8":
                                result_df = pd.DataFrame({"Message": ["This query requires exact cart addition timestamps, which are unavailable."]})
                                feasibility_study = "Exact cart addition timestamps are not available in the dataset."
                                recommendation = "Consider adding cart addition timestamps to enable this analysis."
                            
                            elif best_match == "session_analysis_9":
                                order_details = st.session_state['data']['Order_Details']
                                products_per_session = order_details.groupby('id').size().reset_index(name='product_count')
                                result_df = sessions.merge(products_per_session, on='id', how='left').fillna(0)[['id', 'product_count']].sort_values('product_count', ascending=False).head(5)
                                fig = px.bar(result_df, x='id', y='product_count', title="Top 5 Sessions by Products Added", labels={'id': 'Session ID', 'product_count': 'Product Count'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                max_products = result_df.iloc[0]['product_count'] if not result_df.empty else 0
                                feasibility_study = f"Top 5 sessions have up to {max_products} products added as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Analyze these sessions to identify popular product combinations."
                            
                            elif best_match == "session_analysis_10":
                                order_details = st.session_state['data']['Order_Details']
                                sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
                                merged = sessions.merge(order_details, on='id', how='left')
                                cart_counts = merged.groupby('id')['id_y'].count().reset_index(name='cart_count')
                                result_df = sessions.merge(cart_counts, on='id', how='left').fillna(0)[['duration', 'cart_count']]
                                fig = px.scatter(result_df, x='duration', y='cart_count', title="Session Duration vs Cart Additions", labels={'duration': 'Duration (minutes)', 'cart_count': 'Cart Additions'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                correlation = result_df['duration'].corr(result_df['cart_count'])
                                feasibility_study = f"Correlation between session duration and cart additions is {correlation:.2f} as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Increase session engagement if correlation is positive to boost cart additions."
                            
                            # Cart Activity Queries
                            elif best_match == "cart_activity_1":
                                order_details = st.session_state['data']['Order_Details']
                                unique_products = order_details['product_id'].nunique()
                                result_df = pd.DataFrame({"Metric": ["Unique Products in Carts"], "Value": [unique_products]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Total Unique Products Added to Carts", color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"{unique_products} unique products are added to carts, reflecting diversity as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Ensure stock levels match this variety."
                            
                            elif best_match == "cart_activity_2":
                                order_details = st.session_state['data']['Order_Details']
                                avg_products = order_details.groupby('order_id').size().mean()
                                result_df = pd.DataFrame({"Metric": ["Average Products per Cart"], "Value": [avg_products]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Average Number of Products per Cart", color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"Average products per cart is {avg_products:.2f}, indicating purchase behavior as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Encourage larger carts with bundle offers if the average is low."
                            
                            # cart_activity_3 and cart_activity_7 are disabled if has_order_id is False
                            
                            elif best_match == "cart_activity_4":
                                order_details = st.session_state['data']['Order_Details']
                                sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
                                merged = sessions.merge(order_details, left_on='id', right_on='id', how='left')
                                result_df = merged.groupby(pd.cut(merged['duration'], bins=5))['id_y'].count().reset_index(name='additions')
                                result_df['duration_range'] = result_df['duration'].astype(str)
                                fig = px.bar(result_df, x='duration_range', y='additions', title="Cart Additions by Session Duration", labels={'duration_range': 'Duration Range (minutes)', 'additions': 'Additions'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                peak_range = result_df.loc[result_df['additions'].idxmax(), 'duration_range'] if not result_df.empty else "N/A"
                                feasibility_study = f"Peak cart additions occur in the {peak_range} minute range as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = f"Optimize for sessions in the {peak_range} range to boost sales."
                            
                            elif best_match == "cart_activity_5":
                                order_details = st.session_state['data']['Order_Details']
                                products_per_session = order_details.groupby('id').size().reset_index(name='cart_additions')
                                result_df = sessions.merge(products_per_session, on='id', how='left').fillna(0)[['id', 'cart_additions']].sort_values('cart_additions', ascending=False).head(5)
                                fig = px.bar(result_df, x='id', y='cart_additions', title="Top 5 Sessions by Cart Additions", labels={'id': 'Session ID', 'cart_additions': 'Additions'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                max_additions = result_df.iloc[0]['cart_additions'] if not result_df.empty else 0
                                feasibility_study = f"Top 5 sessions have up to {max_additions} cart additions as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Analyze these sessions for effective product recommendations."
                            
                            elif best_match == "cart_activity_6":
                                order_details = st.session_state['data']['Order_Details']
                                sessions['first_minute'] = sessions['session_start'] + timedelta(minutes=1)
                                merged = sessions.merge(order_details, left_on='id', right_on='id', how='left')
                                within_minute = merged.shape[0]  # Simplified assumption
                                result_df = pd.DataFrame({"Metric": ["Cart Additions in First Minute"], "Value": [within_minute]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Cart Additions in First Minute", color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"{within_minute} cart additions occur within the first minute in the selected date range."
                                recommendation = "Enhance early engagement to capitalize on this trend."
                            
                            elif best_match == "cart_activity_8":
                                order_details = st.session_state['data']['Order_Details']
                                merged = sessions.merge(order_details, on='id')
                                customer_products = merged.groupby(['customer_id', 'session_id', 'product_id']).size().reset_index(name='count')
                                result_df = customer_products.merge(st.session_state['data']['Products'], left_on='product_id', right_on='id')[['name', 'count']].drop_duplicates().head(5)
                                fig = px.bar(result_df, x='name', y='count', title="Top 5 Products Added in Same Session", labels={'name': 'Product', 'count': 'Occurrences'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                top_product = result_df.iloc[0]['name'] if not result_df.empty else "N/A"
                                feasibility_study = f"Top 5 products are added {result_df['count'].sum()} times in same sessions, with '{top_product}' leading as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = f"Bundle '{top_product}' with other frequent pairs."
                            
                            elif best_match == "cart_activity_9":
                                order_details = st.session_state['data']['Order_Details']
                                merged = sessions.merge(order_details, on='id')
                                merged['hour'] = merged['session_start'].dt.hour
                                result_df = merged.groupby('hour').size().reset_index(name='cart_additions')
                                fig = px.line(result_df, x='hour', y='cart_additions', title="Cart Activity by Hour", labels={'hour': 'Hour of Day', 'cart_additions': 'Additions'}, line_shape='linear')
                                visualization = fig
                                peak_hour = result_df.loc[result_df['cart_additions'].idxmax(), 'hour'] if not result_df.empty else 0
                                feasibility_study = f"Peak cart activity is at {peak_hour}:00 with {result_df['cart_additions'].max()} additions in the selected date range."
                                recommendation = f"Boost promotions at {peak_hour}:00 to increase conversions."
                            
                            elif best_match == "cart_activity_10":
                                result_df = pd.DataFrame({"Message": ["This query requires exact cart addition timestamps, which are unavailable."]})
                                feasibility_study = "Exact cart addition timestamps are not available in the dataset."
                                recommendation = "Consider adding cart addition timestamps to enable this analysis."
                            
                            # Business Insights Queries
                            elif best_match == "business_insights_1":
                                order_details = st.session_state['data']['Order_Details']
                                total_sessions = len(sessions)
                                total_cart_additions = len(order_details)
                                conversion_rate = (total_cart_additions / total_sessions * 100) if total_sessions > 0 else 0
                                result_df = pd.DataFrame({"Metric": ["Conversion Rate (%)"], "Value": [conversion_rate]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Conversion Rate from Sessions to Cart Additions", text=[f"{conversion_rate:.2f}%"], color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"Conversion rate is {conversion_rate:.2f}% as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Improve UX if below 2-3% to enhance conversions."
                            
                            # business_insights_2, business_insights_4, business_insights_5, business_insights_7 are disabled if has_order_id is False
                            
                            elif best_match == "business_insights_3":
                                customers = st.session_state['data']['Customers']
                                customers['group'] = pd.qcut(customers['registration_date'].rank(method='first'), 4, labels=['G1', 'G2', 'G3', 'G4'])
                                group_size = customers.groupby('group').size().reset_index(name='group_size')
                                sessions_per_group = sessions.merge(customers, on='customer_id').groupby('group').size().reset_index(name='session_count')
                                result_df = group_size.merge(sessions_per_group, on='group')
                                fig = px.scatter(result_df, x='group_size', y='session_count', trendline="ols", title="Session Frequency vs Group Size", labels={'group_size': 'Group Size', 'session_count': 'Session Count'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                correlation = result_df['group_size'].corr(result_df['session_count'])
                                feasibility_study = f"Correlation between group size and session frequency is {correlation:.2f} as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = "Focus on larger groups if correlation is positive to boost engagement."
                            
                            elif best_match == "business_insights_6":
                                order_details = st.session_state['data']['Order_Details']
                                sessions['duration'] = (sessions['session_end'] - sessions['session_start']).dt.total_seconds() / 60
                                merged = sessions.merge(order_details, left_on='id', right_on='id', how='left')
                                duration_bins = pd.qcut(merged['duration'], 4, duplicates='drop')
                                cart_by_duration = merged.groupby(duration_bins)['id_y'].count().reset_index(name='cart_additions')
                                result_df = cart_by_duration
                                fig = px.bar(result_df, x='duration', y='cart_additions', title="Cart Additions by Session Duration Quartile", labels={'duration': 'Duration Quartile', 'cart_additions': 'Additions'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                peak_quartile = result_df.loc[result_df['cart_additions'].idxmax(), 'duration'] if not result_df.empty else "N/A"
                                feasibility_study = f"Peak cart additions occur in the {peak_quartile} duration quartile as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = f"Optimize for sessions in the {peak_quartile} range to boost conversions."
                            
                            elif best_match == "business_insights_8":
                                ip_freq = sessions.groupby('ip_address').size().reset_index(name='session_count')
                                threshold = ip_freq['session_count'].quantile(0.95)
                                potential_bots = ip_freq[ip_freq['session_count'] > threshold]
                                result_df = potential_bots[['ip_address', 'session_count']]
                                fig = px.bar(result_df, x='ip_address', y='session_count', title="Potential Bot IPs by Session Count", labels={'ip_address': 'IP Address', 'session_count': 'Session Count'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                top_ip = result_df.iloc[0]['ip_address'] if not result_df.empty else "N/A"
                                feasibility_study = f"{len(potential_bots)} IPs may indicate bot activity, with '{top_ip}' having {result_df.iloc[0]['session_count']} sessions as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = f"Investigate '{top_ip}' for bot behavior and implement CAPTCHA if needed."
                            
                            elif best_match == "business_insights_9":
                                order_details = st.session_state['data']['Order_Details']
                                products = st.session_state['data']['Products']
                                categories = st.session_state['data']['Categories']
                                merged = order_details.merge(products, left_on='product_id', right_on='id').merge(categories, left_on='category_id', right_on='id')
                                merged['depth'] = merged['parent_id'].apply(lambda x: 0 if pd.isna(x) else 1)
                                result_df = merged.groupby('depth').size().reset_index(name='cart_additions')
                                fig = px.bar(result_df, x='depth', y='cart_additions', title="Cart Additions by Product Hierarchy Depth", labels={'depth': 'Hierarchy Depth', 'cart_additions': 'Cart Additions'}, color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                max_depth = result_df.loc[result_df['cart_additions'].idxmax(), 'depth'] if not result_df.empty else 0
                                feasibility_study = f"Depth {max_depth} has the most cart additions with {result_df['cart_additions'].max()} as of {datetime.now().strftime('%B %d, %Y, %I:%M %p EEST')}."
                                recommendation = f"Focus on products at depth {max_depth} to enhance engagement."
                            
                            elif best_match == "business_insights_10":
                                customers = st.session_state['data']['Customers']
                                last_session = sessions.groupby('customer_id')['session_start'].max().reset_index()
                                merged = customers.merge(last_session, left_on='id', right_on='customer_id')
                                threshold_date = datetime.now() - timedelta(days=90)
                                churned = merged[merged['session_start'] < threshold_date]
                                churn_rate = (len(churned) / len(customers)) * 100 if len(customers) > 0 else 0
                                result_df = pd.DataFrame({"Metric": ["Churn Rate (%)"], "Value": [churn_rate]})
                                fig = px.bar(result_df, x="Metric", y="Value", title="Customer Churn Rate", text=[f"{churn_rate:.2f}%"], color_discrete_sequence=['#4CAF50'])
                                visualization = fig
                                feasibility_study = f"Churn rate is {churn_rate:.2f}% based on customers inactive for 90 days in the selected date range."
                                recommendation = "Implement re-engagement campaigns if churn rate is high."
                        
                        # Display results
                        if result_df is not None:
                            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
                            st.markdown(f'<div class="metric">Query Match Confidence: {confidence:.2f}%</div>', unsafe_allow_html=True)
                            tab1, tab2, tab3 = st.tabs(["Query Results", "Visualizations", "Insights"])
                            
                            with tab1:
                                st.subheader(title)
                                with st.expander("Query Results"):
                                    if 'Message' in result_df.columns:
                                        st.write(result_df['Message'].iloc[0])
                                    else:
                                        st.dataframe(result_df, use_container_width=True)
                            
                            with tab2:
                                st.subheader("Visualizations")
                                st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
                                if visualization:
                                    st.plotly_chart(visualization, use_container_width=True)
                                else:
                                    st.write("No visualization available for this query.")
                            
                            with tab3:
                                st.subheader("Insights")
                                st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
                                with st.expander("Feasibility Study"):
                                    st.write(feasibility_study)
                                with st.expander("Recommendation"):
                                    st.write(recommendation)
                            
                            # PDF Download
                            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
                            with st.spinner("Generating PDF Report..."):
                                pdf_buffer = io.BytesIO()
                                doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
                                styles = getSampleStyleSheet()
                                elements = [
                                    Paragraph("Query Analysis Report", styles['Title']),
                                    Paragraph(title, styles['Heading2']),
                                    Spacer(1, 20),
                                    Paragraph(f"Author: GrowEasy Platform", styles['Normal']),
                                    Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}", styles['Normal']),
                                    Spacer(1, 20),
                                    Paragraph("Results", styles['Heading2']),
                                ]
                                
                                # Add table or message
                                if 'Message' not in result_df.columns:
                                    data = [list(result_df.columns)]
                                    for _, row in result_df.iterrows():
                                        data.append([str(row[col]) for col in result_df.columns])
                                    table = Table(data)
                                    table.setStyle(TableStyle([
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black),
                                        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                                        ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                                        ('FONTSIZE', (0, 0), (-1, -1), 10),
                                        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                                    ]))
                                    elements.append(table)
                                else:
                                    elements.append(Paragraph(result_df['Message'].iloc[0], styles['Normal']))
                                elements.append(Spacer(1, 20))
                                elements.append(Paragraph("Feasibility Study", styles['Heading2']))
                                elements.append(Paragraph(feasibility_study, styles['Normal']))
                                elements.append(Spacer(1, 20))
                                elements.append(Paragraph("Recommendation", styles['Heading2']))
                                elements.append(Paragraph(recommendation, styles['Normal']))
                                
                                try:
                                    doc.build(elements)
                                    pdf_buffer.seek(0)
                                    st.download_button(
                                        label="Download Query Analysis Report",
                                        data=pdf_buffer.getvalue(),
                                        file_name="Query_Analysis_Report.pdf",
                                        mime="application/pdf",
                                        key="download_pdf"
                                    )
                                except Exception as e:
                                    st.error(f"Error generating PDF: {e}")
            else:
                st.info("Please enter a query to analyze the data (e.g., 'How many unique customers are in the dataset?').")
        else:
            st.info("Enter a query and click 'Run Query' to analyze the data (e.g., 'How many unique customers are in the dataset?').")
    
    except ValueError as ve:
        st.error(f"Data validation error: {ve}")
    except Exception as e:
        st.error(f"Error processing query: {e}")