const navToggle = document.querySelector(".nav-toggle");
const navLinks = document.querySelector(".nav-links");

if (navToggle && navLinks) {
  navToggle.addEventListener("click", () => {
    navLinks.classList.toggle("open");
  });
}

document.querySelectorAll(".nav-links a").forEach((link) => {
  const currentPage = window.location.pathname.split("/").pop() || "index.html";
  const href = link.getAttribute("href");
  const linkPage = href.split("#")[0] || "index.html";

  if (currentPage === linkPage && !href.startsWith("#")) {
    link.classList.add("active");
  }

  link.addEventListener("click", () => {
    navLinks?.classList.remove("open");
  });
});

document.querySelectorAll(".dashboard-button").forEach((button) => {
  button.addEventListener("click", () => {
    const dashboardPath = button.dataset.dashboard;
    alert(`Run the Streamlit dashboard with: streamlit run ${dashboardPath}`);
  });
});
