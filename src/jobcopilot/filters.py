from dataclasses import dataclass, field


@dataclass
class PostingFilter:
    keywords: list[str] = field(default_factory=list)
    remote_only: bool = False
    locations: list[str] = field(default_factory=list)

    def matches(self, title: str, raw_text: str, location: str = "") -> bool:
        haystack = f"{title}\n{raw_text}".lower()
        if self.keywords and not any(keyword.lower() in haystack for keyword in self.keywords):
            return False
        if self.remote_only and "remote" not in haystack:
            return False
        return not self.locations or any(loc.lower() in haystack for loc in self.locations)
