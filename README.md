# Client Code for the Product Site Restful APIs

# Version 0.90

# You will need to get a config file from me to connect to the server

## This code is written using Python 3; may NOT work with Python 2!

## Usage:
1. If you want to get reviews for all products:
* If you want to create the csv with ALL reviews for ALL product:
python SiteClient --api review --output /path/to/your/folder

* If you just need a few reviews for testing purposes:
python SiteClient --api review --output /path/to/your/folder --product_page 1 --review_page 1

By using this commend you will get 1 page of reviews (20 reviews) for 1 page of products (30 products), which is 600 reviews (may < 600 as some products have less than 20 reviews).

2. If you want to get images for all products:
python SiteClient --api image --output /path/to/your/folder

for testing you can run command
python SiteClient --api image --output /path/to/your/folder --product_page 1 --image_category main

This command will download main images for 30 products (1 page of products)

There are two options for --image_category parameter, main or category, if this parameter is not provided, then images of both categories will be downloaded.

for example, 
python SiteClient --api image --output /path/to/your/folder --product_page 2

This command will download images of both main and category types for 60 products to your folder.

Note output param accepts directory name

The code will call corresponding RESUful API to get the data. The code automatcially create

For review data, it outputs data to a CSV file
The CSV file has following fields:
"product_id", "product_tag", "user_name", "comments", "date"

* product_id: product's id in the backend db
* product_tag: the keyword used to search this product (e.g. 婴儿车(baby cart), 办公椅(office chair))

For image data, it outputs a number of directories, with

-output_dir

--product_id

---image_category

----image_id1.jpg

----image_id2.jpg



