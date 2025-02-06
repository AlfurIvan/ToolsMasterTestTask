from envparse import env

env.read_envfile('.env')

CODA_API_KEY = env('CODA_API_KEY')
TOOLS_MASTER_DOC_ID = env('TOOLS_MASTER_DOC_ID')
TIMETRACKER_TABLE_ID = env('TIMETRACKER_TABLE_ID')
BASE_URL = "https://coda.io/apis/v1"