# GDG Certificate Automation Tool

A professional certificate generation automation tool designed for Google Developer Groups (GDG) Chapter Leaders. This tool simplifies the process of creating and distributing certificates for events, workshops, and hackathons.

## About the Tool

The GDG Certificate Automation Tool is a Streamlit-based application that allows community leaders to:
- **Bulk Generate Certificates**: Upload an Excel roster and a certificate template to generate hundreds of certificates in seconds.
- **Visual Customization**: visually position participant names on the certificate using a coordinate picker.
- **Preview**: Real-time preview of the generated certificate before processing.
- **Secure Processing**: Runs locally or in a secure container; no data is stored permanently.

## How to Deploy

### Option 1: Docker (Recommended)

You can run the application in a self-contained environment using Docker.

1.  **Build the image:**
    ```bash
    docker build -t gdg-cert-tool .
    ```

2.  **Run the container:**
    ```bash
    docker run -p 8501:8501 gdg-cert-tool
    ```

3.  Access the tool at `http://localhost:8501`.

### Option 2: Streamlit Cloud

1.  Push this repository to GitHub.
2.  Log in to [Streamlit Community Cloud](https://streamlit.io/cloud).
3.  Click "New app" and select your repository.
4.  Set the main file path to `app.py`.
5.  Click "Deploy".

## Security

### Regional Access Keys
This tool employs a **Regional Access Key** system to restrict access to authorized GDG leads only. 
- Ensure you possess the valid access keys for your region before deployment.
- Access keys should be managed via environment variables or a secure secrets manager in a production environment.

## Legal Warning

**Copyright © Mohammed Robae**

This work is licensed under the **Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International (CC BY-NC-ND 4.0)** License.

**You are free to:**
- **Share** — copy and redistribute the material in any medium or format.

**Under the following terms:**
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made.
- **NonCommercial** — You may not use the material for commercial purposes.
- **NoDerivatives** — If you remix, transform, or build upon the material, you may not distribute the modified material.

> [!WARNING]
> **Unauthorized Commercial Use is Prohibited.**
> Ownership of this tool belongs to **Mohammed Robae**. Any attempt to sell, sublicense, or monetize this code without explicit permission is a violation of the license terms.
