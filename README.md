# Deploying on local machine
clone the repository
set terminal working directory as cloned repository

# Build instructions

```bash
sudo docker build -t my_docker_flask:latest .
```

# Run instructions 

```bash
sudo docker run -p 5000:5000 my_docker_flask:latest 
```

# Check if the container is running

```bash
sudo docker ps
```
# Working command 
```bash
http://0.0.0.0:5000/get_response_form
```

