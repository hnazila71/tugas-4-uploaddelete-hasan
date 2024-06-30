import socket
import json
import base64
import logging

server_address = ('0.0.0.0', 7777)

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    logging.warning(f"connecting to {server_address}")
    try:
        logging.warning(f"sending message ")
        sock.sendall(command_str.encode())
        
        data_received = ""  # empty string
        while True:
            
            data = sock.recv(16)
            if data:
                
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
        
                break
        
        
        hasil = json.loads(data_received)
        logging.warning("data received from server:")
        return hasil
    except Exception as e:
        logging.warning(f"error during data receiving: {e}")
        return {'status': 'ERROR', 'data': str(e)}
    finally:
        sock.close() 

def remote_list():
    command_str = "LIST"
    hasil = send_command(command_str)
    if (hasil['status'] == 'OK'):
        print("daftar file : ")
        for nmfile in hasil['data']:
            print(f"- {nmfile}")
        return True
    else:
        print("Gagal")
        return False

def remote_get(filename=""):
    command_str = f"GET {filename}"
    hasil = send_command(command_str)
    if (hasil['status'] == 'OK'):
      
        namafile = hasil['data_namafile']
        isifile = base64.b64decode(hasil['data_file'])
        with open(namafile, 'wb+') as fp:
            fp.write(isifile)
        print(f"{filename} Success (Download)")
        return True
    else:
        print("Gagal")
        return False

def remote_upload(filename="", chunk_size=16384):
    try:
        with open(filename, 'rb') as fp:
            while True:
                chunk = fp.read(chunk_size)
                if not chunk:
                    break
                filedata = base64.b64encode(chunk).decode()
                command_str = f"UPLOAD {filename} {filedata}"
                hasil = send_command(command_str)
                if hasil['status'] != 'OK':
                    print("Failed (Upload)")
                    return False
        print("Success (Upload)")
        return True
    except FileNotFoundError:
        print("Not Found" + filename)
        return False

def remote_delete(filename=""):
    command_str = f"DELETE {filename}"
    hasil = send_command(command_str)
    if hasil['status'] == 'OK':
        print(f"{filename} Success (Delete)")
        return True
    else:
        print("Failed (Delete)")
        return False

if __name__ == '__main__':
    server_address = ('172.16.16.101', 8989)
    remote_list()
    #remote_get('donalbebek.jpg')
    #remote_upload('hasan2.txt')
    #remote_upload('donalbebek.jpg')
    remote_delete('donalbebek.jpg')
