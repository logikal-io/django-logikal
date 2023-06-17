from pathlib import Path
from typing import Any

from django.contrib.staticfiles import storage


class ManifestStaticFilesStorage(storage.ManifestStaticFilesStorage):
    """
    Remove the unprocessed source files after post-processing.
    """
    default_template = 'url(\'%(url)s\')'  # patch the rewriter to use single quotes

    def post_process(self, *args: Any, **kwargs: Any) -> Any:
        for name, hashed_name, processed in super().post_process(*args, **kwargs):
            yield name, hashed_name, processed
            if processed:
                Path(self.path(name)).unlink()
