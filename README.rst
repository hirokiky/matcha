======
matcha
======

A WSGI dispatcher.

.. image:: https://travis-ci.org/hirokiky/matcha.png
   :target: https://travis-ci.org/hirokiky/matcha

At a glance
===========
matcha is a dispatcher for all WSGI application
based on a matching pattern of PATH_INFO in environ.

Let's register your WSGI applications to matchings and
create WSGI application.

.. code-block:: python

    >>> from wsgiref.simple_server import make_server
    >>> from matcha import Matching as m, bundle, make_wsgi_app
    >>>
    >>> from yourproject import home_app
    >>> from yourproject.blog import post_list_app, post_detail_app
    >>>
    >>>
    >>> matching = bundle(
    ...     m('/', home_app, 'home'),
    ...     m('/post/', post_list_app, 'post_list'),
    ...     m('/post/{post_slug}/', post_detail_app, 'post_detail'),
    ... )
    >>>
    >>> if __name__ == '__main__':
    ...     app = make_wsgi_app(matching)
    ...
    ...     httpd = make_server('', 8000, app)
    ...     httpd.serve_forever()

Now, accessing from your browser:

* http://127.0.0.1:800/ => home_app will be called
* http://127.0.0.1:800/post/ => post_list_app will be called
* http://127.0.0.1:800/post/some_slug/ => post_detail_app will be called

URL arguments
=============
When path elements covered with braces, this handled as **URL arguments**.
This path element can match any string and you can use that string
in your WSGI application.

The URL arguments can get from *environ['matcha.matched_dict']*
in your WSGI application.
For instance, accessing to **'/post/hello_world/'**,
you can get **'hello_world'** string as URL arguments like this:

.. code-block:: python

   >>> # In post_detail_app:
   >>> environ['matcha.matched_dict']
   {'post_slug': 'hello_world'}

Reversing
=========
Web pages usually contains some URLs for a another page.
In this case, post list page is for showing URLs
to each Blog posts (to post_detail application).

Let's take URL to post_detail application. You can do like this:

.. code-block:: python

   >>> # In post_list_app
   >>> matching = environ['matcha.matching']
   >>> matching.reverse('post_detail', post_slug='about_matcha')
   '/post/about_matcha/'

* The positional argument is a signature string for applications.
  It provided as the third argument of each Matching's constructors.
* The keyword argument is a string to fill up the URL arguments.
* Careflly, reverse method will raise NotReverced exception when
  any URLs is not matched.

OK. and then, you can provide this URL to some TemplateEngines
to display HTML pages.

Including another matchings
===========================
For more reusability, let's separate applications for blogs
from core matching.

.. code-block:: python

   # In yourproject/blog/matching.py file
   
   from matcha import Matching as m, bundle
   
   from yourproject.blog import post_list_app, post_detail_app


   matching = bundle(
       m('/', post_list_app, 'list'),
       m('/{post_slug}/', post_detail_app, 'detail'),
   )

And then, applying this to core by using *include* function:

.. code-block:: python

    >>> from matcha import include
    >>> from yourproject.blog.matching import matching as blog_matching
    >>>
    >>> matching = bundle(
    ...     m('/', home_app, 'home'),
    ...     include('/post/', blog_matching, 'post')
    ... )

Matching paths will be like this:

* `/` => home application
* `/post/` => post_list application
* `/post/some_slug/` => post_detail application

By using *include*, you can separate paths based on each applications
and avoid repeating of descriptions (such as '/post/').

In this case, reverisng to childs will be like this:

.. code-block:: python

    >>> matching.reverse('post', 'detail', post_slug='some_slug')
    '/post/some_slug/'

Setting your 404 WSGI application
=================================
The path matching failed the maked application by matcha will
return a plain 404 page.
But most cases, you want to custorm this page more friendly
for users.

For solving this, *matcha.make_wsgi_app* can take `not_found_app`
keyword argument to provide your own WSGI application for showing
404 page.

By default, the not_found_app is matcha.not_found_app.

What is Matching objects
========================
Almost core features provided by matcha dispatcher
is implamented as Matching objects.

Now, through above example, you recognize matching is like this:

* matching is created by using bundle function and Matching class.
* Registering WSGI apllications to matching.
* matching can get from environ dictionaly

Not wrong, but Matching class is something more flexible than
your recognition.

Calling
-------
matching is callable

* taking environ dictionary
* sideeffecting environ dictionary
* returning matched case and dictionary

That sideeffection is for PATH_INFO and SCRIPT_NAME to tell
which path elements are processed to another WSGI application.

.. code-block:: python

   >>> environ = {'PATH_INFO': '/htt', 'SCRIPT_NAME': '/about'}
   >>> Matching('/htt', about_htt_app)(environ)
   (about_htt_app, {})
   >>> environ
   {'PATH_INFO': '', 'SCRIPT_NAME': '/about/htt'}

Getitem from matching
---------------------
cailling of matching requires environ dictionaly, but using getitem
you can only apply path to get matched case and dictionaly.

.. code-block:: python

   >>> Matching('/htt', about_htt_app)['/htt']
   (about_htt_app, {})

Registering not only WSGI app
-----------------------------
Second positional argument (*case* keyword argument) of Matching class
can take any objects you like, not only WSGI app.

.. code-block:: python

    >>> Matching('/home', 'home')['/home']
    ('home', {})
    
For instance, you can register strings and use this as signature
for some views. something like **route_name** on
`Pyramid <http://www.pylonsproject.org/`>_.

Adding matchings
----------------
Actually, *bundle* function used in above examples is just for
adding provided positional arguments (addable objects).
So you can make WSGI application without this function:

.. code-block:: python

    >>> app = make_wsgi_app(
    ...     Matching('/', home_app) + \
    ...     Matching('/abount', about_app)
    ... )

Thanks
======
matcha dispatcher has been influenced these dispatchers:

* `Django <https://github.com/django/django/>`_ 's URL dispatcher
* `WebDispatch <https://github.com/aodag/WebDispatch>`_
* `gargant.dispatch <https://github.com/hirokiky/gargant.dispatch>`_

Thanks for them.

Resources
=========
* `PyPI <https://pypi.python.org/pypi/matcha>`_
* `Repository <https://github.com/hirokiky/matcha>`_
* `Testing <https://travis-ci.org/hirokiky/matcha>`_
