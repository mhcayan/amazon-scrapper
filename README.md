This scirpt can collect all the reviews of any amazon product.

To run the script follow the below steps:

1. In windows install docker desktop
	download link: https://www.docker.com/products/docker-desktop
	
	If you see "WSL 2 installation is incomplete." error. Then update WSL 2 kernel using following two commands and restart your pc
		
		open command prompt as administrator
		i. wsl.exe --update
		ii. wsl --shutdown
		
2. Open powershell and pull splash image with following command
	docker pull scrapinghub/splash

3. Run splash image

	Docker Desktop > Images > scrapinghub/splash > Run > Optional Settings > Ports > Local Host > Enter 8050

	Verify that splash is running in http://localhost:8050/

4. For each product, for which you would like to scrap reivews, enter its id in the text file product.txt. Each product id must be in a newline. You can find the product id
from it's amazon link. For example for the following amazon product-link it's id is B096BKVWZZ
	
	https://www.amazon.com/Samsung-Electronics-Smartwatch-Detection-Bluetooth/dp/B096BKVWZZ/ref=cm_cr_arp_d_product_top?ie=UTF8
5. Run the review-scrapper.py script

6 The scrapped reviews will be in the file reviews.xlsx
	
