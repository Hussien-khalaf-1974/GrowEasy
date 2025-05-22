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

# st.title("Product Analysis")

# if 'data' not in st.session_state:
#     st.error("Please upload an Excel file on the main page.")
# else:
#     products = st.session_state['data']['Products']
#     order_details = st.session_state['data']['Order_Details']
#     reviews = st.session_state['data']['Reviews']
#     wishlists = st.session_state['data']['Wishlists']
#     inventory_movements = st.session_state['data']['Inventory_Movements']
    
#     # Key Present Metrics
#     # List of products with price and stock quantity
#     if 'price' not in products.columns:
#         st.warning("Column 'price' not found in Products data. Using default value of $0.00.")
#         products['price'] = 0.0
#     product_list = products[['name', 'price', 'stock_quantity']]
    
#     # Best-selling products
#     if 'price' not in products.columns:
#         st.warning("Column 'price' not found. Best-selling products will use total sold only.")
#         product_sales = order_details.groupby('product_id').agg({'quantity': 'sum'}).rename(columns={'quantity': 'total_sold'})
#     else:
#         if 'order_date' not in order_details.columns:
#             st.warning("Column 'order_date' not found in Order_Details. Using total sold only.")
#             product_sales = order_details.groupby('product_id').agg({'quantity': 'sum'}).rename(columns={'quantity': 'total_sold'})
#         else:
#             product_sales = order_details.groupby('product_id').agg({
#                 'quantity': 'sum',
#                 'price': lambda x: (x * order_details.loc[x.index, 'quantity']).sum()
#             }).rename(columns={'quantity': 'total_sold', 'price': 'revenue'})
#     best_selling = product_sales.merge(products[['id', 'name']], left_on='product_id', right_on='id', how='left').sort_values('total_sold', ascending=False).head(5)
    
#     # Low stock alerts
#     low_stock = products[products['stock_quantity'] < 10][['name', 'stock_quantity']]
    
#     # Future-Oriented Insights
#     # Predictive stockout risks
#     if 'order_date' not in order_details.columns:
#         st.warning("Column 'order_date' not found. Stockout risks unavailable.")
#         stockout_risk = pd.DataFrame(columns=['name', 'stock_quantity', 'days_to_stockout'])
#     else:
#         recent_sales = order_details.merge(products[['id', 'stock_quantity']], left_on='product_id', right_on='id', how='left')
#         recent_sales['order_date'] = pd.to_datetime(recent_sales['order_date'])
#         recent_sales = recent_sales[recent_sales['order_date'] > datetime.now() - pd.Timedelta(days=30)]
#         sales_rate = recent_sales.groupby('product_id')['quantity'].sum().reset_index(name='monthly_sales')
#         sales_rate = sales_rate.merge(products[['id', 'name', 'stock_quantity']], left_on='product_id', right_on='id', how='left')
#         sales_rate['days_to_stockout'] = sales_rate['stock_quantity'] / (sales_rate['monthly_sales'] / 30)
#         sales_rate['days_to_stockout'] = sales_rate['days_to_stockout'].replace([float('inf'), -float('inf')], float('nan')).fillna(999)  # Handle division by zero
#         stockout_risk = sales_rate[sales_rate['days_to_stockout'] < 15][['name', 'stock_quantity', 'days_to_stockout']]
    
#     # Suggested restocking schedule
#     if stockout_risk.empty:
#         restock_schedule = pd.DataFrame(columns=['name', 'restock_date'])
#     else:
#         restock_schedule = stockout_risk.copy()
#         restock_schedule['restock_date'] = datetime.now() + pd.to_timedelta(restock_schedule['days_to_stockout'], unit='D')
#         restock_schedule = restock_schedule[['name', 'restock_date']].sort_values('restock_date')
    
#     # Product price optimization
#     if 'price' not in products.columns:
#         st.warning("Column 'price' not found. Price optimization skipped.")
#         price_analysis = pd.DataFrame()
#     else:
#         product_reviews = reviews.groupby('product_id')['rating'].mean().reset_index(name='avg_rating')
#         price_analysis = product_sales.merge(product_reviews, on='product_id', how='left').merge(products[['id', 'name', 'price']], left_on='product_id', right_on='id', how='left')
#         price_analysis['price_adjustment'] = price_analysis.apply(
#             lambda x: 'Increase' if (pd.notnull(x['avg_rating']) and x['avg_rating'] > 4 and x['total_sold'] > price_analysis['total_sold'].mean()) else 
#                       'Decrease' if (pd.notnull(x['avg_rating']) and x['avg_rating'] < 3) else 'Maintain',
#             axis=1
#         )
    
#     # Display Metrics
#     st.subheader("Key Present Metrics")
#     st.subheader("Product List")
#     st.dataframe(product_list)
    
#     st.subheader("Best-Selling Products")
#     st.dataframe(best_selling[['name', 'total_sold', 'revenue'] if 'revenue' in best_selling.columns else ['name', 'total_sold']])
    
#     st.subheader("Low Stock Alerts")
#     st.dataframe(low_stock)
    
#     # Future Insights
#     st.subheader("Predictive Stockout Risks")
#     st.dataframe(stockout_risk)
    
#     st.subheader("Suggested Restocking Schedule")
#     st.dataframe(restock_schedule)
    
#     st.subheader("Price Optimization Suggestions")
#     st.dataframe(price_analysis[['name', 'price', 'avg_rating', 'total_sold', 'price_adjustment']] if not price_analysis.empty else pd.DataFrame())
    
#     recommendation = f"Restock {len(stockout_risk)} products at risk of stockout and review pricing for {len(price_analysis[price_analysis['price_adjustment'] != 'Maintain']) if not price_analysis.empty else 0} products."
#     st.write(f"Recommendation: {recommendation}")
    
#     # PDF Download Section
#     pdf_buffer = io.BytesIO()
#     doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
#     styles = getSampleStyleSheet()
#     elements = [
#         Paragraph("Product Analysis Report", styles['Title']),
#         Paragraph("Key Present Metrics", styles['Heading2']),
#         Spacer(1, 12),
#         Paragraph(f"Author: GrowEasy Platform", styles['Normal']),
#         Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}", styles['Normal']),
#         Spacer(1, 12),
#     ]
    
#     # Add Product List (limited to top 5 for brevity in PDF)
#     elements.append(Paragraph("Product List (Top 5)", styles['Heading2']))
#     data = [['Product', 'Price', 'Stock Quantity']]
#     for _, row in product_list.head(5).iterrows():
#         data.append([row['name'], f"${row['price']:.2f}", str(row['stock_quantity'])])
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))
    
#     # Add Best-Selling Products
#     elements.append(Paragraph("Best-Selling Products", styles['Heading2']))
#     data = [['Product', 'Units Sold', 'Revenue']] if 'revenue' in best_selling.columns else [['Product', 'Units Sold']]
#     for _, row in best_selling.head(5).iterrows():
#         row_data = [row['name'], str(row['total_sold'])]
#         if 'revenue' in best_selling.columns:
#             row_data.append(f"${row['revenue']:.2f}")
#         data.append(row_data)
#     table = Table(data)
#     table.setStyle(TableStyle([
#         ('GRID', (0, 0), (-1, -1), 1, colors.black),
#         ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#         ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#     ]))
#     elements.append(table)
#     elements.append(Spacer(1, 12))
    
#     # Add Low Stock Alerts
#     if not low_stock.empty:
#         elements.append(Paragraph("Low Stock Alerts", styles['Heading2']))
#         data = [['Product', 'Stock']]
#         for _, row in low_stock.iterrows():
#             data.append([row['name'], str(row['stock_quantity'])])
#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ]))
#         elements.append(table)
#         elements.append(Spacer(1, 12))
    
#     # Add Stockout Risks
#     if not stockout_risk.empty:
#         elements.append(Paragraph("Predictive Stockout Risks", styles['Heading2']))
#         data = [['Product', 'Stock Quantity', 'Days to Stockout']]
#         for _, row in stockout_risk.iterrows():
#             data.append([row['name'], str(row['stock_quantity']), f"{row['days_to_stockout']:.1f}"])
#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ]))
#         elements.append(table)
#         elements.append(Spacer(1, 12))
    
#     # Add Restocking Schedule
#     if not restock_schedule.empty:
#         elements.append(Paragraph("Suggested Restocking Schedule", styles['Heading2']))
#         data = [['Product', 'Restock Date']]
#         for _, row in restock_schedule.head(5).iterrows():
#             data.append([row['name'], row['restock_date'].strftime('%Y-%m-%d')])
#         table = Table(data)
#         table.setStyle(TableStyle([
#             ('GRID', (0, 0), (-1, -1), 1, colors.black),
#             ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
#             ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
#         ]))
#         elements.append(table)
#         elements.append(Spacer(1, 12))
    
#     # Add Price Optimization
#     if not price_analysis.empty:
#         elements.append(Paragraph("Price Optimization Suggestions", styles['Heading2']))
#         data = [['Product', 'Price', 'Avg Rating', 'Units Sold', 'Price Adjustment']]
#         for _, row in price_analysis.head(5).iterrows():
#             data.append([row['name'], f"${row['price']:.2f}", f"{row['avg_rating']:.1f}" if pd.notnull(row['avg_rating']) else 'N/A', str(row['total_sold']), row['price_adjustment']])
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
#             label="Download Product Analysis Report",
#             data=pdf_buffer.getvalue(),
#             file_name="Product_Analysis_Report.pdf",
#             mime="application/pdf"
#         )
#     except Exception as e:
#         st.error(f"Error generating PDF: {str(e)}. Please ensure reportlab is installed.")



import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import plotly.express as px
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.platypus.tables import TableStyle
import io
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(layout="wide", page_title="GrowEasy: Product Analysis")

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
    .stMultiSelect label, .stSlider label {
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
st.markdown('<div class="title">Product Analysis</div>', unsafe_allow_html=True)

# Check for data
if 'data' not in st.session_state or st.session_state['data'] is None:
    st.error("Please upload an Excel file on the main page.")
else:
    try:
        # Validate required columns
        required_columns = {
            'Products': ['id', 'name', 'stock_quantity'],
            'Order_Details': ['product_id', 'quantity'],
            'Reviews': ['product_id', 'rating'],
            'Wishlists': ['product_id'],
            'Inventory_Movements': ['product_id']
        }
        for sheet, cols in required_columns.items():
            if sheet not in st.session_state['data']:
                raise ValueError(f"Missing required sheet: {sheet}")
            missing_cols = [col for col in cols if col not in st.session_state['data'][sheet].columns]
            if missing_cols:
                raise ValueError(f"Missing columns in {sheet}: {', '.join(missing_cols)}")
        
        products = st.session_state['data']['Products']
        order_details = st.session_state['data']['Order_Details']
        reviews = st.session_state['data']['Reviews']
        wishlists = st.session_state['data']['Wishlists']
        inventory_movements = st.session_state['data']['Inventory_Movements']
        
        # Key Present Metrics
        if 'price' not in products.columns:
            products['price'] = 0.0
        product_list = products[['name', 'price', 'stock_quantity']]
        
        product_sales = order_details.groupby('product_id').agg({'quantity': 'sum'}).rename(columns={'quantity': 'total_sold'})
        best_selling = product_sales.merge(products[['id', 'name']], left_on='product_id', right_on='id', how='left').sort_values('total_sold', ascending=False).head(5)
        
        low_stock = products[products['stock_quantity'] < 10][['name', 'stock_quantity']]
        
        # Future-Oriented Insights
        stockout_risk = pd.DataFrame(columns=['name', 'stock_quantity', 'days_to_stockout'])
        restock_schedule = pd.DataFrame(columns=['name', 'restock_date'])
        
        if 'price' not in products.columns:
            price_analysis = pd.DataFrame()
        else:
            product_reviews = reviews.groupby('product_id')['rating'].mean().reset_index(name='avg_rating')
            price_analysis = product_sales.merge(product_reviews, on='product_id', how='left').merge(products[['id', 'name', 'price']], left_on='product_id', right_on='id', how='left')
            price_analysis['price_adjustment'] = price_analysis.apply(
                lambda x: 'Increase' if (pd.notnull(x['avg_rating']) and x['avg_rating'] > 4 and x['total_sold'] > price_analysis['total_sold'].mean()) else 
                          'Decrease' if (pd.notnull(x['avg_rating']) and x['avg_rating'] < 3) else 'Maintain',
                axis=1
            )
        
        # Sidebar filters
        st.sidebar.subheader("Filter Options")
        category_options = products['category'].dropna().unique() if 'category' in products.columns else ['All']
        category_filter = st.sidebar.multiselect(
            "Select Product Category",
            options=category_options,
            default=category_options,
            key="category_multiselect"
        )
        min_stock = int(products['stock_quantity'].min()) if 'stock_quantity' in products.columns else 0
        max_stock = int(products['stock_quantity'].max()) if 'stock_quantity' in products.columns else 100
        stock_filter = st.sidebar.slider(
            "Stock Quantity Range",
            min_value=min_stock,
            max_value=max_stock,
            value=(min_stock, max_stock),
            step=1,
            key="stock_range"
        )
        min_price = float(products['price'].min()) if 'price' in products.columns else 0.0
        max_price = float(products['price'].max()) if 'price' in products.columns else 1000.0
        price_filter = st.sidebar.slider(
            "Price Range ($)",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
            step=0.01,
            key="price_range"
        )
        st.sidebar.button("Clear Filters", key="clear_filters", on_click=lambda: st.session_state.update(
            category_multiselect=category_options, stock_range=(min_stock, max_stock), price_range=(min_price, max_price)))
        
        # Apply filters
        filtered_products = products
        if category_filter and 'category' in filtered_products.columns:
            filtered_products = filtered_products[filtered_products['category'].isin(category_filter)]
        if 'stock_quantity' in filtered_products.columns:
            min_stock, max_stock = stock_filter
            filtered_products = filtered_products[(filtered_products['stock_quantity'] >= min_stock) & (filtered_products['stock_quantity'] <= max_stock)]
        if 'price' in filtered_products.columns:
            min_price, max_price = price_filter
            filtered_products = filtered_products[(filtered_products['price'] >= min_price) & (filtered_products['price'] <= max_price)]
        
        # Recalculate metrics for filtered data
        total_filtered_products = len(filtered_products)
        filtered_product_list = filtered_products[['name', 'price', 'stock_quantity']]
        filtered_low_stock = filtered_products[filtered_products['stock_quantity'] < 10][['name', 'stock_quantity']]
        filtered_best_selling = best_selling[best_selling['id'].isin(filtered_products['id'])]
        filtered_stockout_risk = stockout_risk
        filtered_restock_schedule = restock_schedule
        filtered_price_analysis = price_analysis[price_analysis['id'].isin(filtered_products['id'])] if not price_analysis.empty else price_analysis
        
        st.write(f"Showing {total_filtered_products} of {len(products)} products after filtering.")
        
        # Tabs
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        tab1, tab2, tab3 = st.tabs(["Present Metrics", "Visualizations", "Future Insights"])
        
        with tab1:
            st.subheader("Key Present Metrics")
            col1, col2 = st.columns(2)
            col1.markdown(f'<div class="metric">Total Products: {total_filtered_products}</div>', unsafe_allow_html=True)
            col2.markdown(f'<div class="metric">Average Price: ${filtered_product_list["price"].mean():.2f}</div>', unsafe_allow_html=True)
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            
            with st.expander("Product List"):
                if not filtered_product_list.empty:
                    st.dataframe(filtered_product_list, use_container_width=True)
                else:
                    st.write("No products available.")
            
            with st.expander("Best-Selling Products"):
                if not filtered_best_selling.empty:
                    st.dataframe(filtered_best_selling[['name', 'total_sold']], use_container_width=True)
                else:
                    st.write("No best-selling products identified.")
            
            with st.expander("Low Stock Alerts"):
                if not filtered_low_stock.empty:
                    st.dataframe(filtered_low_stock, use_container_width=True)
                else:
                    st.write("No low stock products identified.")
        
        with tab2:
            st.subheader("Visualizations")
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            if not filtered_best_selling.empty:
                fig = px.bar(
                    filtered_best_selling,
                    x='name',
                    y='total_sold',
                    title="Best-Selling Products",
                    color_discrete_sequence=['#4CAF50']
                )
                fig.update_traces(hovertemplate='Product: %{x}<br>Units Sold: %{y}')
                fig.update_layout(xaxis_title="Product", yaxis_title="Units Sold")
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("No best-selling products data available for visualization.")
        
        with tab3:
            st.subheader("Future Insights")
            st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
            with st.expander("Predictive Stockout Risks"):
                st.write("Stockout risks unavailable due to missing order date data.")
            
            with st.expander("Suggested Restocking Schedule"):
                st.write("Restocking schedule unavailable due to missing order date data.")
            
            with st.expander("Price Optimization Suggestions"):
                if not filtered_price_analysis.empty:
                    st.dataframe(filtered_price_analysis[['name', 'price', 'avg_rating', 'total_sold', 'price_adjustment']], use_container_width=True)
                else:
                    st.write("No price optimization suggestions available.")
            
            recommendation = f"Address {len(filtered_low_stock)} low stock products and review pricing for {len(filtered_price_analysis[filtered_price_analysis['price_adjustment'] != 'Maintain']) if not filtered_price_analysis.empty else 0} products."
            st.markdown(f"**Recommendation**: {recommendation}")
        
        # PDF Download
        st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)
        with st.spinner("Generating PDF Report..."):
            pdf_buffer = io.BytesIO()
            doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = [
                Paragraph("Product Analysis Report", styles['Title']),
                Paragraph("Key Present Metrics", styles['Heading2']),
                Spacer(1, 20),
                Paragraph(f"Author: GrowEasy Platform", styles['Normal']),
                Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M %Z')}", styles['Normal']),
                Spacer(1, 20),
            ]
            
            # Product List (Top 5)
            if not filtered_product_list.empty:
                elements.append(Paragraph("Product List (Top 5)", styles['Heading2']))
                data = [['Product', 'Price', 'Stock Quantity']]
                for _, row in filtered_product_list.head(5).iterrows():
                    data.append([row['name'], f"${row['price']:.2f}", str(row['stock_quantity'])])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            # Best-Selling Products
            if not filtered_best_selling.empty:
                elements.append(Paragraph("Best-Selling Products", styles['Heading2']))
                data = [['Product', 'Units Sold']]
                for _, row in filtered_best_selling.head(5).iterrows():
                    data.append([row['name'], str(row['total_sold'])])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            # Low Stock Alerts
            if not filtered_low_stock.empty:
                elements.append(Paragraph("Low Stock Alerts", styles['Heading2']))
                data = [['Product', 'Stock']]
                for _, row in filtered_low_stock.iterrows():
                    data.append([row['name'], str(row['stock_quantity'])])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            # Price Optimization
            if not filtered_price_analysis.empty:
                elements.append(Paragraph("Price Optimization Suggestions", styles['Heading2']))
                data = [['Product', 'Price', 'Avg Rating', 'Units Sold', 'Price Adjustment']]
                for _, row in filtered_price_analysis.head(5).iterrows():
                    data.append([row['name'], f"${row['price']:.2f}", f"{row['avg_rating']:.1f}" if pd.notnull(row['avg_rating']) else 'N/A', str(row['total_sold']), row['price_adjustment']])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f2a44')),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#d3d3d3')),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ]))
                elements.append(table)
                elements.append(Spacer(1, 20))
            
            elements.append(Paragraph("Recommendation", styles['Heading2']))
            elements.append(Paragraph(recommendation, styles['Normal']))
            
            try:
                doc.build(elements)
                pdf_buffer.seek(0)
                st.download_button(
                    label="Download Product Analysis Report",
                    data=pdf_buffer.getvalue(),
                    file_name="Product_Analysis_Report.pdf",
                    mime="application/pdf",
                    key="download_pdf"
                )
            except Exception as e:
                st.error(f"Error generating PDF: {e}")
    
    except ValueError as ve:
        st.error(f"Data validation error: {ve}")
    except Exception as e:
        st.error(f"Error processing data: {e}")