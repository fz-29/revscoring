"""
These meta-datasources operate on :class:`revscoring.Datasource`'s that
return `list`'s of items and produce vectors out of the same.

.. autoclass:: revscoring.datasources.meta.vectors
"""
import os.path

from gensim.models.keyedvectors import KeyedVectors

from ..datasource import Datasource

ASSET_SEARCH_DIRS = ["word2vec/", "~/.word2vec/", "/var/share/word2vec/"]
VECTOR_DIMENSIONS = 300


class word2vec(Datasource):
    """
    Generates vectors for a list of items generated by another
    datasource.

    :Parameters:
        words_datasource : :class:`revscoring.Datasource`
            A datasource that returns a list of words.
        vectorize_words : `function`
            a function that takes a list of words and converts it to a list
            of vectors of those words
        name : `str`
            A name for the `revscoring.FeatureVector`
    """  # noqa

    def __init__(self, words_datasource, vectorize_words, name=None):
        name = self._format_name(name, [words_datasource, vectorize_words])

        super().__init__(name, vectorize_words, depends_on=[words_datasource])

    @staticmethod
    def vectorize_words(keyed_vectors, words):
        if not words:
            return [[0] * VECTOR_DIMENSIONS]
        return [keyed_vectors[word] if word in
                keyed_vectors else [0] * VECTOR_DIMENSIONS
                for word in words]

    @staticmethod
    def load_kv(filename=None, path=None, limit=None):
        if path is not None:
            return KeyedVectors.load_word2vec_format(
                path, binary=True, limit=limit)
        elif filename is not None:
            for dir_path in ASSET_SEARCH_DIRS:
                try:
                    path = os.path.join(dir_path, filename)
                    return KeyedVectors.load_word2vec_format(
                        path, binary=True, limit=limit)
                except FileNotFoundError:
                    continue
            raise FileNotFoundError("Please make sure that 'filename' \
                                    specifies the word vector binary name \
                                    in default search paths or 'path' \
                                    speficies file path of the binary")
        else:
            raise TypeError(
                "load_kv() requires either 'filename' or 'path' to be set.")
