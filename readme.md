# How to run
Use python 3.10+ to run
```
    # After cloning the github repository, cd into directory
    # create a venv
    > python -m venv ./venv
    # activating venv in windows
    > .\Venv\Scripts\Activate.ps1
    # install requirements
    > pip install -r requirements.txt
    # run development server
    > uvicorn main:app --reload --port 8000
```
# Using Docker Containers
If you are building using the docker container and have mongodb installed locally,
then you would want to change the `.env` file in the configuration and set 
`MONGO_URI=mongodb://host.docker.internal:27017/`. Then if you have docker installed,
you can do the following commands:
```
    # build docker image, after cd into directory.
    > docker image build -t pj-userservice .
    # run the image as a docker container, in interactive terminal mode.
    # you can remove -it if you want to run it in background
    > docker container run -p 8000:8000 -it --name pj-userservice-container pj-userservice
```
## Restarting the container
```
    # stop the running container
    > docker container kill pj-userservice-container
    # prune/remove the stopped container
    > docker container prune
    # check running containers
    > docker container ls -a
```