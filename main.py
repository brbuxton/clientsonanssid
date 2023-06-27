"""
This is a simple Python script using the Cisco Meraki library to return a list of clients on an SSID for all networks
in an organization.

Authored by Brian Buxton
"""

import time
import requests
import csv

API_KEY = ''
# organizations = dashboard.organizations.getOrganizations()
organization = ''
ssid = ''
APIDelaySeconds = 1


def find_clients(organization, ssid):
    """
    This is a simple function that returns the list of clients on an ssid for an organization.  This function can be
    extended to include any transformations or formatting required in the future.

    :rtype: list
    """
    api = GetAPI(organization)
    client_list: list
    client_list = [client for network in api.get_networks() if 'wireless' in
                   network['productTypes'] for client in api.get_clients(network['id']) if
                   client['ssid'] == ssid]
    return client_list


class GetAPI:

    def __init__(self, organization):
        self.organization = organization

    def get_networks(self):
        url = f"https://api.meraki.com/api/v1/organizations/{self.organization}/networks"

        payload = None

        headers = {
            "Accept": "application/json",
            "X-Cisco-Meraki-API-Key": API_KEY
        }

        response = requests.request('GET', url, headers=headers, data=payload)

        print(response.json())
        return response.json()

    @classmethod
    def get_clients(cls, network):
        url = f"https://api.meraki.com/api/v1/networks/{network}/clients"

        payload = None

        headers = {
            "Accept": "application/json",
            "X-Cisco-Meraki-API-Key": API_KEY
        }
        timer(APIDelaySeconds)
        response = requests.request('GET', url, headers=headers, data=payload)

        print(response.json())
        return response.json()


def timer(secondCnt):
    print(f"Sleeping for {secondCnt} seconds")
    time.sleep(secondCnt)


if __name__ == '__main__':
    clients = find_clients(organization, ssid)
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = clients[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in clients:
            writer.writerow(row)
