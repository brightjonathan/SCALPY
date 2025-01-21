import numpy as np
from sklearn.preprocessing import OneHotEncoder
from typing import Dict

def prepare_data_for_analysis(service_info: Dict[int, str]) -> np.ndarray:
    """
    Prepare data for AI analysis by converting banner text and port numbers into input features.

    Args:
        service_info (dict): Dictionary of open ports and their corresponding service banners.

    Returns:
        np.ndarray: Feature matrix ready for AI analysis.

    Raises:
        ValueError: If service_info is not a dictionary or contains invalid data.
    """
    if not isinstance(service_info, dict):
        raise ValueError("service_info must be a dictionary")

    # Extract ports and banners
    try:
        ports = list(service_info.keys())
        banners = list(service_info.values())
    except Exception as e:
        raise ValueError(f"Invalid data in service_info: {e}")

    # Validate ports and banners
    if not all(isinstance(port, int) and 0 <= port <= 65535 for port in ports):
        raise ValueError("All keys in service_info must be valid port numbers (0-65535)")
    if not all(isinstance(banner, str) for banner in banners):
        raise ValueError("All values in service_info must be strings")

    # Prepare one-hot encoding for banners
    encoder = OneHotEncoder(sparse_output=False)  # Updated for newer Scikit-learn versions
    banner_features = encoder.fit_transform(np.array(banners).reshape(-1, 1))

    # Normalize port numbers to range [0, 1]
    port_features = np.array(ports).reshape(-1, 1) / 65535.0

    # Combine port and banner features
    feature_matrix = np.hstack((port_features, banner_features))

    return feature_matrix