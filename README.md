Django Reusable App Template
============================

This repository aims to help you to kickstart new reusable Django apps within
a few minutes.

It was prepared for our Company developers (Locomotion Technologies Corp.)

In order to kickstart your new reusable app, just do the following

.. code-block:: bash

    git clone git@github.com:locomotion-technologies/ltc-reusable-app.git your-app-name
    cd your-app-name
    nano init.sh
    # change all variables to your needs
    ./init.sh

The init script will replace all placeholders in the project files in the
``template`` folder with your desired values. Then it will rename a few
folders into your desired app name. Next it will remove the ``.git`` folder,
move everything from ``template`` into the root folder and create a first
initial commit. Now you have a new reusable app that does nothing, yet.

After this you can create the virtual environment or your app

.. code-block:: bash

    virtualenv -p python3 your-app-name
    make develop

Now you can run the tests. You might want to modify `tox.ini` so that it only
runs tests for Python/Django versions that you intend to support.

.. code-block:: bash

    tox

Or you can initiate the database and preview your app in the browser

.. code-block:: bash

    ./manage.py migrate

    ./manage.py runserver

The only URL that is hooked up will be the admin url, so you can open
`localhost:8000/admin/`.

Once you have implemented your app, you can publish it on the Python Package
Index like so

.. code-block:: bash

    python setup.py sdist
    twine upload `path/to/dist`

Pypi Config:

     ~/.config/pip/pip.conf (Download packages)

        .. code-block:: bash


            [global]
            index-url = https://developer:thedeveloperpassword@ldynamic-develops.com/nexus/repository/pypi/simple
            extra-index-url = https://pypi.org/simple



    ~/.pypirc (Upload packages)

        .. code-block:: bash

            [distutils]
            index-servers = nexus

            [nexus]
            repository: https://ldynamic-develops.com/nexus/repository/pypi/
            username: developer
            password: thenexuspassword
