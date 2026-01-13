from http.server import BaseHTTPRequestHandler, HTTPServer
import json

HOST = "localhost"
PUERTO = 8000

reservas = []

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">

<title>Reserva de Cancha</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{background:#eaf6ff}
.card{margin-top:80px}
</style>
</head>
<body>

<div class="container">
<div class="row justify-content-center">
<div class="col-md-5">
<div class="card shadow rounded-4">
<div class="card-body">
<h4 class="text-center mb-3">🏐 Reserva de Cancha de Vóley</h4>
<h4 class="text-center mb-3">🏐 PAOLA TAYPE</h4>

<input id="nombre" class="form-control mb-2" placeholder="Nombre del equipo">
<input id="hora" class="form-control mb-3" placeholder="Hora (ej: 5 a 6)">

<button class="btn btn-success w-100 mb-2" onclick="reservar()">Reservar</button>
<button class="btn btn-primary w-100 mb-3" onclick="ver()">Ver reservas</button>

<ul id="lista" class="list-group"></ul>

</div>
</div>
</div>
</div>
</div>

<script>
function reservar(){
fetch("/reservar",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
equipo:nombre.value,
hora:hora.value
})
}).then(r=>r.text()).then(alert)
}

function ver(){
fetch("/reservas")
.then(r=>r.json())
.then(d=>{
lista.innerHTML=""
d.forEach(x=>{
li=document.createElement("li")
li.className="list-group-item"
li.textContent=x.equipo+" - "+x.hora
lista.appendChild(li)
})
})
}
</script>

</body>
</html>
"""

class Servidor(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type","text/html")
            self.end_headers()
            self.wfile.write(HTML.encode())

        elif self.path == "/reservas":
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.end_headers()
            self.wfile.write(json.dumps(reservas).encode())

    def do_POST(self):
        if self.path == "/reservar":
            length = int(self.headers["Content-Length"])
            body = self.rfile.read(length)
            data = json.loads(body)
            reservas.append(data)

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Reserva registrada correctamente")

print("Servidor activo http://localhost:8000")
HTTPServer((HOST, PUERTO), Servidor).serve_forever()
