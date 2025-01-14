import os
import yaml
from app.core.logging import logger

def load_template_config():
    logger.info("Loading template configuration")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(current_dir, 'settings.yaml')
    with open(template_path, 'r') as file:
        config = yaml.safe_load(file)
    logger.info("Template configuration loaded successfully")
    return config

def generate_grag_config(user_id, pdf_id):
    # Define base paths
    logger.info(f"Generating grag config for user_id: {user_id}, pdf_id: {pdf_id}")
    
    # Load and update config
    logger.info("Loading template configuration")
    config = load_template_config()
    
    # Set base directory for user-specific data
    base_dir = os.path.join('app', 'data', str(user_id), str(pdf_id))
    logger.info(f"Base directory set to: {base_dir}")
    
    # Define specific directories
    pdf_output_dir = os.path.join(base_dir, 'output')
    pdf_input_dir = os.path.join(base_dir, 'input')
    pdf_cache_dir = os.path.join(base_dir, 'cache')
    pdf_logs_dir = os.path.join(base_dir, 'logs')
    prompt_path = os.path.join('app', 'prompts')
    
    # Create directories if they don't exist
    logger.info("Creating necessary directories")
    for directory in [pdf_output_dir, pdf_input_dir, pdf_cache_dir, pdf_logs_dir]:
        os.makedirs(directory, exist_ok=True)
    logger.info("Directories created successfully")
    
    # Set environment variables
    logger.info("Setting environment variables")
    os.environ['USER_PDF_OUTPUT_DIR'] = pdf_output_dir
    os.environ['USER_PDF_INPUT_DIR'] = pdf_input_dir
    os.environ['USER_PDF_CACHE_DIR'] = pdf_cache_dir
    os.environ['USER_PDF_LOGS_DIR'] = pdf_logs_dir
    os.environ['PROMPT_PATH'] = prompt_path
    
    # Update config settings
    logger.info("Updating configuration settings")
    config['pdf_output_dir'] = pdf_output_dir
    config['pdf_input_dir'] = pdf_input_dir
    config['pdf_cache_dir'] = pdf_cache_dir
    config['pdf_logs_dir'] = pdf_logs_dir
    config['prompt_path'] = prompt_path

    # Save the updated config
    logger.info(f"Saving configuration to {prompt_path}/_dump.yaml")
    dump_path = os.path.join(prompt_path, '_dump.yaml')
    with open(dump_path, 'w') as file:
        yaml.safe_dump(config, file)

    logger.info("Grag configuration generation completed successfully")
    return config
