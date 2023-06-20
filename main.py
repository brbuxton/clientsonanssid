"""
This is a simple Python script using the Cisco Meraki library to return a list of clients on an SSID for all networks
in an organization.

Authored by Brian Buxton
"""

import meraki
import csv

API_KEY = ''
dashboard = meraki.DashboardAPI(API_KEY)
organizations = dashboard.organizations.getOrganizations()
organization = ''
ssid = ''


def find_clients(organization, ssid):
    """
    This is a simple function that returns the list of clients on an ssid for an organization.  This function can be
    extended to include any transformations or formatting required in the future.

    :rtype: list
    """
    client_list: list
    client_list = [client for network in dashboard.organizations.getOrganizationNetworks('940024') if 'wireless' in
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