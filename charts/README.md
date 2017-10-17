# PyChart
Site for displaying statistical information about local Git repositories

#Installation

- Create the virtual environment
`python3 -m venv myvenv`
- Activate the virtual environment
`<env_name>\scripts\activate.bat`
or
`source <env_name>/bin/activate`
- Install the requirements
`pip install -r requirements.txt`
- Run the Django migration scripts
`python manage.py migrate`
- Add a django administrator
`python manage.py createsuperuser
- Run the django server
`python manage.py runserver`

### Adding a Repository

- Login to the site admin dashboard (localhost:8000/admin)
- Click on "Repositories" under the "Charts" site
- Click "Add Repository"
- Enter the title of the repository and the path to the git folder
- The path can either be a relative path from the pychart folder, or an absolute path

The repository will nwo appear in the list of repositories on the home page of the site.
When you click on a repository, there will be graphs that show statistics about that repository.

The commits in a repository need to loaded first before pychart can create meaningful graphs.
To do that, click the "Load Commits" button.
Loading a repository again will only reload the commits that have changed since the last time the commits were loaded.

You can clear the commit cache by clicking the "Reset Commits" button.
