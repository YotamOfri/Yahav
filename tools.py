from urllib.parse import urljoin, urlparse, quote, unquote

BASE_URL = "https://www.pnay-b-y.org.il/"


def normalize_url(url: str, base_url: str = BASE_URL) -> str:
    """
    Normalize a URL:
    - If relative, join with base_url
    - If absolute, ensure it’s properly encoded for special characters
    """
    # If it's relative, join with base_url
    parsed = urlparse(url)
    if not parsed.scheme:
        # Relative URL; join with base
        full_url = urljoin(base_url, url)
    else:
        full_url = url

    # Now encode special characters properly in the path and query parts
    parsed_full = urlparse(full_url)

    # Encode path and query separately to handle special chars
    path = quote(unquote(parsed_full.path))
    query = quote(unquote(parsed_full.query), safe="=&")  # safe keeps = and & unescaped

    # Rebuild the URL with encoded parts
    normalized = parsed_full._replace(path=path, query=query).geturl()

    return normalized
