window.addEventListener("load", () => {
  document.querySelectorAll("span.go").forEach((element) => {
    if (element.innerText === "<BLANKLINE>") {
      element.innerText = "";
    }
  });
  document.querySelectorAll("span.c1").forEach((element) => {
    if (element.innerText.startsWith("# doctest:")) {
      element.innerText = "";
    }
  });
});
