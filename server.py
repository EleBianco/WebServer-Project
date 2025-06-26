import socket
import os
import mimetypes
import urllib.parse
from datetime import datetime
import threading

class MinimalWebServer:
    def __init__(self, host='localhost', port=8080, document_root='www'):
        self.host = host
        self.port = port
        self.document_root = document_root
        self.running = False
        
        # Configurazione MIME types
        mimetypes.add_type('text/html', '.html')
        mimetypes.add_type('text/css', '.css')
        mimetypes.add_type('image/jpeg', '.jpg')
        mimetypes.add_type('image/png', '.png')
        mimetypes.add_type('image/gif', '.gif')
        
    def log_request(self, client_addr, request_line, status_code, file_path=""):
        """Registra le richieste HTTP in formato di log"""
        timestamp = datetime.now().strftime("[%d/%b/%Y:%H:%M:%S]")
        log_entry = f"{client_addr[0]} - - {timestamp} \"{request_line}\" {status_code} - \"{file_path}\""
        print(log_entry)
        
        # Salva anche su file di log
        try:
            with open('server.log', 'a', encoding='utf-8') as log_file:
                log_file.write(log_entry + '\n')
        except:
            pass
    
    def get_mime_type(self, file_path):
        """Determina il MIME type del file"""
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type or 'text/plain'
    
    def read_file(self, file_path):
        """Legge un file e restituisce il contenuto"""
        try:
            # Per file di testo (HTML, CSS)
            if file_path.endswith(('.html', '.css', '.txt')):
                with open(file_path, 'r', encoding='utf-8') as file:
                    return file.read().encode('utf-8')
            # Per file binari (immagini)
            else:
                with open(file_path, 'rb') as file:
                    return file.read()
        except Exception as e:
            print(f"Errore nella lettura del file {file_path}: {e}")
            return None
    
    def create_404_response(self):
        """Crea una pagina 404 personalizzata"""
        html_404 = """<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pagina Non Trovata - 404</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; margin-top: 100px; background-color: #f0f8ff; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        h1 { color: #1e90ff; font-size: 4em; margin: 0; }
        h2 { color: #333; }
        p { color: #666; font-size: 1.2em; }
        a { color: #1e90ff; text-decoration: none; font-weight: bold; }
        a:hover { text-decoration: underline; }
        .volleyball { font-size: 3em; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>404</h1>
        <div class="volleyball">🏐</div>
        <h2>Pagina Non Trovata</h2>
        <p>Ops! La pagina che stai cercando non esiste.</p>
        <p>Forse è finita fuori dal campo di gioco!</p>
        <p><a href="/">Torna alla Home</a></p>
    </div>
</body>
</html>"""
        return html_404.encode('utf-8')
    
    def handle_request(self, client_socket, client_addr):
        """Gestisce una singola richiesta HTTP"""
        try:
            # Riceve la richiesta
            request = client_socket.recv(1024).decode('utf-8')
            if not request:
                return
            
            # Analizza la prima riga della richiesta
            request_lines = request.split('\n')
            request_line = request_lines[0].strip()
            
            # Estrae metodo, path e versione HTTP
            try:
                method, path, version = request_line.split()
            except ValueError:
                return
            
            # Gestisce solo richieste GET
            if method != 'GET':
                response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"
                client_socket.send(response.encode('utf-8'))
                self.log_request(client_addr, request_line, 405)
                return
            
            # Decodifica URL
            path = urllib.parse.unquote(path)
            
            # Se il path finisce con /, serve index.html
            if path == '/' or path == '':
                path = '/index.html'
            
            # Costruisce il percorso completo del file
            file_path = os.path.join(self.document_root, path.lstrip('/'))
            
            # Normalizza il percorso per sicurezza
            file_path = os.path.normpath(file_path)
            
            # Verifica che il file sia nella directory consentita
            if not file_path.startswith(os.path.abspath(self.document_root)):
                self.send_404(client_socket, client_addr, request_line)
                return
            
            # Verifica se il file esiste
            if os.path.exists(file_path) and os.path.isfile(file_path):
                # File trovato - serve il contenuto
                content = self.read_file(file_path)
                if content is not None:
                    mime_type = self.get_mime_type(file_path)
                    
                    response_headers = f"""HTTP/1.1 200 OK\r
Content-Type: {mime_type}\r
Content-Length: {len(content)}\r
Connection: close\r
Server: MinimalWebServer/1.0\r
\r
"""
                    
                    client_socket.send(response_headers.encode('utf-8'))
                    client_socket.send(content)
                    
                    self.log_request(client_addr, request_line, 200, file_path)
                else:
                    self.send_500(client_socket, client_addr, request_line)
            else:
                # File non trovato - errore 404
                self.send_404(client_socket, client_addr, request_line)
                
        except Exception as e:
            print(f"Errore nella gestione della richiesta: {e}")
        finally:
            client_socket.close()
    
    def send_404(self, client_socket, client_addr, request_line):
        """Invia risposta 404"""
        content = self.create_404_response()
        response = f"""HTTP/1.1 404 Not Found\r
Content-Type: text/html; charset=utf-8\r
Content-Length: {len(content)}\r
Connection: close\r
\r
"""
        client_socket.send(response.encode('utf-8'))
        client_socket.send(content)
        self.log_request(client_addr, request_line, 404)
    
    def send_500(self, client_socket, client_addr, request_line):
        """Invia risposta 500"""
        content = b"<h1>500 Internal Server Error</h1>"
        response = f"""HTTP/1.1 500 Internal Server Error\r
Content-Type: text/html\r
Content-Length: {len(content)}\r
Connection: close\r
\r
"""
        client_socket.send(response.encode('utf-8'))
        client_socket.send(content)
        self.log_request(client_addr, request_line, 500)
    
    def start(self):
        """Avvia il server"""
        # Verifica che la directory www esista
        if not os.path.exists(self.document_root):
            print(f"ERRORE: La directory '{self.document_root}' non esiste!")
            print("Crea la directory e i file HTML prima di avviare il server.")
            return
        
        # Crea il socket del server
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            # Bind e listen
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            
            self.running = True
            print(f"🏐 Server avviato su http://{self.host}:{self.port}")
            print(f"📁 Servendo contenuti da: {os.path.abspath(self.document_root)}")
            print("📝 Log delle richieste salvato in: server.log")
            print("⏹️  Premi Ctrl+C per fermare il server\n")
            
            while self.running:
                try:
                    # Accetta connessioni
                    client_socket, client_addr = server_socket.accept()
                    
                    # Gestisce la richiesta in un thread separato
                    client_thread = threading.Thread(
                        target=self.handle_request,
                        args=(client_socket, client_addr)
                    )
                    client_thread.daemon = True
                    client_thread.start()
                    
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    print(f"Errore nell'accettare connessioni: {e}")
                    
        except Exception as e:
            print(f"Errore nell'avvio del server: {e}")
        finally:
            server_socket.close()
            self.running = False
            print("\n🛑 Server fermato")

def main():
    """Funzione principale"""
    print("🏐 Web Server Minimale - Sito sulla Pallavolo")
    print("=" * 50)
    
    # Crea e avvia il server
    server = MinimalWebServer(host='localhost', port=8080, document_root='www')
    
    try:
        server.start()
    except KeyboardInterrupt:
        print("\n👋 Arresto del server richiesto dall'utente")
    except Exception as e:
        print(f"❌ Errore: {e}")

if __name__ == "__main__":
    main()