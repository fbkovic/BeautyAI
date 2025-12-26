# Deploying Ollama to Hugging Face Spaces

Since Streamlit Cloud doesn't support running Ollama directly (no root access, low resources), we need to host it separately. **Hugging Face Spaces** is a great option.

## 1. Create a Hugging Face Space
1.  Go to [Hugging Face Spaces](https://huggingface.co/spaces).
2.  Click **Create new Space**.
3.  **Name**: `beauty-ai-backend` (or similar).
4.  **License**: `MIT`.
5.  **SDK**: Select **Docker**. (Important!)
6.  **Hardware**: 
    - **Free CPU**: Works, but might be very slow for Llama 3.2.
    - **Paid options**: Much faster if you have credits.
7.  Click **Create Space**.

## 2. Upload Files
You need to upload the `Dockerfile.hf` and `start.sh` I created to this Space.

**Option A: Web Interface**
1.  In your new Space, go to **Files**.
2.  Click **Add file** -> **Upload files**.
3.  Upload `Dockerfile.hf` (rename it to just `Dockerfile` on upload if possible, or edit the content).
    - **Note:** HF expects the file to be named `Dockerfile`.
4.  Upload `start.sh`.
5.  Commit changes.

**Option B: Git (Recommended)**
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/beauty-ai-backend
cd beauty-ai-backend
cp /path/to/your/local/Dockerfile.hf ./Dockerfile
cp /path/to/your/local/start.sh .
git add .
git commit -m "Add Ollama Setup"
git push
```

## 3. Configure Streamlit Cloud
Once your Space is building and running (Status: **Running**), you will get a URL (usually `https://yourname-spacename.hf.space`).

1.  Keep only the base URL: `https://yourname-spacename.hf.space` (without `/tree/main` etc).
2.  Go to your **Streamlit Cloud Dashboard**.
3.  Find your app -> **Settings** -> **Secrets**.
4.  Add this:
```toml
OLLAMA_HOST = "https://yourname-spacename.hf.space"
```
5.  Save. Your app will now talk to the Cloud AI!
