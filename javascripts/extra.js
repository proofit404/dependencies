window.addEventListener("load", () => {
  document.querySelectorAll("span.go").forEach((element) => {
    if (element.innerText === "<BLANKLINE>") {
      element.innerText = "";
    }
  });
});
