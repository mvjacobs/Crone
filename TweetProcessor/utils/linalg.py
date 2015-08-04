"""Helper functions and classes relating to linear algebra algorithms and other
manipulation of vectors and matrices.

"""
import x

with x.require_extra("np", __name__):
    import numpy as np


def normalize(vec, desired_norm=1, ord=2):
    """Normalize a vector to a specified length.

    Parameters
    ----------
    vec : numpy.ndarray
        The vector to be normalized.
    norm : float, optional
        The desired norm of the vector. Default :py:obj:`1`.
    ord : {non-zero int, inf, -inf, 'fro'}, optional
        The order of the norm to use. Default :py:obj:`2`.

    Returns
    -------
    ::py:class:`numpy.ndarray`
        The vector :py:obj:`vec` normalized to :py:obj:`norm`.

    Raises
    ------
    ::py:class:`ValueError`
        If an attempt to normalize the vector leads to non-finite values
        (+/- inf, nan).

    See Also
    --------
    :py:func:`numpy.linalg.norm`
        For explanation of the various norm orders.

    """
    current_norm = np.linalg.norm(vec, ord=ord)
    scale_factor = desired_norm / current_norm
    result = vec * scale_factor
    if not all(np.isfinite(result)):
        raise ValueError(
            "Invalid norm {0} for array {1}".format(current_norm, vec)
        )
    return result
