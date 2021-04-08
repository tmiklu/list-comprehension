import json
import boto3
import urllib3
import os
import re
import time

ssm    = boto3.client('ssm')
http   = urllib3.PoolManager()
url    = 'https://jira.xxx.net/rest/api/2/issue/'
#auth   = urllib3.make_headers(basic_auth='xxxx:xxxx')


def _send_status(comment_url, phases):
    data         = {'body': phases }
    encoded_data = json.dumps(data).encode('utf-8')
    req          = http.request(
        'POST',
        comment_url,
        body=encoded_data,
        headers={"Accept": "application/json", 'Content-Type': 'application/json', 'Authorization': 'Basic <base64>'}
    )
    return 'Status sent'


def lambda_handler(event, context):
    # TODO implement
    #print(event)

    #print(dir_list)
    #return {
    #    'statusCode': 200,
    #    'body': json.dumps('OK')
    #}
    
    issue_url   = next(item for item in event['detail']['additional-information']['environment']['environment-variables'] if item['name'] == 'url')
    comment_url = issue_url['value'] + 'comment/'

    if event['detail']['build-status'] == 'FAILED':
        get_event   = next(item for item in event['detail']['additional-information']['phases'] if item['phase-status'] == 'FAILED')
        arr         = get_event['phase-context']
        result      = 'build-status: ' + '{color:red}*' + event['detail']['build-status'] + '*{color} ' + arr[0]
        
        print(_send_status(comment_url ,result))
        return 'Failed'
    else:
        print('build-status:', event['detail']['build-status'])
    
    
    
    #issue_url   = next(item for item in event['detail']['additional-information']['environment']['environment-variables'] if item['name'] == 'url')
    #comment_id  = next(item for item in event['detail']['additional-information']['environment']['environment-variables'] if item['name'] == 'ci')
    #issue_id    = next(item for item in event['detail']['additional-information']['environment']['environment-variables'] if item['name'] == 'id')
    #comment_url = issue_url['value'] + 'comment/'+ comment_id['value']
    
    
    #completed_phase         = event['detail']['completed-phase']
    #completed_phase_status  = event['detail']['completed-phase-status']
    #completed_phase_context = re.sub(r'\[:?\s*?\]', '', event['detail']['completed-phase-context'])
    
    #result = "{0} {1} {2}".format(completed_phase, completed_phase_status, completed_phase_context)
    
    #os.chdir('/tmp')
    
    #f = open('/tmp/' + issue_id['value'] + '.txt', 'a+')
    #f.write(result)
    #f.close()
    
    #dir_list = os.listdir('/tmp/')
    #print(dir_list)
    
    #f = open('/tmp/' + issue_id['value'] + '.txt', 'r')
    #print(f.read())

    #_getApi(comment_url, result)
    
    #for get_event in event['detail']['additional-information']['environment']['environment-variables']:
    #    if get_event['name'] == 'id':
    #        
    #        comment_url = url + get_event['value'] + '/' + 'comment' + '/'
        
    #        completed_phase_context = re.sub(r'\[:?\s*?\]', '', event['detail']['completed-phase-context'])
    #        completed_phase_status  = event['detail']['completed-phase-status']
    #        completed_phase         = event['detail']['completed-phase']
    #        issue_id                = get_event['value']
            
    #        phases = issue_id + ' ' + completed_phase + ' ' + completed_phase_status + ' ' + completed_phase_context
    #        print(comment_url)
    #    if get_event['name'] == 'ci':
    #        comment_id = get_event['value']
    #        print(comment_url + comment_id)
                #_getApi(comment_url, phases, comment_component)
            #time.sleep(0.8)
            #a += phases
            #_getApi(comment_url, a)
