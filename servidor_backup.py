from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

HOST = "0.0.0.0"
PUERTO = int(os.environ.get("PORT", 10000))

reservas = []

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Cancha de Vóley</title>
<style>
body{font-family:Arial;background:#e3f2fd}
.card{background:white;width:420px;margin:80px auto;padding:20px;border-radius:10px}
button,input{width:100%;padding:10px;margin-top:10px}
li{background:#bbdefb;margin-top:5px;padding:5px;border-radius:5px}
</style>
</head>
<body>

<div class="card">
<h2>🏐 Reserva de Cancha de Vóley</h2>
<input id="nombre" placeholder="Nombre del equipo">
<input id="hora" placeholder="Hora (ej: 4pm - 5pm)">
<button onclick="reservar()">Reservar cancha</button>
<button onclick="ver()">Ver reservas</button>
<ul id="lista"></ul>
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
let li=document.createElement("li")
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
            self.send_header("Content-Type","text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML.encode("utf-8"))

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

print(f"Servidor activo en puerto {PUERTO}")
HTTPServer((HOST, PUERTO), Servidor).serve_forever()

