# Use a specific version of Python to ensure stability  
FROM python:3.8-slim  

# Set the working directory  
WORKDIR /app  

# Copy only requirements.txt first to leverage Docker cache  
COPY requirements.txt ./  

# Install dependencies (this layer will be cached if requirements.txt does not change)  
RUN pip install --no-cache-dir -r requirements.txt  

# Copy the rest of the application code  
COPY . .  

# Run the main_telegram_bot.py application  
CMD ["python", "main_telegram_bot.py"]
