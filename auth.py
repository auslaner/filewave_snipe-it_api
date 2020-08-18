import os


def get_filewave_api_key(key="FW_API_KEY"):
    key = os.environ.get(key, None)

    if key is None:
        raise Exception("No Filewave API key found. Make sure to export your Filewave API key as an environment " +
                        "variable. The default environment variable is FW_API_KEY")
    else:
        return key


def get_snipe_it_api_key(key="SNIPE_IT_API_KEY"):
    key = os.environ.get(key, None)

    if key is None:
        raise Exception("No Snipe-IT API key found. Make sure to export your Snipe-IT API key as an environment " +
                        "variable. The default environment variable is SNIPE_IT_API_KEY")
    else:
        return key
