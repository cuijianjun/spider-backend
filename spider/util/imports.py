from __future__ import absolute_import

import pkgutil


def import_submodules(context, root_module, path):
    """
    Import all submodules and register them in the ``context`` namespace.
    for examples:
    >>> import_submodules(locals(), __name__, __path__)
    :param context: locals()
    :param root_module: __name__
    :param path: __path__
    :return: None
    """
    for loader, module_name, is_pkg in pkgutil.walk_packages(path, root_module + '.'):
        module = loader.find_module(module_name).load_module(module_name)
        for k, v in vars(module).items():
            if not k.startswith('_'):
                context[k] = v
        context[module_name] = module
