#=======================================================================================================================================================================
# Import necessary libraries
#=======================================================================================================================================================================

import os
import streamlit as st
import pandas as pd
from datetime import datetime

#=======================================================================================================================================================================
# Streamlit UI
#=======================================================================================================================================================================

st.title("File Uploader Example")

# Sidebar for selecting export folder
st.sidebar.title("Options")

# File uploader for selecting multiple files
files = st.sidebar.file_uploader("Import CSV or Excel Files", type=['csv', 'xlsx'], accept_multiple_files=True, key='file_selector')

# Button to merge files in the sidebar
merge_button = st.sidebar.button("Merge Files")

# Display the list of selected files with their sizes
if files:
    st.write(f"Number of Files Imported: {len(files)}")
    st.write("Selected Files:")
    for file in files:
        file_size = len(file.getvalue()) / (1024 * 1024)  # Convert to MB
        st.write(f"{file.name}\n{file_size:.1f}MB")

#=======================================================================================================================================================================
# Logic to merge files when the button is clicked
#=======================================================================================================================================================================

if merge_button and files:
    try:
        # Merging logic (example: concatenating CSV files)
        df_list = [pd.read_csv(file) for file in files]
        merged_df = pd.concat(df_list, ignore_index=True)

        # Generate the current date to include in the file name
        current_date = datetime.now().strftime("%Y-%m-%d")

        # Save the merged file with the date in the file name
        merged_file_path = f"merged_file_{current_date}.csv"
        merged_df.to_csv(merged_file_path, index=False)

        st.success(f"Files merged successfully! Merged file saved as {merged_file_path}")

        # You can perform additional processing on the merged_df if needed
    except Exception as e:
        st.error(f"An error occurred while merging files: {str(e)}")
elif merge_button and not files:
    st.sidebar.warning("Please select one or more CSV or Excel files.")
