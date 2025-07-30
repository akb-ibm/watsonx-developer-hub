from .tools import (
    web_search,
    get_arxiv_contents
)

from .modules.extractor_agent import (
    ExtractorAgent
)
from .modules.validator_agent import (
    ValidatorAgent
)
TOOLS = [
    web_search,
    get_arxiv_contents
]
