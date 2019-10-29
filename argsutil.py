#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 12 10:58:48 2018

@author: yulkang
"""

from collections import OrderedDict as odict

def varargin2props(obj, kw, skip_absent=True, error_absent=False):
    keys0 = obj.__dict__.keys()
    for key in kw.keys():
        if (key in keys0):
            obj.__dict__[key] = kw[key]
        elif error_absent:
            raise AttributeError('Attribute %s does not exist!' % key)
        elif not skip_absent:
            obj.__dict__[key] = kw[key]

def kwdefault(kw_given, **kw_default):
    """
    To ensure the order is preserved, use odict or [(key:value), ...]
    :param kw_given:
    :param kw_default:
    :return:
    """
    kw_given = odict(kw_given)
    kw_default = odict(kw_default)
    for k in kw_given:
        kw_default[k] = kw_given[k]
    return kw_default

def kwdef(kw_given, kw_def=None,
          sort_def=False, sort_given=False, def_bef_given=True):
    """
    To ensure the order is preserved, use odict or [(key:value), ...]
    :param kw_given:
    :param kw_def:
    :param sort_def:
    :param sort_given:
    :param def_bef_given:
    :rtype: odict
    """
    if kw_def is None:
        kw_def = {}

    kw_def = odict(kw_def)
    kw_given = odict(kw_given)
    if sort_def:
        kw_def = odict(sorted(kw_def.items()))
    if sort_given:
        kw_def = odict(sorted(kw_given.items()))

    if def_bef_given:
        for k in kw_given:
            kw_def[k] = kw_given[k]
    else:
        for k in kw_def:
            kw_given[k] = kw_def[k]
    return kw_def

def dict2fname(d, skip_None=True):
    def to_include(k):
        if skip_None:
            return d[k] is not None
        else:
            return True
    return '+'.join(['%s=%s' % (k, d[k]) for k in d if to_include(k)])
