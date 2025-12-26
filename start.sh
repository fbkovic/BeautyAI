#!/bin/bash

# Start Ollama in the background
ollama serve &

# Wait for Ollama to start
echo "Waiting for Ollama to start..."
sleep 5

# Pull the model (this happens every time the container starts, strictly speaking we should bake it in, but this is easier for now)
echo "Pulling llama3.2..."
ollama pull llama3.2

# Output for debugging
echo "Ollama is running!"

# Keep the container running
wait
