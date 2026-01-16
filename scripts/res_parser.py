import json
import glob
import os
import pandas as pd


SEARCH_DIR = "eval_res"
OUTPUT_CSV = "eval_res/DoRA_Evaluation_Summary.csv"

def parse_and_summarize(directory):
    json_files = glob.glob(os.path.join(directory, "*.json"))
    
    if not json_files:
        print(f"No JSON files found in {directory}. Please check the path.")
        return

    summary_data = []

    print(f"Processing {len(json_files)} files...")

    for filepath in json_files:
        filename = os.path.basename(filepath)
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                print(f"Skipping {filename}: Not a list.")
                continue
                
            total = len(data)
            if total == 0:
                print(f"Skipping {filename}: Empty file.")
                continue

            # Calculate Accuracy
            correct = sum(1 for entry in data if entry.get('flag') is True)
            accuracy = (correct / total) * 100

            summary_data.append({
                "File Name": filename,
                "Total Questions": total,
                "Correct": correct,
                "Accuracy (%)": round(accuracy, 2)
            })

        except Exception as e:
            print(f"Error reading {filename}: {e}")

    # 2. Create DataFrame and Export
    if summary_data:
        df = pd.DataFrame(summary_data)
        df = df.sort_values(by="File Name")
        
        # Save to CSV
        df.to_csv(OUTPUT_CSV, index=False)
        
        print("\n" + "="*40)
        print(f"Successfully saved results to: {OUTPUT_CSV}")
        print("="*40)
        print(df.to_string(index=False)) # Print a preview
    else:
        print("No valid data found to export.")

# Run the function
parse_and_summarize(SEARCH_DIR)