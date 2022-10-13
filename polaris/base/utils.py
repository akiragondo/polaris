def has_method(object, function_name):
    """
    Checks to see if object contains a function under the function name {function_name}
    :param object: Object to be analysed
    :param function_name: function name to be searched
    :return: if function name exists within object
    """
    function_ref = getattr(object, function_name, None)
    if function_ref is None:
        return False
    else:
        return True if callable(function_ref) else False
