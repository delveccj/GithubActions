# GithubActions
CI/CD for newbies!

Here is a simple Flask server.  

Running Locally

To run the server:

```bash
python3.10 app.py
```

To run the tests:

```bash
python -m unittest discover -s tests -p "test_unit.py"
```

If you run into issues with missing libraries - you might need to install the requirements.txt:

```bash
pip install -r requirements.txt
```

To run the integration test:

```bash
python -m unittest discover -s tests -p "test_integration.py"
```
Once you have reached this point - you know you have a running applicaiton.  Which is great!

To create the docker container, you do:

```bash
docker build -t ci_example .
```

##What is CI/CD##

Now we are on to understanding CI/CD.  Look in the folder .gihub/workflows.  You will find in there a file named ci.workflow.  What is this!  Let's take a look:

```bash
# This YAML file defines a CI (Continuous Integration) workflow for GitHub Actions.

# CI automatically runs tasks like building your code, testing it, and even deploying it, every time you push to a repository.

on:
  push:
    branches:
      - main  # This workflow will run whenever code is pushed to the 'main' branch.

jobs:
  build:
    # This defines a job called "build". Jobs are tasks that GitHub Actions will run.
    runs-on: ubuntu-latest  # The job will run on the latest version of an Ubuntu virtual machine (VM).

    steps:
    # Steps are the specific tasks that will run in sequence inside the job.

    - name: Checkout the code
      # This step checks out (downloads) the code from your repository so that the following steps can use it.
      uses: actions/checkout@v2  # This is a pre-built action provided by GitHub for checking out code.

    - name: Set up Python
      # This step installs the Python environment needed to run your code.
      uses: actions/setup-python@v2  # Another pre-built action that sets up Python.
      with:
        python-version: '3.x'  # You specify here that you want any version of Python 3.x to be installed.

    - name: Install dependencies
      # This step installs the required Python libraries listed in your 'requirements.txt' file.
      run: pip install -r requirements.txt  # The 'run' keyword executes a shell command in the VM.

    - name: Run unit tests
      # This step runs the unit tests to verify that your code is working as expected.
      # Unit tests are small, isolated tests that check individual functions or components.
      run: python -m unittest discover -s tests -p "test_unit.py"  # It discovers and runs tests in the 'tests' folder with names matching "test_unit.py".

    - name: Set up Docker Buildx
      # This sets up Docker Buildx, which is a tool that extends Docker's capabilities, allowing you to build multi-platform images.
      uses: docker/setup-buildx-action@v1  # A pre-built GitHub action to enable Docker Buildx.

    - name: Log in to Docker Hub
      # This step logs into your Docker Hub account, which is necessary to push Docker images to your repository.
      # The username and password are stored securely in GitHub Secrets to avoid exposing sensitive data in the code.
      uses: docker/login-action@v2  # This is a pre-built action to log into Docker Hub.
      with:
        username: ${{ secrets.DOCKER_USERNAME }}  # Your Docker Hub username stored in GitHub Secrets.
        password: ${{ secrets.DOCKER_PASSWORD }}  # Your Docker Hub password stored in GitHub Secrets.

    - name: Build and tag Docker image
      # This step builds a Docker image from your code and tags it with a name.
      run: docker build -t your-dockerhub-username/flask_project:latest .  # This command builds the Docker image from the current directory ('.') and tags it with 'latest'.

    - name: Run integration tests in Docker container
      # This step runs integration tests, which test how different components of your application work together.
      # It starts a Docker container, waits for it to be ready, runs the tests, and then stops and removes the container.
      run: |
        docker run -d -p 5000:5000 --name flask_app your-dockerhub-username/flask_project:latest  # This command runs the Docker container in detached mode (-d) and maps port 5000 of the container to port 5000 on your machine.
        sleep 10  # Pauses for 10 seconds to give the Flask app time to start.
        python -m unittest discover -s tests -p "test_integration.py"  # Runs integration tests in the 'tests' folder with names matching "test_integration.py".
        docker stop flask_app  # Stops the Flask container after the tests have finished.
        docker rm flask_app  # Removes the container to clean up the environment.

    - name: Push Docker image to Docker Hub
      # This step pushes the built Docker image to your Docker Hub repository so that it can be deployed elsewhere.
      if: success()  # This ensures that the image is only pushed to Docker Hub if all previous steps have succeeded.
      run: docker push your-dockerhub-username/flask_project:latest  # Pushes the 'latest' tagged Docker image to Docker Hub.

```

In a nutshell, when you do a push to this repository, it will run this workflow automatically!  There are many steps going on here, from building the code, to running the unit tests, to building the dockerfile to running the container.  Pretty much everything you would want!

