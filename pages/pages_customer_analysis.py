# import streamlit as st
# import pandas as pd
# from sklearn.linear_model import LogisticRegression
# from sklearn.preprocessing import StandardScaler
# from datetime import datetime
# import plotly.express as px
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors
# from reportlab.platypus.tables import TableStyle
# import io

# st.title("Customer Analysis")

# if 'data' not in st.session_state:
#     st.error("Please upload an Excel file on the main page.")
# else:
#     customers = st.session_state['data']['Customers']
#     orders = st.session_state['data']['Orders']
#     wishlists = st.session_state['data']['Wishlists']
#     sessions = st.session_state['data']['Customer_Sessions']
    
#     # Key Present Metrics
#     # Total number of customers
#     total_customers = len(customers)
    
#     # Registration trends (monthly/weekly)
#     if 'registration_date' not in customers.columns:
#         st.warning("Column 'registration_date' not found in Customers data. Registration trends unavailable.")
#         monthly_registrations = pd.Series(dtype='int64')
#         weekly_registrations = pd.Series(dtype='int64')
#     else:
#         customers['registration_date'] = pd.to_datetime(customers['registration_date'])
#         monthly_registrations = customers.resample('M', on='registration_date')['id'].count()
#         weekly_registrations = customers.resample('W', on='registration_date')['id'].count()
    
#     # Top customer locations (parse address)
#     if 'address' in customers.columns:
#         customers['city'] = customers['address'].str.extract(r',\s*([A-Za-z\s]+),', expand=False).str.strip()
#         top_locations = customers['city'].value_counts().head(3)
#     else:
#         top_locations = pd.Series([], dtype='float64')  # Empty series if no address
    
#     # Contact information completeness
#     email_completeness = (customers['email'].notnull() & (customers['email'] != '')).mean() * 100
#     phone_completeness = (customers['phone'].notnull() & (customers['phone'] != '')).mean() * 100
    
#     # Customer Metrics
#     customer_orders = orders.groupby('customer_id').agg({
#         'id': 'count',
#         'total_amount': 'sum',
#         'order_date': 'max'
#     }).rename(columns={'id': 'order_count', 'total_amount': 'total_spent', 'order_date': 'last_order'})
#     customer_wishlists = wishlists.groupby('customer_id').size().reset_index(name='wishlist_count')
#     customer_df = customers.merge(customer_orders, left_on='id', right_on='customer_id', how='left').merge(
#         customer_wishlists, left_on='id', right_on='customer_id', how='left').fillna(0)
#     repeat_rate = len(customer_df[customer_df['order_count'] > 1]) / total_customers if total_customers > 0 else 0
#     clv = customer_df['total_spent'].mean() * customer_df['order_count'].mean()
    
#     # Future-Oriented Insights
#     # Predictive churn
#     customer_df['days_since_last_order'] = (datetime.now() - pd.to_datetime(customer_df['last_order'])).dt.days
#     features = ['order_count', 'total_spent', 'days_since_last_order', 'wishlist_count']
#     X = customer_df[features]
#     y = (customer_df['days_since_last_order'] > 90).astype(int)
#     scaler = StandardScaler()
#     X_scaled = scaler.fit_transform(X)
#     model = LogisticRegression()
#     model.fit(X_scaled, y)
#     churn_probs = model.predict_proba(X_scaled)[:, 1]
#     customer_df['churn_probability'] = churn_probs
#     high_risk = customer_df[customer_df['churn_probability'] > 0.7][['email', 'churn_probability']]
    
#     # Potential for loyalty programs
#     customer_sessions = sessions.groupby('customer_id').size().reset_index(name='session_count')
#     customer_df = customer_df.merge(customer_sessions, left_on='id', right_on='customer_id', how='left').fillna(0)
#     loyalty_potential = customer_df[(customer_df['order_count'] > 3) | (customer_df['session_count'] > 5)][['email', 'order_count', 'session_count']]
    
#     # Display Metrics
#     st.subheader("Key Present Metrics")
#     col1, col2, col3 = st.columns(3)
#     col1.metric("Total Customers", total_customers)
#     col2.metric("Repeat Rate", f"{repeat_rate*100:.1f}%")
#     col3.metric("Average CLV", f"${clv:.2f}")
    
#     # Registration Trends
#     st.subheader("Registration Trends")
#     if monthly_registrations.empty:
#         st.write("Registration trends unavailable due to missing 'registration_date' column.")
#     else:
#         fig_monthly = px.line(monthly_registrations, title="Monthly Registrations")
#         fig_weekly = px.line(weekly_registrations, title="Weekly Registrations")
#         st.plotly_chart(fig_monthly)
#         st.plotly_chart(fig_weekly)
    
#     # Top Locations
#     st.subheader("Top Customer Locations")
#     if not top_locations.empty:
#         st.write(top_locations)
#     else:
#         st.write("Address data not available.")
    
#     # Contact Completeness
#     st.subheader("Contact Information Completeness")
#     col1, col2 = st.columns(2)
#     col1.metric("Email Completeness", f"{email_completeness:.1f}%")
#     col2.metric("Phone Completeness", f"{phone_completeness:.1f}%")
    
#     # High-Risk Churn Customers
#     st.subheader("High-Risk Churn Customers")
#     st.dataframe(high_risk)
    
#     # Loyalty Potential
#     st.subheader("Potential for Loyalty Programs")
#     st.dataframe(loyalty_potential)
    
#     recommendation = f"Target {len(high_risk)} high-risk customers with retention campaigns and consider loyalty programs for {len(loyalty_potential)} frequent customers."
#     st.write(f"Recommendation: {recommendation}")
    
#     # PDF Download Section
#     pdf_buffer = io.BytesIO()
#     doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
#     styles = getSampleStyleSheet()
#     elements = [
#         Paragraph("Customer Analysis Report", styles['Title']),
#         Paragraph("Key Present Metrics", styles['Heading2']),
#         Spacer(1, 12),
#         Paragraph(f"Author: GrowEasy Platform", styles['Normal']),
#         Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}", styles['Normal']),
#         Spacer(1, 12),
#     ]
    
#     # Add Customer Insights table
#     data = [['Metric', 'Value']]
#     data.append(['Total Customers', str(total_customers)])
#     data.append(['Repeat Rate', f"{repeat_rate*100:.1f}%"])
#     data.append(['Average CLV', f"${clv:.2f}"])
#     data.append(['Email Completeness', f"{email_completeness:.1f}%"])
#     data.append(['Phone Completeness', f"{phone_completeness:.1f}%"])
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))
    
#     # Add Top Locations
#     if not top_locations.empty:
#         elements.append(Paragraph("Top Customer Locations", styles['Heading2']))
#         data = [['Location', 'Count']]
#         for loc, count in top_locations.items():
#             data.append([loc, str(count)])
#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ]))
#         elements.append(table)
#         elements.append(Spacer(1, 12))
    
#     # Add High-Risk Churn Customers
#     if not high_risk.empty:
#         elements.append(Paragraph("High-Risk Churn Customers", styles['Heading2']))
#         data = [['Email', 'Churn Probability']]
#         for _, row in high_risk.iterrows():
#             data.append([row['email'], f"{row['churn_probability']*100:.1f}%"])
#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ]))
#         elements.append(table)
#         elements.append(Spacer(1, 12))
    
#     # Add Loyalty Potential
#     if not loyalty_potential.empty:
#         elements.append(Paragraph("Potential for Loyalty Programs", styles['Heading2']))
#         data = [['Email', 'Order Count', 'Session Count']]
#         for _, row in loyalty_potential.iterrows():
#             data.append([row['email'], str(row['order_count']), str(row['session_count'])])
#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ]))
#         elements.append(table)
#         elements.append(Spacer(1, 12))
    
#     elements.append(Paragraph("Recommendation", styles['Heading2']))
#     elements.append(Paragraph(recommendation, styles['Normal']))
    
#     try:
#         doc.build(elements)
#         pdf_buffer.seek(0, 2)
#         buffer_size = pdf_buffer.tell()
#         st.write(f"Debug: PDF buffer size is {buffer_size} bytes")
#         pdf_buffer.seek(0)
#         st.download_button(
#             label="Download Customer Analysis Report",
#             data=pdf_buffer.getvalue(),
#             file_name="Customer_Analysis_Report.pdf",
#             mime="application/pdf"
#         )
#     except Exception as e:
#         st.error(f"Error generating PDF: {str(e)}. Please ensure reportlab is installed.")









import streamlit as st
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import plotly.express as px
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus.tables import TableStyle
import io
from datetime import datetime, timedelta

# Set page config for professional layout
st.set_page_config(layout="wide", page_title="GrowEasy: Customer Analysis")

# Professional CSS with harmonious dark palette and increased spacing
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
    .stMultiSelect label {
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
    </style>
    """,
    unsafe_allow_html=True
)

# Animated title
st.markdown('<div class="title">Customer Analysis</div>', unsafe_allow_html=True)

# Check for data in session state
if 'data' not in st.session_state or st.session_state['data'] is None:
    st.error("Please upload an Excel file on the main page.")
else:
    try:
        # Load data with column renaming
        customers = st.session_state['data']['Customers'].rename(columns={'id': 'customer_id'})
        orders = st.session_state['data']['Orders'].rename(columns={'id': 'order_id'})
        wishlists = st.session_state['data']['Wishlists'].rename(columns={'id': 'wishlist_id'})
        sessions = st.session_state['data']['Customer_Sessions'].rename(columns={'id': 'session_id'})
        
        # Key Present Metrics
        total_customers = len(customers)
        
        # Registration Trends
        monthly_registrations = pd.Series(dtype='int64')
        weekly_registrations = pd.Series(dtype='int64')
        if 'registration_date' in customers.columns:
            customers['registration_date'] = pd.to_datetime(customers['registration_date'], errors='coerce')
            monthly_registrations = customers.resample('M', on='registration_date')['customer_id'].count()
            weekly_registrations = customers.resample('W', on='registration_date')['customer_id'].count()
        elif 'order_date' in orders.columns:
            orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')
            monthly_registrations = orders.resample('M', on='order_date')['customer_id'].count()
            weekly_registrations = orders.resample('W', on='order_date')['customer_id'].count()
        
        # Top Customer Locations
        top_locations = pd.Series([], dtype='float64')
        if 'address' in customers.columns:
            customers['city'] = customers['address'].str.extract(r',\s*([A-Za-z\s]+),', expand=False).str.strip()
            top_locations = customers['city'].value_counts().head(3)
        
        # Contact Information Completeness
        email_completeness = (customers['email'].notnull() & (customers['email'] != '')).mean() * 100 if 'email' in customers.columns else 0
        phone_completeness = (customers['phone'].notnull() & (customers['phone'] != '')).mean() * 100 if 'phone' in customers.columns else 0
        
        # Customer Metrics
        customer_orders = pd.DataFrame(columns=['order_count', 'total_spent', 'last_order'])
        customer_wishlists = pd.DataFrame(columns=['wishlist_count'])
        if 'customer_id' in orders.columns:
            customer_orders = orders.groupby('customer_id').agg({
                'order_id': 'count',
                'total_amount': 'sum',
                'order_date': 'max'
            }).rename(columns={'order_id': 'order_count', 'total_amount': 'total_spent', 'order_date': 'last_order'})
        if 'customer_id' in wishlists.columns:
            customer_wishlists = wishlists.groupby('customer_id').size().reset_index(name='wishlist_count')
        
        customer_df = customers.merge(customer_orders, left_on='customer_id', right_on='customer_id', how='left').merge(
            customer_wishlists, left_on='customer_id', right_on='customer_id', how='left').fillna({'order_count': 0, 'total_spent': 0, 'wishlist_count': 0})
        repeat_rate = len(customer_df[customer_df['order_count'] > 1]) / total_customers if total_customers > 0 else 0
        clv = customer_df['total_spent'].mean() * customer_df['order_count'].mean() if not customer_df.empty else 0
        
        # Predictive Churn
        high_risk = pd.DataFrame(columns=['email', 'churn_probability'])
        if 'last_order' in customer_df.columns and not customer_df['last_order'].isnull().all():
            customer_df['days_since_last_order'] = (datetime.now() - pd.to_datetime(customer_df['last_order'])).dt.days.fillna(365)
            features = ['order_count', 'total_spent', 'days_since_last_order', 'wishlist_count']
            X = customer_df[features]
            y = (customer_df['days_since_last_order'] > 90).astype(int)
            try:
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                model = LogisticRegression()
                model.fit(X_scaled, y)
                churn_probs = model.predict_proba(X_scaled)[:, 1]
                customer_df['churn_probability'] = churn_probs
                high_risk = customer_df[customer_df['churn_probability'] > 0.7][['email', 'churn_probability']]
            except Exception as e:
                st.error(f"Error in churn prediction: {e}")
        
        # Loyalty Potential
        loyalty_potential = pd.DataFrame(columns=['email', 'order_count', 'session_count'])
        if 'customer_id' in sessions.columns:
            customer_sessions = sessions.groupby('customer_id').size().reset_index(name='session_count')
            customer_df = customer_df.merge(customer_sessions, left_on='customer_id', right_on='customer_id', how='left').fillna({'session_count': 0})
            loyalty_potential = customer_df[(customer_df['order_count'] > 3) | (customer_df['session_count'] > 5)][['email', 'order_count', 'session_count']]
        
        # Interactive Filters
        st.sidebar.subheader("Filter Options")
        city_options = customers['city'].dropna().unique() if 'city' in customers.columns else []
        city_filter = st.sidebar.multiselect(
            "Select Cities",
            options=city_options,
            default=city_options,
            help="Filter by customer city.",
            key="city_multiselect"
        )
        churn_risk_filter = st.sidebar.selectbox(
            "Churn Risk Level",
            options=["All", "High (>70%)", "Medium (30-70%)", "Low (<30%)"],
            help="Filter by churn probability.",
            key="churn_risk_select"
        )
        st.sidebar.button("Clear Filters", key="clear_filters", on_click=lambda: st.session_state.update(
            city_multiselect=city_options, churn_risk_select="All"))
        
        # Apply filters
        filtered_customer_df = customer_df
        if city_filter and 'city' in filtered_customer_df.columns:
            filtered_customer_df = filtered_customer_df[filtered_customer_df['city'].isin(city_filter)]
        if churn_risk_filter != "All" and 'churn_probability' in filtered_customer_df.columns:
            if churn_risk_filter == "High (>70%)":
                filtered_customer_df = filtered_customer_df[filtered_customer_df['churn_probability'] > 0.7]
            elif churn_risk_filter == "Medium (30-70%)":
                filtered_customer_df = filtered_customer_df[(filtered_customer_df['churn_probability'] >= 0.3) & (filtered_customer_df['churn_probability'] <= 0.7)]
            else:  # Low (<30%)
                filtered_customer_df = filtered_customer_df[filtered_customer_df['churn_probability'] < 0.3]
        filtered_high_risk = high_risk[high_risk['email'].isin(filtered_customer_df['email'])] if not high_risk.empty else high_risk
        filtered_loyalty_potential = loyalty_potential[loyalty_potential['email'].isin(filtered_customer_df['email'])] if not loyalty_potential.empty else loyalty_potential
        
        # Tabs for organized display
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["Present Metrics", "Visualizations", "Future Insights"])
        
        with tab1:
            st.subheader("Key Present Metrics")
            col1, col2, col3 = st.columns(3)
            col1.markdown(f'<div class="metric">Total Customers: {total_customers}</div>', unsafe_allow_html=True)
            col2.markdown(f'<div class="metric">Repeat Rate: {repeat_rate*100:.1f}%</div>', unsafe_allow_html=True)
            col3.markdown(f'<div class="metric">Average CLV: ${clv:.2f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            
            with st.expander("Contact Information Completeness"):
                col1, col2 = st.columns(2)
                col1.markdown(f'<div class="metric">Email Completeness: {email_completeness:.1f}%</div>', unsafe_allow_html=True)
                col2.markdown(f'<div class="metric">Phone Completeness: {phone_completeness:.1f}%</div>', unsafe_allow_html=True)
            
            with st.expander("Top Customer Locations"):
                if not top_locations.empty:
                    st.dataframe(top_locations.reset_index().rename(columns={'index': 'City', 'city': 'Count'}), use_container_width=True)
                else:
                    st.write("Address data not available.")
        
        with tab2:
            st.subheader("Registration Trends")
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            if not monthly_registrations.empty:
                fig_monthly = px.line(monthly_registrations, title="Monthly Registrations", color_discrete_sequence=['#4CAF50'])
                fig_weekly = px.line(weekly_registrations, title="Weekly Registrations", color_discrete_sequence=['#4CAF50'])
                st.plotly_chart(fig_monthly, use_container_width=True)
                st.plotly_chart(fig_weekly, use_container_width=True)
            else:
                st.write("Registration trends unavailable due to missing data.")
        
        with tab3:
            st.subheader("Insights")
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            with st.expander("High-Risk Churn Customers"):
                if not filtered_high_risk.empty:
                    st.dataframe(filtered_high_risk, use_container_width=True)
                else:
                    st.write("No high-risk churn customers identified.")
            
            with st.expander("Potential for Loyalty Programs"):
                if not filtered_loyalty_potential.empty:
                    st.dataframe(filtered_loyalty_potential, use_container_width=True)
                else:
                    st.write("No customers identified for loyalty programs.")
            
            recommendation = f"Target {len(filtered_high_risk)} high-risk customers with retention campaigns and consider loyalty programs for {len(filtered_loyalty_potential)} frequent customers."
            st.markdown(f"**Recommendation**: {recommendation}")
        
        # PDF Download
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        with st.spinner("Generating PDF Report..."):
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = [
                Paragraph("Customer Analysis Report", styles['Title']),
                Paragraph("Key Present Metrics", styles['Heading2']),
                Spacer(1, 20),
                Paragraph("Author: GrowEasy Platform", styles['Normal']),
                Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}", styles['Normal']),
                Spacer(1, 20),
            ]
            
            # Metrics Table
            data = [['Metric', 'Value']]
            data.append(['Total Customers', str(total_customers)])
            data.append(['Repeat Rate', f"{repeat_rate*100:.1f}%"])
            data.append(['Average CLV', f"${clv:.2f}"])
            data.append(['Email Completeness', f"{email_completeness:.1f}%"])
            data.append(['Phone Completeness', f"{phone_completeness:.1f}%"])
            table = Table(data)
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 20))
            
            # Top Locations
            if not top_locations.empty:
                elements.append(Paragraph("Top Customer Locations", styles['Heading2']))
                data = [['City', 'Count']]
                for loc, count in top_locations.items():
                    data.append([loc, str(count)])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            # High-Risk Churn Customers
            if not filtered_high_risk.empty:
                elements.append(Paragraph("High-Risk Churn Customers", styles['Heading2']))
                data = [['Email', 'Churn Probability']]
                for _, row in filtered_high_risk.iterrows():
                    data.append([row['email'], f"{row['churn_probability']*100:.1f}%"])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            # Loyalty Potential
            if not filtered_loyalty_potential.empty:
                elements.append(Paragraph("Potential for Loyalty Programs", styles['Heading2']))
                data = [['Email', 'Order Count', 'Session Count']]
                for _, row in filtered_loyalty_potential.iterrows():
                    data.append([row['email'], str(row['order_count']), str(row['session_count'])])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            elements.append(Paragraph("Recommendation", styles['Heading2']))
            elements.append(Paragraph(recommendation, styles['Normal']))
            
            try:
                doc.build(elements)
                pdf_buffer.seek(0)
                st.download_button(
                    label="Download Customer Analysis Report",
                    data=pdf_buffer.getvalue(),
                    file_name="Customer_Analysis_Report.pdf",
                    mime="application/pdf",
                    key="download_pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
    
    except Exception as e:
        st.error(f"Error processing data: {e}")

