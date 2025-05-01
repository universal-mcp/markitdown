import re

from markitdown import MarkItDown
from universal_mcp.applications import BaseApplication


class MarkitdownApp(BaseApplication):
    def __init__(self, **kwargs):
        super().__init__(name="markitdown", **kwargs)
        self.markitdown = MarkItDown()

    async def convert_to_markdown(self, uri: str) -> str:
        """
        Asynchronously converts a URI or local file path to markdown format
        using the markitdown converter.

        This tool aims to extract the main text content from various sources.
        It automatically prepends 'file://' to the input string if it appears
        to be a local path without a specified scheme (like http, https, data, file).

        Args:
            uri (str): The URI pointing to the resource or a local file path.
                       Supported schemes:
                       - http:// or https:// (Web pages, feeds, APIs)
                       - file:// (Local or accessible network files)
                       - data: (Embedded data)
                       
        Returns:
            A string containing the markdown representation of the content at the specified URI

        Raises:
            ValueError: If the URI is invalid, empty, or uses an unsupported scheme
                        after automatic prefixing.

        Tags:
            convert, markdown, async, uri, transform, document, important
        """
        if not uri:
            raise ValueError("URI cannot be empty")

        known_schemes = ["http://", "https://", "file://", "data:"]
        has_scheme = any(uri.lower().startswith(scheme) for scheme in known_schemes)
        if not has_scheme and not re.match(r'^[a-zA-Z]+:', uri):
             if re.match(r'^[a-zA-Z]:[\\/]', uri): # Check for Windows drive letter path
                 normalized_path = uri.replace('\\', '/') # Normalize backslashes
                 processed_uri = f"file:///{normalized_path}"
             else: # Assume Unix-like path or simple relative path
                 processed_uri = f"file://{uri}" if uri.startswith('/') else f"file:///{uri}" # Add leading slash if missing for absolute paths

             uri_to_process = processed_uri
        else:
             # Use the uri as provided
             uri_to_process = uri


        return self.markitdown.convert_uri(uri_to_process).markdown

    def list_tools(self):
        return [
            self.convert_to_markdown,
        ]
