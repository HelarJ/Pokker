ID = Math.round(Math.random() * (999999-99999) + 100000) //genereerib kasutajale suvalise kuuekohalise ID
socket = null
var yhendatud = false
var andmed = null
var registreeritud = false
var ready = false
document.getElementById('sisend').value = "127.0.0.1"
inputkirjeldus = document.getElementById("inputkirjeldus")
panusekirjeldus = document.getElementById("panusekirjeldus")

function yhendus(ip){
    console.log(ip)
    try{
        console.log("Üritan ühendada...");
        socket = new WebSocket("ws://"+ip+":8765");
        socket.onopen = function () {
            console.log("Ühendatud")
            socket.send(ID+": Tere server!"); 
        }
        socket.onmessage = function (event) {
            if (event.data == "Tere "+ID){
                inputkirjeldus.innerText = "Kasutajanimi"
                yhendatud = true
            }
            else if (event.data == "Registreeritud"){
                inputkirjeldus.innerText = ""
                document.getElementById('submitnupp').innerText = "Chat"
                registreeritud = true
                document.getElementById("ready").hidden = false
                
            }
            else if (event.data.slice(0,4)=="chat"){
                uusrida = document.createElement("p"); 
                uusrida.innerText = event.data.slice(5)
                document.getElementById("kast").append(uusrida)
            }
            else if (event.data.charAt(0) == "{"){
                andmed = JSON.parse(event.data)
                document.getElementById("ready").hidden = true
                document.getElementById("nupud").hidden = false
                document.getElementById("info").hidden = false
                console.log(andmed)
                str = ""
                for (i=0; i<andmed["panused"].length;i++){
                    str = str + (i+1) + ": "+  andmed["chipid"][i] + ", "
                }
                folditud = ""
                for (i=0;i<andmed["folditud"].length;i++){
                    folditud = folditud + (andmed["folditud"][i]+1) + " "
                }

                document.getElementById("folditud").innerText = "Folditud: "+ folditud
                str = str.slice(0,-1)
                document.getElementById("kohalik").innerText = "Sina oled mängija "+ (andmed["number"]+1)
                document.getElementById("m2ngijad").innerText = "Mängijad: "+ str
                document.getElementById("k2ik").innerText = "Hetkel käib mängija "+ (andmed["kellek2ik"]+1)
                document.getElementById("laud").innerText = "Laud: "+ JSON.stringify(andmed["laud"])
                document.getElementById("k2si").innerText = "Käsi: " + JSON.stringify(andmed["k2si"])
                if (andmed["v6itja"]){
                    document.getElementById("k2ik").innerText = "Mäng on läbi"
                    document.getElementById("v6itja").innerText = "Võitis mängija " + JSON.stringify(andmed["v6itja"])
                    document.getElementById("ready").hidden = false
                    document.getElementById("nupud").hidden = true
                    document.getElementById("info").hidden = true
                    document.getElementById("ready").disabled = false
                } else {
                    document.getElementById("v6itja").innerText = ""
                }
                
            }
            console.log("Server: "+event.data);
        }
    }
    catch (err){
        inputkirjeldus.innerText = "Error"
        console.log(err)

    }
}

function valmis(){
    document.getElementById("ready").disabled = true
    socket.send(ID+":ready:")
}
function k2ik(sisend){
    document.getElementById("check").disabled = true
    document.getElementById("panusta").disabled = true
    document.getElementById("fold").disabled = true
    setTimeout(() => {
        document.getElementById("check").disabled = false
        document.getElementById("panusta").disabled = false
        document.getElementById("fold").disabled = false
    }, 1000);
    if (andmed && andmed["number"] != andmed["kellek2ik"]){
        panusekirjeldus.innerText = "Pole sinu kord"
        return
    }
    panusekirjeldus.innerText = "Panus"
    if (sisend.charAt(0)=="R"){
        p = document.getElementById("panus").value
        p = parseInt(p)
        document.getElementById("panus").value = p
        sisend = sisend+p
        if (isNaN(p) || !Number.isInteger(p) || p<1){
            panusekirjeldus.innerText = "Sisesta korrektne panus."
            return
        }
    }

    panusekirjeldus.innerText = "Panus"
    socket.send(ID+":k2ik:"+sisend)
}
function chatbox(s6num){
    if (s6num){
        socket.send(ID+":chat:"+s6num);
    }
}

function kasutajanimi(nimi){
    if (!nimi){
        nimi = "Anonymous"
    }
    socket.send(ID+":nimi:"+nimi);
}

function submitvajutus(sisend){
    document.getElementById('sisend').value = ""
    document.getElementById("submitnupp").disabled = true
    setTimeout(() => {
        document.getElementById("submitnupp").disabled = false
    }, 1000);
    if (!yhendatud){
        yhendus(sisend)
    }
    else if (!registreeritud){
        kasutajanimi(sisend)
    }
    else {
        chatbox(sisend)
    }
}
var input = document.getElementById("sisend");

nupuvajutus = function(event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        document.getElementById("submitnupp").click()
    }
};
input.addEventListener("keyup", function(event){
    if (event) {nupuvajutus(event)}})

