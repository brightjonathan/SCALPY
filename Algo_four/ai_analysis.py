import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.feature_extraction.text import CountVectorizer
import pickle

# Step 1: Prepare Data (convert banner text & port numbers into features)
def prepare_data_for_ai(open_ports, service_info):
    """
    Prepare the input features for AI model training or prediction.
    Args:
        open_ports (list): List of open ports with protocols.
        service_info (list): List of tuples containing port, protocol, service, and banner.

    Returns:
        X (array): Features (port and banner text).
        y (array): Labels (predicted services or vulnerabilities).
    """
    # Initialize lists for features and labels
    port_numbers = []
    banner_texts = []
    
    # Loop through open_ports and service_info
    for (port, protocol), (s_port, s_protocol, service, banner) in zip(open_ports, service_info):
        port_numbers.append(port)
        banner_texts.append(banner)

    # Feature extraction: one-hot encode port numbers and use CountVectorizer for banner text
    vectorizer = CountVectorizer(max_features=100)
    banner_features = vectorizer.fit_transform(banner_texts).toarray()

    # Convert port numbers to a numpy array
    port_array = np.array(port_numbers).reshape(-1, 1)

    # Combine the features into one dataset
    X = np.hstack((port_array, banner_features))

    # In this case, the service is the label we want to predict
    y = np.array([service for _, _, service, _ in service_info])

    return X, y, vectorizer

# Step 2: Load Pre-trained Model or Train Model (if no model exists)
def load_or_train_model(X, y, model_file="port_service_model.pkl"):
    """
    Load a pre-trained model, or train a new model if none exists.
    Args:
        X (array): Features for training the model.
        y (array): Labels for training the model.
        model_file (str): The path to the pre-trained model.

    Returns:
        model: Trained model.
    """
    try:
        # Try loading the pre-trained model from disk
        with open(model_file, 'rb') as file:
            model = pickle.load(file)
        print("Loaded pre-trained model.")
    except FileNotFoundError:
        print("Model not found, training a new one.")
        # Split data into training and test sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Standardize the data
        scaler = StandardScaler()
        X_train = scaler.fit_transform(X_train)
        X_test = scaler.transform(X_test)

        # Train a RandomForestClassifier
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(X_train, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, y_pred))
        print("Classification Report:", classification_report(y_test, y_pred))

        # Save the trained model to disk for future use
        with open(model_file, 'wb') as file:
            pickle.dump(model, file)
        print("Model saved.")
    
    return model

# Step 3: Perform AI-powered analysis on open ports and services
def ai_analysis(open_ports, service_info, model=None):
    """
    Perform AI-powered analysis to predict vulnerabilities or services.
    Args:
        open_ports (list): List of open ports with protocols.
        service_info (list): List of tuples containing port, protocol, service, and banner.
        model: Trained machine learning model (RandomForestClassifier).
    
    Returns:
        predictions (list): Predicted vulnerabilities or services.
    """
    # Prepare the data for the AI model
    X, y, vectorizer = prepare_data_for_ai(open_ports, service_info)

    # If no pre-trained model is passed, load or train the model
    if model is None:
        model = load_or_train_model(X, y)

    # Make predictions
    predictions = model.predict(X)

    # Print the predicted services or vulnerabilities
    for (port, protocol), service, prediction in zip(open_ports, service_info, predictions):
        print(f"Port {port}/{protocol} - Predicted Service: {prediction}")
    
    return predictions

# Step 4: Integrate AI analysis with the results of the port scan
def integrate_ai_with_scan(target, open_ports, service_info):
    """
    Integrates AI analysis into the port scan and service detection results.
    Args:
        target (str): The target host.
        open_ports (list): List of open ports with protocols.
        service_info (list): List of tuples containing port, protocol, service, and banner.
    
    Returns:
        None
    """
    print(f"Performing AI-powered analysis for target: {target}")
    ai_analysis(open_ports, service_info)

