# from flask import Flask, render_template, jsonify
# from x_scrapper import TwitterScraper
# from database import MongoDB
# from datetime import datetime

#

# app = Flask(__name__)

# # Load environment variables
# 

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/scrape')
# def scrape():
#     # Use proxy URL from environment variable
#     proxy = PROXYMESH_URL
#     scraper = TwitterScraper(TWITTER_EMAIL, TWITTER_PASSWORD, TWITTER_USERNAME)

#     try:
#         scraper.setup_driver(proxy)
#         if scraper.login():
#             trends = scraper.get_trending_topics()
            
#             # Save to MongoDB
#             db = MongoDB()
#             record = db.save_trends(trends, scraper.get_current_ip())
            
#             return jsonify({
#                 'success': True,
#                 'trends': trends,
#                 'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
#                 'ip_address': scraper.get_current_ip(),
#                 'record': db.get_latest_record()
#             })
#         else:
#             return jsonify({
#                 'success': False,
#                 'error': 'Login failed'
#             })
#     except Exception as e:
#         return jsonify({
#             'success': False,
#             'error': str(e)
#         })
#     finally:
#         scraper.close()

# if __name__ == '__main__':
#     # Explicitly set to run on HTTP
#     app.run(host='127.0.0.1', port=5000, debug=True)  # HTTP default settings
from flask import Flask, jsonify, request
from datetime import datetime
from x_scrapper import TwitterScraper
from dotenv import load_dotenv




import os

app = Flask(__name__)
load_dotenv()

TWITTER_EMAIL = os.getenv('TWITTER_EMAIL')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')
PROXYMESH_URL = os.getenv('PROXYMESH_URL')
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')

@app.route('/scrape')
def scrape():
    scraper = TwitterScraper(
        email=TWITTER_EMAIL,
        password=TWITTER_PASSWORD,
        username=TWITTER_USERNAME 
    )
    try:
        if scraper.setup_driver():
            if scraper.login():
                trends = scraper.get_trending_topics()
                if trends:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    return jsonify({
                        'success': True,
                        'trends': trends,
                        'timestamp': timestamp
                    })
            return jsonify({
                'success': False,
                'message': 'Login failed'
            })
        return jsonify({
            'success': False,
            'message': 'Failed to initialize browser'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        })
    finally:
        if hasattr(scraper, 'driver'):
            scraper.close()

@app.route('/')
def index():
    return "Welcome to Twitter Scraper"

if __name__ == '__main__':
    # Force HTTP only
    app.config['PREFERRED_URL_SCHEME'] = 'http'
    app.run(
        host='127.0.0.1',  # Local host only
        port=5000,
        debug=True,
        ssl_context=None  # Explicitly disable SSL
    )
