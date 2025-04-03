// Sidebar Aç/Kapat
const sidebarToggle = document.getElementById("sidebarToggle");
const sidebar = document.getElementById("sidebar");
const mainContent = document.getElementById("mainContent");
const navbar = document.getElementById("navbar");
// Sayfa yüklendiğinde navbarın genişliğini kontrol eden fonksiyon
window.addEventListener("load", function () {
  let sidebar = document.getElementById("sidebar");
  let navbar = document.getElementById("navbar");

  if (sidebar.classList.contains("d-none")) {
    navbar.style.width = "100%";
  } else {
    navbar.style.width = "83.7%";
  }
});
sidebarToggle.addEventListener("click", function () {
  // Sidebar'ı gizle veya göster
  sidebar.classList.toggle("d-none");

  // Main içeriğin konumunu değiştir
  if (sidebar.classList.contains("d-none")) {
    mainContent.style.marginLeft = "0";
  } else {
    mainContent.style.marginLeft = "250px";
  }
  // Navbarın genişliiğini değiştir
  if (sidebar.classList.contains("d-none")) {
    navbar.style.width = "100%";
    navbar.style.left = "0"; // Sidebar'ın genişliğini dengelemek için Left kullanın
  } else {
    navbar.style.width = "83.7%";
    navbar.style.left = "250px"; // Sidebar açık olduğunda navbar tam genişlik alır
  }
});
