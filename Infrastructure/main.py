"""
Visitor count
"""

from flask import jsonify
from google.cloud import firestore


def get_visitor_count():
    """
    Get the number of visitors
    :return: the number of visitor
    """
    database = firestore.Client()
    visitor_nb = 0
    # Get the document
    visitor_ref = database.collection(u'cloudresume').document(u'visitor_count')
    doc = visitor_ref.get()
    # If the documents exists
    if doc.exists:
        # Get the last number of visitor
        visitor_nb = int(doc.to_dict()['count'])

    return visitor_nb


def save_visitor_data(visitor_nb):
    """
    Save the number of visitors to Firestore
    :param visitor_nb: number of visitor
    """
    database = firestore.Client()
    visitor_ref = database.collection(u'cloudresume').document(u'visitor_count')

    # Write the new number of visitors
    visitor_ref.set({'count': visitor_nb})


def visitor_count(request):  # pylint: disable=unused-argument
    """
    :param request: the client request
    :return: the current visitor number
    """
    visitor_nb = get_visitor_count()
    current_visitor = str(visitor_nb + 1)
    save_visitor_data(current_visitor)
    client_data = {
        'currentVisitor': current_visitor
    }
    headers = {
        'Access-Control-Allow-Origin': '*'
    }

    return jsonify(client_data), 200, headers
