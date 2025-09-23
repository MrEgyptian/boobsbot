import asyncio
from fileinput import filename
import os,aiohttp,bs4
from io import BytesIO
async def get_comic_info(url: str) -> dict:
    """
    Extracts metadata for an EroFus comic.
    Returns a dictionary with author, title, etc.
    """
    try:
        parts = url.rstrip('/').split('/')
        comic_author = parts[-2]
        comic_title = parts[-1]
        info= {
            "author": comic_author.replace('-', ' ').title(),
            "title": comic_title.replace('-', ' ').title(),
            "webpage_url": url
        }
        headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.erofus.com/?search=gender-bender",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0, i",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers",
}
        print(url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    content = await resp.text()
                    print('content',content)
                    soup = bs4.BeautifulSoup(content, 'html.parser')
                    #thumbnail = soup.select_one('div.col-xs-12:nth-child(3) > a:nth-child(1) > div:nth-child(1) > img:nth-child(1)')
                    thumbnail = soup.select_one('html body div.content.col-md-12 div.row-content.row div.col-xs-12.col-sm-6.col-md-4.col-lg-2 a.a-click div.thumbnail img')
                    if thumbnail:
                        info["thumbnail"] = f"https://www.erofus.com/{thumbnail['src']}"
                        print("Thumbnail found:", info["thumbnail"])
                    pages = soup.select("html body div.content.col-md-12 div.row-content.row div.col-xs-12.col-sm-6.col-md-4.col-lg-2 a.a-click")
                    #chapters=soup.select("html body div.content.col-md-12 div.row-content.row div.col-xs-12.col-sm-6.col-md-4.col-lg-2 a.a-click")
                    if pages:
                        
                        info['first_page']=await download_erofus_page(pages[0]['href'])
                        if info['first_page']:
                            info["page_count"] = len(pages)
                        else:
                            info['page_count']=0
                            info['chapters']=pages
                        #print("Page count:", info["page_count"])
                    else:
                        info['page_count']=0
                    if info['page_count']==0:
                        info['chapters']=[f"https://www.erofus.com{a['href']}" for a in pages if a.get('href')]
                    else:
                     info["pages"] = [f"https://www.erofus.com{a['href']}" for a in pages if a.get('href')]
                    info['tags']=soup.select("html body div.content.col-md-12 div.row-content.row div.album-tag-container.col-xs-12.col-sm-12.col-md-12.col-lg-12.text-center div a.album-tag.btn.btn-default.btn-lg")
                    info['tags']=[tag.text.strip().replace(" ",'_').replace("-","_") for tag in info['tags']]
            #await session.close()
        return info
        
    except Exception as e:
        print(f"[get_comic_info] Error: {e}")
        return {}
async def download_erofus_page(url: str) -> str:
    """
    Downloads the image from a single EroFus comic page URL.
    Returns the local file path of the downloaded image.
    """
    try:
        headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:143.0) Gecko/20100101 Firefox/143.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.erofus.com/?search=gender-bender",
    "Sec-GPC": "1",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Priority": "u=0, i",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache",
    "TE": "trailers",
}
        if url.startswith("http"):
            pass
        else:
            url=f"https://www.erofus.com{url}"
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    content = await resp.text()
                    soup = bs4.BeautifulSoup(content, 'html.parser')
                    image_tag = soup.select_one('.a-click > img:nth-child(1)')
                    if image_tag and image_tag.get('src'):
                        image_url = f"https://www.erofus.com/{image_tag['src']}"
                        print("Downloading image:", image_url)
                        async with session.get(image_url, headers=headers) as img_resp:
                            if img_resp.status == 200:
                                img_data = await img_resp.read()
                                file=BytesIO(img_data)
                                file.name = image_url.split("?")[0]
                                file.write(img_data)
                                file.seek(0)
                                return file
                            else:
                                print(f"Failed to download image: {img_resp.status}")
                    else:
                        print("Image tag not found on page.")
                else:
                    print(f"Failed to fetch page: {resp.status}")
    except Exception as e:
        print(f"[download_erofus_page] Error: {e}")
        return None