# Deploying on local machine
1. Clone the repository
2. Set terminal working directory as Cloned repository

# Build instructions

```bash
sudo docker build -t my_docker_flask:latest .
```

# Run instructions 
The app is binded to port 5000

```bash
sudo docker run -p 5000:5000 my_docker_flask:latest 
```

# Check if the container is running

```bash
sudo docker ps
```
# Working command 
Go to the below page & run the app!
```bash
http://0.0.0.0:5000/get_response_form
```

In the candidates string box enter all the candidate strings separated by commas (that's how its being split & preprocessed). 
```
eg: hello, i hate spinach, christmas is in december, iphone 12 will launch this year,..... 
```

