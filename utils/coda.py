import httpx
from codaio import Coda, Document
from envparse import env

env.read_envfile('.env')

CODA_API_KEY = env('CODA_API_KEY')
TOOLS_MASTER_DOC_ID = env('TOOLS_MASTER_DOC_ID')
TIMETRACKER_TABLE_ID = env('TIMETRACKER_TABLE_ID')
BASE_URL ="https://coda.io/apis/v1"
auth_header = {'Authorization': 'Bearer ' + CODA_API_KEY}

def get_coda_params():
    _coda = Coda(CODA_API_KEY)
    _coda_doc = Document(TOOLS_MASTER_DOC_ID,coda=_coda)
    _timetracker_table = _coda_doc.get_table(TIMETRACKER_TABLE_ID)
    return _coda, _coda_doc, _timetracker_table

async def get_columns():
    async with httpx.AsyncClient() as client:
        columns = await client.get(
                BASE_URL + f'/docs/{TOOLS_MASTER_DOC_ID}/tables/{TIMETRACKER_TABLE_ID}/columns',
                headers=auth_header
            )
    return columns.json()

coda, coda_doc, timetracker_table = get_coda_params()
timetracker_columns = get_columns()

