from util import util
from auth.auth import Auth
from projects.project import Project

# Select Auth Action
item = util.select_item(util.auth_menu)

auth = Auth()

match item['key']:
    case 1:
        # Register
        auth.register()
    case 2:
        # Login
        uid = auth.login()
    case 3:
        # Exit
        quit()

# Move to next stage

if(uid):
    # Select Projects Action
    while True:
        item = util.select_item(util.projects_menu)

        project = Project(uid)

        match item['key']:
            case 1:
                # Create
                project.create()
            case 2:
                # View All
                project.view_all()
            case 3:
                # View Own
                project.view_own()
            case 4:
                # Open
                project.open()
            case 5:
                # Exit
                quit()
