import pandas as pd
import matplotlib.pyplot as plt
import os

# Define paths (Ensure correct capitalization for Linux)
data_path = "data/blinks_movements.csv"
output_dir = "output"
output_graph = os.path.join(output_dir, "cognitive_load_graph.png")

# Ensure output directory exists
try:
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
except PermissionError:
    print(f"❌ Permission denied: Unable to create {output_dir}. Check your access rights!")
    exit(1)

try:
    # Ensure the data file exists
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"File not found at {data_path}")

    # Load CSV file
    df = pd.read_csv(data_path)

    # Validate required columns
    required_columns = {"Time Interval", "Blinks", "Eye Movements"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing required columns. Expected: {required_columns}, Found: {set(df.columns)}")

    # Drop any rows with missing values in required columns
    df = df.dropna(subset=["Time Interval", "Blinks", "Eye Movements"])

    # Convert timestamp to string if needed
    df["Time Interval"] = df["Time Interval"].astype(str)

    # Compute cognitive load as a weighted sum of blinks and eye movements
    alpha = 0.7  # Weight for blinks
    beta = 0.3   # Weight for eye movements
    df["Cognitive Load"] = alpha * df["Blinks"] + beta * df["Eye Movements"]

    # Plot cognitive load over time
    plt.figure(figsize=(12, 6))
    plt.plot(df["Time Interval"], df["Cognitive Load"], marker='o', linestyle='-', color='b', label="Cognitive Load")
    plt.axhline(y=0.6, color="r", linestyle="--", label="Overload Threshold")

    plt.xlabel("Time Interval")
    plt.ylabel("Cognitive Load")
    plt.title("Cognitive Load Over Time")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save graph
    plt.savefig(output_graph)
    plt.close()
    print(f"✅ Graph saved at: {output_graph}")

except FileNotFoundError as e:
    print(f"❌ Error: {e}")

except PermissionError:
    print(f"❌ Permission denied: Cannot access {output_graph}. Check file permissions!")

except pd.errors.EmptyDataError:
    print("❌ Error: The CSV file is empty.")

except pd.errors.ParserError:
    print("❌ Error: Failed to parse the CSV file. Check its format!")

except Exception as e:
    print(f"❌ Unexpected Error: {e}")
