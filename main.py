import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
password = "2401"
with st.sidebar:
    st.image("broker.png",width=200)
# Streamlit app
menu = st.sidebar.radio("Menu", ["Employee Details", "Graph Analysis"])
st.title('Employee Performance Analysis')
uploaded_file = None
password_input = st.text_input("Enter Password:", type="password")
access_granted = False  # Initialize access as denied
if password_input == password:
    st.success("Access granted.")
    access_granted = True  # Set access as granted
else:
    st.error("Incorrect password. Please enter the correct password to upload a file.")

if access_granted:
   uploaded_file = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file is not None:
    file_extension = uploaded_file.name.split('.')[-1].lower()  # Extract the file extension

    if file_extension == 'csv':
        df = pd.read_csv(uploaded_file)
    elif file_extension == 'xlsx':
        df = pd.read_excel(uploaded_file)
    else:
        st.error("Unsupported file format. Please upload a CSV or Excel file.")

    # Sidebar filters
    st.sidebar.header('Filters')
    selected_department = st.sidebar.selectbox('Select Department', df['Department'].unique())
    selected_employee_code = st.sidebar.text_input('Enter EMP CODE')
    DaysConsumed = st.sidebar.radio('Select Time Period', ['Monthly', 'Weekly', 'Daily'])

    # Data filtering based on department
    filtered_df = df[df['Department'] == selected_department]

    # Filter based on entered employee code
    if selected_employee_code:
        selected_employee_code = int(selected_employee_code)  # Convert input to integer
        filtered_df = filtered_df[filtered_df['EMP CODE'] == selected_employee_code]
    total_weight = filtered_df['Weight'].sum()
    total_polished_weight = filtered_df['Polished Weight'].sum()
    total_estimate_weight = filtered_df['Estimate Weight'].sum()
    st.sidebar.write(f'Total Weight: {total_weight:.2f}')
    st.sidebar.write(f'Total Polished Weight: {total_polished_weight:.2f}')
    st.sidebar.write(f'Total Estimate Weight: {total_estimate_weight:.2f}')

    # Calculate performance based on time period
    if DaysConsumed == 'Monthly':
        performance_metric = 'polished per Month'
        time_period_days = 1
    elif DaysConsumed == 'Weekly':
        performance_metric = 'polished per Week'
        time_period_days = 7
    elif DaysConsumed == 'Daily':
        performance_metric = 'polished per Day'
        time_period_days = 30

    filtered_df[performance_metric] = filtered_df['Issue Pcs'] / time_period_days

    # Clear Filters button
    if st.sidebar.button('Clear Filters'):
        selected_department = None
        selected_employee_code = None
        DaysConsumed = None

    # Display the filtered data with additional columns
    st.write(f'Performance Metrics for {selected_department} Department ({DaysConsumed}):')
    st.dataframe(filtered_df[['Employee Name', 'Lot Id', 'Lot Name', 'Polished Weight', 'Weight', 'Issue Pcs', 'Color', 'Clarity', performance_metric]])


    # Performance Summary
    st.sidebar.header('Performance Summary')
    average_performance = filtered_df[performance_metric].mean()
    total_performance = filtered_df['Receive Pcs'].sum()

    # Total Unique Employee Count
    total_unique_employees = filtered_df['Employee Name'].nunique()

    # Display employee name, grade, and other details
    if not filtered_df.empty:
        employee_name = filtered_df['Employee Name'].iloc[0]
        grade = filtered_df['Grade'].iloc[0]
        Specialist = filtered_df['Specialist'].iloc[0]
        st.sidebar.write(f'Employee Name: {employee_name}')
        st.sidebar.write(f'Grade: {grade}')
        st.sidebar.write(f'Specialist: {Specialist}')

    st.sidebar.write(f'Average {performance_metric}: {average_performance:.2f}')
    st.sidebar.write(f'Total Diamonds Polished: {total_performance}')
    st.sidebar.write(f'Total Unique Employees: {total_unique_employees}')

if menu == "Graph Analysis":
    if uploaded_file is not None:
        if st.button("Show Qty by Specialist Pie Chart"):
            st.set_option('deprecation.showPyplotGlobalUse', False)
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))  # Create two subplots: one for the pie chart and one for the column chart

            # Create a rectangular border around the entire figure
            border = plt.Rectangle((0.25, -0.5), 1.5, 2, color='white', fill=False, linewidth=2)
            ax1.add_patch(border)

            qty_by_specialist = filtered_df.groupby('Specialist')['Qty'].sum()
            labels = qty_by_specialist.index
            sizes = qty_by_specialist

            # Plot the pie chart
            patches, texts, autotexts = ax1.pie(
                sizes,
                labels=labels,
                autopct='%1.1f%%',
                startangle=150,
                textprops={'fontsize': 20}
            )
            ax1.set_title('Qty by Specialist')

            # Plot the clustered column chart for "Qty by Shape" with data labels
            shape_qty = filtered_df.groupby('Shape')['Qty'].sum()
            x = np.arange(len(shape_qty))
            width = 0.40
            ax2.bar(x, shape_qty, width, label='Qty by Shape')
            ax2.set_xlabel('Shape')
            ax2.set_ylabel('Qty')
            ax2.set_title('Qty by Shape')
            ax2.set_xticks(x)
            ax2.set_xticklabels(shape_qty.index)
            ax2.legend()

            for i, v in enumerate(shape_qty):
                ax2.text(i, v, str(v), ha='center', va='bottom', fontsize=15)

            plt.tight_layout()

            st.pyplot()
if menu == "Graph Analysis":
    if uploaded_file is not None:
       if st.button("Show Clustered Column Charts"):
        polished_weight_by_shape = filtered_df.groupby('Shape')['Polished Weight'].sum()
        qty_by_clarity = filtered_df.groupby('Clarity')['Qty'].sum()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))  # Create two subplots side by side

        # Left subplot: Polished Weight by Shape
        x1 = np.arange(len(polished_weight_by_shape))
        width = 0.4
        ax1.bar(x1 - width/2, polished_weight_by_shape, width, label='Polished Weight by Shape')
        ax1.set_xlabel('Shape')
        ax1.set_ylabel('Polished Weight')
        ax1.set_title('Polished Weight by Shape')
        ax1.set_xticks(x1)
        ax1.set_xticklabels(polished_weight_by_shape.index)
        ax1.legend()

        for i, v in enumerate(polished_weight_by_shape):
            ax1.text(i - width/2, v, f'{v:.2f}', ha='center', va='bottom', fontsize=10)

        # Right subplot: Qty by Clarity
        x2 = np.arange(len(qty_by_clarity))
        ax2.bar(x2 - width/2, qty_by_clarity, width, label='Qty by Clarity', color='orange')
        ax2.set_xlabel('Clarity')
        ax2.set_ylabel('Qty')
        ax2.set_title('Qty by Clarity')
        ax2.set_xticks(x2)
        ax2.set_xticklabels(qty_by_clarity.index)
        ax2.legend()

        for i, v in enumerate(qty_by_clarity):
            ax2.text(i - width/2, v, str(v), ha='center', va='bottom', fontsize=10)

        plt.tight_layout()

        st.pyplot()
if menu == "Graph Analysis":
    if uploaded_file is not None:
       if st.button("Show Charts"):
        qty_by_color = filtered_df.groupby('Color')['Qty'].sum()
        unique_employees_by_grade = filtered_df.groupby('Grade')['Employee Name'].nunique()

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))  # Create two subplots side by side

        # Left subplot: Qty by Color Clustered Column Chart (as you already have)
        x1 = np.arange(len(qty_by_color))
        width = 0.4
        ax1.bar(x1 - width/2, qty_by_color, width, label='Qty by Color', color='blue')
        ax1.set_xlabel('Color')
        ax1.set_ylabel('Qty')
        ax1.set_title('Qty by Color')
        ax1.set_xticks(x1)
        ax1.set_xticklabels(qty_by_color.index)
        ax1.legend()

        for i, v in enumerate(qty_by_color):
            ax1.text(i - width/2, v, str(v), ha='center', va='bottom', fontsize=10)

        # Right subplot: Count of Unique Employee Names by Grade with Area Chart
        grades = unique_employees_by_grade.index
        employee_counts = unique_employees_by_grade.values
        ax2.fill_between(grades, employee_counts, color='green', alpha=0.7)
        ax2.plot(grades, employee_counts, marker='o', color='green', label='Unique Employees by Grade')
        ax2.set_xlabel('Grade')
        ax2.set_ylabel('Unique Employees')
        ax2.set_title(' Employees by Grade')
        ax2.legend()

        for i, count in enumerate(employee_counts):
            ax2.text(grades[i], count, str(count), ha='center', va='bottom', fontsize=10)

        plt.tight_layout()

        st.pyplot()





# Add your code for creating and displaying graphs here
# (Code for creating and displaying graphs can be added here)

