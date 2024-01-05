# Amazon-Price-tracker
Things used in this project : Python | Selenium | HTML | CSS | Pandas |
Selenium is used to automate the browser to get the information.
HTML and CSS is used to design the Frontend to access the website.
Pandas is used to convert the extracted data into a CSV file.
OS Module of Python to create a dataframe on the system locally until hosted on the cloud.

#  Completed Progress

By the use of selenium we access the webpage of Amazon India (https://www.amazon.in/) and try to retrieve the information.
As Amazon is a dynamic type website. It doesnot allows normal scraping tools like requests and beautifulsoup to access its information and temporarily blocks the IP of the user trying to send the request.
So using Selenium is a great way to access the data without getting the IP blocked by amazon because selenium allows tests to be executed quickly and smoothly.
Selenium uses the url provided by us (i.e https://www.amazon.in/) and automates the test and skips the captcha logins and jumps directly to the website.
Then it enters the given search term provided by the user and runs the code to get the desired products.
When the products are available, selenium extracts its information like url, price, name of the product, product id, number of stars, number of total reviews.
After getting all this data and putting into a python dictionary to be converted, python uses pandas library to create a dataframe out of this data
This dataframe is saved on the system locally as a CSV file.

# Still in progress

- Linking the webpage to the python code
- Uploading the code to the cloud
- Making a feature to autoexecute the code everyday on the cloud
- Training an AI to keep progress of the change of price and ratings on the products.
- Providing the best given price and time to buy a product.
