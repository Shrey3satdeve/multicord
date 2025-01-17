from __main__ import client
from __main__ import app
from __main__ import db
import urllib3
import time

@app.route('/api/settings')
def api_settings():
    return db.get('settings')

@app.route('/api/guilds')
def api_guilds():
    db.create_session()
    guild_data = db.session['guilds']['data']
    return guild_data

@app.route('/api/guilds/refresh')
def api_guilds_refresh():
    db.create_session()
    try:
        guild_data = client.api.get_guilds()
        db.set(['guilds'], {
            'last_refresh': time.time(),
            'data': guild_data
        })
    except urllib3.exceptions.ProtocolError:
        guild_data = db.get(['guilds', 'data']) # it updates? not exactly sure what causes this
    return guild_data
