#!/usr/bin/python3

"""
the following command needs ran in the webserver directory
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
"""

# Import standard libraries ---------------------------------------------------
import sys

from flask import Flask, render_template, request

# Import application libraries ------------------------------------------------
sys.path.append('..')  # noqa: E402
import paths
from xchg import XchgData
from logger import BrewfermLogger

from datetime import timedelta, datetime
from dateutil import parser

"""
Creates a rotating log
"""
logger = BrewfermLogger('webs.py').getLogger()
logger.info("webs starting up")

xd = XchgData()
app = Flask(__name__)


@app.route('/values')
def values():
    current = xd.get(paths.beer_temp) + xd.get(paths.beer_temp_offset)
    target = xd.get(paths.beer_target)
    chamber = xd.get(paths.chamber_temp) + xd.get(paths.beer_temp_offset)
    sg = xd.get(paths.blue_sg)

    try:
        sg_ts = xd.get(paths.blue_ts)

        expired_ts = (datetime.now() - timedelta(minutes=2))
        last_update = parser.parse(sg_ts)

        if (last_update < expired_ts):
            sg = '0.000'
    except Exception as e:
        logger.exception("Some other error %s %s", type(e), e)


    templateData = {
        'title': 'Brewferm Controller',
        'current': str(round(current, 1)),
        'target': str(round(target, 1)),
        'chamber': str(round(chamber, 1)),
        'sg': sg
    }
    return templateData


@app.route('/')
def index():
    current = xd.get(paths.beer_temp) + xd.get(paths.beer_temp_offset)
    target = xd.get(paths.beer_target)
    chamber = xd.get(paths.chamber_temp) + xd.get(paths.chamber_temp_offset)
    sg = xd.get(paths.blue_sg)

    templateData = {
        'title': 'Brewferm Controller',
        'current': str(round(current, 1)),
        'target': str(round(target, 1)),
        'chamber': str(round(chamber, 1)),
        'sg': sg,
        'values_url': request.host_url
    }

    return render_template('index.html', **templateData)


# Run Loop Here --------------------------------------------------------
if __name__ == '__main__':
    try:
        logger.debug("Inside main")
        app.run(debug=False,
                host='0.0.0.0',
                port=8000,
                ssl_context=('cert.pem', 'key.pem'))  # port=80 requires sudo to run!!
    except Exception as e:
        logger.exception("Some other error %s %s", type(e), e)
        sys.exit(1)
    else:
        logger.info("clean exit")
        sys.exit(0)
else:
    application = app
