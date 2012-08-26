#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Helper functions for processing HTML """

from lxml import etree
import re


def get_rx(regex, body):
    """ Return first result of regular expression 'regex' in 'body' """
    results = re.compile(regex).findall(body)
    if not results:
        return False
    return results[0]


def get_tree(html):
    return etree.HTML(html)


def get_inputs(html):
    inputs = {}
    root = etree.HTML(html)
    for i in root.xpath("//input"):
        inputs[i.get('name')] = i.get('value') or ''
        if inputs[i.get('name')]:
            inputs[i.get('name')] = inputs[i.get('name')].encode('utf-8')
    for i in root.xpath("//textarea"):
        inputs[i.get('name')] = i.text or ''
    for i in root.xpath("//select"):
        options = i.xpath("option")
        if options:
            options = options[0].get('value')
        else:
            options = ''
        inputs[i.get('name')] = options
    if None in inputs:
        del inputs[None]
    return inputs


def get_forms(html, form_name=None, action=None, xpath=None):
    forms = []
    root = etree.HTML(html)
    if form_name:
        xpath_exp = "//form[@name='%s' or @id='%s']" % (form_name, form_name)
    elif action:
        xpath_exp = "//form[@action='%s']" % action
    elif xpath:
        xpath_exp = xpath
    else:
        xpath_exp = "//form"
    for form in root.xpath(xpath_exp):
        form = {'name': form.get('name') or form.get('id'),
                'action': form.get('action'),
                'fields': get_inputs(etree.tostring(form)), }
        forms.append(form)
    return forms


def get_title(html):
    root = etree.HTML(html)
    title = root.xpath("//title")
    if title:
        return title[0].text
    else:
        return None


if __name__ == '__main__':
    pass
