import asyncio
import graphrag.api as api
from graphrag.index.typing import PipelineRunResult
from graphrag.config.create_graphrag_config import create_graphrag_config
import yaml
import os

try:
    with open("settings.yaml", "r") as config_file:
        settings = yaml.safe_load(config_file)
except FileNotFoundError:
    print("Error: 'settings.yaml' not found.")
    exit(1)
except yaml.YAMLError as e:
    print(f"Error parsing 'settings.yaml': {e}")
    exit(1)

# Update prompt_path to current directory's prompts path
current_prompts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "z_input\prompts")

# Add check if prompts directory exists
if not os.path.exists(current_prompts_path):
    print(f"Error: Prompts directory not found at {current_prompts_path}")
    exit(1)

# Set PROMPT_PATH environment variable and update settings
os.environ['PROMPT_PATH'] = current_prompts_path
settings['prompt_path'] = current_prompts_path

#print(settings)

# Dump updated settings to _dump.yaml
try:
    with open('_dump.yaml', 'w') as dump_file:
        yaml.dump(settings, dump_file, default_flow_style=False)
    print("Updated settings saved to _dump.yaml")
except Exception as e:
    print(f"Error saving settings dump: {e}")

try:
    graphrag_config = create_graphrag_config(values=settings, root_dir="./")
except Exception as e:
    print(f"Error initializing GraphRAG: {e}")
    exit(1)

async def process_indexing():
    try:
        index_result: list[PipelineRunResult] = await api.build_index(config=graphrag_config)
        for workflow_result in index_result:
            status = f"error\n{workflow_result.errors}" if workflow_result.errors else "success"
            print(f"Workflow Name: {workflow_result.workflow}\tStatus: {status}")

    except Exception as e:
        print(f"An error occurred while processing the PDF: {e}")

# Main logic
if __name__ == "__main__":
    asyncio.run(process_indexing())
    # import pandas as pd

    # # Load a Parquet file into a DataFrame
    # df = pd.read_parquet("output/create_final_community_reports.parquet")
    # df.to_csv("output/final_communitiy_reports.csv", index=False)
