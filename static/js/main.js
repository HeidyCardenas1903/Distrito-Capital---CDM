// Functions
function panelLateral(){
    const panel = document.querySelector(".panel-lateral");
    panel.classList.toggle('active');
}

const password = document.querySelector("#contraseña");
const eye = document.querySelector(".ojo");

eye.addEventListener("click", function() {
  if (password.type === "password") {
    password.type = "text";
    eye.classList.add("active");
  } else {
    password.type = "password";
    eye.classList.remove("active");
  }
});

let map;

async function initMap() {
  //@ts-ignore
  const { Map } = await google.maps.importLibrary("maps");

  map = new Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 8,
  });
}

initMap();
