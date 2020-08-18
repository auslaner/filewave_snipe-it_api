from auth import get_filewave_api_key, get_snipe_it_api_key
from filewave import FilewaveConnection, id_from_query_name
from snipe_it import SnipeITConnection, id_from_value


def add_to_snipe(snipe_connection, machine_list, label_id):
    for machine in machine_list:
        response = snipe_connection.add_hardware_asset(machine, label_id)
        print(response.json())


def transfer_filewave_to_snipe(filewave_connection, snipe_connection):
    # Get lists so we can search them and get the IDs we need
    fw_queries = filewave_connection.get_all_queries()
    snipe_labels = snipe_connection.get_status_labels()

    # Get the ID for query named "All OS X"
    all_os_x_query_id = id_from_query_name(fw_queries.json(), "All OS X")

    # Get the ID for the "Ready to Deploy" status
    ready_to_deploy_id = id_from_value(snipe_labels.json(), "Ready to Deploy")

    # Get a list of all machines in returned by the "All OS X" FW query
    osx_fw_machines = filewave_connection.get_query_results_by_id(all_os_x_query_id)
    osx_fw_machines = osx_fw_machines.json()['values']

    add_to_snipe(snipe_connection, osx_fw_machines, ready_to_deploy_id)


def main():
    # Create API connection objects for Filewave & Snipe IT
    fw_api_key = get_filewave_api_key()
    filewave_server = "https://filewave.redbutte.utah.edu"
    fw_conn = FilewaveConnection(fw_api_key, filewave_server)

    snipe_api_key = get_snipe_it_api_key()
    snipe_it_server = "https://snipeit.intranet.redbutte.utah.edu"
    snipe_conn = SnipeITConnection(snipe_api_key, snipe_it_server)


if __name__ == "__main__":
    main()
