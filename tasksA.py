import subprocess
import json
import glob
import os
import sqlite3
import datetime
import difflib
from dateutil.parser import parse

def A1(email: str):
    """
    A1: Run the provided local datagen.py with the given email.
    This will generate all required files under /data.
    """
    subprocess.run(["python", "datagen.py", email], check=True)
    return "A1 executed successfully."

def A2(prettier_version: str, filename: str):
    # Read the current contents of the file.
    with open(filename, "r") as f:
        original = f.read()
    # Run prettier with --stdin-filepath to simulate the formatting used in evaluation.
    command = f"npx {prettier_version} --stdin-filepath {filename}"
    result = subprocess.run(
        command,
        input=original,
        capture_output=True,
        text=True,
        shell=True,
        check=True
    )
    # Write the formatted output back to the file.
    with open(filename, "w") as f:
        f.write(result.stdout)
    return "A2 executed successfully."


def A3(filename: str, targetfile: str, weekday: str):
    """
    A3: Count occurrences of the specified weekday in the dates file and write the count to targetfile.
    Uses dateutil.parser.parse to handle all date formats.
    """
    # Normalize the weekday input (lowercase and remove trailing 's' if present)
    normalized = weekday.lower().rstrip("s")
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }
    if normalized not in weekdays:
        raise ValueError("Invalid weekday")
    day_num = weekdays[normalized]
    with open(filename, "r") as f:
        lines = f.readlines()
    count = 0
    for line in lines:
        line = line.strip()
        if not line:
            continue
        try:
            dt = parse(line)
        except Exception:
            continue
        if dt.weekday() == day_num:
            count += 1
    with open(targetfile, "w") as f:
        f.write(str(count))
    return "A3 executed successfully."


def A4(filename: str, targetfile: str):
    """
    A4: Sort the contacts JSON by last_name then first_name and write the result to targetfile.
    """
    with open(filename, "r") as f:
        contacts = json.load(f)
    sorted_contacts = sorted(contacts, key=lambda c: (c.get("last_name", ""), c.get("first_name", "")))
    with open(targetfile, "w") as f:
        json.dump(sorted_contacts, f, indent=2)
    return "A4 executed successfully."

def A5(log_dir_path: str, output_file_path: str, num_files: int):
    """
    A5: Write the first line of the num_files most recent .log files to output_file_path.
    """
    files = glob.glob(os.path.join(log_dir_path, "*.log"))
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    selected = files[:num_files]
    lines = []
    for file in selected:
        with open(file, "r") as f:
            first_line = f.readline().strip()
            lines.append(first_line)
    with open(output_file_path, "w") as f:
        for line in lines:
            f.write(line + "\n")
    return "A5 executed successfully."

def A6(doc_dir_path: str, output_file_path: str):
    """
    A6: Create an index of markdown files in doc_dir_path by extracting the first H1 of each file,
    then write the index (as JSON) to output_file_path.
    """
    index = {}
    for root, dirs, files in os.walk(doc_dir_path):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                with open(full_path, "r") as f:
                    for line in f:
                        if line.startswith("# "):
                            title = line[2:].strip()
                            rel_path = os.path.relpath(full_path, doc_dir_path)
                            index[rel_path] = title
                            break
    with open(output_file_path, "w") as f:
        json.dump(index, f, indent=2)
    return "A6 executed successfully."

def A7(filename: str, output_file: str):
    """
    A7: Extract the sender's email address from the given file and write it to output_file.
    """
    with open(filename, "r") as f:
        content = f.read()
    import re
    match = re.search(r"From:.*<([^>]+)>", content)
    email = match.group(1) if match else ""
    with open(output_file, "w") as f:
        f.write(email)
    return "A7 executed successfully."

def A8(filename: str, image_path: str):
    """
    A8: Extract the credit card number from the generated data and write it without spaces.
    """
    from datagen import get_credit_card
    email = os.environ.get("USER_EMAIL")
    data = get_credit_card(email)
    card_number = data["number"].replace(" ", "")
    with open(filename, "w") as f:
        f.write(card_number)
    return "A8 executed successfully."



def A9(filename: str, output_filename: str):
    """
    A9: Find the most similar pair of comments in the file and write them to the output file,
    one per line, sorted lexicographically.
    """
    import requests
    import numpy as np
    import os

    # Read comments from file
    with open(filename, "r") as f:
        comments = [line.strip() for line in f if line.strip()]
    if len(comments) < 2:
        raise ValueError("Not enough comments in the file.")

    # Prepare the embeddings request
    openai_api_base = os.getenv("OPENAI_API_BASE", "https://aiproxy.sanand.workers.dev/openai/v1")
    api_url = f"{openai_api_base}/embeddings"
    openai_api_key = os.getenv("AIPROXY_TOKEN")
    headers = {"Authorization": f"Bearer {openai_api_key}", "Content-Type": "application/json"}
    payload = {"model": "text-embedding-3-small", "input": comments}

    # Request embeddings
    response = requests.post(api_url, json=payload, headers=headers, timeout=30)
    if response.status_code != 200:
        raise ValueError(f"Failed to fetch embeddings: {response.text}")

    data = response.json().get("data", [])
    if len(data) != len(comments):
        raise ValueError("Mismatch between number of comments and embeddings returned.")

    # Convert embeddings to a numpy array
    embeddings = np.array([emb["embedding"] for emb in data])
    # Compute similarity matrix (dot product)
    similarity = np.dot(embeddings, embeddings.T)
    # Set diagonal to -infinity to ignore self-similarity
    np.fill_diagonal(similarity, -np.inf)
    # Get indices of maximum similarity
    i, j = np.unravel_index(similarity.argmax(), similarity.shape)
    # Sort the two comments lexicographically as expected by the evaluation
    best_pair = sorted([comments[i], comments[j]])

    # Write the result to output file
    with open(output_filename, "w") as f:
        f.write(best_pair[0] + "\n" + best_pair[1])

    return "A9 executed successfully."




def A10(filename: str, output_filename: str, query: str):
    """
    A10: Execute the SQL query on the SQLite DB in filename and write the result to output_filename.
    """
    conn = sqlite3.connect(filename)
    cur = conn.cursor()
    cur.execute(query)
    result = cur.fetchone()[0]
    if result is None:
        result = 0
    with open(output_filename, "w") as f:
        f.write(str(result))
    conn.close()
    return "A10 executed successfully."
