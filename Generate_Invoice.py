#====================================================================================================================================
# Installation Libraries
#====================================================================================================================================
import pandas as pd
import streamlit as st
import locale

#====================================================================================================================================
# Global variables for merged table and inventory table
#====================================================================================================================================
merged_table = pd.DataFrame()  # Initialize an empty DataFrame
inventory_table = pd.DataFrame()  # Initialize an empty DataFrame

#====================================================================================================================================
# HTML Styling Section
#====================================================================================================================================
html_and_css = """
<style>
    .reportview-container {
        flex-direction: row-reverse;
    }

    header > .toolbar {
        flex-direction: row-reverse;
        left: 1rem;
        right: auto;
    }

    .sidebar .sidebar-collapse-control {
        left: auto;
        right: 0.5rem;
    }

    .sidebar.--collapsed .sidebar-collapse-control {
        left: auto;
        right: 0.5rem;
    }

    .sidebar .sidebar-content {
        transition: margin-right 0.3s, box-shadow 0.3s;
    }

    body {
        background-color: Green;
    }

    .sidebar.--collapsed .sidebar-content {
        margin-left: auto;
        margin-right: -21rem;
    }

    @media (max-width: 991.98px) {
        .sidebar .sidebar-content {
            margin-left: auto;
        }
    }
</style>
"""

# Display the HTML and CSS content
st.markdown(html_and_css, unsafe_allow_html=True)

# Streamlit UI
st.markdown("<h2 style='text-align: center;'>Good Company Invoice Generator</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Version 1.0.24 App</p>", unsafe_allow_html=True)

#====================================================================================================================================
# Create a navigation menu in the sidebar
#====================================================================================================================================
page = st.sidebar.selectbox("Select a Page", ["Merged Table", "Inventory Table", "Show Both"])

#====================================================================================================================================
# Sidebar for user input
#====================================================================================================================================
desired_customer_name = st.sidebar.text_input("Enter Customer Name:", 'Cable Rack')

#====================================================================================================================================
# File uploader for new data for Merged Table
#====================================================================================================================================
new_file_merged = st.sidebar.file_uploader("Upload a new Excel/CSV file for Merged Table")

#====================================================================================================================================
# File uploader for new data for Inventory Table
#====================================================================================================================================
new_file_inventory = st.sidebar.file_uploader("Upload a new Excel/CSV file for Inventory Table")

#====================================================================================================================================
# Function to generate the pivot table for MERGED TABLE
#====================================================================================================================================
def generate_merged_table(desired_customer_name, new_file, merged_table):
    if new_file:
        try:
            # Read the new file, detect the file format, and read it into a DataFrame
            if new_file.name.endswith('.csv'):
                new_data = pd.read_csv(new_file, low_memory=False)
            elif new_file.name.endswith(('.xls', '.xlsx')):
                new_data = pd.read_excel(new_file, low_memory=False)
            else:
                st.error("Unsupported file format. Please upload a CSV or Excel file.")
                return

            # Concatenate the new data with the existing data
            merged_table = pd.concat([merged_table, new_data], ignore_index=True)

            # Rename columns
            merged_table.rename(columns={
                'Customer name (customer)': 'Customer',
                'Fee (charge)': 'Description',
                'Quantity (charge)': 'Quantity',
                'Total (charge)': 'Total'
            }, inplace=True)

            # Convert the 'Quantity' and 'Total' columns to numeric types (float)
            merged_table['Quantity'] = pd.to_numeric(merged_table['Quantity'], errors='coerce')
            merged_table['Total'] = pd.to_numeric(merged_table['Total'], errors='coerce')

            # Ensure that 'Customer' values are stripped of leading/trailing whitespaces
            merged_table['Customer'] = merged_table['Customer'].str.strip()

            # Filter the data to show only the specified customer
            customer_data = merged_table[merged_table['Customer'].str.lower() == desired_customer_name.lower()]

            # Check if any data is found for the specified customer
            if customer_data.empty:
                st.warning(f"No data found for customer '{desired_customer_name}' in MERGED TABLE.")
            else:
                # Set locale for currency formatting
                locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

                # Create a pivot table to show 'Customer,' 'Description,' 'Quantity,' and 'Total'
                pivot_table_desired_customer = customer_data.pivot_table(
                    index=['Customer', 'Description'],
                    values=['Quantity', 'Total'],
                    aggfunc='sum'
                )

                # Reset the index to make it look cleaner
                pivot_table_desired_customer.reset_index(inplace=True)

                # Calculate the grand total of 'Quantity' and 'Total'
                grand_total_quantity_desired_customer = pivot_table_desired_customer['Quantity'].sum()
                grand_total_total_desired_customer = pivot_table_desired_customer['Total'].sum()

                # Format the 'Quantity' column with two decimal places
                pivot_table_desired_customer['Quantity'] = pivot_table_desired_customer['Quantity'].apply(
                    lambda x: f'{x:,.2f}'
                )

                # Format the 'Total' column with currency in the pivot table
                pivot_table_desired_customer['Total'] = pivot_table_desired_customer['Total'].apply(
                    lambda x: f"${x:,.2f}"
                )

                # Format the grand total for 'Quantity' with two decimal places and commas
                grand_total_quantity_desired_customer = '{:,.2f}'.format(grand_total_quantity_desired_customer)

                # Format the grand total for 'Total' with currency
                grand_total_total_desired_customer = locale.currency(grand_total_total_desired_customer, grouping=True)

                # Add a row for Grand Total to the pivot table
                grand_total_row = pd.DataFrame({
                    'Customer': ['Grand Total'],
                    'Description': [''],
                    'Quantity': [grand_total_quantity_desired_customer],
                    'Total': [grand_total_total_desired_customer]
                })

                pivot_table_desired_customer = pd.concat([pivot_table_desired_customer, grand_total_row])

                # Display the pivot table using Streamlit with left alignment
                st.subheader(f"Pivot Table for {desired_customer_name} in MERGED TABLE:")
                st.table(pivot_table_desired_customer)

                # Display a success message
                st.success("Merged Table imported successfully.")

        except pd.errors.ParserError:
            st.error("Invalid file format. Please upload a valid CSV or Excel file.")
        except Exception as e:
            st.error(f"An error occurred while processing the Merged Table: {str(e)}")

#====================================================================================================================================
# Function to generate the pivot table for INVENTORY TABLE
#====================================================================================================================================
def generate_inventory_table(desired_customer_name, new_file, inventory_table):
    if new_file:
        try:
            # Read the new file, detect the file format, and read it into a DataFrame
            if new_file.name.endswith('.csv'):
                new_data = pd.read_csv(new_file, low_memory=False)
            elif new_file.name.endswith(('.xls', '.xlsx')):
                new_data = pd.read_excel(new_file, low_memory=False)
            else:
                st.error("Unsupported file format. Please upload a CSV or Excel file.")
                return

            # Concatenate the new data with the existing data
            inventory_table = pd.concat([inventory_table, new_data], ignore_index=True)

            # Continue with the rest of your code after the 'try' block
            # Strip spaces from both sides of the '3PL Customer' column
            inventory_table['3PL Customer'] = inventory_table['3PL Customer'].str.strip()
            desired_customer_name_inventory = desired_customer_name.strip()

            # Check if '3PL Customer' column exists in the DataFrame
            if '3PL Customer' not in inventory_table.columns:
                st.warning("The '3PL Customer' column is not found in the INVENTORY TABLE.")
                return

            # Filter the DataFrame for the specific customer
            desired_customer_data_inventory = inventory_table[inventory_table['3PL Customer'] == desired_customer_name_inventory]

            # Pivot the DataFrame to get the sum of 'On Hand' and 'Allocated'
            pivot_table_inventory = desired_customer_data_inventory.pivot_table(
                index='3PL Customer',
                values=['On Hand', 'Allocated'],
                aggfunc='sum'
            )

            # Reset the index to make it look cleaner
            pivot_table_inventory.reset_index(inplace=True)

            # Calculate and display the grand total of 'On Hand' and 'Allocated' with commas
            grand_total_on_hand_inventory = '{:,.2f}'.format(desired_customer_data_inventory['On Hand'].sum())
            grand_total_allocated_inventory = '{:,.2f}'.format(desired_customer_data_inventory['Allocated'].sum())

            # Format the 'Allocated' column with two decimal places
            pivot_table_inventory['Allocated'] = pivot_table_inventory['Allocated'].apply(
                lambda x: f'{x:,.2f}'
            )

            # Format the 'On Hand' column with two decimal places
            pivot_table_inventory['On Hand'] = pivot_table_inventory['On Hand'].apply(
                lambda x: f'{x:,.2f}'
            )

           # Remove commas and convert to float
            grand_total_on_hand_inventory = float(grand_total_on_hand_inventory.replace(',', ''))
            grand_total_allocated_inventory = float(grand_total_allocated_inventory.replace(',', ''))

           # Format the grand total with commas and two decimal places
            grand_total_on_hand_inventory = '{:,.2f}'.format(grand_total_on_hand_inventory)
            grand_total_allocated_inventory = '{:,.2f}'.format(grand_total_allocated_inventory)


            # Add a row for Grand Total to the pivot table
            grand_total_row_inventory = pd.DataFrame({
                '3PL Customer': ['Grand Total'],
                'On Hand': [grand_total_on_hand_inventory],  # Format to two decimal places
                'Allocated': [grand_total_allocated_inventory]  # Format to two decimal places
})


            pivot_table_inventory = pd.concat([pivot_table_inventory, grand_total_row_inventory])

            # Display the pivot table using Streamlit with left alignment
            st.subheader("Pivot Table for 'On Hand' and 'Allocated' in INVENTORY TABLE:")
            st.table(pivot_table_inventory)

            # Display a success message
            st.success("Inventory Table imported successfully.")

        except pd.errors.ParserError:
            st.error("Invalid file format. Please upload a valid CSV or Excel file.")
        except Exception as e:
            st.error(f"An error occurred while processing the Inventory Table: {str(e)}")

#====================================================================================================================================
# Generate tables based on user input
#====================================================================================================================================
if page == "Merged Table":
    generate_merged_table(desired_customer_name, new_file_merged, merged_table)
elif page == "Inventory Table":
    generate_inventory_table(desired_customer_name, new_file_inventory, inventory_table)
elif page == "Show Both":
    generate_merged_table(desired_customer_name, new_file_merged, merged_table)
    generate_inventory_table(desired_customer_name, new_file_inventory, inventory_table)
