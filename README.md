
# Cfddns

![enter image description here](https://res.cloudinary.com/suleman/image/upload/v1686394440/Cfddns.png)

A no nonsense python script to treat Cloudflare as a dynamic DNS. Run as Docker container/scheduled task.

I couldn't find a decent tool to dynamically update IP address in my Cloudflare account, so I created this one here. It is based on Cloudflare and by default is set to update the IP address hourly. But the schedule can be changed and record type as well.

**Only requires domain and API token !!**

There are various ways to set it up.

## 1. Run Directly
Perhaps the easiest way. Run the script directly if you have Python and `requests` library installed. Or, grab one of the binary releases if you don't want to install Python and dependencies.

**Run it like this**:

    python3 cfddns.py <Domain> <API_Key> <Record_Type> 

Example:

    python3 cfddns.py test.example.com sjdgbueioengfai-sdfjkbf A
![enter image description here](https://res.cloudinary.com/suleman/image/upload/v1685180449/cfddn.png)
## 2. Via Task Scheduler on Windows
I have already provided the `task.scheduler.bat` file in the repository.
Open it with a text editor and change the path to the script and path to the python.

Next, just double click on the bat file and a task will be created.

![enter image description here](https://res.cloudinary.com/suleman/image/upload/v1681814326/taskschcfddns.png)

This task will run hourly, but you can also tweak the schedule to make it run at desired interval.
## 3. Run as a Docker Container
There is a Dockerfile so that you can make it run as a docker container.
Make sure that Docker is installed. On Debian and Ubuntu based systems and servers, you can install Docker via Snapcraft by running:

    snap install docker

Here's next.

 1. Clone the repo: `git clone https://github.com/Suleman-Elahi/Cfddns`
 2. Change directory: `cd Cfddns`
 3. Edit the **crontab** file. Enter your API Key, Record Type to update, and domain.
 4. Build image: `docker build -t cfddns .`
 5. Run the container: `docker run -d --name cfddns --restart=always cfddns`
 
 Or, you can also run it in interactive mode:

    docker run -it --rm cfddns
**Note**: On personal computers, you may need to use `sudo docker` instead of just `docker` in the above commands.

--------------------------------
The script only updates the IP if your machine's public IP and IP on Cloudflare do not match.

PRs are welcome :)
