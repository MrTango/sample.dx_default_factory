# -*- coding: utf-8 -*-
from sample.dx_default_factory.content.sample_type import ISampleType  # NOQA E501
from sample.dx_default_factory.testing import SAMPLE_DX_DEFAULT_FACTORY_INTEGRATION_TESTING  # noqa
from plone import api
from plone.api.exc import InvalidParameterError
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest




class SampleTypeIntegrationTest(unittest.TestCase):

    layer = SAMPLE_DX_DEFAULT_FACTORY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.parent = self.portal

    def test_ct_sample_type_schema(self):
        fti = queryUtility(IDexterityFTI, name='SampleType')
        schema = fti.lookupSchema()
        self.assertEqual(ISampleType, schema)

    def test_ct_sample_type_fti(self):
        fti = queryUtility(IDexterityFTI, name='SampleType')
        self.assertTrue(fti)

    def test_ct_sample_type_factory(self):
        fti = queryUtility(IDexterityFTI, name='SampleType')
        factory = fti.factory
        obj = createObject(factory)

        self.assertTrue(
            ISampleType.providedBy(obj),
            u'ISampleType not provided by {0}!'.format(
                obj,
            ),
        )

    def test_ct_sample_type_adding(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        obj = api.content.create(
            container=self.portal,
            type='SampleType',
            id='sample_type',
        )

        self.assertTrue(
            ISampleType.providedBy(obj),
            u'ISampleType not provided by {0}!'.format(
                obj.id,
            ),
        )

        parent = obj.__parent__
        self.assertIn('sample_type', parent.objectIds())

        # check that deleting the object works too
        api.content.delete(obj=obj)
        self.assertNotIn('sample_type', parent.objectIds())

    def test_ct_sample_type_globally_addable(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='SampleType')
        self.assertTrue(
            fti.global_allow,
            u'{0} is not globally addable!'.format(fti.id)
        )

    def test_ct_sample_type_filter_content_type_true(self):
        setRoles(self.portal, TEST_USER_ID, ['Contributor'])
        fti = queryUtility(IDexterityFTI, name='SampleType')
        portal_types = self.portal.portal_types
        parent_id = portal_types.constructContent(
            fti.id,
            self.portal,
            'sample_type_id',
            title='SampleType container',
         )
        self.parent = self.portal[parent_id]
        with self.assertRaises(InvalidParameterError):
            api.content.create(
                container=self.parent,
                type='Document',
                title='My Content',
            )
