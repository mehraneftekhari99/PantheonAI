from zep_python import ZepClient

_zep_base_url = "http://localhost:8000"  # TODO: get from env
_zep_client = ZepClient(_zep_base_url)

def get_zep_client():
    return _zep_client