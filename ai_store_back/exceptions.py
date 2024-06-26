from rest_framework.views import exception_handler


def core_exception_handler(e, context):
    # If an exception occurs that we don't handle explicitly here, we
    # want to pass it to the default exception handler offered by
    # DRF. And yet, if we handle this type of exception, we need
    # access to the generated DRF - get it in advance here.
    response = exception_handler(e, context)

    handlers = {"ValidationError": _handle_generic_error}

    # Determine the type of the current exception. We will use this immediately next,
    # to decide whether to do it ourselves or give this work to DRF.
    exception_class = e.__class__.__name__

    # If this exception can be handled - handle :) Otherwise
    # return the response generated by standard means in advance
    if exception_class in handlers:
        return handlers[exception_class](e, context, response)

    return response


def _handle_generic_error(e, context, response):
    # This is the simplest exception handler we can create. We
    # take the response generated by DRF and enclose it in the 'errors' key.
    response.data = {"errors": response.data}

    return response
