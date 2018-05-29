import logging
import os
from flask import Flask, Response, send_from_directory
from flask_restful import Resource, Api
from ExtractRedditMetricsData import ScrapeRedditMetrics

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='./app.log', filemode='w')

application = Flask(__name__)

@application.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

api = Api(application)

class ExtractRedditMetricsDataAPI(Resource):
    def get(self, rm_user):
        get_data = ScrapeRedditMetrics(url='http://redditmetrics.com/r/'+rm_user)
        resp = get_data.retrieve_data(get_data.get_script_text())
        logging.info({'Searched for': rm_user})
        return Response(response=resp, mimetype='application/json')
        #return render_template("./df_template.html", html_data=get_data.convert_text_to_dataframe(resp_html).to_html(escape=False))

api.add_resource(ExtractRedditMetricsDataAPI, '/<string:rm_user>')

if __name__ == '__main__':
    application.run(debug=True)
    #test_url = ScrapeRedditMetrics(url='http://redditmetrics.com/r/waltonchain')
    #print(test_url.convert_text_to_dataframe(test_url.retrieve_data(test_url.get_script_text())))