#!/usr/bin/python3

import webapp
import csv


class contentApp (webapp.webApp):

    list_urls = {}
    list_espj = {}

    def inicializa(self):
        import os.path
        if os.path.isfile('urls.csv'):
            with open('urls.csv', 'r') as fich:
                read = csv.reader(fich, delimiter=',')
                for row in read:
                    self.list_urls[row[0]] = row[1]
                    self.list_espj[row[1]] = row[0]
            self.numurl = len(self.list_urls)
        else:
            self.numurl = 0

    def persiste(self):
        with open('urls.csv', 'w', newline='') as fich:
            salida = csv.writer(fich, delimiter=',')
            for element in self.list_urls:
                salida.writerow([element, self.list_urls[element]])

    def parse(self, request):
        self.inicializa()

        metodo = request.split(' ', 1)[0]
        recurso = request.split(' ', 2)[1]
        find_url = request.count('url_larga=')
        if (find_url == 0):
            url = ""
        elif (find_url == 1):
            url = request.split('url_larga=')[1]

        return (metodo, recurso, url)

    def process(self, parsed):
        metodo, recurso, url_larga = parsed
        if (metodo == "GET"):
            if recurso == "favicon.ico":
                httpCode = "HTTP/1.1 404 Not found"
                httpBody = "<html><body><h1>Not Found</h1></body></html>"

            elif recurso == "/":
                if self.numurl == 0:
                    url_guard = "No hay urls guardadas."
                else:
                    url_guard = "La lista de urls guardadas es:<br>"
                for corta, larga in self.list_urls.items():
                    url_guard = url_guard + (corta + " -> " + larga + "<br>")

                httpCode = "HTTP/1.1 200 OK"
                htmlBody = "<html><body>" + url_guard +\
                           "<form method='POST' action=''><input type='text'" \
                           " name='url_larga'><input type='submit' " \
                           "value='Acortar'></form></body></html>"

            else:
                num_corta = recurso[1:]
                if num_corta in self.list_urls:
                    url_larga = self.list_urls[num_corta]
                    httpCode = "HTTP/1.1 302 Redirect"
                    htmlBody = "<html><body>Redireccionando a: " + url_larga +\
                               "<meta http-equiv='Refresh' content='1;url=" +\
                               url_larga + "'></body></html>"
                else:
                    httpCode = "HTTP/1.1 404 Not Found"
                    htmlBody = "<html><body>Recurso no disponible" +\
                               "</body></html>"

        elif (metodo == "POST"):
            if (recurso == "/"):
                if url_larga == "":
                    httpCode = "HTTP/1.1 404 Not Found"
                    htmlBody = "<html><body>Error. Debes introducir una url." \
                               "</body></html>"
                else:
                    httpCode = "HTTP/1.1 200 OK"
                    import urllib.parse
                    url_larga = urllib.parse.unquote(url_larga)

                    if (url_larga[0:7] != "http://" and
                            url_larga[0:8] != "https://"):
                        url_larga = "http://" + url_larga

                    if url_larga in self.list_espj:
                        url_corta = "/" + self.list_espj[url_larga]
                    else:
                        self.list_urls[str(self.numurl)] = url_larga
                        self.persiste()
                        url_corta = "/" + str(self.numurl)

                    htmlBody = "<html><body>La URL acortada de <a href=" +\
                               url_larga + ">" + url_larga + "</a> es " +\
                               "<a href=" + url_corta +\
                               ">http://localhost:1234" +\
                               url_corta + "</a></body></html>"
                    self.numurl += 1

        return (httpCode, htmlBody)


if __name__ == "__main__":
    testWebApp = contentApp("localhost", 1234)
