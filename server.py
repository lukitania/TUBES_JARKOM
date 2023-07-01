# Modul soket membentuk dasar dari semua komunikasi jaringan dengan Python
from socket import *
import sys 

serverHost = socket(AF_INET, SOCK_STREAM)   # server membuat soket TCP yang akan digunakan untuk menerima dan mengirim data melalui protokol TCP pada server
serverPort = 8080   # mengatur serverPort variabel integer ke 8080

serverHost.bind(('', serverPort))   # socket serverHost diikat (bind) ke alamat dan nomor port yang ditentukan
serverHost.listen(1)    # server akan menerima hingga satu koneksi pada satu waktu

while True:
    #Establish the connections
    print('Server is Ready')
    
    connectionSocket, addr = serverHost.accept()    # Ketika koneksi masuk diterima, metode accept() akan mengembalikan objek socket baru connectionSocket yang akan digunakan untuk berkomunikasi dengan klien, serta alamat addr dari klien
    try:
        name = connectionSocket.recv(1024)  # server menerima data dari klien yang dikirim melalui socket connectionSocket menggunakan metode recv() dan disimpan dalam variabel `name`
        filename = name.split()[1]  # memecah data `name` menjadi beberapa kata dengan metode `split()` lalu mengambil kata kedua (name.split()[1]), yang akan berisi path atau nama file yang diminta oleh klien
        print(filename) # server mencetak nama file yang diminta oleh klien
        if filename == b'/':    # mengecek apakah nama file yang diminta adalah '/'
            raise Exception     # jika benar server akan melemparkan exception dengan raise Exception
        file = open(filename[1:], "rb")    # server membuka file yang diminta oleh klien, `filename[1:]` untuk menghapus karakter pertama('/') dan "rb" untuk membaca file dalam mode biner
        outputdata = file.read() # server membaca seluruh data file yang dibuka sebelumnya dan disimpan dalam variabel `outputdata`
        
        #Send one HTTP header line into socket
        header = '\nHTTP/1.1 200 OK\n\n' #header ini menampung string \nHTTP/1.1 200 OK\n\n yang menunjukan bahwa header ini berisi tanggapan dari server terhadap request yang diterima. kode status 200 OK dari server ini menunjukan bahwa permintaan yang diterima berhasil.
        connectionSocket.send(header.encode())  # dengan `encode()` header diubah menjadi byte dan server mengirimkan HTTP header yang telah dibentuk ke klien
   
        #Send the content of the requested file to the client
        for i in range(0, len(outputdata)):  
            connectionSocket.send(outputdata[i:i+1]) #mengirim data dalam bentuk byte ke socket yang terhubun dengan client. parameter outputdata[i:i+1] mengambil 1 byte data dri variabel 'outputdata' pada indeks ke 'i'.
        connectionSocket.send(b'\r\n\r\n')  # server mengirimkan karakter newline (CR-LF) sebagai pemisah antara header dan isi file yang dikirim ke klien
        print('Response done, waiting for server...\n') #menampilkan teks/ output di konsol

        connectionSocket.close()  # mengakhiri komunikasi dengan klien
    
    except IOError: #digunakan apabila terjadi kesalahan I/O pada file "tindakan alternatif" ketika 'try' dijalankan.
        #Send response name for file not found
        filename = b'/NotFound.html'  # nama file yang akan digunakan sebagai respons ketika file yang diminta oleh klien tidak ditemukan 
        file = open(filename[1:], "rb")  # server membuka file yang diminta oleh klien, `filename[1:]` untuk menghapus karakter pertama('/') dan "rb" untuk membaca file dalam mode biner
        outputdata = file.read()  # membaca seluruh data file yang dibuka sebelumnya dan disimpan dalam variabel `outputdata`
        header = '\nHTTP/1.1 404 Not Found\n\n' #server memberikan tanggapan dengan kode 404 yg menandakan bahwa permintaan yg diminta client tidak ditemukan di server.
        connectionSocket.send(header.encode())  # dengan `encode()` header diubah menjadi byte dan server mengirimkan HTTP header yang telah dibentuk ke klien
        
        for i in range(0, len(outputdata)):  
            connectionSocket.send(outputdata[i:i+1])  # #mengirim data dalam bentuk byte ke socket yang terhubun dengan client. parameter outputdata[i:i+1] mengambil 1 byte data dri variabel 'outputdata' pada indeks ke 'i'.
        connectionSocket.send(b'\r\n\r\n')  # server mengirimkan karakter newline (CR-LF) sebagai pemisah antara header dan isi file yang dikirim ke klien

        connectionSocket.close()  # mengakhiri komunikasi dengan klien
        print('Response done, waiting for server...\n')  #menampilkan teks/ output di konsol

        #Close client socket
        connectionSocket.close() #menutup/mengakhiri koneksi socket antara server dan client
    
    except Exception: #ketika 'try' dijalankan, apabila terjadi kesalahan yang tidak ditangani oleh blok 'except' yg lebih spesifik sebelumnya, maka blok ini akan menangani kesalahan tersebut.
        #Send response name for file welcomePage
        filename = b'/WelcomePage.html'
        file = open(filename[1:], "rb") #server membuka file yang diminta oleh klien, `filename[1:]` untuk menghapus karakter pertama('/') dan "rb" untuk membaca file dalam mode biner
        outputdata = file.read() #membaca seluruh data file yang dibuka sebelumnya dan disimpan dalam variabel `outputdata`
        header = '\nHTTP/1.1 200 OK\n\n'#header ini menampung string \nHTTP/1.1 200 OK\n\n yang menunjukan bahwa header ini berisi tanggapan dari server terhadap request yang diterima. kode status 200 OK dari server ini menunjukan bahwa permintaan yang diterima berhasil.
        connectionSocket.send(header.encode()) #dengan `encode()` header diubah menjadi byte dan server mengirimkan HTTP header yang telah dibentuk ke klien

        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i:i+1]) #mengirim data dalam bentuk byte ke socket yang terhubun dengan client. parameter outputdata[i:i+1] mengambil 1 byte data dri variabel 'outputdata' pada indeks ke 'i'.
        connectionSocket.send(b'\r\n\r\n') #server mengirimkan karakter newline (CR-LF) sebagai pemisah antara header dan isi file yang dikirim ke klien

        connectionSocket.close() #menutup/mengakhiri koneksi socket antara server dan client
        print('Response done, waiting for server...\n') #menampilkan teks/ output di konsol

        #Close client socket
        connectionSocket.close() #enutup/mengakhiri koneksi socket antara server dan client
    
serverHost.close() #digunakan untuk menutup (mengakhiri) socket server yang sedang terbuka
sys.exit() # Terminate the program after sending the corresponding data / menghentikan program setelah mengirimkan data yg sesuai
