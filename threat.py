import pandas as pd

# Sample data
data = {
    'id': [1, 2, 3, 4, 5],
    'source_ip': ['192.168.1.1', '192.168.1.2', '192.168.1.3', '192.168.1.4', '192.168.1.5'],
    'destination_ip': ['10.0.0.1', '10.0.0.2', '10.0.0.3', '10.0.0.4', '10.0.0.5'],
    'protocol': ['TCP', 'UDP', 'TCP', 'ICMP', 'TCP'],
    'port': [80, 53, 443, 7, 22],
    'threat_type': ['Safe', 'Safe', 'Safe', 'Safe', 'Safe'],
    'severity': ['Low', 'Low', 'Medium', 'Low', 'Medium']
}

# Create DataFrame
df = pd.DataFrame(data)

# Save to CSV with ISO-8859-1 encoding
df.to_csv('unharmed_threats.csv', index=False, encoding='ISO-8859-1')

