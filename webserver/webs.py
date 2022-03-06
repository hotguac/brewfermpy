#!/usr/bin/python3

# Import standard libraries ---------------------------------------------------
import logging
import sys

from flask import Flask, render_template, request

# Import application libraries ------------------------------------------------
sys.path.append('..')  # noqa: E402
import paths
from xchg import XchgData

logging.basicConfig(
    level=logging.DEBUG, filename=paths.logs,
    format='%(asctime)s-%(process)d-webs.py -%(levelname)s-%(message)s')

logging.info("webs starting up")

xd = XchgData()
app = Flask(__name__)


@app.route('/values')
def values():
    current = xd.get(paths.beer_temp)
    target = xd.get(paths.beer_target)
    chamber = xd.get(paths.chamber_temp)
    sg = xd.get(paths.blue_sg)

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
    current = xd.get(paths.beer_temp)
    target = xd.get(paths.beer_target)
    chamber = xd.get(paths.chamber_temp)
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
        logging.debug("Inside main")
        app.run(debug=False, host='0.0.0.0', port=8000)  # port=80 requires sudo to run!!
    except Exception as e:
        logging.exception("Some other error %s %s", type(e), e)
        sys.exit(1)
    else:
        logging.info("clean exit")
        sys.exit(0)
else:
    application = app
