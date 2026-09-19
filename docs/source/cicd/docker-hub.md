# Docker Hub Image Publishing

The production Docker image is built and published to Docker Hub.

## Target Repository & Tag
- **Docker Hub Repository**: `deepakkumar889/bmw-service-rag`
- **Tag**: `latest`

## Pulling & Running the Published Image

```bash
# Pull the latest published image
docker pull deepakkumar889/bmw-service-rag:latest

# Run container linking to host Ollama
docker run -d -p 8000:8000 \
  -e OLLAMA_BASE_URL=http://host.docker.internal:11434 \
  -e OLLAMA_MODEL=qwen2.5:1.5b \
  --name bmw-service-rag \
  deepakkumar889/bmw-service-rag:latest
```

## GitHub Secrets for Docker Hub Deployment
- `DOCKERHUB_USERNAME`: ${{ secrets.DOCKERHUB_USERNAME }}
- `DOCKERHUB_TOKEN`: ${{ secrets.DOCKERHUB_TOKEN }}
