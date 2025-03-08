import os
from flask import jsonify, make_response

from app import FEATURE_DIR
from app.function.test_suites import bind_test_case, format_feature, get_testsuites, parse_feature_file


def test_suites():
    testsuites_list = get_testsuites()
    return make_response(jsonify({
        'status': 'success',
        'message': 'Test Suites',
        'data': {
            'testsuites': testsuites_list 
        }
        }), 200)

def test_suite_detail(payload):
    testsuite_name = payload.get('testsuite_name')
    testcase_list = bind_test_case(testsuite_name+'.json')
    feature_data = []
    for testcase in testcase_list:
        feature_file = format_feature(testcase)
        feature_path = os.path.join(FEATURE_DIR, feature_file)
        data = parse_feature_file(feature_path)
        feature_data.append(data)
    return make_response(jsonify({
        'status': 'success',
        'message': 'Detail Test Suite',
        'data': {
            'testsuite_name':testsuite_name,
            'feature_data': feature_data 
        }
        }), 200)