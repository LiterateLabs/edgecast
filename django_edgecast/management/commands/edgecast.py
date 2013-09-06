import sys
import django.core.management.base as base

class Command(base.BaseCommand):
    args = "<command> [<url> ...]"
    help = '''Edgecast purge and load command-line.

Specify the url(s) to purge or load.

Commands:
    purge       purge path from CDN edges.
    load        load path from CDN origin to CDN edges.
'''

    def handle(self, *args, **options):
        def print_help():
            self.stdout.write('python %s edgecast %s\n'%(sys.argv[0],Command.args))
            self.stdout.write('%s\n'%(Command.help))

        if len(args):
            args = list(args)
            cmd = args.pop(0)
            if cmd in ['purge','load'] and len(args):
                from django_edgecast import client, MEDIA_TYPE_HTTP_SMALL_OBJECT
                from django.conf import settings
                media_type = getattr(settings, 'EDGECAST_MEDIA_TYPE', MEDIA_TYPE_HTTP_SMALL_OBJECT)

                method = getattr(client,cmd)
                for url in args:
                    method( media_type, url)

                return

        print_help()
