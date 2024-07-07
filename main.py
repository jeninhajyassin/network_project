import os
from socket import *

serverPort = 12345  # port number

serverSocket = socket(AF_INET, SOCK_STREAM)  # creates the socket at port 9977
serverSocket.bind(("", serverPort))
serverSocket.listen(1)

print("Ready to Receive")

while True:  # forever loop
    try:
        Socket, address = serverSocket.accept()  # accepts connection from client
        temp = Socket.recv(2048).decode()

        if not temp.isspace():
            print("=====================================")
            print("Request\n " + temp)
            print("=====================================")
            words = temp.split()
            if len(words) >= 2:
                request = words[1]
            else:
                print("Invalid input: Unable to split into enough elements")

        if (request == '/') or (request == ('/main_en.html')) or (
                request == '/en'):  # if request ends with html or / send the main html file
            f1 = open('main_en.html')
            htmlFile = f1.read()
            f1.close()
            type = 'text/html'  # assigning type of request to text/html
            Socket.send('HTTP/1.1 200 ok\r\n'.encode())  # sends to client the ok http message
            Socket.send('Content-Type: text/html \r\n'.encode())  # assigning content type
            Socket.send('\r\n'.encode())  # end of response
            Socket.send(htmlFile.encode())  # sending the file

        elif request.endswith('.html') or request.endswith('.html/'):
            fileName = request.split('/')[1]

            file = open(fileName, encoding="utf8")
            fileData = file.read()
            file.close()

            Socket.send('HTTP/1.1 200 ok\r\n'.encode())  # sends to client the ok http message
            Socket.send('Content-Type: text/html \r\n'.encode())  # assigning content type
            Socket.send('\r\n'.encode())  # end of response
            Socket.send(fileData.encode())  # sending the file
        elif request.endswith('.png') or request.endswith(
                '.png/'):  # if request ends with png send thefile name requested of type png
            imageName = request.split('/')[1]  # gets image name
            imageType = imageName.split('.')[1]  # gets image type
            Socket.send('HTTP/1.1 200 ok\r\n'.encode())
            Socket.send(('Content-Type: image/' + imageType + ' \r\n').encode())  # sending the content type
            Socket.send('\r\n'.encode())
            imagePath = os.path.join('images', imageName)
            image = open(imagePath, 'rb')  # opening the image
            imageData = image.read()
            image.close()
            Socket.send(imageData)

        elif request.endswith('.jpg') or request.endswith(
                '.jpg/'):  # if request ends with jpg send the file name requested of type jpg
            imageName = request.split('/')[1]  # image name
            imageType = imageName.split('.')[1]  # image type
            if imageType == 'jpg':
                imageType = 'jpeg'
                Socket.send('HTTP/1.1 200 ok\r\n'.encode())
                Socket.send(('Content-Type: image/' + imageType + ' \r\n').encode())  # send the content type
                Socket.send('\r\n'.encode())
                imagePath = os.path.join('images', imageName)
                image = open(imagePath, 'rb')  # so here we will open the file in RB (read binary) format
                imageData = image.read()
                image.close()
                Socket.send(imageData)

        elif request.endswith(".css"):  # if css is requested, send the css
            f1 = open('style.css')  # open the aa image file and read it
            cssFile = f1.read()
            f1.close()
            type = 'text/html'  # type of request = text/html
            Socket.send('HTTP/1.1 200 ok\r\n'.encode())  # sends client the ok message
            Socket.send('Content-Type:  text/css \r\n'.encode())  # send the content type
            Socket.send('\r\n'.encode())  # end of response
            Socket.send(cssFile.encode())  # sends file

        elif request == "/ar":
            f1 = open('main_ar.html', encoding="utf8")
            htmlFile = f1.read()
            f1.close()
            type = 'text/html'  # assigning type of request to text/html
            Socket.send('HTTP/1.1 200 ok\r\n'.encode())  # sends to client the ok http message
            Socket.send('Content-Type: text/html \r\n'.encode())  # assigning content type
            Socket.send('\r\n'.encode())  # end of response
            Socket.send(htmlFile.encode())  # sending the file

        elif request == "/azn":
            Socket.send('HTTP/1.1 307 Temporary Redirect\r\n'.encode())
            Socket.send('Location: https://www.amazon.com/\r\n'.encode())
            Socket.send('\r\n'.encode())

        elif request == "/so":
            Socket.send('HTTP/1.1 307 Temporary Redirect\r\n'.encode())
            Socket.send('Location: https://stackoverflow.com/\r\n'.encode())
            Socket.send('\r\n'.encode())

        elif request == "/bzu":
            Socket.send('HTTP/1.1 307 Temporary Redirect\r\n'.encode())
            Socket.send('Location: https://www.birzeit.edu/\r\n'.encode())
            Socket.send('\r\n'.encode())

        elif request == "/SortByName":
            f1 = open('laptops.csv', encoding="utf8")
            laptops = f1.read()
            f1.close()

            # name, price
            laptops = laptops.split('\n')

            laptop_dict = {}
            for laptop in laptops:
                if laptop == '' or laptop == '\n':
                    continue

                laptop = laptop.split(',')

                if len(laptop) != 2:
                    continue

                laptop_dict[laptop[0]] = laptop[1]

            laptops = ''
            for key in sorted(laptop_dict.keys()):
                laptops += key.upper() + ',' + laptop_dict[key] + '\n'

            Socket.send('HTTP/1.1 200 ok\r\n'.encode())
            Socket.send('Content-Type: text/plain; charset=UTF-8\r\n'.encode())
            Socket.send('\r\n'.encode())
            Socket.send(laptops.encode())


        elif request == "/SortByPrice":
            f1 = open('laptops.csv', encoding="utf8")
            laptops = f1.read()
            f1.close()

            # name, price
            laptops = laptops.split('\n')

            laptop_dict = {}
            for laptop in laptops:
                if laptop == '' or laptop == '\n':
                    continue

                laptop = laptop.split(',')

                if len(laptop) != 2:
                    continue

                laptop_dict[laptop[0]] = laptop[1]

            laptops = ''

            sum_price = 0
            for key in sorted(laptop_dict, key=laptop_dict.get):
                sum_price += int(laptop_dict[key])
                laptops += key.upper() + ',' + laptop_dict[key] + '\n'

            laptops += "===================================\n"
            laptops += "Total Price: " + str(sum_price) + "\n"

            Socket.send('HTTP/1.1 200 ok\r\n'.encode())
            Socket.send('Content-Type: text/plain; charset=UTF-8\r\n'.encode())
            Socket.send('\r\n'.encode())
            Socket.send(laptops.encode())

        else:  # if none of the cases above, send the error file as an html
           notFound = open('error.html')
        notFoundPage = notFound.read()  # reading file
        notFound.close()

        # Get the client's IP address and port
        client_ip, client_port = Socket.getpeername()
        
        # Replace placeholders in the HTML
        notFoundPage = notFoundPage.replace('{client_ip}', client_ip)
        notFoundPage = notFoundPage.replace('{client_port}', str(client_port))

        Socket.send('HTTP/1.1 404 Not Found\r\n'.encode())  # sends the client the 404 not found error
        Socket.send('Content-Type: text/html\r\n'.encode())
        Socket.send('\r\n'.encode())
        Socket.send(notFoundPage.encode())  # sends the page
        Socket.close()  # closes the connection
    except Exception as e:
        # Handle the exception and print the error message
        print("An error occurred:", str(e))
    Socket.close()
