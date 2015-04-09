from models.imagedata import ImageData 
from deviantart.scraper import Scraper

if __name__=="__main__":
    def default_callback(image_data_items):
        for image_data in image_data_items:
            print image_data
    print Scraper(default_callback)
