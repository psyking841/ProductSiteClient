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
    args = parser.parse_args()

    url = hostaddress
    writer_header = True
    #create output root dir
    if not os.path.exists(args.output):
        os.makedirs(args.output)

    if args.api == 'review':
        #step 1: make request to get all products
        page = 1
        while True:
            resp = requests.get(url + '/products/all_products/' + str(page))
            jsondata = json.loads(resp.text)
            print("Feting product page: " + str(page))
            if len(jsondata) == 0 or page == args.max_page + 1:
                break

            for item in jsondata:
                product_id = item['_id']
                print("Processing reviews for product id: " + product_id)
                comment_page = 1
                while True:
                    comm_resp = requests.get(url + '/reviews/get_reviews?product_id=' + product_id + '&page=' + str(page))
                    jsondata2 = json.loads(comm_resp.text)
                    if len(jsondata2) == 0 or comment_page == args.max_comm_page + 1:
                        break
                    with open(args.output + '/review.csv', 'a+', newline='') as csvfile:
                        for comm in jsondata2:
                            writer = csv.writer(csvfile)
                            if writer_header:
                                writer.writerow(["product_id", "user_name", "comments", "date"])
                                writer_header = False

                            writer.writerow([product_id, comm['user_name'], comm['comment_contents'],
                                             comm['comment_date']])

                    comment_page+=1

            page+=1
        print("Done!")


