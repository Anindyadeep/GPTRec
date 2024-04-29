# GPT4Rec

Using LLMs to enhance Recommendation Systems. An application to get the movies of your desire.

## How to set up the server

You can manually build the dependencies on the server, or just use docker to build the environment using this command:

```bash
# Go to server/ folder 
cd server

# Build the image
docker build -t gpt4rec-server:v1 -f Dockerfile.local .
```

This should build the image, and now run the server using this command:

```bash
docker run --gpus all -d -p 8000:8000 gpt4rec-server:v1
```
