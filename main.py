import os
import time

from auth import get_filewave_api_key, get_snipe_it_api_key
from filewave import FilewaveConnection, id_from_query_name
from parser import SpreadsheetParser
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
    snipe_api_key = get_snipe_it_api_key()
    snipe_it_server = "https://snipeit.intranet.redbutte.utah.edu"
    snipe_conn = SnipeITConnection(snipe_api_key, snipe_it_server)

    # Create an object to help us manage the parsing of an exel document
    excel_parser = SpreadsheetParser(os.environ.get("SPREADSHEET_FILE_LOCATION"))
    ws = excel_parser.workbook.active  # Get the active worksheet
    # Asset numbers are in Column C starting at row 4
    for row in ws.iter_rows(min_row=4, min_col=2, max_col=8, max_row=209):
        asset_num = row[1].value
        purchase_date = row[6].value

        # If asset number isn't a valid number or purchase_date is None, skip ahead
        if asset_num is None or not asset_num.isdigit() or purchase_date is None:
            continue

        print(f"[*] Searching for asset {row[0].value} using search term {asset_num}.")

        # Now we need to match the asset number to a hardware ID in Snipe IT
        hardware = snipe_conn.get_hardware_assets(search=asset_num).json()
        # Confirm that we didn't get more than one hardware asset
        assert hardware['total'] <= 1

        # If we didn't get any hardware assets, skip to next row
        if hardware['total'] == 0:
            print("No matching asset in Snipe IT. Skipping...")
            continue
        else:
            print(f"[*] Updating hardware asset {hardware['rows'][0]['name']} with purchase date: {purchase_date}")
            update_resp = snipe_conn.update_hardware_asset(hardware['rows'][0]['id'], purchase_date=purchase_date)
            print(update_resp.text)

            # Wait between requests so we don't hit the throttle limit
            time.sleep(2)


if __name__ == "__main__":
    main()
