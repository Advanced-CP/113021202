import scrapy

class GitHubRepoSpider(scrapy.Spider):
    name = 'github_repo'
    allowed_domains = ['github.com']
    
    # Replace with your repo URL
    start_urls = ['https://github.com/Advanced-CP/113021202']

    def parse(self, response):
        # Extract all file rows
        files = response.css('div[role="row"]:not([aria-labelledby="files"])')  # Skip header row
        
        for file in files:
            # Extract file name and type (e.g., "pdf" from "report.pdf")
            name = file.css('div[role="rowheader"] a::text').get().strip()
            file_type = name.split('.')[-1] if '.' in name else "folder"
            
            # Extract last modified date (ISO format)
            last_modified = file.css('relative-time::attr(datetime)').get()
            
            # Build download URL (raw link)
            file_url = file.css('div[role="rowheader"] a::attr(href)').get()
            raw_url = response.urljoin(file_url).replace('/blob/', '/raw/')

            # Yield only PDF/PNG files (and include all if needed)
            if name in ['report.pdf', 'see.png']:
                yield {
                    'file_name': name,
                    'file_type': file_type.upper(),  # e.g., "PDF", "PNG"
                    'last_modified': last_modified,
                    'download_url': raw_url
                }