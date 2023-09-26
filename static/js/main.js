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