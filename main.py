from socket import *
from item import *

def getName(item):
    return  item.name

def getPrice(item):
    return  item.price

itemList = []
PORT = 6500
# defining the socket, and binding it to the port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", PORT))
# socket listening for response
serverSocket.listen(1)
print('The server is ready to receive')
# a function to read the phones csv file

f=open("phonesPrices.csv","r")
line=" "
next(f)
while line:
    line=f.readline()
    #print(line)
    if line != "" :
        l=line.split(',')
        x=item(l[0],l[1])
        itemList.append(x)

while True:
    connection , add = serverSocket.accept()
    print(add,connection)
    sentence = connection.recv(1024).decode('utf-8')
    print(sentence)
    requesting_file = sentence.split(' ')[1]  # from the request sentence, getting the requested file

    requestedFile = requesting_file.lstrip('/')  # removing the first / to get the requested file name

    if requestedFile == '' or requestedFile == "index.html":  # default request
        requestedFile = 'main.html'  # Load main.html file as default

    try:
        sortedBy = ''

        # accepting different file formats
        if requestedFile.endswith(".jpg"):

            requestedType = 'image/jpg'

        elif requestedFile.endswith(".jpeg"):

            requestedType = 'image/jpeg'

        elif requestedFile.endswith(".png"):

            requestedType = 'image/png'

        elif requestedFile.endswith(".css"):

            requestedType = 'text/css'

        elif requestedFile.upper() == "SORTBYNAME":
            itemList.sort(key=getName)

            sortedBy = 'Name'
            requestedType = 'text/html'

        elif requestedFile.upper() == "SORTBYPRICE":
            #print(itemList)
            itemList.sort(key=getPrice)
            #print(itemList)
            sortedBy = 'Price'
            requestedType = 'text/html'

        else:
            requestedType = 'text/html'

        if requestedFile.upper() != "SORTBYNAME" and requestedFile.upper() != "SORTBYPRICE":
            file = open(requestedFile, 'rb')  # opening the requested file
            response = file.read()  # reading the file
            file.close()  # closing the file

        else:
            response = ('<!DOCTYPE html><html><head><title>Cars price</title><style type="text/css">.header {'
                        'width:100%;height: 85px;background-color: #67826b;padding: 10px 0 0 20px;border: '
                        '0px;border-radius:0px;}table {font-family: arial, sans-serif;border-collapse: '
                        'collapse;width: 100%;}td, th {border: 1px solid #dddddd;text-align: center;padding: '
                        '8px; width: 50%; font-weight: normal;}tr:nth-child(even) {background-color: '
                        '#dddddd;}</style></head><body><div class="header"><h1 style="color: white;">Cars '
                        'PRICES</h1></div><p>Cars Sorted By ' + sortedBy + '</p><table><tr><th style="border: '
                        '1px solid black; font-weight: bold;">Car model</th><th style="border: 1px solid black; '
                        'font-weight: bold;">Price</th></tr>').encode()
            for item in itemList:
                response += ('<tr><th>' + str(item.name) + '</th><th>' + str(item.price) + '</th></tr>').encode()
            response += '</table></body></html>'.encode()

        header = 'HTTP/1.1 200 OK\r\n'  # the first part of the header to send.
        header += 'Content-Type: ' + str(requestedType) + '\r\n\r\n'

    except Exception as e:  # Exception if the request the user has entered doesn't exist

        header = 'HTTP/1.1 404 Not Found\r\n'
        header += 'Content-Type: text/html\r\n\r\n'
        response = '<!DOCTYPE html><html><head><title>Error</title><style type="text/css">h1 {text-align: center;}li ' \
                   '{font-weight: bold;}</style></head><body><h1 style="color:red">The file is not ' \
                   'found</h1><br><ul><li> Ibraheem Duhaidi 1190283</li><li> Zakiya Abumurra 1191636</li><li> Sahar ' \
                   'Fayyad 1190119</li></ul><div style="position: relative; top: 120px;"><p>Client IP: ' + \
                   str(add[0]) + '</p><p>Client PORT: ' + str(add[1]) + '</p></div></body></html>'
        response = response.encode()

    final_response = header.encode() + response  # encoding the header and adding the response to the request
    connection.send(final_response)  # sending the final response with all parts of header
    connection.close()
      # Print the HTTP request on the terminal window
