#!/usr/bin/env python
import socket
import sys
import optparse
from ..app import app
from ..version import VERSION


def main():
    parser = optparse.OptionParser("usage: %prog [options]")
    parser.add_option('-b', '--bind', dest='bind_addr',
                      metavar='ADDR',
                      help='IP addr or hostname to bind to')
    parser.add_option('-p', '--port', dest='port', type='int',
                      metavar='PORT',
                      help='port to bind to')
    parser.add_option('-H', '--redis-host', dest='redis_host',
                      metavar='ADDR',
                      help='IP addr or hostname of Redis server')
    parser.add_option('-P', '--redis-port', dest='redis_port', type='int',
                      metavar='PORT',
                      help='port of Redis server')
    parser.add_option('-D', '--redis-database', dest='redis_database',
                      type='int', metavar='DB',
                      help='database of Redis server')
    parser.add_option('-u', '--redis_url', dest='redis_url_connection',
                      metavar='REDIS_URL',
                      help='redis url connection')
    parser.add_option('--redis-password', dest='redis_password',
                      metavar='PASSWORD',
                      help='password for Redis server')
    parser.add_option('--auth-user', dest='auth_user',
                      metavar='AUTH_USER',
                      help='username for auth')
    parser.add_option('--auth-pass', dest='auth_pass',
                      metavar='AUTH_PASS',
                      help='password for auth')
    parser.add_option('--interval', dest='poll_interval', type='int',
                      metavar='POLL_INTERVAL',
                      help='refresh interval')
    parser.add_option('--site-name', dest='site_name',
                      metavar='SITENAME',
                      help='sitename to show, otherwise hostname is displayed')
    parser.add_option('--debug', dest='debug', action='store_true',
                      metavar='DEBUG',
                      help='run app in debug mode')
    (options, args) = parser.parse_args()

    # Populate app.config from options, defaulting to app.config's original
    # values, if specified, finally defaulting to something sensible.
    app.config['BIND_ADDR'] = (options.bind_addr or
                               app.config.get('BIND_ADDR', '0.0.0.0'))
    app.config['PORT'] = options.port or app.config.get('PORT', 9181)

    # Override app.config from options if specified. Otherwise leave untouched,
    # so the client can use its own defauls if app.config has no values.
    if options.redis_host:
        app.config['REDIS_HOST'] = options.redis_host
    if options.redis_port:
        app.config['REDIS_PORT'] = options.redis_port
    if options.redis_password:
        app.config['REDIS_PASSWORD'] = options.redis_password
    if options.redis_database:
        app.config['REDIS_DB'] = options.redis_database
    if options.auth_user:
        app.config['AUTH_USER'] = options.auth_user
    if options.auth_pass:
        app.config['AUTH_PASS'] = options.auth_pass
    if options.poll_interval:
        app.config['RQ_POLL_INTERVAL'] = options.poll_interval
    if options.site_name:
        app.config['SITENAME'] = options.site_name
    else:
        app.config['SITENAME'] = socket.gethostname()

    app.config['DEBUG'] = False
    if options.debug:
        app.config['DEBUG'] = options.debug

    app.config['REDIS_URL'] = options.redis_url_connection or None

    if len(args) > 0:
        parser.print_help()
        sys.exit(2)

    print('RQ Dashboard, version %s' % VERSION)
    app.run(host=app.config['BIND_ADDR'], port=app.config['PORT'],
            debug=app.config['DEBUG'])

if __name__ == '__main__':
    main()
