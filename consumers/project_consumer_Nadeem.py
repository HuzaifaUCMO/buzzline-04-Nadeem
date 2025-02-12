"""
project_consumer_nadeem.py
--------------------------
A file-based consumer that reads JSON messages from a local file written
by the unmodified producer `project_producer_case.py`. For each new message,
we compute the average sentiment and update a real-time line chart.

Author: Nadeem
"""
import json
import time
import os
import matplotlib.pyplot as plt

# Path to the file where the producer writes messages
DATA_FILE = "data/project_producer_case.json"

# Global variables to keep track of sentiment info
message_count = 0
total_sentiment = 0.0
average_sentiment_values = []

# Set up Matplotlib in interactive mode
plt.ion()
fig, ax = plt.subplots()

def update_chart():
    """Updates the Matplotlib chart with the latest average sentiment."""
    ax.clear()
    ax.set_title("Average Sentiment Over Time - Nadeem")
    ax.set_xlabel("Number of Messages")
    ax.set_ylabel("Average Sentiment (0.0 - 1.0)")

    ax.plot(average_sentiment_values, color='blue', marker='o')
    plt.pause(0.001)

def process_message(record: dict):
    """
    Extracts the 'sentiment' field from the JSON record and updates
    the running average.
    """
    global message_count, total_sentiment

    sentiment = record.get("sentiment", 0.0)
    message_count += 1
    total_sentiment += sentiment

    average = total_sentiment / message_count
    average_sentiment_values.append(average)

    # Update the chart to reflect the new average
    update_chart()

def main():
    """
    Continuously reads new lines in DATA_FILE. Each line is expected to be valid JSON.
    For each line, we process the message and update the chart in real time.
    """
    print("Starting file-based consumer... Press Ctrl+C to exit at any time.")

    # Keep track of how many lines we've already processed
    lines_processed = 0

    try:
        while True:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                # Process any new lines that haven't been processed yet
                while lines_processed < len(lines):
                    line = lines[lines_processed].strip()
                    lines_processed += 1

                    if not line:
                        continue  # skip empty lines

                    try:
                        record = json.loads(line)
                        process_message(record)
                    except json.JSONDecodeError:
                        # If there's a parsing error, skip this line
                        pass

            # Sleep briefly before checking the file again
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nShutting down consumer.")
    finally:
        # Turn off interactive mode and display final chart
        plt.ioff()
        plt.show()

if __name__ == "__main__":
    main()
