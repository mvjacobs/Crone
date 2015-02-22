import logging
import os
import subprocess as sp
import tempfile

from utils import file, x

with x.require_extra("nltk", __name__):
    import nltk


log = logging.getLogger(__name__)


class Tweebo(object):
    """Wrapper class around the `TweeboParser`_ project out of Noah Smith's
    group at CMU.

    TweeboParser is a tokenization, POS tagging, and dependency parsing engine
    specialized for "Twitter English". This includes an improved ability to
    tokenize various emoticons, hashtags, etc, as well as proper tagging of
    acronyms and other shorthand.

    Parameters
    ----------
    tweebo_path : str or unicode, optional
        Path to a TweeboParser installation (or path to which Tweebo should
        install it). Defaults to $HOME/tweebo.
    sudo : bool, optional
        If TweeboParser needs to be installed, this flag controls whether
        superuser privileges will be attempted. Depending on the system
        environment, this may be required. Default :py:obj:`False`

    Raises
    ------
    ::py:class:`dstlib.utils.x.TweeboException`
        If the `tweebo_path` directory is nonexistent and cannot be
        created, if Tweebo attempts to install TweeboParser but the remote
        download fails, or if Tweebo attempts to install TweeboParser but
        the install script fails.

    Notes
    -----
    As is typical for an academic project, TweeboParser is not in the
    friendliest format when it comes to code reuse. The simplest way to use it
    in Python code is to just wrap the TweeboParser binary, running it in a
    subprocess and parsing the output back into the main Python process. That's
    what this class accomplishes.

    .. _TweeboParser: http://www.ark.cs.cmu.edu/TweetNLP/

    """

    # Our updated version contains some minor bugfixes
    _tweebo_remote = ('https://app.box.com/shared/static'
                      '/b9vyjalfojot7g7l2oew.tgz')

    def __init__(self, tweebo_path=None, sudo=False, shell="bash"):
        self.home = tweebo_path or os.path.join(
            os.environ['HOME'],
            'tweebo'
        )

        self.tweebo = os.path.join(self.home, "TweeboParser", "run.sh")

        self.sudo = ''
        if sudo:
            self.sudo = 'sudo '

        self.shell = ''
        if shell == "bash":
            self.shell = "/bin/bash "

        self._ensure_tweebo_parser_install_path()
        self._ensure_tweebo_parser_install()

    def _ensure_tweebo_parser_install_path(self):
        if os.path.exists(self.home):
            # Then install directory exists. Nothing to do.
            return

        # Attempt to create install directory.
        try:
            os.mkdir(self.home)
        except OSError as e:
            raise x.TweeboException(
                ("Tried to install TweeboParser at {0} but couldn't create "
                 "directory. Set tweebo_path parameter to a TweeboParser "
                 "source directory or a writable location.".format(self.home)),
                e)

    def _ensure_tweebo_parser_install(self):
        if os.path.exists(self.tweebo):
            # Then we're already installed. Nothing to do.
            return

        log.info("TweeboParser install not located. Attempting to install "
                 "from source.")
        print "TweeboParser install not located. Attempting to install from source."
        # Install-specific imports
        from requests import get
        from tarfile import open as taropen
        from time import sleep

        # Try and download tweeboparser remote file.
        try:
            log.debug("Downloading TweeboParser source... ")
            print "Downloading TweeboParser source... "
            tweebo_tarball = get(self._tweebo_remote, stream=True)
        except Exception as e:
            raise x.TweeboException(("Tried to install TweeboParser but "
                                     "couldn't download source from {0}. Set "
                                     "Tweebo._tweebo_remote to a valid "
                                     "TweeboParser download "
                                     "url.".format(self._tweebo_remote)),
                                    e)
        log.debug("Done.")
        print "Done."

        log.debug("Extracting source archive... ")
        print("Extracting source archive... ")
        # Wrap up the response content and untar to self.path
        tarfile = taropen(mode='r|*', fileobj=tweebo_tarball.raw)
        tarfile.extractall(self.home)
        log.debug("Done.")
        print "Done."

        log.debug("Compiling TweeboParser from source. This may take a few "
                  "minutes...")
        print("Compiling TweeboParser from source. This may take a few "
              "minutes...")
        sleep(1)

        # Execute install script.
        install = sp.Popen(
            [self.sudo + self.shell + os.path.join(self.home, "TweeboParser", "install.sh")],
            shell=True,
            #stdout=sp.PIPE,
            stderr=sp.STDOUT,
            bufsize=1)
        stdout, stderr = install.communicate()

        if install.returncode:
            raise x.TweeboException(
                "TweeboParser install failed.\n\nstdout:\n{0}\n\nstderr:\n"
                "{1}".format(stdout, stderr)
            )

        log.info("TweeboParser install completed.")
        print("TweeboParser install completed.")

    def _execute(self, path):
        """Runs the TweeboParser binary on the file at :py:obj:`path`.

        Parameters
        ----------
        path : str or unicode
            Valid file path pointing to a file of tweets, one per line.

        Returns
        -------
        None

        Notes
        -----
        Output written to :py:obj:`path + '.predict'`

        """
        parse = sp.Popen(
            self.sudo + self.shell + " ".join([self.tweebo, path]),
            cwd=os.path.join(self.home, "TweeboParser"),
            shell=True,
            #stdout=sp.PIPE,
            stderr=sp.STDOUT,
            bufsize=1)

        stdout, stderr = parse.communicate()
        if parse.returncode:
            raise x.TweeboException(
                "TweeboParer failed to parse tweets at {0}.\n\nstdout:\n{1}\n"
                "\nstderr:\n{2}".format(path, stdout, stderr)
            )
        log.debug(stdout)


def parse(self, tweets):
        """Tokenizes, tags POS, and parses sentence structure of
        :py:obj:`tweets`.

        Parameters
        ----------
        tweets : list-like
            A list, array, or Series of raw tweet text.

        Yields
        ------
        ::py:class:`nltk.parse.DependencyGraph`
            Parse trees of each tweet, in the order given by
            :py:obj:`list(tweets)`.

        """
        # The TweeboParser binary doesn't use stdin/stdout, so we need to work
        # on disk.
        tweets_file = tempfile.NamedTemporaryFile()
        tweets_file.file.write(
            '\n'.join(tweet for tweet in tweets if tweet).encode('utf-8')
        )
        tweets_file.file.flush()

        self._execute(tweets_file.name)

        outfile = tweets_file.name + '.predict'
        tweets_file.close()

        try:
            with open(outfile) as out:
                out_tweets = file.lazy_file_split(out, '\n\n')

                output = (to_conll10(item) for item in out_tweets)

                for item in output:
                    try:
                        result = nltk.parse.DependencyGraph(tree_str=item)
                        result.root = result.nodelist[0]
                    except IndexError:
                        result = nltk.parse.DependencyGraph()
                    yield result
        finally:
            os.remove(outfile)


def to_conll10(conll8):
    """Converts an 8-field CoNLL tree to the 10-field format expected by nltk.

    Parameters
    ----------
    conll8 : str or unicode
        Strings of 8 tab-delimited fields, separated by newlines.

    Returns
    -------
    [str or unicode]
        Input with dummy fields appended.

    """
    return '\n'.join([item + "\t_\t_" for item in conll8.splitlines()])