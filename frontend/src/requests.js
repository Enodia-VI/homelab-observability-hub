const label_visite = document.getElementById("label_visite");

async function  fetchVisite() {
    fetch(`/incrementa`)
        .then(handleFetchResponse)
        .then(data => {

	console.log("Dati ricevuti dal backend:", data);
	if (data.visite !== undefined) {
            document.getElementById('label_visite').innerText = data.visite;
        } else {
            console.error("La chiave 'visite' non è presente nel JSON:", data);
            document.getElementById('label_visite').innerText = "Errore dati";
        }

	})
        .catch(err => console.log(err));
}

function handleFetchResponse(response) {
    if (!response.ok) throw new Error('Errore HTTP nel fetch response:  ' + response.statusText);
    return response.json();
}

fetchVisite();
