import re
import logging
import numbers

class NoDefault:
    pass
no_default = NoDefault()

def pop_rest_args(request_handler):
    keys = request_handler.request.arguments.keys()
    return {key: pop_str_args(request_handler, key) for key in list(keys)}

def pop_str_args(request_handler, argument_name, regex_string=None, default=no_default):
    if default == no_default:
        inputs = request_handler.request.arguments.pop(argument_name)
    else:
        inputs = request_handler.request.arguments.pop(argument_name, [])

    if len(inputs) > 0 and isinstance(inputs[0], bytes):
        inputs = [str(input, "utf-8") for input in inputs]

    for input in inputs:
        assert isinstance(input, str), "input \"%s\" must be a string" % input
        if regex_string:
            assert re.match(regex_string, input), "input \"%(input)s\" must match regex \"%(regex)s\"" % {"input": input, "regex": regex_string}

    inputs = [input.lower() for input in inputs]
    return inputs or default

def pop_str_arg(request_handler, argument_name, default=no_default, **kwargs):
    if default == no_default:
        inputs = pop_str_args(request_handler, argument_name, default=no_default, **kwargs)
    else:
        inputs = pop_str_args(request_handler, argument_name, default=[None], **kwargs)

    assert len(inputs) > 0, "no inputs found"
    assert len(inputs) < 2, "only one value can be mapped to input %s" % argument_name
    [input] = inputs
    return input or default


def pop_int_args(request_handler, argument_name, regex_string=None, default=no_default):
    if default == no_default:
        inputs_str = request_handler.request.arguments.pop(argument_name)
    else:
        inputs_str = request_handler.request.arguments.pop(argument_name, [])

    if inputs_str:
        try:
            inputs = []
            for input_str in inputs_str:
                inputs.append(int(input_str))
        except ValueError as v:
            raise Exception("input \"%s\" must be a number" % input_str)

    return inputs or default

def pop_int_arg(request_handler, argument_name, default=None, **kwargs):
    if default == no_default:
        inputs = pop_int_args(request_handler, argument_name, default=no_default, **kwargs)
    else:
        inputs = pop_int_args(request_handler, argument_name, default=[None], **kwargs)

    assert len(inputs) > 0, "no inputs found"
    assert len(inputs) < 2, "only one value can be mapped to input %s" % argument_name
    [input] = inputs
    return input or default


def log(*args, **kwargs):
    logging.debug(*args, **kwargs)
