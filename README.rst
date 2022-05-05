Django Addresses
================

An app that allow manage addresses.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install dj-geocomplete-addresses

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git@github.com:amgcorp-tech/dj-addresses.git#egg=addresses

Configuration
-------------

Add ``addresses`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'addresses',
    )

You can either store your Google API key in an environment variable as GOOGLE_API_KEY or you can specify the key in settings.py.

Add ``dj-addresses`` configuration variables in your ``settings.py``

.. code-block:: python

    GOOGLE_API_KEY = 'AIzaSyD--your-google-maps-key-SjQBE'

Or export into your ``environment``

.. code-block:: python

    export GOOGLE_API_KEY=<your-api-key>

Add the ``addresses`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = [
        path('addresses/', include('addresses.urls')),
    ]

Include a menu items in your template:

.. code-block:: python

    {% load addresses_tags %}
    {% render_addresses_menu %}

If you need to modify the template, update the menu template found in

.. code-block:: python

   /templates/addresses/inc/sidebar_menu.html

Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate addresses


Run server and preview your app in the browser

.. code-block:: bash

    ./manage.py runserver


Usage
-----

The rationale behind the model structure is centered on trying to make it easy to enter addresses that may be poorly defined.
The model field included uses Google Maps API v3 (via the nicely done geocomplete jquery plugin) to determine a proper address where possible.
However if this isn't possible the raw address is used and the user is responsible for breaking the address down into components.

It's currently assumed any address is represent-able using four components: country, state, locality and street address.
In addition, country code, state code and postal code may be stored, if they exist.


- AddressField

    To simplify storage and access of addresses, a subclass of ForeignKey named AddressField has been created.
    It provides an easy method for setting new addresses.

- ON_DELETE behavior of Address Field

    By default, if you delete an Address that is related to another object, Django's cascade behavior is used.
    This means the related object will also be deleted.
    You may also choose to set null=True when defining an address field to have the address set to Null instead of deleting the related object.

- The model:

.. code-block:: bash

    from addresses.models import AddressField

    class Person(models.Model):
        address1 = AddressField()
        address2 = AddressField(on_delete=models.CASCADE)
        address3 = AddressField(related_name='+', blank=True, null=True)

- The form:

.. code-block:: bash

    from addresses.forms import AddressField

    class PersonForm(forms.Form):
      address = AddressField()


- The template:

.. code-block:: bash

    <head>
        {{ form.media }} <!-- needed for JS/GoogleMaps lookup -->
    </head>
    <body>
        {{ form }}
    </body>
