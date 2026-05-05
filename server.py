from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        """
           Обрабатывает входящие GET-запросы от клиента.

           В зависимости от URL:
           - возвращает HTML-страницы сайта
           - или отдает статические файлы (например, изображения)
           """
        path = self.path

        # 🔹 Обработка картинки
        if path.endswith(".jpg"):
            try:
                with open(path[1:], "rb") as file:
                    self.send_response(200)
                    self.send_header("Content-type", "image/jpeg")
                    self.end_headers()
                    self.wfile.write(file.read())
            except:
                self.send_error(404)
            return

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()


        # 🔥 Роутинг (куда переходить)
        if path == "/" or path == "/index":
            filename = "index.html"
        elif path == "/catalog":
            filename = "catalog.html"
        elif path == "/category":
            filename = "category.html"
        elif path == "/contacts":
            filename = "contacts.html"
        else:
            filename = "contacts.html"  # на любой другой запрос

        with open(filename, "r", encoding="utf-8") as file:
            html = file.read()

        self.wfile.write(bytes(html, "utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        # 👉 декодируем строку
        data = post_data.decode("utf-8")

        # 👉 превращаем в словарь
        parsed_data = parse_qs(data)

        print("\n📩 Получены данные формы:")

        for key, value in parsed_data.items():
            print(f"{key}: {value[0]}")

        # ответ клиенту
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open("contacts.html", "r", encoding="utf-8") as file:
            html = file.read()

        self.wfile.write(bytes(html, "utf-8"))


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")