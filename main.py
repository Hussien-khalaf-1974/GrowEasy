# import streamlit as st
# import pandas as pd
# import os

# st.title("GrowEasy: E-Commerce Analytics Platform")

# # Initialize session state for file and filename
# if 'excel_file' not in st.session_state:
#     st.session_state['excel_file'] = None
# if 'filename' not in st.session_state:
#     st.session_state['filename'] = None
# if 'data' not in st.session_state:
#     st.session_state['data'] = None

# st.write("Upload your Excel file to analyze your e-commerce data.")
# uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx"], key="file_uploader")

# # Handle file upload
# if uploaded_file is not None:
#     # Update session state with new file and filename
#     st.session_state['excel_file'] = uploaded_file
#     st.session_state['filename'] = uploaded_file.name
    
#     # Load sheets
#     try:
#         sheets = ['Categories', 'Customer_Sessions', 'Customers', 'Discounts', 'Inventory_Movements', 
#                   'Order_Details', 'Orders', 'Payments', 'Products', 'Returns', 'Reviews', 
#                   'Shipping', 'Suppliers', 'Wishlists']
#         data = {sheet: pd.read_excel(uploaded_file, sheet_name=sheet) for sheet in sheets}
#         st.session_state['data'] = data
#         st.success(f"File '{st.session_state['filename']}' uploaded successfully! Navigate to analysis pages using the sidebar.")
#     except Exception as e:
#         st.error(f"Error loading file: {e}")
#         st.session_state['excel_file'] = None
#         st.session_state['filename'] = None
#         st.session_state['data'] = None

# # Display uploaded file info if it exists
# if st.session_state['filename']:
#     st.info(f"Uploaded file: {st.session_state['filename']}")
# else:
#     st.warning("Please upload an Excel file to proceed.")











# import streamlit as st
# import pandas as pd
# import os

# # Set page configuration for wide layout
# st.set_page_config(layout="wide", page_title="GrowEasy Analytics")

# # Custom CSS for consistent styling across all pages
# st.markdown(
#     """
#     <style>
#     /* General styling */
#     body {
#         font-family: 'Arial', sans-serif;
#     }
#     /* Button styling with hover effect */
#     .stButton>button {
#         background-color: #4CAF50;
#         color: white;
#         border-radius: 8px;
#         padding: 10px 20px;
#         transition: all 0.3s ease;
#         border: none;
#     }
#     .stButton>button:hover {
#         background-color: #45a049;
#         transform: scale(1.05);
#     }
#     /* Fade-in animation for titles */
#     @keyframes fadeIn {
#         0% { opacity: 0; transform: translateY(-20px); }
#         100% { opacity: 1; transform: translateY(0); }
#     }
#     .title {
#         animation: fadeIn 1s ease-in-out;
#         color: #4f627c;
#         font-size: 5em;
#         text-align: center;
#     }
#     /* File uploader styling */
#     .stFileUploader label {
#         color: #34495e;
#         font-weight: bold;
#     }
#     /* Spinner centering */
#     .stSpinner {
#         display: flex;
#         justify-content: center;
#     }
#     /* Sidebar styling */
#     .css-1d391kg {
#         background-color: #f8f9fa;
#     }
#     /* Expander styling */
#     .stExpander {
#         border-radius: 8px;
#         background-color: #45a049;
#         box-shadow: 0 2px 4px rgba(0,0,0,0.1);
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # Animated title
# st.markdown('<div class="title">GrowEasy: E-Commerce Analytics Platform</div>', unsafe_allow_html=True)

# # Initialize session state
# if 'excel_file' not in st.session_state:
#     st.session_state['excel_file'] = None
# if 'filename' not in st.session_state:
#     st.session_state['filename'] = None
# if 'data' not in st.session_state:
#     st.session_state['data'] = None

# # Sidebar for navigation and file upload
# with st.sidebar:
#     st.header("Upload & Navigation")
#     st.write("Upload your Excel file to analyze e-commerce data.")
    
#     # Form for batch processing file upload
#     with st.form(key="upload_form"):
#         uploaded_file = st.file_uploader(
#             "Choose an Excel file",
#             type=["xlsx"],
#             key="file_uploader",
#             help="Upload an Excel file containing sheets like Categories, Orders, etc."
#         )
#         submit_button = st.form_submit_button("Upload File")

# # Handle file upload on form submission
# if submit_button and uploaded_file is not None:
#     with st.spinner("Processing your file..."):
#         # Update session state
#         st.session_state['excel_file'] = uploaded_file
#         st.session_state['filename'] = uploaded_file.name
        
#         # Load sheets
#         try:
#             sheets = ['Categories', 'Customer_Sessions', 'Customers', 'Discounts', 'Inventory_Movements', 
#                       'Order_Details', 'Orders', 'Payments', 'Products', 'Returns', 'Reviews', 
#                       'Shipping', 'Suppliers', 'Wishlists']
#             data = {sheet: pd.read_excel(uploaded_file, sheet_name=sheet) for sheet in sheets}
#             st.session_state['data'] = data
#             st.success(f"File '{st.session_state['filename']}' uploaded successfully! Navigate to analysis pages using the sidebar.")
#         except Exception as e:
#             st.error(f"Error loading file: {e}")
#             st.session_state['excel_file'] = None
#             st.session_state['filename'] = None
#             st.session_state['data'] = None

# # Display uploaded file info
# if st.session_state['filename']:
#     st.info(f"Uploaded file: {st.session_state['filename']}")
#     with st.expander("Quick Stats"):
#         st.write("Select analysis options from the sidebar to view insights.")
# else:
#     st.warning("Please upload an Excel file to proceed.")

# # Sidebar navigation for analysis pages
# with st.sidebar:
#     st.subheader("Analysis Options")
#     analysis_option = st.selectbox(
#         "Choose an analysis",
#         ["Category Analysis", "Customer Analysis", "Product Analysis", "Order Analysis", "Session Analysis", "Query Analysis"],
#         help="Select an analysis to explore your data."
#     )
#     if analysis_option:
#         st.write(f"Selected: {analysis_option}")


















import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# Set page configuration for wide layout
st.set_page_config(layout="wide", page_title="GrowEasy Analytics")

# Custom CSS for consistent styling
st.markdown(
    """
    <style>
    body { font-family: 'Arial', sans-serif; }
    .stButton>button {
        background-color: #4CAF50;
        color: #d3d3d3;
        border-radius: 8px;
        padding: 10px 20px;
        transition: all 0.3s ease;
        border: 1px solid #2c3e50;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
        transform: scale(1.05);
        box-shadow: 0 3px 6px rgba(0,0,0,0.2);
    }
    @keyframes fadeIn { 
        0% { opacity: 0; transform: translateY(-20px); } 
        100% { opacity: 1; transform: translateY(0); } 
    }
    .title { 
        animation: fadeIn 1s ease-in-out; 
        color: #4f627c; 
        font-size: 5em; 
        text-align: center; 
        margin: 30px 0; 
    }
    .stFileUploader label, .stDateInput label, .stSelectbox label {
        color: #000000;
        font-weight: bold;
        font-family: 'Arial', sans-serif;
        margin-top: 15px;
    }
    .stSpinner { display: flex; justify-content: center; }
    .css-1d391kg { background-color: #f8f9fa; }
    .metric {
        animation: fadeIn 1.2s ease-in-out;
        background: linear-gradient(145deg, #141c30, #1f2a44);
        color: #d3d3d3;
        padding: 25px;
        border-radius: 12px;
        border: 1px solid #2c3e50;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        text-align: center;
        margin: 15px 0;
        transition: all 0.3s ease;
        min-height: 200px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .metric:hover {
        transform: scale(1.02);
        border-color: #4CAF50;
        box-shadow: 0 6px 12px rgba(0,0,0,0.3);
    }
    .metric-label {
        font-size: 1.5em;
        color: #a9b7c6;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .metric-value {
        font-size: 3em;
        font-weight: bold;
        color: #d3d3d3;
    }
    .metric-icon {
        font-size: 2em;
        color: #4CAF50;
        margin-bottom: 10px;
    }
    .section-spacer { margin: 20px 0; }
    </style>
    """,
    unsafe_allow_html=True
)

# Animated title
st.markdown('<div class="title">GrowEasy</div>', unsafe_allow_html=True) # : E-Commerce Analytics Platform

# Initialize session state
if 'excel_file' not in st.session_state:
    st.session_state['excel_file'] = None
if 'filename' not in st.session_state:
    st.session_state['filename'] = None
if 'data' not in st.session_state:
    st.session_state['data'] = None

# Sidebar for navigation and file upload
with st.sidebar:
    st.header("Upload & Navigation")
    st.write("Upload your Excel file to analyze e-commerce data.")
    
    with st.form(key="upload_form"):
        uploaded_file = st.file_uploader(
            "Choose an Excel file",
            type=["xlsx"],
            key="file_uploader",
            help="Upload an Excel file containing sheets like Categories, Orders, etc."
        )
        submit_button = st.form_submit_button("Upload File")

    st.subheader("Dashboard Filters")
    date_start, date_end = st.date_input(
        "Select Date Range",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        min_value=datetime(2020, 1, 1),
        max_value=datetime.now(),
        key="date_range"
    )
    st.button("Clear Filters", key="clear_filters", on_click=lambda: st.session_state.update(
        date_range=(datetime.now() - timedelta(days=30), datetime.now())
    ))

# Handle file upload
if submit_button and uploaded_file is not None:
    with st.spinner("Processing your file..."):
        st.session_state['excel_file'] = uploaded_file
        st.session_state['filename'] = uploaded_file.name
        
        try:
            sheets = ['Categories', 'Customer_Sessions', 'Customers', 'Discounts', 'Inventory_Movements',
                      'Order_Details', 'Orders', 'Payments', 'Products', 'Returns', 'Reviews',
                      'Shipping', 'Suppliers', 'Wishlists']
            data = {}
            for sheet in sheets:
                try:
                    data[sheet] = pd.read_excel(uploaded_file, sheet_name=sheet)
                except ValueError:
                    st.warning(f"Sheet '{sheet}' not found in the uploaded file. Some features may be unavailable.")
            st.session_state['data'] = data
            st.success(f"File '{st.session_state['filename']}' uploaded successfully! Navigate to analysis pages using the sidebar.")
        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.session_state['excel_file'] = None
            st.session_state['filename'] = None
            st.session_state['data'] = None

# Dashboard display
if st.session_state['filename']:
    st.info(f"Uploaded file: {st.session_state['filename']}")
    
    # Apply date filter
    start_date = pd.to_datetime(date_start)
    end_date = pd.to_datetime(date_end) + pd.Timedelta(days=1)
    
    # Key Metrics Section
    st.subheader("Key Metrics")
    if st.session_state['data']:
        # Filter Orders by date range
        total_orders = 0
        total_revenue = 0.0
        if 'Orders' in st.session_state['data']:
            orders = st.session_state['data']['Orders']
            if 'order_date' in orders.columns and 'total_amount' in orders.columns:
                orders['order_date'] = pd.to_datetime(orders['order_date'], errors='coerce')
                filtered_orders = orders[
                    (orders['order_date'] >= start_date) & (orders['order_date'] < end_date)
                ]
                total_orders = len(filtered_orders)
                total_revenue = filtered_orders['total_amount'].sum()
        
        # Active Customers (last 30 days within date range)
        active_customers = 0
        if 'Customers' in st.session_state['data'] and 'Orders' in st.session_state['data']:
            customers = st.session_state['data']['Customers']
            if 'id' in customers.columns and 'customer_id' in filtered_orders.columns:
                active_customers = filtered_orders['customer_id'].nunique()
        
        # Display enhanced metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                f"""
                <div class="metric">
                    <div class="metric-icon">🛒</div>
                    <div class="metric-label">Total Orders</div>
                    <div class="metric-value">{total_orders}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col2:
            st.markdown(
                f"""
                <div class="metric">
                    <div class="metric-icon">💰</div>
                    <div class="metric-label">Total Revenue</div>
                    <div class="metric-value">${total_revenue:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        with col3:
            st.markdown(
                f"""
                <div class="metric">
                    <div class="metric-icon">👥</div>
                    <div class="metric-label">Active Customers</div>
                    <div class="metric-value">{active_customers}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
    else:
        st.write("No data available to display metrics.")

else:
    st.warning("Please upload an Excel file to proceed.")

# Sidebar navigation for analysis pages
with st.sidebar:
    st.subheader("Analysis Options")
    analysis_option = st.selectbox(
        "Choose an analysis",
        ["Category Analysis", "Customer Analysis", "Product Analysis", "Order Analysis", "Session Analysis", "Query Analysis"],
        help="Select an analysis to explore your data."
    )
    if analysis_option:
        st.write(f"Selected: {analysis_option}")

st.markdown('<div class="section-spacer"></div>', unsafe_allow_html=True)