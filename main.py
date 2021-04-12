import json
from related_image_crawler import RelatedImageCrawler
def main():
    crawler = RelatedImageCrawler()
    related_url = 'https://www.google.com/search?q=ve%20xo%20so%20kien%20giang&tbm=isch&tbs=rimg:CTeFjUVjd5KDYT4pf11Ioizc'
    img_urls = crawler.crawl(related_url)
    print(json.dumps(img_urls, indent=4))

if __name__ == '__main__':
    main()
