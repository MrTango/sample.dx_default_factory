# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import sample.dx_default_factory


class SampleDxDefaultFactoryLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=sample.dx_default_factory)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'sample.dx_default_factory:default')


SAMPLE_DX_DEFAULT_FACTORY_FIXTURE = SampleDxDefaultFactoryLayer()


SAMPLE_DX_DEFAULT_FACTORY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(SAMPLE_DX_DEFAULT_FACTORY_FIXTURE,),
    name='SampleDxDefaultFactoryLayer:IntegrationTesting',
)


SAMPLE_DX_DEFAULT_FACTORY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(SAMPLE_DX_DEFAULT_FACTORY_FIXTURE,),
    name='SampleDxDefaultFactoryLayer:FunctionalTesting',
)


SAMPLE_DX_DEFAULT_FACTORY_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        SAMPLE_DX_DEFAULT_FACTORY_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='SampleDxDefaultFactoryLayer:AcceptanceTesting',
)
