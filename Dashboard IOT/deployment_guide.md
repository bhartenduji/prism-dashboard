# Deployment Guide: PRISM Dashboard on Vercel

Follow these steps to take your PRISM Dashboard live on the web using Vercel.

## Prerequisites
1.  A **GitHub** account.
2.  A **Vercel** account (connected to your GitHub).
3.  **Git** installed on your local machine.

---

## Step 1: Initialize Git and Push to GitHub
Open your terminal in the project directory (`c:\Users\anubh\Downloads\Dashboard IOT`) and run the following commands:

1.  **Initialize Git:**
    ```bash
    git init
    ```
2.  **Add all files:**
    ```bash
    git add .
    ```
3.  **Commit the changes:**
    ```bash
    git commit -m "Initial PRISM Dashboard Deployment"
    ```
4.  **Create a new repository on GitHub** (e.g., named `prism-dashboard`).
5.  **Link and Push:** (Replace the URL with your actual GitHub repo URL)
    ```bash
    git remote add origin https://github.com/YOUR_USERNAME/prism-dashboard.git
    git branch -M main
    git push -u origin main
    ```

---

## Step 2: Deploy on Vercel
1.  Go to the [Vercel Dashboard](https://vercel.com/dashboard).
2.  Click **"Add New..."** > **"Project"**.
3.  Select your `prism-dashboard` repository from the list.
4.  **Configuration:**
    - Vercel will automatically detect the Python environment because of `requirements.txt` and `app.py`.
    - Ensure the **Framework Preset** is set to "Other" (it usually detects this automatically).
    - You don't need to change any build commands.
5.  Click **"Deploy"**.

---

## Step 3: Verify the Live Dashboard
1.  Once the deployment is complete, Vercel will provide you with a production URL (e.g., `prism-dashboard.vercel.app`).
2.  Open the URL in your browser.
3.  **Important**: Since Vercel uses serverless functions, the in-memory data (parking slots) will reset if the site isn't visited for a while. This is normal for a free-tier deployment.

---

## Step 4: Connecting your Hardware (Arduino/ESP32)
To send data to your live dashboard, you must update your hardware code to point to the new URL:

- **Local URL (Previous)**: `http://192.168.x.x:5000/update-slot`
- **Vercel URL (New)**: `https://your-app-name.vercel.app/update-slot`

> [!WARNING]
> Ensure your hardware library supports **HTTPS**, as Vercel enforces SSL. If you are using an ESP32 or Arduino R4, use the secure client library (`WiFiClientSecure`).

---

## Troubleshooting
- **ModuleNotFoundError**: Ensure `requirements.txt` contains `flask` and `flask-cors`.
- **404 Errors**: Check if `vercel.json` is correctly routing all traffic to `app.py`.
- **Deployment Failed**: Check the "Build Logs" in Vercel for specific Python errors.

---
**Your PRISM Dashboard is now globally accessible!**
