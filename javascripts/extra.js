window.addEventListener("load", (event) => {
  document.querySelectorAll("span.go").forEach((element) => {
    if (element.innerText === "<BLANKLINE>") {
      element.innerText = "";
    }
  });
});
