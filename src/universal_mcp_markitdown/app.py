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

        It supports:
        - Web Pages: General HTML, specific handlers for RSS/Atom feeds, Wikipedia articles (main content), YouTube (transcripts if available), Bing SERPs.
        - Documents: PDF (attempts OCR), DOCX, XLSX, PPTX, XLS, EPUB, Outlook MSG, IPYNB notebooks.
        - Plain Text files.
        - Images: Extracts metadata and attempts OCR to get text.
        - Audio: Extracts metadata and attempts transcription to get text.
        - Archives: ZIP (extracts and attempts to convert supported files within, concatenating results).

        Args:
            uri (str): The URI pointing to the resource or a local file path.
                       Supported schemes:
                       - http:// or https:// (Web pages, feeds, APIs)
                       - file:// (Local or accessible network files)
                       - data: (Embedded data)
                       - If no scheme is provided and the string looks like a path,
                         'file://' is automatically prepended.

        Returns:
            A string containing the markdown representation of the content at the specified URI

        Raises:
            ValueError: If the URI is invalid, empty, or uses an unsupported scheme
                        after automatic prefixing.

        Tags:
            convert, markdown, async, uri, transform, document, important

        Example Usage:
            # Local File Path (scheme added automatically)
            markdown_content = await app.convert_to_markdown("/home/user/documents/report.pdf")

            # Explicit File URI
            markdown_content = await app.convert_to_markdown("file:///home/user/documents/another_report.docx")

            # Web Page (HTTP)
            # Note: Most websites now use HTTPS, HTTP examples are less common
            # markdown_content = await app.convert_to_markdown("http://example.com/old_page.html")

            # Web Page (HTTPS)
            markdown_content = await app.convert_to_markdown("https://www.wikipedia.org/wiki/Markdown")

            # Data URI (Embedded content)
            markdown_content = await app.convert_to_markdown("data:text/plain;charset=UTF-8,Hello%2C%20World%21")
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
