def lazy_file_split(file_obj, sep):
    """Lazily splits a file by a particular separator.

    Parameters
    ----------
    file_obj : file-like
        File containing the content to be split
    sep : str
        Separator to split the file content on

    Yields
    ------
    str
        Content of :py:obj:`file_obj` split on occurrences of :py:obj:`sep`
        (dropping separator)
    """
    buf = ''
    char = file_obj.read(1)
    while char:
        buf += char
        if buf.endswith(sep):
            yield buf[:-len(sep)]
            buf = ''
        char = file_obj.read(1)
    if buf:
        yield buf
