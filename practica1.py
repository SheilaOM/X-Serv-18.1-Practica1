#!/usr/bin/python3

import webapp
import csv


class contentApp (webapp.webApp):

    list_urls = {}

    def inicializa(self):
        import os.path
        if os.path.isfile('urls.csv'):
            with open('urls.csv', 'r') as fich:
                read = csv.reader(fich, delimiter=',')
                for row in read:
                    self.list_urls[row[0]] = row[1]
            self.numurl = int(row[0])
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
            if (recurso == "/"):
                if self.numurl == 0:
                    url_guardadas = "No hay urls guardadas."
                else:
                    url_guardadas = "La lista de urls guardadas es:<br>"
                for element in self.list_urls:
                    url_guardadas = url_guardadas + (element + " -> " + self.list_urls[element] + "<br>")

                httpCode = "200 OK"
                htmlBody = "<html><body>" + url_guardadas + \
                            "<form method='POST' action=''><input type='text'" \
                            " name='url_larga'><input type='submit' value='Acortar'></form>" \
                            + "</body></html>"

            else:
                num_corta = recurso[1:]
                url_larga = self.list_urls[num_corta]
                httpCode = "HTTP/1.1 302 Redirect"
                htmlBody = "<html><body>Redireccionando a: " + url_larga +\
                            "<meta http-equiv='Refresh' content='1;url=" + url_larga + "'></body></html>"

        elif (metodo == "POST"):
            if (recurso == "/"):
                httpCode = "200 OK"
                import urllib.parse
                url_larga = urllib.parse.unquote(url_larga)
                self.list_urls[str(self.numurl)] = url_larga
                self.persiste()
                url_corta = "/" + str(self.numurl)
                htmlBody = "<html><body>La URL acortada de <a href=" + url_larga + ">" + url_larga +\
                            "</a> es <a href=" + url_corta + ">http://localhost:1234" + url_corta + "</a></body></html>"
                self.numurl += 1

        return (httpCode, htmlBody)


if __name__ == "__main__":
    testWebApp = contentApp("localhost", 1234)
