import os,argparse
import requests
import json
import csv
from configs.configs import *

# def myClient(*args):
#     clientType = args[1]

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--api', dest='api')
    parser.add_argument('--output', dest='output')
    parser.add_argument('--product_page', dest='max_page', type=int)
    parser.add_argument('--review_page', dest='max_comm_page', type=int)
    parser.add_argument('--image_category', dest='category')
    args = parser.parse_args()

    url_head = hostaddress
    writer_header = True
    #create output root dir
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    if args.api == 'review':
        #step 1: make request to get all products
        page = 1
        while True:
            resp = requests.get(url_head + '/products/all_products/' + str(page))
            jsondata = json.loads(resp.text)
            print("Feting product page: " + str(page))
            if len(jsondata) == 0 or (args.max_page and page == args.max_page + 1):
                break

            for item in jsondata:
                product_id = item['_id']
                product_tag = item['searching_keyword']
                print("Processing reviews for product id: " + product_id)
                comment_page = 1
                while True:
                    comm_resp = requests.get(url_head + '/reviews/get_reviews?product_id='
                                             + product_id + '&page=' + str(page))
                    jsondata2 = json.loads(comm_resp.text)
                    if len(jsondata2) == 0 or (args.max_comm_page and comment_page == args.max_comm_page + 1):
                        break
                    with open(args.output + '/review.csv', 'a+', newline='') as csvfile:
                        for comm in jsondata2:
                            writer = csv.writer(csvfile)
                            if writer_header:
                                writer.writerow(["product_id", "product_tag", "user_name", "comments", "date"])
                                writer_header = False

                            writer.writerow([product_id, comm['user_name'], comm['comment_contents'],
                                             comm['comment_date']])

                    comment_page+=1

            page+=1
        print("Done!")

    elif args.api == 'image':
        page = 1
        while True:
            resp = requests.get(url_head + '/products/all_products/' + str(page))
            jsondata = json.loads(resp.text)
            print("Feting product page: " + str(page))
            if len(jsondata) == 0 or (args.max_page and page == args.max_page + 1):
                break

            for item in jsondata:
                product_id = item['_id']
                #create the folder for the product
                product_dir = args.output + '/' + product_id
                if not os.path.exists(product_dir):
                    os.makedirs(product_dir)

                #get image info from product_id
                #get images in main category (images on the front page)
                for cat in range(2): # 0 = category, 1 = main
                    if args.category == 'main' and cat == 1:
                        cat_folder = "main_image"
                    elif args.category == 'category' and cat == 0:
                        cat_folder == "category_image"
                    elif cat == 0 and args.category == None:
                        cat_folder = "category_image"
                    elif cat == 1 and args.category == None:
                        cat_folder = "main_image"
                    else:
                        continue

                    image_dir = product_dir + '/' + cat_folder

                    if not os.path.exists(image_dir):
                        os.makedirs(image_dir)

                    #fetch all image ids
                    img_info_resp = requests.get(url_head +
                        '/images/get_images_info?product_id=' + product_id + '&category=' + str(cat))

                    jsondata2 = json.loads(img_info_resp.text)
                    image_id_list = jsondata2["images_info"].values()
                    print("Processing images for category: " + jsondata2['image_category'] + "; " + str(image_id_list))

                    for img_id in image_id_list:
                        img_resp = requests.get(url_head + '/images/' + img_id, stream=True)
                        newFile = open(image_dir + "/" + img_id + ".jpg", "wb")
                        newFile.write(img_resp.raw.read())
                        newFile.close()

            page+=1
        print("Done!")


