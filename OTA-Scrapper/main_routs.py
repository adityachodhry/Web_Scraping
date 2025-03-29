# from flask import Flask, request, jsonify
# from threading import Thread
# from event_processor import process_events

# app = Flask(__name__)

# @app.route('/extract-events', methods=['POST'])
# def extract_events():
#     data = request.json

#     # Return the initial response
#     response = jsonify({'message': 'Your events data is being prepared'})
#     response.status_code = 200

#     # Start a new thread to process events data
#     t = Thread(target=process_events, args=(data,))
#     t.start()

#     return response

# if __name__ == "__main__":
#     app.run(debug=True)
