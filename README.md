# Cloudflare Dynamic DNS Update

This is a fork of [Cfddns](https://github.com/Suleman-Elahi/Cfddns) by [Suleman](https://github.com/Suleman-Elahi). Awesome stuff! Give them a follow!

---

This Docker container automates the process of updating a Cloudflare DNS record to match your public IP address. It is especially useful if you have a domain pointing to a dynamic IP address that changes regularly.


## Features

- Uses the Cloudflare API to fetch and update DNS records.
- Supports both IPv4 and IPv6.
- Easily configurable via environment variables.
- Runs as a cron job within the container.

## Prerequisites

- Docker
- Cloudflare account with domain setup
- API token with permissions to read and update DNS records for your Cloudflare domain.

## Building the Docker Image

1. Clone this repository:
   ```bash
   git clone [Your Repo URL]
   cd [Your Repo Folder Name]
   ```

2. Build the Docker image:
   ```bash
   docker build -t [your-dockerhub-username]/dyndns-client-cloudflare .
   ```

## Usage

1. Run the Docker container:

   ```bash
   docker run -d \
   -e DOMAIN=your.domain.com \
   -e CLOUDFLARE_API_KEY=your_cloudflare_api_key \
   -e RECORD_TYPE=A \
   [your-dockerhub-username]/dyndns-client-cloudflare
   ```

   Replace `your.domain.com`, `your_cloudflare_api_key`, and `A` with your specific details.

2. The script will run at the start of every hour, checking and updating your Cloudflare DNS record if necessary. You can view logs using:

   ```bash
   docker logs [container_id or container_name]
   ```

## Configuration

- `DOMAIN`: The domain you want to update, e.g., `subdomain.domain.com`.
- `CLOUDFLARE_API_KEY`: Your Cloudflare API token.
- `RECORD_TYPE`: The type of DNS record to update, e.g., `A` for IPv4 addresses or `AAAA` for IPv6.

## License

Copyright (c) 2023 Suleman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
