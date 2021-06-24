#  Copyright (c) 2020 Yul HR Kang. hk2699 at caa dot columbia dot edu.
from . import cacheutil
from . import argsutil
from .cacheutil import dict2fname
import os, shutil
from collections import OrderedDict as odict
from typing import Union, Iterable
from .cacheutil import mkdir4file


def replace_ext(fullpath, ext_new):
    """

    :param fullpath:
    :param ext_new: Should start with a '.'
    :return: fullpath with the old extension replaced with ext_new
    """
    fp = os.path.splitext(fullpath)[0]
    return fp + ext_new


def add_subdir(fullpath: str, subdir: str) -> str:
    pth, nam = os.path.split(fullpath)
    return os.path.join(pth, subdir, nam)


def copy2subdir(fullpath: str, subdir: str = None, verbose=True) -> str:
    """

    :param fullpath:
    :param subdir: if None or '', skip copying
    :param verbose:
    :return: full path to the destination
    """
    if subdir is None or subdir == '':
        return fullpath

    dst = add_subdir(fullpath, subdir)
    pth = os.path.split(dst)[0]
    if not os.path.exists(pth):
        os.mkdir(pth)
    shutil.copy2(fullpath, dst)
    if verbose:
        print('Copied to %s' % dst)
    return dst


class LocalFile(object):
    replace_ext = replace_ext

    def __init__(
            self,
            pth_root='../Data',
            subdir_default='',
            cache_dir='cache',
            ext_fig='.pdf',
    ):
        self.pth_root = pth_root
        self.subdir_default = subdir_default
        self.cache_dir = cache_dir
        self.ext_fig = ext_fig

    def get_pth_out(self, subdir=None):
        if subdir is None:
            subdir = self.subdir_default
        if isinstance(subdir, dict):
            subdir = argsutil.dict2fname(subdir)
        pth_out = os.path.join(self.pth_root, subdir)
        return pth_out

    def get_pth_cache(self, subdir=None, cache_dir=None):
        if cache_dir is None:
            cache_dir = self.cache_dir
        pth_cache = os.path.join(
            self.get_pth_out(subdir), cache_dir)
        if not os.path.exists(pth_cache):
            mkdir4file(pth_cache)
        return pth_cache

    def get_file_cache(
            self,
            d: [Iterable[tuple], dict, odict, None],
            subdir=None, cache_dir=None) -> str:
        """
        """
        return os.path.join(
            self.get_pth_cache(subdir, cache_dir=cache_dir),
            cacheutil.dict2fname(d) + '.zpkl'
        )

    def get_file(self, filekind, kind: str,
                 d: Union[Iterable[tuple], dict, odict, str, None] = None,
                 ext=None, subdir=None):
        """
        :type filekind: str
        :type kind: str
        :type d: Union[Iterable[tuple], dict, odict, None]
        :type ext: str
        :rtype: str
        """
        if ext is None:
            ext = '.' + filekind
        if d is None:
            d = {}
        elif isinstance(d, str):
            pass
        elif not (type(d) is list):
            d = [d]

        if isinstance(d, str):
            fname = d
        else:
            kw_fname = argsutil.kwdef(
                    argsutil.merge_fileargs(d),
                    {},
                    sort_merged=False, sort_given=True, def_bef_given=True
                )
            fname = cacheutil.dict2fname(argsutil.merge_fileargs(kw_fname))

        fname = '%s=%s+%s' % (filekind, kind, fname)
        return os.path.join(
            self.get_pth_out(subdir), fname + ext
        )

    def get_cache(
            self, cache_kind: str,
            d: Union[str, dict] = None,
            subdir: Union[str, dict] = None,
            **kwargs) -> cacheutil.Cache:
        """
        :type cache_kind: str
        :type d: Union[Iterable[tuple], dict, odict, None]
        """
        file = self.get_file(
            filekind='cache', kind=cache_kind,
            d=d, ext='.zpkl', subdir=subdir
        )
        return cacheutil.Cache(file, **{
            'ignore_key': True,
            **kwargs
        })

    def get_file_fig(self, fig_kind,
                     d: Union[Iterable[tuple], dict, odict, None] = None,
                     ext=None, subdir=None) -> str:
        """
        """
        if ext is None:
            ext = self.ext_fig
        return self.get_file('plt', fig_kind, d=d, ext=ext, subdir=subdir)


    def get_file_csv(self, kind,
                     d: Union[Iterable[tuple], dict, odict, None] = None,
                     ext='.csv', subdir=None) -> str:
        """
        """
        return self.get_file('tab', kind, d, ext='.csv', subdir=subdir)
