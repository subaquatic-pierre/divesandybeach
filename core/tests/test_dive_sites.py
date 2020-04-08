from diving.models import DiveSite
from django.test import TestCase, Client
from django.shortcuts import reverse
from diving.models import DiveSite


class DiveSiteTest(TestCase):
    fixtures = ['diving.json']

    def setUp(self):
        self.client = Client()
        self.dive_sites = DiveSite.objects.all()

    def test_dive_site_list_seo_title(self):
        """ Test dive site list view Title """
        response = self.client.get(reverse('diving:dive-site-list'))
        self.assertEqual('Fujairah Dive Sites', response.context['title'])

    def test_dive_site_list_seo_description(self):
        """ Test dive site list view desciption """
        response = self.client.get(reverse('diving:dive-site-list'))
        self.assertEqual('Check out our dive sites along the Fujairah coastline. Each site offering abundant marine life, ranging from ship wrecks to beautiful coral reef.',
                         response.context['seo_description'])

    def test_dive_site_list_seo_keywords(self):
        """ Test dive site list view keywords """
        response = self.client.get(reverse('diving:dive-site-list'))
        self.assertEqual('Fujairah Dive Sites, Scuba Dive Fujairah',
                         response.context['seo_keywords'])

    def test_dive_site_detail_title(self):
        """ Test correct title passed to dive site detail page """
        dive_site = DiveSite.objects.all().first()
        url = reverse('diving:dive-site-detail', args=(dive_site.slug,))
        response = self.client.get(url)
        self.assertEqual(dive_site.title, response.context['title'])

    def test_dive_site_detail_description(self):
        """ Ensure correct seo description is passed into dive site detail page """
        dive_site = DiveSite.objects.all().first()
        url = reverse('diving:dive-site-detail', args=(dive_site.slug,))
        response = self.client.get(url)
        self.assertEqual(dive_site.seo_description,
                         response.context['seo_description'])

    def test_dive_site_detail_title(self):
        """ Correct dive site keywords are in dive site detail page """
        dive_site = DiveSite.objects.all().first()
        url = reverse('diving:dive-site-detail', args=(dive_site.slug,))
        response = self.client.get(url)
        self.assertEqual(dive_site.seo_keywords,
                         response.context['seo_keywords'])
