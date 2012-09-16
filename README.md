kismetclient
============

A Python client for the Kismet server protocol.

A trivial example application is included in `runclient.py`.

To use the client in your own application, create an instance of
`client.Client`, then create and register handlers for messages of
interest. Once handlers are registered, call the `read()` method in a
loop to handle the responses.

A handler is a callable whose first argument is the client
which generated the message, and subsequent arguments are named after
parameters chosen during capability enumeration.

A handler may specify only a `client` and `**fields` parameters in
order to get all fields for a message, in the default order.