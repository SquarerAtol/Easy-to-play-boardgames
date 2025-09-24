document.addEventListener("DOMContentLoaded", function() {
  const listButton = document.getElementById("menu-button");
  const sideMenu = document.getElementById("side-menu");
  const closeButton = document.getElementById("close-button");
  const mainContent = document.getElementById("main-content");

  listButton.addEventListener("click", function(event) {
      event.preventDefault();
      sideMenu.style.width = "200px";

      if (window.innerWidth < 1360) {
          mainContent.style.marginLeft = "200px";
      }
  });

  closeButton.addEventListener("click", function(event) {
      event.preventDefault();
      sideMenu.style.width = "0";

      if (window.innerWidth < 1360) {
          mainContent.style.marginLeft = "0";
      }
  });

  // 사이드 메뉴 크기 조절
  window.addEventListener("resize", function() {
      if (window.innerWidth >= 1360) {
          mainContent.style.marginLeft = "0";
      } else if (sideMenu.style.width === "200px") {
          mainContent.style.marginLeft = "200px";
      }
  });
});
