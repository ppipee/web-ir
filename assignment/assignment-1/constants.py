BASE_PATH = 'html/'

BASE_URL = 'ku.ac.th'
SEED_URL = 'https://ku.ac.th/faculty-of-engineering'

MAX_URL_VISITED = 10000
ERROR = 0.1
URL_ERROR = MAX_URL_VISITED*ERROR

FILE_BLACKLISTS = ['.css', '.js', '.json', '.webp', '.xml', '.c', '.cc',
                   '.png', '.jpg', '.svg', '.jpeg', '.tiff',  '.bmp',
                   '.mp3', '.mp4', '.gif', '.ts', '.avi', '.flv', '.mkv', '.ovf', '.vmdk',
                   '.pdf', '.xlsx', '.pptx', '.docx', '.txt', '.ppt',
                   '.zip', '.rar', '.tar.gz', '.deb', '.exe'
                   ]

WORD_BLACKLISTS = ['download']

WORDS_HIGH_PRIORITY = ['cpe.ku.ac.th', 'cpe']
