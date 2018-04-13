#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: cb_Lian
# Mail: 787162506@qq.com
# Created Time:  2018-3-13 19:59:34
#############################################


from setuptools import setup, find_packages

setup(
    name = "TradeInterface",
	py_modules = ['TradeInterface'],
    version = "0.2.2",
    keywords = ("pip", "TradeInterface","trade",'haizhi'),
    description = "a interface of simulate-trading stocks",
    long_description = "a interface of simulate-trading stocks",
    license = "MIT Licence",
    url = "https://github.com/Inistlwq/TradeInterface",
    author = "cb_Lian",
    author_email = "787162506@qq.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any"
)