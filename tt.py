# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt

# # Example: Define gene IDs and a sample data matrix.
# # Make sure that the number of gene IDs equals the number of columns in data_matrix.
# gene_ids = ["Gene1", "Gene2", "Gene3", "Gene4", "Gene5", "Gene6", "Gene7", "Gene8", "Gene9"]

# # Example data_matrix where each inner list represents one sample's expression values for 9 genes.
# data_matrix = [
#     [74, 221, 180, 72, 77, 51, 58, 62, 70],  # Sample 1
#     [39, 198, 468, 31, 22, 26, 35, 31, 39],  # Sample 2
#     [62, 839, 258, 69, 54, 36, 35, 121, 16],  # Sample 3
#     [66, 219, 318, 58, 51, 66, 53, 47, 46],   # Sample 4
#     [26, 182, 317, 30, 32, 26, 31, 33, 39]    # Sample 5
#     # Add additional samples as needed
# ]

# # Verify the dimensions of data_matrix and the number of gene IDs
# data_matrix = np.array(data_matrix)
# print("Data matrix shape:", data_matrix.shape)
# print("Number of gene IDs:", len(gene_ids))

# if data_matrix.shape[1] != len(gene_ids):
#     raise ValueError("The number of gene IDs must match the number of columns in the data matrix.")

# # Create sample names based on the number of samples (rows in data_matrix)
# sample_names = [f"Sample{i+1}" for i in range(data_matrix.shape[0])]

# # Create DataFrame: rows will represent samples and columns represent genes
# df = pd.DataFrame(data_matrix, columns=gene_ids, index=sample_names)

# # Optionally, if you prefer genes as rows and samples as columns, simply transpose the DataFrame:
# df_transposed = df.T

# # Plot a heatmap of the gene expression data.
# plt.figure(figsize=(10, 8))
# sns.heatmap(df_transposed, cmap="RdBu_r", annot=True, fmt="d")
# plt.title("Gene Expression Heatmap")
# plt.xlabel("Samples")
# plt.ylabel("Genes")
# plt.show()

from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# URL of the deployed model API
API_URL = "http://your-api-url.com/predict"

# HTML template defined as a string
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Genomic Data Analysis</title>
    <!--=============== FAVICON ===============-->
      <link rel="shortcut icon" href="assets/img/logo2.png" type="image/x-icon" style="border-radius:50%;">

      <!--=============== REMIXICONS ===============-->
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/remixicon/4.2.0/remixicon.css">

      <!--=============== CSS ===============-->
      <link rel="stylesheet" href="styles.css">
    <link rel="stylesheet" href="index.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.2.1/css/fontawesome.min.css">
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link  rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.2/css/fontawesome.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.4.2/css/fontawesome.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@700&family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,700;0,900;1,300;1,400;1,700;1,900&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f6f9;
            margin: 0;
            padding: 0;
            color: #333;
        }

        header {
            background-color: #2d3e50;
            color: white;
            padding: 20px 0;
            text-align: center;
        }

        h1 {
            margin: 0;
            font-size: 2.5rem;
        }

        .container {
            width: 80%;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            font-size: 1.1rem;
            margin-bottom: 8px;
            display: inline-block;
        }

        input[type="file"] {
            font-size: 1rem;
            padding: 10px;
            border: 2px solid #ddd;
            border-radius: 5px;
            width: 100%;
            background-color: #f9f9f9;
        }

        .button {
            background-color: #007bff;
            color: white;
            font-size: 1rem;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            width: 100%;
            transition: background-color 0.3s;
        }

        .button:hover {
            background-color: #0056b3;
        }

        h2 {
            color: #333;
            margin-top: 30px;
        }

        pre {
            background-color: #f1f1f1;
            padding: 15px;
            border-radius: 5px;
            white-space: pre-wrap;
            word-wrap: break-word;
            font-family: 'Courier New', Courier, monospace;
            font-size: 1rem;
            color: #333;
        }
        a{
            text-decoration:none;
            color:#000
        }
        .result-container {
            padding: 20px;
            background-color: #e9f5ff;
            border: 2px solid #b3d7ff;
            border-radius: 8px;
        }
    </style>
</head>
<body>

    <header>
        <h1>Genomic Data Analysis</h1>
    </header>

    <div class="container">
        <form action="/predict" method="POST" enctype="multipart/form-data">
            <div class="form-group">
                <label for="genomic_file">Upload Genomic Data File:</label>
                <input type="file" name="genomic_file" id="genomic_file" required>
            </div>
          <div type="submit" class="button"><a href="https://drive.google.com/file/d/1NTE1OgLmkkL1ua7LaVlnm61jUIsvNr4O/view?usp=sharing">Submit for Prediction</a></div>
        </form>

        {% if result %}
        <div class="result-container">
            <h2>Prediction Results:</h2>
            <pre>{{ result | tojson }}</pre>
        </div>
        {% endif %}
    </div>

</body>
</html>

"""

@app.route("/")
def home():
    return render_template_string(html_template)

@app.route("/predict", methods=["POST"])
def predict():
    # Ensure a file was submitted
    if "genomic_file" not in request.files:
        return "No file part", 400

    file = request.files["genomic_file"]

    if file.filename == "":
        return "No selected file", 400

    # Send the file to the model API
    response = requests.post(API_URL, files={"file": file})
    
    if response.status_code == 200:
        result = response.json()
        return render_template_string(html_template, result=result)
    else:
        return "Error in prediction", 500

if __name__ == "__main__":
    app.run(debug=True)
