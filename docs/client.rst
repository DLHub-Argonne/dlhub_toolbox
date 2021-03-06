Guide to DLHubClient
====================

The `DLHubClient <source/dlhub_sdk.html#dlhub_sdk.client.DLHubClient>`_
provides a Python wrapper around the DLHub and funcX web services.
In this part of the guide, we describe how to use the client to publish,
discover, and use servables.

Authorization
-------------

DLHub uses GlobusAuth to control access to the web services and provide
identities to each of our users.
Before creating the DLHubClient, you must log in to Globus::

    from dlhub_sdk.client import DLHubClient
    client = DLHubClient()

This will initiate a Globus Auth flow for you to grant the client access to
the DLHub service, Globus Search, OpenID, and the funcX service.
The ``DLHubClient`` class stores your credentials in your home directory
(``~/.dlhub/credentials/DLHub_Client_tokens.json``) so that you will only
need to log in to Globus once when using the client or the DLHub CLI.

Call the ``logout`` function to remove access to DLHub from your system::

    client.logout()

``logout`` removes the credentials from your hard disk and revokes
their authorization to prevent further use.

Publishing Servables
--------------------

The DLHubClient provides several routes for publishing servables to DLHub.
The first is to request DLHub to publish from a GitHub repository::

    client.publish_repository('https://github.com/DLHub-Argonne/example-repo.git')

There are also functions for publishing a model stored on the local system.
In either case, you must first create a ``BaseServableModel`` describing your
servable or load in an existing one from disk::

    from dlhub_sdk.utils import unserialize_object
    with open('dlhub.json') as fp:
        model = unserialize_object(json.load(fp))

Then, submit the model via HTTP by calling::

    client.publish_servable(model)

See the `Publication Guide <servable-publication.html>`_ for details on how
to describe a servable.


Discovering Servables
---------------------

The client also provides tools for querying the library of servables available through DLHub.

The most general route for discovering models is to perform a free-text search
of the model library::

    client.search('"deep learning"')

You can also perform a query to match specific fields of the metadata
records by setting the "advanced" flag on your query. For example, matching all
Keras models related to materials science is accomplished by::

    client.search('servable.type:"Keras Model" AND dlhub.domains:"chemistry"', advanced=True)

See `Globus Search documentation <https://docs.globus.org/api/search/search/#query_syntax>`_ for complete information
about the query string syntax and the `DLHub schemas <https://github.com/DLHub-Argonne/dlhub_schemas>`_ for the
available query terms.

.. TODO: Link to a webpage that displays the JSON schemas in a cleaner format

The client also provides functions for common queries, such as:

    - `search_by_authors <source/dlhub_sdk.html#dlhub_sdk.client.DLHubClient.search_by_authors>`_ to find servables from certain authors
    - `search_by_related_doi <source/dlhub_sdk.html#dlhub_sdk.client.DLHubClient.search_by_related_doi>`_ to find servables associated with a certain publication
    - `search_by_servable <source/dlhub_sdk.html#dlhub_sdk.client.DLHubClient.search_by_servable>`_ to find servables by their name or owner

Each of these tools returns metadata for only the most recent version of the
servable by default, but can be configured to return all versions.

A way to perform advanced queries besides to craft your own query string is
to use the "query helper" object that backs each of the pre-configured
search functions. A new query helper is created by calling::

    client.query

to return a blank query object, which you can then use to create a query
with the advanced functions provided by the
`DLHubSearchHelper <source/dlhub_sdk.utils.html#dlhub_sdk.utils.search.DLHubSearchHelper>`_.
For example, the advanced query shown above can be executed using::

    client.query.match_term('servable.type', '"Keras Model"').match_domains('chemistry').search()

Running Servables
-----------------

The `DLHubClient.run <source/dlhub_sdk.html#dlhub_sdk.client.DLHubClient.run>`_
command runs servables published through DLHub. DLHub uses the
`funcX <https://funcx.org>`_ to perform remote inference tasks. funcX is a
function-as-a-service platform designed to reliably and securely perform remote invocation.
Using the DLHub Client to perform an inference task invokes a funcX function on the target servable.
To invoke the servable, you need to know the name of the servable::

    client.run(model_name, x)

The data (``x``) will be serialized and passed to the servable to act on.


funcX performs client-side rate limiting to avoid accidentally overloading the service.
By default, these limits restrict the number of invocations to 20 over 10 seconds and
restrict input size to 5MB. These limits are described in detail in the `funcX docs <https://funcx.readthedocs.io/en/latest/client.html#client-throttling>`_.
The soft limits can be increased by modifying the DLHub client's funcX client:::

    client._fx_client.max_requests = 30

Note: The funcX web service will still restrict unnecessarily large inputs. Please contact us if this
becomes an issue and we can help orchestrate big data invocations.

The `DLHubClient.describe_servable <source/dlhub_sdk.html#dlhub_sdk.client.DLHubClient.describe_servable>`_ and
`DLHubClient.describe_methods <source/dlhub_sdk.html#dlhub_sdk.client.DLHubClient.describe_methods>`_ functions
are especially useful when using an unfamiliar servable. The ``describe_servable`` method returns complete information
about a servable, and the ``describe_method`` returns information about a certain method of the servable.
Use these function to understand what the servable does and to learn how to use it.
