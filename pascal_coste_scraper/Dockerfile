# Use official python runtime as a parent image
FROM python:3.9

# Select the working directory
WORKDIR /app/pascalcoste

# Copy the current directory contents to the conatiner at /app/pascalcoste
COPY . .

# Run the command to insall all the requirements.txt
RUN pip install -r requirements.txt

# Copy startup script
COPY startup.sh .

# Make the startup script executable
RUN chmod +x startup.sh

# Run the startup script when container launches
CMD ["./startup.sh"]