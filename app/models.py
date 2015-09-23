import requests, json
from app import app

class codero_api():
    def __init__(self):
        self.api_key = app.config['CODERO_API_KEY']
        self.url = app.config['CODERO_API_URL']
        self.version = 'v1'

    def api_request(self, api, command, request_type = 'GET', data=''):

        url = self.url + '/' + api + '/' + self.version + '/' + command

        if request_type == 'POST':
            return requests.post("%s" % (url),data=json.dumps(data),headers={'Authorization':'%s' % self.api_key, 'Content-Type':'application/json'})
        elif request_type == 'DELETE':
            return requests.delete("%s" % (url, data), headers={'Authorization': '%s' % self.api_key})
        else:
            return requests.get("%s" % (url), headers={'Authorization': '%s' % self.api_key})


    def list_running(self):
        return self.api_request('cloud', 'servers').json()

    def create_vm(self, hostname, email):
        available_bases = self.list_bases()
        docker_base = available_bases['data'][0]['id']

        regions = self.list_regions()

        region = regions['data'][1]['id']

        data = {
            'name': hostname,
            'codelet': docker_base,
            'region': region,
            'billing': app.config['CODERO_API_BILLING_TYPE']
        }

        print data
        self.api_request('cloud', 'servers', 'POST', data)

    def delete_vm(self, vm_id):
        self.api_request('servers', 'DELETE', vm_id)

    def list_bases(self):
        return self.api_request('cloud', 'codelets?os=docker&ram=2048').json()


    def list_regions(self):
        return self.api_request('services', 'regions').json()

    def get_password(self):
        return 'password'