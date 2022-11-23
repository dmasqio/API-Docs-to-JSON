from flask import Flask, render_template, request, Response
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', response={})

@app.route('/convert', methods=['POST'])
def convert():
    # Get the API documentation from the form
    api_doc = request.form['api_doc']

    # Convert the API documentation into a structured JSON format
    endpoint_json = convert_api_doc_to_json(api_doc)

    # Return the JSON as a text box value
    return render_template('index.html', response=endpoint_json)

@app.route('/download', methods=['POST'])
def download():
    data = request.form['data']  # This should be the JSON data you want to download
    
    # Generate a unique filename based on the current timestamp and example response
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"api_data_{timestamp}.json"
    
    response = Response(
        json.dumps(data),
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment;filename={filename}'}
    )
    return response

def convert_api_doc_to_json(api_doc):
    # Split the API documentation into lines
    lines = api_doc.split("\n")

    # Extract the HTTP method and endpoint from the first line
    http_method_and_endpoint = lines[0].strip()

    # Extract the curl command from the second line
    curl_command = lines[1].strip()

    # Extract the example response from the third line
    example_response = lines[2].strip()

    # Extract the description from the fourth line
    description = lines[3].strip()

    # Extract the parameters from the remaining lines
    parameters_text = lines[4:]

    # Split the parameters text into individual parameters
    parameters = []
    for line in parameters_text:
        if "\t" in line:
            parts = line.split("\t")
            if len(parts) >= 3:
                name = parts[0].strip()
                required = parts[1].strip().lower() == 'yes'
                param_description = parts[2].strip()
                # Remove "(true/false)" from the description
                param_description = param_description.replace("(true/false)", "").strip()
                parameters.append({"name": name, "required": required, "description": param_description})

    # Return the structured JSON
    endpoint_json = {
        "http_method_and_endpoint": http_method_and_endpoint,
        "curl_command": curl_command,
        "example_response": example_response,
        "description": description,
        "parameters": parameters
    }

    # Save the JSON to a file in the 'trainings' directory
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"trainings/api_data_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(endpoint_json, f)

    return endpoint_json
    # Split the API documentation into lines
    lines = api_doc.split("\n")

    # Extract the HTTP method and endpoint from the first line
    http_method_and_endpoint = lines[0].strip()

    # Extract the curl command from the second line
    curl_command = lines[1].strip()

    # Extract the example response from the third line
    example_response = lines[2].strip()

    # Extract the description from the fourth line
    description = lines[3].strip()

    # Extract the parameters from the remaining lines
    parameters_text = lines[4:]

    # Split the parameters text into individual parameters
    parameters = []
    for line in parameters_text:
        if "\t" in line:
            parts = line.split("\t")
            if len(parts) >= 3:
                name = parts[0].strip()
                required = parts[1].strip().lower() == 'yes'
                param_description = parts[2].strip()
                # Remove "(true/false)" from the description
                param_description = param_description.replace("(true/false)", "").strip()
                parameters.append({"name": name, "required": required, "description": param_description})

    # Save the JSON to a file in the 'trainings' directory
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"trainings/api_data_{timestamp}.json"
    with open(filename, 'w') as f:
        json.dump(endpoint_json, f)

    # Return the structured JSON
    return {
        "http_method_and_endpoint": http_method_and_endpoint,
        "curl_command": curl_command,
        "example_response": example_response,
        "description": description,
        "parameters": parameters
    }

if __name__ == '__main__':
    app.run(debug=True)
