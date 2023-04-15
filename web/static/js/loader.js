const page = document.getElementById("page-container");
const loader = document.getElementById("loader");

document.onreadystatechange = function () {
  let state = document.readyState;
  if (state === "interactive" || state === "complete") {
    loader.style.display = "none";
    page.style.display = "block";
  } else {
    loader.style.display = "block";
    page.style.display = "none";
  }
};
