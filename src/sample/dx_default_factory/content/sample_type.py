# -*- coding: utf-8 -*-
from plone.app.textfield import RichText
# from plone.autoform import directives
from plone.dexterity.content import Container
# from plone.namedfile import field as namedfile
from plone.supermodel import model
from sample.dx_default_factory import _
# from plone.supermodel.directives import fieldset
# from z3c.form.browser.radio import RadioFieldWidget
# from zope import schema
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def get_default_text(context):
    print("url: " + context.absolute_url())
    return (context.title)


class ISampleType(model.Schema):
    """ Marker interface and Dexterity Python Schema for SampleType
    """

    text = RichText(
        title=_(u'Text'),
        required=False,
        defaultFactory=get_default_text,
    )


@implementer(ISampleType)
class SampleType(Container):
    """
    """
