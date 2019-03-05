document.addEventListener('DOMContentLoaded', () => {

  if (location.pathname.split('/')[1] === "recipes"){
      let item = document.getElementById("nav-recipes");
      item.classList.add("nav-active");
  }

  if (location.pathname.split('/')[1] === "ingredients"){
      let item = document.getElementById("nav-ingredients");
      item.classList.add("nav-active");
  }

  if (location.pathname.split('/')[1] === "about"){
      let item = document.getElementById("menu-about");
      item.classList.add("active");
  }
  if (location.pathname.split('/')[1] === "process"){
      let item = document.getElementById("menu-process");
      item.classList.add("active");
  }

  if (location.pathname.split('/')[1] === ""){
      let item = document.getElementById("menu-login");
      item.classList.add("active");
  }

});
