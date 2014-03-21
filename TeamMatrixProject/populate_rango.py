import os
import sys

def populate():
    #python_cat = add_cat('Python')

    add_user('tester1','tester@gmail.com','John','Doe','tester')

    # Print out what we have added to the user.
    for u in User.objects.all():
        print "- {0}".format(str(u))

            
def add_user(username, email, first_name, last_name, password):
    p = User.objects.get_or_create(username=username,email=email, first_name=first_name, last_name=last_name, password=password)[0]
    return p

# Start execution here!
if __name__ == '__main__':
    print "Starting Rango population script..."

    if '/home/takemura/MyCode/RequirementTracker_TeamMatrix' not in sys.path:
        sys.path.insert(0, '/home/takemura/MyCode/RequirementTracker_TeamMatrix')

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RequirementTracker.settings')

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()

    from django.contrib.auth.models import User
    populate()