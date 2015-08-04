from contextlib import contextmanager
from logging import getLogger


log = getLogger(__name__)


class DSTLibException(Exception):
    pass


class FullContactException(DSTLibException):
    pass


class SomaException(DSTLibException):
    pass


class TweeboException(DSTLibException):
    pass


class NLPException(DSTLibException):
    pass


@contextmanager
def require_extra(extra_name, module_name):
    """Provide a friendlier error message when importing an extra module
    without installing its requirements.

    Parameters
    ----------
    extra_name : str or unicode
        the name of the extras requirement as specified in setup.py
    module : str or unicode
        the :py:attr:`__name__` attribute of the module attempting the import
    """
    try:
        yield
    except ImportError:
        raise NotImplementedError(
            "Dstlib installed without '{0}' extra. {1} "
            "not importable.".format(extra_name, module_name))


@contextmanager
def optional_extra(extra_name, module_name):
    """Provide a warning message when attempting to import an extra module
    without installing its requirements, then skip the block and continue
    execution of the module. Note that use of this manager requires that the
    imported names not be referenced outside of the managed block.

    Parameters
    ----------
    extra_name : str or unicode
        the name of the extras requirement as specified in setup.py
    module : str or unicode
        the :py:attr:`__name__` attribute of the module attempting the import
    """
    try:
        yield
    except (ImportError, NotImplementedError):
        log.warn("Dstlib installed without '{0}' extra. Some functionality of "
                 "{1} may not be available.".format(extra_name, module_name))
