import streamlit as st
import re
import pickle
from sklearn.preprocessing import LabelEncoder

# Load the trained Random Forest model
loaded_random_forest_model = pickle.load(open('RandomForestClassifier.pkl', 'rb'))

# Regular expression patterns
ip_pattern = r'(^\S+\.[\S+\.]+\S+)\s'
timestamp_pattern = r'\[(\w+)/(\d{2})/(\d{4}):(\d{2}):(\d{2}):(\d{2})\s\+\d{4}\]'
request_pattern = r'\"(\S+)\s(\S+)\s*(\S*)\"'
status_pattern = r'(\d{3})'
size_pattern = r'\s(\d+) "'
protocol_pattern = r'HTTP/([\d.]+)'

# Function to preprocess log data
def preprocess_log(log_text):
    ip = None
    timestamp = None
    request_line = None
    status_code = None
    size = None
    protocol_encoded = None
    anomaly_detected = False  # Initialize anomaly detection flag

    if log_text:
        # Apply regular expressions to extract relevant information
        ip_match = re.search(ip_pattern, log_text)
        if ip_match:
            ip = ip_match.group(1)
        
        timestamp_match = re.search(timestamp_pattern, log_text)
        if timestamp_match:
            timestamp = timestamp_match.group(0)  # Use the full timestamp
        
        request_line_match = re.search(request_pattern, log_text)
        if request_line_match:
            request_line = request_line_match.group(0)  # Use the full request line
            protocol = request_line.split()[2]
            protocol_encoder = LabelEncoder()
            protocol_encoded = protocol_encoder.fit_transform([protocol])[0]
        
        status_match = re.search(status_pattern, log_text)
        if status_match:
            status_code = int(status_match.group(1))
        
        size_match = re.search(size_pattern, log_text)
        if size_match:
            size = int(size_match.group(1))
        
        # Example anomaly detection logic (you can customize this)
        if size > 10000:
            anomaly_detected = True
    
    # Return anomaly detection result
    return anomaly_detected

# Streamlit UI
st.set_page_config(page_title="Log Anomaly Detection", layout="wide")
st.title("Log Anomaly Detection App")
st.sidebar.title("Navigation")

# Sidebar navigation
tabs = ["Home", "Anomaly Detection"]
selected_tab = st.sidebar.radio("Go to", tabs)

# Home tab
if selected_tab == "Home":
    st.write("Welcome to the Log Anomaly Detection App!")

# Anomaly Detection tab
elif selected_tab == "Anomaly Detection":
    st.write("Detect anomalies in your log data:")
    
    # User input for log text
    user_input = st.text_area("Enter log text:", "")
    
    if st.button("Detect Anomaly"):
        if user_input:
            # Detect anomaly
            anomaly_detected = preprocess_log(user_input)
            
            # Display anomaly detection result
            if anomaly_detected:
                st.write("Anomaly Detected: Yes")
            else:
                st.write("Anomaly Detected: No")

# Run the app
if __name__ == '__main__':
    st.sidebar.markdown("Anomaly Detection App")
