# Saizme: The Dynamic Image Transformation API

<p align="center">
  <img src="https://placehold.co/600x300/1e293b/ffffff?text=Saizme+API&font=raleway" alt="Saizme API Banner">
</p>

**Saizme** is a powerful backend service that provides a flexible API to upload and dynamically transform your photography for a perfect fit anywhere. Instead of saving countless versions of an image, you store one original and generate variations on-the-fly using simple URL parameters.

It's built with Python and Flask, containerized with Docker, and designed with a clean, modular architecture that allows you to easily switch between storage backends.

---
## ✨ Features

* **On-the-Fly Transformations:** Never store another thumbnail. Generate images in real-time.
* **Dynamic Resizing & Padding:** Change width (`w`), height (`h`), and add padded borders.
* **Smart Cropping & Fitting:** Use `fit=crop` for exact dimensions or `fit=contain` to preserve aspect ratio.
* **Perfect Fit:** Automatically trim empty space around an image and add uniform padding.
* **Creative Filters:** Apply effects like `grayscale` and `sepia`.
* **Artistic Effects:** Add a `blur` effect with adjustable intensity.
* **Modular Storage:** Defaults to local filesystem for easy development, with full support for Google Cloud Storage for production.
* **Extensible by Design:** A clean adapter pattern makes it simple to add new storage providers (like AWS S3 or Azure Blob).

---
## 🚀 Running the Application

You can run this application in two modes.

### Option 1: Quick Local Setup (Recommended for First-Time Users)

This method is ideal for quick local testing without needing a cloud account. Files will be saved to a `local_uploads` directory inside the Docker container.

1.  **Configure for Local Storage:**
    * Create a `.env` file by copying the example: `cp .env.example .env`
    * Ensure the `.env` file is set to `local`:
        ```dotenv
        STORAGE_PROVIDER=local
        ```

2.  **Build and Run with Docker:**
    * Build the image:
        ```sh
        docker build -t saizme-app .
        ```
    * Run the container, mounting only the `.env` file:
        ```sh
        docker run \
          -p 8080:8080 \
          -d \
          --name saizme \
          -v "$(pwd)/.env:/app/.env" \
          saizme-app
        ```

### Option 2: Full GCS Setup (Production-Ready)

Follow these steps for a complete deployment using Google Cloud Storage.

#### **Step 1: Google Cloud Configuration**

*(Follow the detailed steps from the previous README version to create a GCS bucket, make it public, create a service account, grant it permissions, and download the JSON key file.)*

1.  Move the downloaded key file to `credentials/` and rename it to `gcs-key.json`.

#### **Step 2: Local Project Setup**

1.  **Create Environment File:**
    * `cp .env.example .env`

2.  **Edit `.env` File:**
    * Open `.env` and configure it for GCS. **Replace `your-gcs-bucket-name` with your actual bucket name.**
    ```dotenv
    STORAGE_PROVIDER=gcs
    GCS_BUCKET_NAME="your-gcs-bucket-name"
    GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/gcs-key.json
    ```

#### **Step 3: Build and Run with Docker**

1.  **Build the Image:**
    * `docker build -t saizme-app .`

2.  **Run the Container:**
    * This command mounts both the configuration and credential files into the container.
    ```sh
    docker run \
      -p 8080:8080 \
      -d \
      --name saizme \
      -v "$(pwd)/.env:/app/.env" \
      -v "$(pwd)/credentials/gcs-key.json:/app/credentials/gcs-key.json" \
      saizme-app
    ```

---
## 📖 API Usage

The API is simple: upload an image to get an ID, then use that ID to view and transform it.

### 1. Upload an Image

Send a `POST` request with your image file to the `/api/upload` endpoint.

```sh
curl -X POST -F "file=@/path/to/your/photo.jpg" http://localhost:8080/api/upload

✅ **Example Success Response:**

```json
{
  "success": true,
  "image_id": "original-image-0ba8ed42-46cb-4158-9d31-edd6a18cc792.png",
  "message": "Image uploaded successfully."
}
```

### 2. View and Transform the Image

Use a `GET` request to the `/api/view/<image_id>` endpoint. Add query parameters to the URL to apply transformations.

#### Available Transformations:

| Parameter | Values | Description |
|-----------|--------|-------------|
| `w` | integer | Sets the width for resizing the source image. |
| `h` | integer | Sets the height for resizing the source image. |
| `fit` | `crop`, `contain` | **crop**: Resizes and crops to exact w & h.<br>**contain**: Fits within w & h, preserving aspect ratio. |
| `perfect_fit` | integer | Trims empty space and adds uniform padding of this many pixels. |
| `pad_w` | integer | Sets the width of the final padded canvas. |
| `pad_h` | integer | Sets the height of the final padded canvas. |
| `pad_color` | color name or hex | Sets the background color for canvas padding. |
| `filter` | `grayscale`, `sepia` | Applies a color filter. |
| `blur` | integer (1-50) | Applies a Gaussian blur effect. |

#### Examples:

**Crop to a 200x200 square:**
```
http://localhost:8080/api/view/your-image-id.png?w=200&h=200&fit=crop
```

**Trim whitespace, add 20px padding, then resize result to 500px wide:**
```
http://localhost:8080/api/view/your-image-id.png?perfect_fit=20&w=500
```

**Fit image within 300x300, then place on a 400x400 black canvas:**
```
http://localhost:8080/api/view/your-image-id.png?w=300&h=300&pad_w=400&pad_h=400&pad_color=black
```

🔧 Extending the Application
The modular design makes it easy to add new storage backends (e.g., AWS S3).

Create Your Adapter Class:

In app/storage/, create a new file (e.g., s3_adapter.py).

Your class must implement the StorageInterface and have save() and read() methods.

Update the Storage Factory:

In app/storage/__init__.py, import your new class and add it to the get_storage_adapter() function with a new provider name (e.g., s3).

Update Your Configuration:

Add any new required environment variables (e.g., AWS_ACCESS_KEY_ID) to your .env files.

Set STORAGE_PROVIDER=s3 in your .env to activate your new adapter.