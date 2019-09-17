# -*- coding: utf-8 -*-
from sample.dx_default_factory.content.sample_item import ISampleItem  # NOQA E501
from sample.dx_default_factory.testing import SAMPLE_DX_DEFAULT_FACTORY_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class SampleItemIntegrationTest(unittest.TestCase):

    layer = SAMPLE_DX_DEFAULT_FACTORY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_sample_item_schema(self):
        fti = queryUtility(IDexterityFTI, name='SampleItem')
        schema = fti.lookupSchema()
        self.assertEqual(ISampleItem, schema)

    def test_ct_sample_item_fti(self):
        fti = queryUtility(IDexterityFTI, name='SampleItem')
        self.assertTrue(fti)

    def test_ct_sample_item_factory(self):
        fti = queryUtility(IDexterityFTI, name='SampleItem')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ISampleItem.providedBy(obj),
            u'ISampleItem not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_sample_item_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='SampleItem',
            id='sample_item',
        )

        self.assertTrue(
            ISampleItem.providedBy(obj),
            u'ISampleItem not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('sample_item', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('sample_item', parent.objectIds())

    def test_ct_sample_item_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='SampleItem')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )
