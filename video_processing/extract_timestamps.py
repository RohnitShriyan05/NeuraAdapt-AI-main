import pandas as pd
import numpy as np
import os

# Define paths
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, "../data/blinks_movements.csv")  # Ensure correct file name
output_path = os.path.join(script_dir, "../output/timestamps.txt")

print(f"📌 Using Data Path: {data_path}")

try:
    # Load data
    df = pd.read_csv(data_path)

    # Ensure the required columns exist
    required_columns = {"Time Interval", "Blinks", "Eye Movements"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"❌ Error: Missing required columns! Expected: {required_columns}, Found: {set(df.columns)}")

    # Compute cognitive load
    alpha = 0.7
    beta = 0.3
    df["Cognitive Load"] = alpha * df["Blinks"] + beta * df["Eye Movements"]

    # Find timestamps where Cognitive Load crosses the threshold (0.6)
    threshold = 0.6
    overload_timestamps = df.loc[df["Cognitive Load"] > threshold, "Time Interval"]

    # Ensure output directory exists
    os.makedirs(os.path.join(script_dir, "../output"), exist_ok=True)

    # Save extracted timestamps to a file
    with open(output_path, "w") as f:
        for ts in overload_timestamps:
            f.write(str(ts) + "\n")

    print(f"✅ Overload timestamps saved to {output_path}")

except FileNotFoundError:
    print(f"❌ Error: {data_path} not found!")
except ValueError as ve:
    print(str(ve))
except Exception as e:
    print(f"❌ Unexpected Error: {e}")
