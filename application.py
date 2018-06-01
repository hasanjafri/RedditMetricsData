import logging
import os
from flask import Flask, Response, send_from_directory, jsonify
from flask_restful import Resource, Api
from ExtractRedditMetricsData import ScrapeRedditMetrics

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='./app.log', filemode='w')

application = Flask(__name__)

@application.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(application.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

api = Api(application)

class retrieve_data(Resource):
    def get(self, rm_user):
        get_data = ScrapeRedditMetrics(url='http://redditmetrics.com/r/'+rm_user)
        resp = get_data.retrieve_data(get_data.get_script_text())
        logging.info({'Searched for': rm_user})
        return jsonify(response=resp)
        #return render_template("./df_template.html", html_data=get_data.convert_text_to_dataframe(resp_html).to_html(escape=False))

class get_script_text(Resource):
    def get(self, rm_user):
        get_data = ScrapeRedditMetrics(url='http://redditmetrics.com/r/'+rm_user)
        resp = get_data.get_script_text()
        logging.info({'Searched for': rm_user})
        return Response(response=resp, mimetype='text/html')

class convert_text_to_dataframe(Resource):
    def get(self, rm_user):
        get_data = ScrapeRedditMetrics(url='http://redditmetrics.com/r/'+rm_user)
        resp = get_data.convert_text_to_dataframe(get_data.retrieve_data(get_data.get_script_text())).to_csv()
        logging.info({'Searched for': rm_user})
        return Response(response=resp, mimetype='text/csv')

api.add_resource(retrieve_data, '/rd/<string:rm_user>')
api.add_resource(get_script_text, '/gst/<string:rm_user>')
api.add_resource(convert_text_to_dataframe, '/ctd/<string:rm_user>')

if __name__ == '__main__':
    application.run(debug=True)
    #test_url = ScrapeRedditMetrics(url='http://redditmetrics.com/r/waltonchain')
    #print(test_url.convert_text_to_dataframe(test_url.retrieve_data(test_url.get_script_text())))