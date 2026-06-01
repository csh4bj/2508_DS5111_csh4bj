# Setting up our Vitual Machine and Virtual Environment

Before running these set up steps, make sure to have a new virtual machine instance running Ubuntu 
and a valid SSH key configured and added to your GitHub account.

## Creating Virtual Machine
Run the init.sh script to bring the VM snapshot up to date with package versions and install 'make', 'python3.14-venv', and 'tree'. 
You can do this by running 'bash scripts/init.sh'. 
To verify this worked, try running the command "tree" and instead of an error you should see the name of the init.sh script.

## Set up gihub credentials
To set up configuration setting, run the 'bash scripts/init_git_creds.sh'.
To verify this worked, you should see your email and user name echoed when you run the script.

## Creating a virtual environment for Python
Run the 'make update' to generate our virtual environment.
To quickly test that it worked, you can execute the command '. env/bin/activate' and you should see an (env) on the left of the prompt.
You can also test this by executing 'pip list' and seeing pandas and numpy listed to the console as installed packages.

If this all worked, you shoudl now have a working python environment backed up with github!
