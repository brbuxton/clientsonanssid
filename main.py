"""
This is a simple Python script using the Cisco Meraki library to return a list of clients on an SSID for all networks
in an organization.

Authored by Brian Buxton
"""

import meraki
import csv

API_KEY = '8271c48b328d8f1fb191c196c6035b5793852e8f'
dashboard = meraki.DashboardAPI(API_KEY, wait_on_rate_limit=True, nginx_429_retry_wait_time=2, maximum_retries=5)
organizations = dashboard.organizations.getOrganizations()
organization = '940024'
ssid = 'pickles'


def find_clients(organization, ssid):
    """
    This is a simple function that returns the list of clients on an ssid for an organization.  This function can be
    extended to include any transformations or formatting required in the future.

    :rtype: list
    """
    client_list: list
    client_list = [client for network in dashboard.organizations.getOrganizationNetworks(organization) if 'wireless' in
                   network['productTypes'] for client in dashboard.networks.getNetworkClients(network['id']) if
                   client['ssid'] == ssid]
    return client_list


if __name__ == '__main__':
    clients = find_clients(organization, ssid)
    with open('output.csv', 'w', newline='') as csvfile:
        fieldnames = clients[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in clients:
            writer.writerow(row)
