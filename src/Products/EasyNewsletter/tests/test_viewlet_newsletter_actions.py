# -*- coding: utf-8 -*-
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from Products.EasyNewsletter.interfaces import IProductsEasyNewsletterLayer
from Products.EasyNewsletter.testing import PRODUCTS_EASYNEWSLETTER_FUNCTIONAL_TESTING
from Products.EasyNewsletter.testing import PRODUCTS_EASYNEWSLETTER_INTEGRATION_TESTING
from Products.Five.browser import BrowserView
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

import unittest


class ViewletIntegrationTest(unittest.TestCase):

    layer = PRODUCTS_EASYNEWSLETTER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.app = self.layer['app']
        self.request = self.app.REQUEST
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.newsletter = api.content.create(container=self.portal, type='Newsletter', id='newsletter')
        self.issue = api.content.create(container=self.newsletter, type='Newsletter Issue', id='issue')

    def test_newsletter_actions_is_registered(self):
        view = BrowserView(self.newsletter, self.request)
        manager_name = 'plone.abovecontentbody'
        alsoProvides(self.request, IProductsEasyNewsletterLayer)
        manager = queryMultiAdapter(
            (self.newsletter, self.request, view),
            IViewletManager,
            manager_name,
            default=None
        )
        self.assertIsNotNone(manager)
        manager.update()
        my_viewlet = [v for v in manager.viewlets if v.__name__ == 'newsletter-actions']  # NOQA: E501
        self.assertEqual(len(my_viewlet), 1)

    # XXX would be nice to have this test working:
    # def test_newsletter_actions_is_not_available_on_newsitem(self):
    #     view = BrowserView(self.portal['newsitem'], self.request)
    #     manager_name = 'plone.abovecontenttitle'
    #     alsoProvides(self.request, IProductsEasyNewsletterLayer)
    #     manager = queryMultiAdapter(
    #         (self.portal['newsitem'], self.request, view),
    #         IViewletManager,
    #         manager_name,
    #         default=None
    #     )
    #     self.assertIsNotNone(manager)
    #     manager.update()
    #     my_viewlet = [v for v in manager.viewlets if v.__name__ == 'newsletter-actions']  # NOQA: E501
    #     self.assertEqual(len(my_viewlet), 0)


class ViewletFunctionalTest(unittest.TestCase):

    layer = PRODUCTS_EASYNEWSLETTER_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
