'use strict';

// variables for menu
const _navbar = 'header-menu';
const _navbar_toggle = 'menu-toggler';
const _navbar_active = 'active';
const _navbar_fixed = 'has-fixed';
const _navbar_mobile = 'mobile-menu';
const _navbar_break = 992;
const _menu_toggle = 'menu-toggle';
const _menu_sub = 'menu-sub';
const _menu_active = 'active';


const navbar = document.querySelector('.'+_navbar);
const navbar_toggle = document.querySelector('.'+_navbar_toggle);
const menu_toggle = document.querySelectorAll('.'+_menu_toggle);

// Toggle Dropdown Menu
function toggleDropdown(parent,subMenu,_active) {
  if(!parent.classList.contains(_active)){
    parent.classList.add(_active);
    slideDown(subMenu);
  }else{
    parent.classList.remove(_active);
    slideUp(subMenu);
  }
}

// Close Dropdown Menu Siblings
function closeDropdownSiblings(siblings,menu,_sub,_active) {
  Array.from(siblings).forEach(item => {
      if(item.classList.contains(_active) && !menu.classList.contains(_active)){
        item.classList.remove(_active);
        Array.from(item.children).forEach(subItem => {
          if(subItem.classList.contains(_sub)){
            slideUp(subItem);
          }
        });
      }
  });
}

//Dropdown Menu
function menuDropdown(toggle,_sub,_active) {
  toggle.forEach(item => {
    item.addEventListener("click", function(e){
      e.preventDefault();
      let itemParent = item.parentElement;
      let itemSibling = item.nextElementSibling;
      let itemParentSiblings = item.parentElement.parentElement.children;
      closeDropdownSiblings(itemParentSiblings,itemParent,_sub,_active);
      toggleDropdown(itemParent,itemSibling,_active);
    });
  });
}
//Dropdown Menu Init
menuDropdown(menu_toggle,_menu_sub,_menu_active);

// mobile nav class add/remove
function mobileNavInit() {
  if (window.innerWidth <= _navbar_break) {
    navbar.classList.add(_navbar_mobile);
  }
}
mobileNavInit();

function mobileNavResize() {
  if (window.innerWidth <= _navbar_break) {
    navbar.classList.add(_navbar_mobile);
  }else{
    navbar.classList.remove(_navbar_mobile, _navbar_active);
    navbar_toggle.classList.remove(_navbar_active);
  }
}
window.addEventListener('resize', function () {
  mobileNavResize();
});

/*  =======================================================
  Mobile nav toggle
========================================================== */
function mobileNavToggle() {
  navbar_toggle.classList.toggle(_navbar_active);
  navbar.classList.toggle(_navbar_active);
}
if(navbar_toggle) {
  navbar_toggle.addEventListener("click", function () {
    mobileNavToggle();
  });
}

/*  =======================================================
  Mobile Remove / close nav when overlay is clicked
========================================================== */
function navOutSideClick(event) {
  if(event.target !== navbar && event.target !== navbar_toggle && event.target !== userSidebar && event.target !== sidebarMenuOpen &&
    event.target.closest('.'+_navbar) == null &&  event.target.closest('.'+_navbar_toggle) == null){
    if(navbar_toggle) {
      navbar_toggle.classList.remove(_navbar_active);
    }
    if(userSidebar) {
      userSidebar.classList.remove(_navbar_active);
    }
    navbar.classList.remove(_navbar_active);
  }
}
document.addEventListener("click", function (event) {
  navOutSideClick(event);
});

/*  =======================================================
  Sticky navbar on scroll down
========================================================== */
function stickyMenu(selector) {
  let elem = document.querySelectorAll(selector);
  if(elem.length > 0){
    elem.forEach(item => {
      let _item_offset = item.offsetTop;
      window.addEventListener("scroll", function () {
        if(window.scrollY > _item_offset){
          item.classList.add(_navbar_fixed);
        }else{
          item.classList.remove(_navbar_fixed);
        }
      });
    });
  }
}
stickyMenu('.is-sticky');

/*  =======================================================
  User sidebar menu
========================================================== */
var sidebarMenuOpen = document.querySelector(".menu-toggler-user-open");
var userSidebar = document.querySelector(".sidebar-user-mobile");
var sidebarMenuClose = document.querySelector(".menu-toggler-user-close");

function userSidebarMenu() {
  if(sidebarMenuOpen) {
    sidebarMenuOpen.addEventListener("click", function(e) {
      e.preventDefault();
      userSidebar.classList.add(_menu_active);
    });
  }
  if(sidebarMenuClose) {
    sidebarMenuClose.addEventListener("click", function(e) {
      e.preventDefault();
      userSidebar.classList.remove(_menu_active);
    });
  }

}

userSidebarMenu();


/*  =======================================================
  Countdown
========================================================== */
function countDownTimer(selector){
  let elem = document.querySelectorAll(selector);
  if(elem.length > 0){
    elem.forEach(item => {
        let itemid = item.id;
        let exptime = item.dataset.expTime;
        let expMessage = item.dataset.expMessage ? item.dataset.expMessage : "Countdown Ended";
        const year = new Date().getFullYear();
        const choosenDate = new Date(exptime).getTime();
        
        let countdown = setInterval(function() {
          const today = new Date().getTime();
          const diff = choosenDate - today;
          let hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
          let minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
          let seconds = Math.floor((diff % (1000 * 60)) / 1000);
        
          if(choosenDate >= today){
            document.getElementById(itemid).innerHTML =
            `<div class="countdown-item"><span class="countdown-amount">${hours}</span><span class="countdown-text"> Hours</span></div>
            <div class="countdown-item"><span class="countdown-amount">${minutes}</span><span class="countdown-text"> Minutes</span></div>
            <div class="countdown-item"><span class="countdown-amount">${seconds}</span><span class="countdown-text"> Seconds</span></div>`;
          }else{
            document.getElementById(itemid).innerHTML = `<div class="countdown-note">${expMessage}</div>`;
          }
        }, 1000);
    });
  }
}
countDownTimer('.countdown-timer');

/*  =======================================================
  Custom Tooltips
========================================================== */
function customTooltip(selector, active) {
  let elem = document.querySelectorAll(selector);
  if(elem.length > 0){
    elem.forEach(item => {
      const parent = item.parentElement;
      const next = item.nextElementSibling;
      Popper.createPopper(item, next);
      parent.addEventListener("mouseenter", function(event) {
        parent.classList.add(active)
      });
      parent.addEventListener("mouseleave", function(event) {
        parent.classList.remove(active)
      });
    });
  }
}

customTooltip('.custom-tooltip','active');

/*  =======================================================
  Swiper carousel
========================================================== */
function swiperCarousel(selector) {
  let elem = document.querySelectorAll(selector);
  if(elem.length > 0){
    elem.forEach(item => {
      let _breakpoints = item.dataset.breakpoints ? JSON.parse(item.dataset.breakpoints) : null;
      let _autoplay = item.dataset.autoplay ? JSON.parse(item.dataset.autoplay) : false;
      let _loop = item.dataset.loop ? JSON.parse(item.dataset.loop) : false;
      let _centeredSlides = item.dataset.centeredslides ? JSON.parse(item.dataset.centeredslides) : false;
      let _speed = item.dataset.speed ? parseInt(item.dataset.speed) : 1000;
      var swiper = new Swiper(item, {
        // Optional parameters
        centeredSlides: _centeredSlides,
        loop: _loop,
        speed: _speed,
        autoplay:_autoplay,
        // If we need pagination
        pagination: {
          el: ".swiper-pagination",
          type: 'bullets',
          clickable: true,
        },
        // Navigation arrows
        navigation: {
          nextEl: '.swiper-button-next',
          prevEl: '.swiper-button-prev',
          clickable: true,
        },
        breakpoints: _breakpoints,
      });
    });
  }
}

swiperCarousel('.swiper-carousel');

/*  =======================================================
  Bootstrap Tooltips
========================================================== */
function bootstrapTooltip(selector) {
  let tooltipEl = document.querySelectorAll(selector);
  let tooltipTriggerList = [].slice.call(tooltipEl);
  let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })
}

bootstrapTooltip('[data-bs-toggle="tooltip"]');

/*  =======================================================
  Clipboard js
========================================================== */
function copyToClipboard(selector) {
  var clipboardEl = document.querySelectorAll(selector);
  if( typeof(clipboardEl) != 'undefined' && clipboardEl != null ){
    var clipboard = new ClipboardJS(clipboardEl);
  }
  clipboard.on("success", function(e){
    let target = e.trigger.querySelector(".tooltip-text");
    let prevText = target.innerHTML;
    target.innerHTML = "Copied";
    setTimeout(function(){
      target.innerHTML = prevText;
    }, 1000)
  });
}

copyToClipboard(".copy-text");

/*  =======================================================
  File upload
========================================================== */
function fileUpload(selector) {
  let elem = document.querySelectorAll(selector);
  if(elem.length > 0) {
    elem.forEach(item => {
      item.addEventListener("change", function(){
        var target = document.getElementById(item.dataset.target);
        var allowedExtensions  = ["jpg", "png", "gif", "webp", "mp4", "mp3"];
        var fileExtension  = this.value.split(".").pop();
        var lastDot = this.value.lastIndexOf('.');
        var ext = this.value.substring(lastDot + 1);
        var extTxt = target.value = ext;

        if(!allowedExtensions.includes(fileExtension)) {
          alert(extTxt + " file type not allowed, Please upload jpg, png, gif, webp, mp4 or mp3 file");
          target.innerHTML = "Please upload jpg, png, gif, webp, mp4 or mp3 file";
        }else {
          target.innerHTML = item.files[0].name;
        }
      })
    })
  }
}

fileUpload(".file-upload-input");

/*  =======================================================
  Unlock once purchased Checkbox switcher
========================================================== */
function checkboxSwitcher(selector) {
  let elem = document.querySelectorAll(selector);
  if(elem.length > 0) {
    elem.forEach(item => {
      item.addEventListener("change", function(){
        let target = document.getElementById(item.dataset.target);
        if(this.checked) {
          target.classList.add("is-shown");
        }else {
          target.classList.remove("is-shown");
        }
      });
    });
  }
 }

 checkboxSwitcher(".checkbox-switcher");

 /*  =======================================================
  Show/Hide passoword
========================================================== */
function showHidePassword(selector){
  let elem = document.querySelectorAll(selector);
  if(elem.length > 0){
    elem.forEach(item => {
      item.addEventListener("click", function(e){
        e.preventDefault();
        let target = document.getElementById(item.getAttribute("href"));
        if(target.type == "password") {
          target.type = "text";
          item.classList.add("is-shown");
        }else{
          target.type = "password";
          item.classList.remove("is-shown");
        }
      });

    });
  }
}

showHidePassword(".password-toggle");

/*  =======================================================
  International Teliphone Input
========================================================== */
function internationalTeliphone(selector) {
  let intlTeliphoneInput = document.querySelectorAll(selector);
  if(intlTeliphoneInput.length > 0) {
    intlTeliphoneInput.forEach(item => {
      intlTelInput(item);
    })
  }
}
internationalTeliphone(".phone-number");

/*  ==========================================
    Dark/Light mode configaration
========================================== */
function themeSwitcher(selector){
  let themeToggler = document.querySelectorAll(selector);
  if(themeToggler.length > 0) {
    themeToggler.forEach(item => {
      item.addEventListener("click", function(e){
        e.preventDefault();
        document.body.classList.toggle("dark-mode");
        if(document.body.classList.contains("dark-mode")) {
          localStorage.setItem("website_theme", "dark-mode");
        }else {
          localStorage.setItem("website_theme", "default");
        }
      });
    })
  }

  function retrieveTheme(){ 
    var theme = localStorage.getItem('website_theme');
    if(theme != null){
        document.body.classList.remove('default', 'dark-mode');
        document.body.classList.add(theme);
    }
  }

  retrieveTheme();

  if(window) {
    window.addEventListener("storage", function(){
      retrieveTheme();
    },false);
  }
}

themeSwitcher(".theme-toggler");

/*  ==========================================
    SHOW UPLOADED IMAGE
========================================== */
function uploadImage(selector) {
  let elem = document.querySelectorAll(selector);
  if(elem.length > 0) {
    elem.forEach(item => {
      item.addEventListener("change", function(){
        if(item.files && item.files[0]) {
          let img = document.getElementById(item.dataset.target);
          img.onload = function() {
            URL.revokeObjectURL(img.src);
          }
          img.src = URL.createObjectURL(item.files[0]);

          let allowedExtensions  = ["jpg", "JPEG", "JPG", "png" ];
          let fileExtension  = this.value.split(".").pop();
          var lastDot = this.value.lastIndexOf('.');
          var ext = this.value.substring(lastDot + 1);
          var extTxt = img.value = ext;
          if (!allowedExtensions.includes(fileExtension)) {
              alert(extTxt + " file type not allowed, Please upload jpg, JPG, JPEG, or png file");
              img.src = " ";
          }
        }

      })
    });
  }
}

uploadImage(".upload-image");

/*  ================================================
    Check/Uncheck all checkboxes  with single click
===================================================== */
function checkboxAllToggle(selector, selectorInputText) {
  let checkAllBtn = document.querySelectorAll(selector);
  let checkAllInput = document.querySelectorAll(selectorInputText);
  
  if(checkAllBtn.length > 0) {
    checkAllBtn.forEach(item => {
      item.addEventListener("click", function(e){
        if (e.target.value == 'Check All') {
          checkAllInput.forEach(function(checkbox){
            checkbox.checked = true;
          });
          e.target.value = 'Uncheck All';
        } else {
          checkAllInput.forEach(function(checkbox){
            checkbox.checked = false;
          });
          e.target.value = 'Check All';
        }
      })
    })
  }
}

checkboxAllToggle(".check-all", ".check-all-input");

/*  ================================================================
  Remove bootstrap dropdown menu when you hover on header navigation
==================================================================== */
function hideDropdown(selector, dropdown, dropdownToggler) {
  let elem = document.querySelectorAll(selector);
  let hideDropdownMenu = document.querySelector(dropdown);
  let dropdownBtn = document.querySelector(dropdownToggler);
  if(elem.length > 0) {
    elem.forEach(item => {
      item.addEventListener("mouseenter", function(e) {
        if(hideDropdownMenu) {
          hideDropdownMenu.classList.remove("show");
        }
      })
    })
  }
  if(dropdownBtn) {
     dropdownBtn.addEventListener("click", function() {
        if(hideDropdownMenu) {
          hideDropdownMenu.classList.add("show");
        }
     })
  }
}

hideDropdown(".menu-link", ".hide-dropdown", ".dropdown-toggle-show");
