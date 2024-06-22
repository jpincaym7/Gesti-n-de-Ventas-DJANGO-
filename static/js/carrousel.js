document.addEventListener("DOMContentLoaded", function() {
  // Cuando se hace clic en el icono del carrito
  document.querySelector(".indicator").addEventListener("click", function() {
      // Alternar la visibilidad del menú del carrito
      document.querySelector("#cart-menu").classList.toggle("hidden");
  });

  // Cuando se hace clic en cualquier parte de la página (excepto en el menú del carrito)
  document.addEventListener("click", function(event) {
      const cartMenu = document.querySelector("#cart-menu");
      const indicator = document.querySelector(".indicator");
      if (!cartMenu.contains(event.target) && !indicator.contains(event.target)) {
          // Ocultar el menú del carrito si se hace clic fuera de él
          cartMenu.classList.add("hidden");
      }
  });
});