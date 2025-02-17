from flask import Flask, request, jsonify
import os
import subprocess
from datetime import datetime
import json

app = Flask(__name__)

# Define the base directory
BASE_DIR = "/mnt/c/Users/ABHIJITH VS/OneDrive/Documents/TDS/Project 1/LLM-based-Automation-Agent/dataworks-agent"

def run_task(task_description):
    try:
        if "format" in task_description and "prettier" in task_description:
            result = subprocess.run(["npx", "prettier", "--write", os.path.join(BASE_DIR, "data/format.md")], capture_output=True, text=True)
            if result.returncode == 0:
                return {"status": "success", "message": "File formatted successfully."}
            else:
                return {"status": "error", "message": result.stderr}
        elif "count wednesdays" in task_description and "dates" in task_description:
            return count_wednesdays()
        elif "sort contacts" in task_description:
            return sort_contacts()
        elif "extract recent logs" in task_description:
            return extract_recent_logs()
        elif "generate report" in task_description:
            return generate_report()
        elif "backup data" in task_description:
            return backup_data()
        elif "delete temporary files" in task_description:
            return delete_temp_files()
        # Add more task handlers here
        return {"status": "error", "message": "Unknown task."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def count_wednesdays():
    try:
        with open(os.path.join(BASE_DIR, 'data/dates.txt'), 'r') as file:
            dates = file.readlines()
        wednesdays = sum(1 for date in dates if datetime.strptime(date.strip(), '%Y-%m-%d').weekday() == 2)
        with open(os.path.join(BASE_DIR, 'data/dates-wednesdays.txt'), 'w') as file:
            file.write(str(wednesdays))
        return {"status": "success", "message": "Wednesdays counted successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def sort_contacts():
    try:
        with open(os.path.join(BASE_DIR, 'data/contacts.json'), 'r') as file:
            contacts = json.load(file)
        sorted_contacts = sorted(contacts, key=lambda x: (x['last_name'], x['first_name']))
        with open(os.path.join(BASE_DIR, 'data/contacts-sorted.json'), 'w') as file:
            json.dump(sorted_contacts, file, indent=4)
        return {"status": "success", "message": "Contacts sorted successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def extract_recent_logs():
    try:
        log_dir = os.path.join(BASE_DIR, 'data/logs')
        log_files = [f for f in os.listdir(log_dir) if f.endswith('.log')]
        log_files.sort(key=lambda x: os.path.getmtime(os.path.join(log_dir, x)), reverse=True)
        recent_logs = log_files[:10]
        with open(os.path.join(BASE_DIR, 'data/logs-recent.txt'), 'w') as outfile:
            for log_file in recent_logs:
                with open(os.path.join(log_dir, log_file), 'r') as infile:
                    first_line = infile.readline().strip()
                    outfile.write(first_line + '\n')
        return {"status": "success", "message": "Recent logs extracted successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def generate_report():
    try:
        report_content = "Report Generated Successfully\n"
        with open(os.path.join(BASE_DIR, 'data/report.txt'), 'w') as file:
            file.write(report_content)
        return {"status": "success", "message": "Report generated successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def backup_data():
    try:
        subprocess.run(["cp", "-r", os.path.join(BASE_DIR, "data"), os.path.join(BASE_DIR, "data_backup")], check=True)
        return {"status": "success", "message": "Data backed up successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def delete_temp_files():
    try:
        temp_dir = os.path.join(BASE_DIR, 'data/temp')
        for file_name in os.listdir(temp_dir):
            file_path = os.path.join(temp_dir, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return {"status": "success", "message": "Temporary files deleted successfully."}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.route('/run', methods=['POST'])
def run():
    task_description = request.args.get('task')
    result = run_task(task_description)
    if result["status"] == "success":
        return jsonify(result), 200
    elif "Unknown task" in result["message"]:
        return jsonify(result), 400
    else:
        return jsonify(result), 500

@app.route('/read', methods=['GET'])
def read():
    file_path = request.args.get('path')
    try:
        with open(os.path.join(BASE_DIR, file_path[1:]), 'r') as file:
            content = file.read()
        return content, 200
    except FileNotFoundError:
        return '', 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
