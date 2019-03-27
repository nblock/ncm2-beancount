import re

import vim
from ncm2 import Ncm2Source, getLogger

logger = getLogger(__name__)


class Source(Ncm2Source):
    def on_warmup(self, ctx):
        filepath = ctx["filepath"]
        logger.debug("filepath: %s", filepath)

        self.accounts = []
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                pattern = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}\s+open\s+(\S+)")
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    mo = pattern.search(line)
                    if mo:
                        self.accounts.append(mo.group(1))
        except FileNotFoundError:
            # A new, unsaved buffer
            pass

        logger.debug("accounts: %s", self.accounts)

    def on_complete(self, ctx):
        base = ctx["base"]
        logger.debug("base: %s", base)

        matcher = self.matcher_get(ctx["matcher"])

        matches = []
        for line in self.accounts:
            item = self.match_formalize(ctx, line)
            if matcher(base, item):
                matches.append(item)
        self.complete(ctx, ctx["startccol"], matches)


source = Source(vim)

on_warmup = source.on_warmup
on_complete = source.on_complete
