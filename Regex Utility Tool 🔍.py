import streamlit as st
import re  # Import regex module

# Set up page configuration (optional)
st.set_page_config(page_title="Regex Utility Tool", page_icon="🔍")

# Set up the Streamlit interface
st.title("Regex Utility Tool")

# Input text area
st.header("Input Text")
text = st.text_area("Enter the text you want to process:", "The order numbers are 12345, 67890, and 23456. Error occurred at 12:00. Visit us at https://example.com or call (123) 456-7890. Call us at +62 812-3456-7890 or 0812-3456-7890.")

# Input search keyword (for Search Text operation)
search_keyword = st.text_input("Enter the word you want to search for (case-insensitive):", "error")

# Select operation
operation = st.selectbox(
    "Choose an operation:",
    ("Search Text", "Manipulate String", "Extract Data")
)

# Process based on operation
if operation == "Search Text":
    st.header("Search Text")
    
    # Use the user-defined search keyword in regex
    regex = rf"({re.escape(search_keyword)})"  # Define regex pattern with capture group for highlighting
    matches = re.findall(regex, text, re.IGNORECASE)  # Find all matches ignoring case
    
    # Highlight the matches in the original text
    if matches:
        # Replace matched words with a <span> that highlights the word with a blue background
        highlighted_text = re.sub(regex, r'<span style="background-color: lightblue;">\1</span>', text, flags=re.IGNORECASE)
        
        st.write(f"Matches found: {len(matches)}")
        st.write(f"Matched text: {', '.join(matches)}")
        
        # Display the highlighted text using markdown with unsafe_allow_html=True
        st.markdown(f"Original Text with Highlight: {highlighted_text}", unsafe_allow_html=True)
    else:
        st.write("No matches found.")
    
elif operation == "Manipulate String":
    st.header("Manipulate String")
    
    # Dropdown for common string manipulations
    manipulation_option = st.selectbox("Choose a string manipulation operation:",
                                       ["Lowercase text", "Uppercase text", "Remove leading/trailing spaces", 
                                        "Replace spaces with underscores", "Remove all digits", "Replace digits with #", 
                                        "Remove punctuation", "Replace URLs with '[LINK]'"])
    
    # Set regex and replacement based on the selection
    if manipulation_option == "Lowercase text":
        manipulated_text = text.lower()
        count = "N/A"
    elif manipulation_option == "Uppercase text":
        manipulated_text = text.upper()
        count = "N/A"
    elif manipulation_option == "Remove leading/trailing spaces":
        manipulated_text = text.strip()
        count = "N/A"
    elif manipulation_option == "Replace spaces with underscores":
        regex = r"\s+"
        replacement = "_"
        manipulated_text, count = re.subn(regex, replacement, text)
    elif manipulation_option == "Remove all digits":
        regex = r"\d+"
        replacement = ""
        manipulated_text, count = re.subn(regex, replacement, text)
    elif manipulation_option == "Replace digits with #":
        regex = r"\d+"
        replacement = "#"
        manipulated_text, count = re.subn(regex, replacement, text)
    elif manipulation_option == "Remove punctuation":
        regex = r"[^\w\s]"
        replacement = ""
        manipulated_text, count = re.subn(regex, replacement, text)
    elif manipulation_option == "Replace URLs with '[LINK]'":
        regex = r"https?://[^\s]+"
        replacement = "[LINK]"
        manipulated_text, count = re.subn(regex, replacement, text)
    
    # Display the manipulated text and number of replacements if applicable
    st.write(f"Number of replacements made: {count}")
    st.write(f"Manipulated Text: {manipulated_text}")

elif operation == "Extract Data":
    st.header("Extract Data")
    
    # Dropdown for common extraction patterns
    extract_option = st.selectbox("Choose a data extraction operation:",
                                  ["Extract all numbers", "Extract all words", "Extract all email addresses", 
                                   "Extract all URLs", "Extract phone numbers (general format)", "Extract all dates (dd/mm/yyyy)"])
    
    # Set regex based on the selection
    if extract_option == "Extract all numbers":
        regex = r"\d+"
    elif extract_option == "Extract all words":
        regex = r"\b\w+\b"
    elif extract_option == "Extract all email addresses":
        regex = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    elif extract_option == "Extract all URLs":
        regex = r"https?://[^\s]+"
    elif extract_option == "Extract phone numbers (general format)":
        # Regex to capture phone numbers in different formats like +62 812-3456-7890 or 0812-3456-7890
        regex = r"(\+?\d{1,3}[-\s]?\d{2,4}[-\s]?\d{2,4}[-\s]?\d{2,4})"
    elif extract_option == "Extract all dates (dd/mm/yyyy)":
        regex = r"\b\d{2}/\d{2}/\d{4}\b"
    
    # Perform the extraction and show results
    extracted_data = re.findall(regex, text)
    st.write(f"Extracted Data: {extracted_data}")

# Display the original text for reference
st.header("Original Text")
st.write(text)