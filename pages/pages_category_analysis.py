# import streamlit as st
# import pandas as pd
# from sklearn.linear_model import LinearRegression
# import plotly.express as px
# from reportlab.lib.pagesizes import A4
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.lib import colors
# from reportlab.platypus.tables import TableStyle
# import io
# from datetime import datetime

# st.title("Category Analysis")

# if 'data' not in st.session_state:
#     st.error("Please upload an Excel file on the main page.")
# else:
#     categories = st.session_state['data']['Categories'].rename(columns={'id': 'category_id'})
#     products = st.session_state['data']['Products'].rename(columns={'id': 'product_id'})
#     order_details = st.session_state['data']['Order_Details'].rename(columns={'id': 'order_detail_id'})
#     discounts = st.session_state['data']['Discounts'].rename(columns={'id': 'discount_id'})
#     inventory_movements = st.session_state['data']['Inventory_Movements'].rename(columns={'id': 'movement_id'})
    
#     # Key Present Metrics
#     # Total number of categories and subcategories
#     total_categories = len(categories[categories['parent_id'].isnull()])
#     total_subcategories = len(categories[categories['parent_id'].notnull()])
    
#     # Number of products per category
#     if 'category_id' not in products.columns:
#         st.error("Column 'category_id' not found in Products data. Analysis cannot proceed.")
#         products_per_category = pd.DataFrame(columns=['name', 'product_count'])
#     else:
#         products_per_category = products.groupby('category_id').size().reset_index(name='product_count')
#         products_per_category = products_per_category.merge(categories[['category_id', 'name']], on='category_id', how='left')
    
#     # Average product price per category
#     if 'category_id' not in products.columns or 'price' not in products.columns:
#         st.warning("Column 'category_id' or 'price' not found. Average price per category unavailable.")
#         avg_price_per_category = pd.DataFrame(columns=['name', 'avg_price'])
#     else:
#         avg_price_per_category = products.groupby('category_id')['price'].mean().reset_index(name='avg_price')
#         avg_price_per_category = avg_price_per_category.merge(categories[['category_id', 'name']], on='category_id', how='left')
    
#     # Category Metrics
#     if 'category_id' not in products.columns:
#         st.error("Column 'category_id' not found. Category sales unavailable.")
#         category_agg = pd.DataFrame(columns=['name', 'category_id', 'total_sold', 'revenue'])
#     else:
#         # First merge: order_details with products
#         category_sales = order_details.merge(
#             products[['product_id', 'category_id', 'price']],
#             left_on='product_id',
#             right_on='product_id',
#             how='left'
#         )
#         # Second merge: with categories
#         category_sales = category_sales.merge(
#             categories[['category_id', 'name']],
#             on='category_id',
#             how='left'
#         )
#         if 'price' not in category_sales.columns:
#             st.warning("Column 'price' not found in merged data. Revenue calculation unavailable.")
#             category_agg = category_sales.groupby(['name', 'category_id']).agg({
#                 'quantity': 'sum'
#             }).rename(columns={'quantity': 'total_sold'}).reset_index()
#             category_agg['revenue'] = 0.0
#         else:
#             category_agg = category_sales.groupby(['name', 'category_id']).agg({
#                 'quantity': 'sum',
#                 'price': lambda x: (x * category_sales.loc[x.index, 'quantity']).sum()
#             }).rename(columns={'quantity': 'total_sold', 'price': 'revenue'}).reset_index()
    
#     # Future-Oriented Insights
#     # Underperforming categories (low sales, low stock movement)
#     if 'category_id' not in products.columns:
#         st.error("Column 'category_id' not found. Underperforming categories unavailable.")
#         underperforming = pd.DataFrame(columns=['name', 'total_sold', 'stock_movement'])
#     else:
#         stock_movement = inventory_movements.groupby('product_id')['quantity'].sum().reset_index()
#         stock_movement = stock_movement.merge(products[['product_id', 'category_id']], on='product_id')
#         stock_movement_per_category = stock_movement.groupby('category_id')['quantity'].sum().reset_index(name='stock_movement')
#         underperforming = category_agg.merge(stock_movement_per_category, on='category_id', how='left').fillna(0)
#         underperforming['performance_score'] = underperforming['total_sold'] + underperforming['stock_movement']
#         underperforming = underperforming[underperforming['performance_score'] < underperforming['performance_score'].quantile(0.25)][['name', 'total_sold', 'stock_movement']]
    
#     # Opportunities for bundling/expansion (categories with growing product counts)
#     # Note: Products does not have a created_at column; skipping this logic as it's not applicable
#     st.warning("Products table lacks a creation date column. Opportunities for bundling/expansion unavailable.")
#     growing_categories = pd.DataFrame(columns=['name', 'recent_product_count'])
    
#     # Display Metrics
#     st.subheader("Key Present Metrics")
#     col1, col2 = st.columns(2)
#     col1.metric("Total Categories", total_categories)
#     col2.metric("Total Subcategories", total_subcategories)
    
#     st.subheader("Products per Category")
#     st.dataframe(products_per_category[['name', 'product_count']])
    
#     st.subheader("Average Product Price per Category")
#     st.dataframe(avg_price_per_category[['name', 'avg_price']])
    
#     st.subheader("Top Categories by Sales")
#     st.dataframe(category_agg[['name', 'total_sold', 'revenue']].sort_values('revenue', ascending=False).head(3))
    
#     # Visualization
#     if not category_agg.empty and 'revenue' in category_agg.columns and category_agg['revenue'].sum() > 0:
#         fig = px.bar(category_agg, x='name', y='revenue', title="Category Revenue")
#         st.plotly_chart(fig)
#     else:
#         st.write("Revenue data unavailable for visualization.")
    
#     # Future Insights
#     st.subheader("Underperforming Categories")
#     st.dataframe(underperforming)
    
#     st.subheader("Opportunities for Bundling/Expansion")
#     st.dataframe(growing_categories)
    
#     recommendation = f"Focus on revitalizing {len(underperforming)} underperforming categories and explore bundling in {len(growing_categories)} growing categories."
#     st.write(f"Recommendation: {recommendation}")
    
#     # PDF Download Section
#     pdf_buffer = io.BytesIO()
#     doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
#     styles = getSampleStyleSheet()
#     elements = [
#         Paragraph("Category Analysis Report", styles['Title']),
#         Paragraph("Key Present Metrics", styles['Heading2']),
#         Spacer(1, 12),
#         Paragraph(f"Author: GrowEasy Platform", styles['Normal']),
#         Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}", styles['Normal']),
#         Spacer(1, 12),
#     ]
    
#     # Add Metrics Table
#     data = [['Metric', 'Value']]
#     data.append(['Total Categories', str(total_categories)])
#     data.append(['Total Subcategories', str(total_subcategories)])
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))
    
#     # Add Products per Category
#     elements.append(Paragraph("Products per Category", styles['Heading2']))
#     data = [['Category', 'Product Count']]
#     for _, row in products_per_category.iterrows():
#         data.append([row['name'] if pd.notnull(row['name']) else 'Unknown', str(row['product_count'])])
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))
    
#     # Add Average Price per Category
#     elements.append(Paragraph("Average Product Price per Category", styles['Heading2']))
#     data = [['Category', 'Average Price']]
#     for _, row in avg_price_per_category.iterrows():
#         data.append([row['name'] if pd.notnull(row['name']) else 'Unknown', f"${row['avg_price']:.2f}"])
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))
    
#     # Add Top Categories by Sales
#     elements.append(Paragraph("Top Categories by Sales", styles['Heading2']))
#     data = [['Category', 'Total Sold', 'Revenue']]
#     for _, row in category_agg[['name', 'total_sold', 'revenue']].sort_values('revenue', ascending=False).head(3).iterrows():
#         data.append([row['name'], str(row['total_sold']), f"${row['revenue']:.2f}"])
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))
    
#     # Add Underperforming Categories
#     if not underperforming.empty:
#         elements.append(Paragraph("Underperforming Categories", styles['Heading2']))
#         data = [['Category', 'Total Sold', 'Stock Movement']]
#         for _, row in underperforming.iterrows():
#             data.append([row['name'] if pd.notnull(row['name']) else 'Unknown', str(row['total_sold']), str(row['stock_movement'])])
#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ]))
#         elements.append(table)
#         elements.append(Spacer(1, 12))
    
#     # Add Opportunities for Bundling
#     if not growing_categories.empty:
#         elements.append(Paragraph("Opportunities for Bundling/Expansion", styles['Heading2']))
#         data = [['Category', 'Recent Product Count']]
#         for _, row in growing_categories.iterrows():
#             data.append([row['name'] if pd.notnull(row['name']) else 'Unknown', str(row['recent_product_count'])])
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
#             label="Download Category Analysis Report",
#             data=pdf_buffer.getvalue(),
#             file_name="Category_Analysis_Report.pdf",
#             mime="application/pdf"
#         )
#     except Exception as e:
#         st.error(f"Error generating PDF: {str(e)}. Please ensure reportlab is installed.")






import streamlit as st
import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus.tables import TableStyle
import io
from datetime import datetime, timedelta

# Set page config for professional layout
st.set_page_config(layout="wide", page_title="GrowEasy: Category Analysis")

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
        color: #ffffff;
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
        color: #ffffff;
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
        color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #2c3e50;
        font-family: 'Arial', sans-serif;
        margin: 10px 0;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1f2a44;
        color: #ffffff;
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
st.markdown('<div class="title">Category Analysis</div>', unsafe_allow_html=True)

# Check for data in session state
if 'data' not in st.session_state or st.session_state['data'] is None:
    st.error("Please upload an Excel file on the main page.")
else:
    try:
        # Load data with column renaming
        categories = st.session_state['data']['Categories'].rename(columns={'id': 'category_id'})
        products = st.session_state['data']['Products'].rename(columns={'id': 'product_id'})
        order_details = st.session_state['data']['Order_Details'].rename(columns={'id': 'order_detail_id'})
        discounts = st.session_state['data']['Discounts'].rename(columns={'id': 'discount_id'})
        inventory_movements = st.session_state['data']['Inventory_Movements'].rename(columns={'id': 'movement_id'})
        
        # Key Present Metrics
        total_categories = len(categories[categories['parent_id'].isnull()])
        total_subcategories = len(categories[categories['parent_id'].notnull()])
        
        # Products per Category
        products_per_category = pd.DataFrame(columns=['name', 'product_count'])
        if 'category_id' in products.columns:
            products_per_category = products.groupby('category_id').size().reset_index(name='product_count')
            products_per_category = products_per_category.merge(categories[['category_id', 'name']], on='category_id', how='left')
        else:
            st.error("Column 'category_id' not found in Products data.")
        
        # Average Product Price per Category
        avg_price_per_category = pd.DataFrame(columns=['name', 'avg_price'])
        if 'category_id' in products.columns and 'price' in products.columns:
            avg_price_per_category = products.groupby('category_id')['price'].mean().reset_index(name='avg_price')
            avg_price_per_category = avg_price_per_category.merge(categories[['category_id', 'name']], on='category_id', how='left')
        else:
            st.warning("Column 'category_id' or 'price' not found in Products data.")
        
        # Category Sales
        category_agg = pd.DataFrame(columns=['name', 'category_id', 'total_sold', 'revenue'])
        if 'category_id' in products.columns and 'product_id' in order_details.columns:
            try:
                category_sales = order_details.merge(
                    products[['product_id', 'category_id', 'price']],
                    on='product_id',
                    how='left'
                ).merge(
                    categories[['category_id', 'name']],
                    on='category_id',
                    how='left'
                )
                if 'price' in category_sales.columns:
                    category_agg = category_sales.groupby(['name', 'category_id']).agg({
                        'quantity': 'sum',
                        'price': lambda x: (x * category_sales.loc[x.index, 'quantity']).sum()
                    }).rename(columns={'quantity': 'total_sold', 'price': 'revenue'}).reset_index()
                else:
                    st.warning("Column 'price' not found in merged data.")
                    category_agg = category_sales.groupby(['name', 'category_id']).agg({
                        'quantity': 'sum'
                    }).rename(columns={'quantity': 'total_sold'}).reset_index()
                    category_agg['revenue'] = 0.0
            except Exception as e:
                st.error(f"Error processing category sales: {e}")
        
        # Underperforming Categories
        underperforming = pd.DataFrame(columns=['name', 'total_sold', 'stock_movement'])
        if 'category_id' in products.columns and 'product_id' in inventory_movements.columns:
            try:
                stock_movement = inventory_movements.groupby('product_id')['quantity'].sum().reset_index()
                stock_movement = stock_movement.merge(products[['product_id', 'category_id']], on='product_id', how='left')
                stock_movement_per_category = stock_movement.groupby('category_id')['quantity'].sum().reset_index(name='stock_movement')
                underperforming = category_agg.merge(stock_movement_per_category, on='category_id', how='left').fillna(0)
                underperforming['performance_score'] = underperforming['total_sold'] + underperforming['stock_movement']
                underperforming = underperforming[underperforming['performance_score'] < underperforming['performance_score'].quantile(0.25)][['name', 'total_sold', 'stock_movement']]
            except Exception as e:
                st.error(f"Error processing underperforming categories: {e}")
        
        # Growing Categories: Use recent sales or fallback to total sales
        growing_categories = pd.DataFrame(columns=['name', 'category_id', 'recent_sales'])
        if 'order_date' in order_details.columns:
            try:
                order_details['order_date'] = pd.to_datetime(order_details['order_date'], errors='coerce')
                recent_sales = order_details[order_details['order_date'] > datetime.now() - timedelta(days=30)]
                growing_categories = recent_sales.merge(
                    products[['product_id', 'category_id']],
                    on='product_id',
                    how='left'
                ).merge(
                    categories[['category_id', 'name']],
                    on='category_id',
                    how='left'
                ).groupby(['name', 'category_id'])['quantity'].sum().reset_index(name='recent_sales')
                growing_categories = growing_categories.sort_values('recent_sales', ascending=False).head(5)
            except Exception as e:
                st.error(f"Error processing recent sales: {e}")
        if growing_categories.empty and not category_agg.empty:
            growing_categories = category_agg[['name', 'category_id', 'total_sold']].rename(columns={'total_sold': 'recent_sales'}).sort_values('recent_sales', ascending=False).head(5)
        
        # Interactive Filters
        st.sidebar.subheader("Filter Options")
        category_filter = st.sidebar.multiselect(
            "Select Categories",
            options=categories['name'].unique(),
            default=categories['name'].unique(),
            help="Filter data by category.",
            key="category_multiselect"
        )
        st.sidebar.button("Clear Filters", key="clear_filters", on_click=lambda: st.session_state.update(category_multiselect=categories['name'].unique().tolist()))
        
        # Apply filters
        filtered_products_per_category = products_per_category[products_per_category['name'].isin(category_filter)]
        filtered_avg_price_per_category = avg_price_per_category[avg_price_per_category['name'].isin(category_filter)]
        filtered_category_agg = category_agg[category_agg['name'].isin(category_filter)]
        filtered_underperforming = underperforming[underperforming['name'].isin(category_filter)]
        filtered_growing_categories = growing_categories[growing_categories['name'].isin(category_filter)]
        
        # Tabs for organized display
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["Present Metrics", "Visualizations", "Future Insights"])
        
        with tab1:
            st.subheader("Key Metrics")
            col1, col2 = st.columns(2)
            col1.markdown(f'<div class="metric">Total Categories: {total_categories}</div>', unsafe_allow_html=True)
            col2.markdown(f'<div class="metric">Total Subcategories: {total_subcategories}</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            
            with st.expander("Products per Category"):
                if not filtered_products_per_category.empty:
                    st.dataframe(filtered_products_per_category[['name', 'product_count']], use_container_width=True)
                else:
                    st.write("No data available for selected categories.")
            
            with st.expander("Average Product Price per Category"):
                if not filtered_avg_price_per_category.empty:
                    st.dataframe(filtered_avg_price_per_category[['name', 'avg_price']], use_container_width=True)
                else:
                    st.write("No data available for selected categories.")
            
            with st.expander("Top Categories by Sales"):
                if not filtered_category_agg.empty:
                    st.dataframe(filtered_category_agg[['name', 'total_sold', 'revenue']].sort_values('revenue', ascending=False).head(3), use_container_width=True)
                else:
                    st.write("No sales data available for selected categories.")
        
        with tab2:
            st.subheader("Revenue by Category")
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            if not filtered_category_agg.empty and 'revenue' in filtered_category_agg.columns and filtered_category_agg['revenue'].sum() > 0:
                fig = px.bar(filtered_category_agg, x='name', y='revenue', title="Category Revenue", color_discrete_sequence=['#4CAF50'])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Revenue data unavailable for visualization.")
        
        with tab3:
            st.subheader("Insights")
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            with st.expander("Underperforming Categories"):
                if not filtered_underperforming.empty:
                    st.dataframe(filtered_underperforming, use_container_width=True)
                else:
                    st.write("No underperforming categories identified.")
            
            with st.expander("Opportunities for Bundling/Expansion"):
                if not filtered_growing_categories.empty:
                    st.dataframe(filtered_growing_categories[['name', 'recent_sales']], use_container_width=True)
                else:
                    st.write("No recent sales data available for bundling opportunities.")
            
            recommendation = f"Focus on revitalizing {len(filtered_underperforming)} underperforming categories and explore bundling in {len(filtered_growing_categories)} high-demand categories."
            st.markdown(f"**Recommendation**: {recommendation}")
        
        # PDF Download
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        with st.spinner("Generating PDF Report..."):
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = [
                Paragraph("Category Analysis Report", styles['Title']),
                Paragraph("Key Present Metrics", styles['Heading2']),
                Spacer(1, 20),
                Paragraph("Author: GrowEasy Platform", styles['Normal']),
                Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}", styles['Normal']),
                Spacer(1, 20),
            ]
            
            # Metrics Table
            data = [['Metric', 'Value']]
            data.append(['Total Categories', str(total_categories)])
            data.append(['Total Subcategories', str(total_subcategories)])
            table = Table(data)
            table.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ]))
            elements.append(table)
            elements.append(Spacer(1, 20))
            
            # Products per Category
            if not filtered_products_per_category.empty:
                elements.append(Paragraph("Products per Category", styles['Heading2']))
                data = [['Category', 'Product Count']]
                for _, row in filtered_products_per_category.iterrows():
                    data.append([row['name'] if pd.notnull(row['name']) else 'Unknown', str(row['product_count'])])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            # Average Price per Category
            if not filtered_avg_price_per_category.empty:
                elements.append(Paragraph("Average Product Price per Category", styles['Heading2']))
                data = [['Category', 'Average Price']]
                for _, row in filtered_avg_price_per_category.iterrows():
                    data.append([row['name'] if pd.notnull(row['name']) else 'Unknown', f"${row['avg_price']:.2f}"])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            # Top Categories by Sales
            if not filtered_category_agg.empty:
                elements.append(Paragraph("Top Categories by Sales", styles['Heading2']))
                data = [['Category', 'Total Sold', 'Revenue']]
                for _, row in filtered_category_agg.sort_values('revenue', ascending=False).head(3).iterrows():
                    data.append([row['name'], str(row['total_sold']), f"${row['revenue']:.2f}"])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            # Underperforming Categories
            if not filtered_underperforming.empty:
                elements.append(Paragraph("Underperforming Categories", styles['Heading2']))
                data = [['Category', 'Total Sold', 'Stock Movement']]
                for _, row in filtered_underperforming.iterrows():
                    data.append([row['name'] if pd.notnull(row['name']) else 'Unknown', str(row['total_sold']), str(row['stock_movement'])])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            # Growing Categories
            if not filtered_growing_categories.empty:
                elements.append(Paragraph("Opportunities for Bundling/Expansion", styles['Heading2']))
                data = [['Category', 'Recent Sales (Last 30 Days)']]
                for _, row in filtered_growing_categories.iterrows():
                    data.append([row['name'] if pd.notnull(row['name']) else 'Unknown', str(row['recent_sales'])])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            elements.append(Paragraph("Recommendation", styles['Heading2']))
            elements.append(Paragraph(recommendation, styles['Normal']))
            
            try:
                doc.build(elements)
                pdf_buffer.seek(0)
                st.download_button(
                    label="Download Category Analysis Report",
                    data=pdf_buffer.getvalue(),
                    file_name="Category_Analysis_Report.pdf",
                    mime="application/pdf",
                    key="download_pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
    
    except Exception as e:
        st.error(f"Error processing data: {e}")
