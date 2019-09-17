# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from sample.dx_default_factory.testing import SAMPLE_DX_DEFAULT_FACTORY_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that sample.dx_default_factory is properly installed."""

    layer = SAMPLE_DX_DEFAULT_FACTORY_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if sample.dx_default_factory is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'sample.dx_default_factory'))

    def test_browserlayer(self):
        """Test that ISampleDxDefaultFactoryLayer is registered."""
        from sample.dx_default_factory.interfaces import (
            ISampleDxDefaultFactoryLayer)
        from plone.browserlayer import utils
        self.assertIn(
            ISampleDxDefaultFactoryLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = SAMPLE_DX_DEFAULT_FACTORY_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['sample.dx_default_factory'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if sample.dx_default_factory is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'sample.dx_default_factory'))

    def test_browserlayer_removed(self):
        """Test that ISampleDxDefaultFactoryLayer is removed."""
        from sample.dx_default_factory.interfaces import \
            ISampleDxDefaultFactoryLayer
        from plone.browserlayer import utils
        self.assertNotIn(
            ISampleDxDefaultFactoryLayer,
            utils.registered_layers())
