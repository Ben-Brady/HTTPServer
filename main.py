import curses
import socket
from utils import parse_request, encode_response, generate_response, Response, Request
import colorama
from colorama import Style, Fore, Back


HOSTNAME = "127.0.0.1"
PORT = 43421

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        print(f"Server started on {HOSTNAME}:{PORT}")
        print(f"URL: http://{HOSTNAME}:{PORT}")
        try:
            s.bind((HOSTNAME, PORT))
            
            while True:
                s.listen()
                conn, addr = s.accept()
                with conn:
                    req_data = conn.recv(1024)
                    req = parse_request(req_data)
                    res = generate_response(req)
                    res_data = encode_response(res)
                    log(addr, res, req)
                    conn.send(res_data)
                
        except (KeyboardInterrupt, Exception) as e:
            s.close()
            raise e


def log(addr: tuple[str, int], res: Response, req: Request):
    ip, port = addr
    sections = []
    sections.append(Fore.CYAN + f"{ip}:{port}" + Fore.RESET)
    if str(res.status_code)[0] == "4":
        sections.append(Fore.RED + str(res.status_code) + Fore.RESET)
    else:
        sections.append(Fore.BLUE + str(res.status_code) + Fore.RESET)
    sections.append(Fore.GREEN + req.path + Fore.RESET)
    
    print(" | ".join(sections))


if __name__ == "__main__":
    colorama.init()
    main()