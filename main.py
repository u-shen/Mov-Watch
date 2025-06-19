#!/usr/bin/python3
import requests
import urllib3
import subprocess
import re

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def main():
    s = input('[+] Movie Name : ')
    url = f"https://app.arabypros.com/api/search/{s}/0/4F5A9C3D9A86FA54EACEDDD635185/d506abfd-9fe2-4b71-b979-feff21bcad13/"
    headers = {'User-Agent': "okhttp/4.8.0", 'Accept-Encoding': "gzip"}

    try:
        res = requests.get(url, headers=headers, verify=False).json()
        movies = res.get('posters', [])

        if not movies:
            print("No movies found.")
            return

        # Prepare movie choices for fzf
        choices = []
        for m in movies:
            n = m['title']
            id = m['id']
            choices.append(f"{n} [{id}]")

        # Call fzf for movie selection
        proc = subprocess.Popen(
            ['fzf', '--height=40%', '--prompt=Select Movie: '],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout, stderr = proc.communicate(input='\n'.join(choices))

        if proc.returncode != 0:
            print("Movie selection canceled.")
            return

        selected_line = stdout.strip()
        if not selected_line:
            print("No movie selected.")
            return

        # Extract ID from selection
        try:
            movie_id = re.search(r'\[([^\]]+)\]', selected_line).group(1)
        except AttributeError:
            print("Error parsing movie ID.")
            return

        # Fetch movie sources
        url = f"https://app.arabypros.com/api/movie/source/by/{movie_id}/4F5A9C3D9A86FA54EACEDDD635185/d506abfd-9fe2-4b71-b979-feff21bcad13/"
        headers = {
            'User-Agent': "okhttp/4.8.0",
            'Accept-Encoding': "gzip",
            'if-modified-since': "Mon, 23 Dec 2024 21:42:48 GMT"
        }

        res2 = requests.get(url, headers=headers, verify=False).json()
        links = [l['url'] for l in res2]

        if not links:
            print("No links found for this movie.")
            return

        # Prepare link choices for fzf
        link_choices = [f"[Link {i+1}] {link}" for i, link in enumerate(links)]

        # Call fzf for link selection (multi-select enabled)
        proc_links = subprocess.Popen(
            ['fzf', '--multi', '--height=60%', '--prompt=Select Links (TAB to multi-select): '],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        stdout_links, stderr_links = proc_links.communicate(input='\n'.join(link_choices))

        if proc_links.returncode != 0:
            print("Link selection canceled.")
            return

        selected_output = stdout_links.strip()
        if not selected_output:
            print("No links selected.")
            return

        # Extract actual URLs from selection
        selected_entries = selected_output.split('\n')
        selected_urls = []
        for entry in selected_entries:
            match = re.search(r'(https?://\S+)', entry)
            if match:
                selected_urls.append(match.group(1))

        # Open selected URLs in Chromium
        for url in selected_urls:
            print(f"Opening: {url}")
            subprocess.Popen(['chromium', url], start_new_session=True)

    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
    except KeyError as e:
        print(f"Error parsing response - missing key: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
