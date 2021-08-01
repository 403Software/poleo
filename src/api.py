"""
Main execution for recommendation api
"""



from os import getenv
import numpy

from __init__ import create_app
print(numpy.version.version)

app = create_app(getenv('FLASK_ENV') or 'default')

if __name__ == '__main__':
    host = app.config['HOST']
    port = app.config['APP_PORT']
    debug = app.config['DEBUG']

    app.run(
        host=host, debug=debug, port=port, use_reloader=debug
    )
    