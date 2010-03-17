from optparse import make_option
import urllib

from django.contrib.auth.models import User
from django.core.management.base import LabelCommand, CommandError


class DummyRequest(object):

    def __init__(self, user, gadget_url):
        self.POST = {'template_uri': gadget_url}
        self.REQUEST = self.POST
        self.user = user


class Command(LabelCommand):
    """
    Load gadgets from a catalog URL
    """
    option_list = LabelCommand.option_list + (
        make_option('--verbosity', action='store', dest='verbosity', default='1',
            type='choice', choices=['0', '1', '2'],
            help='Verbosity level; 0=minimal output, 1=normal output, 2=all output'),
    )
    label = 'catalog'
    args = '<url_to_catalog>'
    help = "Load gadgets from a catalog URL. Catalog URL will be a URL list to the gadgets (separated by \\n)"

    def handle(self, *labels, **options):
        from catalogue.views import GadgetsCollection
        user = User.objects.filter(is_superuser=True)[0]
        print 'Using user %s as gadget creator...' % user
        url = urllib.urlopen(labels[0])
        lines = url.read().splitlines()
        gadgets = GadgetsCollection()
        for gadget_url in lines:
            print '\tFetching gadget from %s...' % gadget_url
            request = DummyRequest(user, gadget_url)
            gadgets.create(request, user.username, fromWGT=False)
        print 'Process finished.'