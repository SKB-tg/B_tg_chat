/* libs start */
;(function() {
  var canUseWebP = function() {
    var elem = document.createElement('canvas');

    if (!!(elem.getContext && elem.getContext('2d'))) {
        // was able or not to get WebP representation
        return elem.toDataURL('image/webp').indexOf('data:image/webp') == 0;
    }

    // very old browser like IE 8, canvas not supported
    return false;
  };
  
  var isWebpSupported = canUseWebP();

  if (isWebpSupported === false) {
    var lazyItems = document.querySelectorAll('[data-src-replace-webp]');

    for (var i = 0; i < lazyItems.length; i += 1) {
      var item = lazyItems[i];

      var dataSrcReplaceWebp = item.getAttribute('data-src-replace-webp');
      if (dataSrcReplaceWebp !== null) {
        item.setAttribute('data-src', dataSrcReplaceWebp);
      }
    }
  }

  // var lazyLoadInstance = new LazyLoad({
  //   elements_selector: ".lazy"
  // });
})();
/* libs end */

/* myLib start */
;(function() {
  window.myLib = {};

  window.myLib.body = document.querySelector('body');

  window.myLib.closestAttr = function(item, attr) {
    var node = item;
    while(node) {
      var attrValue = node.getAttribute(attr);
      if (attrValue) {
        return attrValue;
      }

      node = node.parentElement;
    }

    return null;
  };
// ****задействует родительские элменты
  window.myLib.closestItemByClass = function(item, className) {
    var node = item;

    while(node) {
      if (node.classList.contains(className)) {
        return node;
      }

      node = node.parentElement;
    }

    return null;
  };

  window.myLib.toggleScroll = function() {
    myLib.body.classList.toggle('no-scroll');
  };

  window.myLib.dataDocker = function(arg, name) {
    localStorage.setItem(`${name}`, JSON.stringify(arg));
    return localStorage.getItem(`${name}`);
    // body...
  }
})();
/* myLib end */

/* header start */
;(function() {
  if (window.matchMedia('(max-width: 992px)').matches) {
    return;
  }

  var headerPage = document.querySelector('.header-page');

  window.addEventListener('scroll', function() {
    if (window.pageYOffset > 0) {
      headerPage.classList.add('is-active');
    } else {
      headerPage.classList.remove('is-active');
    }
  });

})();
/* header end */

/* popup start */
;(function() {
  var showPopup = function(target) {
    target.classList.add('is-active');
    console.log("showPopup");
  };

  var closePopup = function(target) {
    // g=target.classList;
    // d='.'+g[0]+'.'+g[1]+'.'+g[2];
    // console.log(d);
    // $(d).fadeOut(1000, function (g) {g.remove('is-active');});
    // var op=target.getAttribute("style") //style.opacity;
    // setInterval(op = op - 0.1, 100);
    //target.classList.remove('is-active');
    var opacity = 1; 
     var interval = setInterval(function() { opacity -= 0.05; 
      target.style.opacity=opacity;
        if (opacity < 0) { clearInterval(interval); 
          if (document.querySelector('body').classList.contains('no-scroll')) { myLib.toggleScroll();} target.classList.remove('is-active');
         target.removeAttribute("style"); return; } }, 40); 
     

  };

  myLib.body.addEventListener('click', function(e) {
    var target = e.target;
    var popupClass = myLib.closestAttr(target, 'data-popup');

    if (popupClass === null) {
      return;
    }

    e.preventDefault();
    var popup = document.querySelector('.' + popupClass);

    if (popup) {
      showPopup(popup);
      myLib.toggleScroll();
      closeMainButton();
    }
  });

  myLib.body.addEventListener('click', function(e) {
    var target = e.target;
    var popupItemClose = myLib.closestItemByClass(target, 'popup-close');

    var popup_thanks = myLib.closestItemByClass(target, 'popup-thanks') || null;

    if (popupItemClose ||
        target.classList.contains('popup__inner')) {
          var popup = myLib.closestItemByClass(target, 'popup');
          if (popup_thanks) { delete_popup__chek__order('chek__order_id');
           }
          closePopup(popup);
          //myLib.toggleScroll();

    }
  });

  myLib.body.addEventListener('keydown', function(e) {
    if (e.keyCode !== 27) {
      return;
    }

    var popup = document.querySelector('.popup.is-active');

    if (popup) {
      closePopup(popup);
     // myLib.toggleScroll();
    }
  });
})();

/* popup end */

/* scrollTo start */
;(function() {
  var scroll = function(target) {
    var targetTop = target.getBoundingClientRect().top;
    var scrollTop = window.pageYOffset;
    var targetOffsetTop = targetTop + scrollTop;
    var headerOffset = document.querySelector('.header-page').clientHeight;
    window.scrollTo(0, targetOffsetTop - headerOffset);
  } 

  myLib.body.addEventListener('click', function(e) {
    var target = e.target;
    var scrollToItemClass = myLib.closestAttr(target, 'data-scroll-to');
    if (scrollToItemClass === null) {
      return;
    }

    e.preventDefault();
    var scrollToItem = document.querySelector('.' + scrollToItemClass);

    if (scrollToItem) {
      scroll(scrollToItem);
    }
  });
})();
/* scrollTo end */

/* catalog start */
;(function() {
  var catalogSection = document.querySelector('.js-section-catalog');

  if (catalogSection === null) {
    return;
  }

  var removeChildren = function(item) {
    while (item.firstChild) {
      item.removeChild(item.firstChild);
    }
  };

  var updateChildren = function(item, children) {
    removeChildren(item);
    for (var i = 0; i < children.length; i += 1) {
      item.appendChild(children[i]);
    }
  };

  var catalog = catalogSection.querySelector('.catalog');
  var catalogNav = catalogSection.querySelector('.catalog-nav');
  var catalogItems = catalogSection.querySelectorAll('.catalog__item');

  catalogNav.addEventListener('click', function(e) {
    var target = e.target;
    var item = myLib.closestItemByClass(target, 'catalog-nav__btn');

    if (item === null || item.classList.contains('is-active')) {
      return;
    }

    e.preventDefault();
    var filterValue = item.getAttribute('data-filter');
    var previousBtnActive = catalogNav.querySelector('.catalog-nav__btn.is-active');

    previousBtnActive.classList.remove('is-active');
    item.classList.add('is-active');

    if (filterValue === 'all') {
      updateChildren(catalog, catalogItems);
      return;
    }

    var filteredItems = [];
    for (var i = 0; i < catalogItems.length; i += 1) {
      var current = catalogItems[i];
      var categories = current.getAttribute('data-category').split(',');

      if (categories.indexOf(filterValue) !== -1) {
        filteredItems.push(current);
      }
    }

    updateChildren(catalog, filteredItems);
  });
})();
/* catalog ennd */

// ;(function() {
//   var sectionContacts = document.querySelector('.section-contacts');

//   var ymapInit = function() {
//     if (typeof ymaps === 'undefined') {
//       return;
//     }
  
//     ymaps.ready(function () {
//       var myMap = new ymaps.Map('ymap', {
//               center: [53.917559, 27.585313],
//               zoom: 16
//           }, {
//               searchControlProvider: 'yandex#search'
//           }),
  
//           myPlacemark = new ymaps.Placemark(myMap.getCenter(), {
//               balloonContent: 'г. Минск, площадь Якуба Коласа, 2'
//           }, {
//               iconLayout: 'default#image',
//               iconImageHref: 'img/common/marker.png',
//               iconImageSize: [40, 50.2],
//               iconImageOffset: [-50, -38]
//           });
  
//       myMap.geoObjects.add(myPlacemark);
  
//       myMap.behaviors.disable('scrollZoom');
//     });
//   };

//   var ymapLoad = function() {
//     var script = document.createElement('script');
//     script.src = 'https://api-maps.yandex.ru/2.1/?lang=en_RU';
//     myLib.body.appendChild(script);
//     script.addEventListener('load', ymapInit);
//   };

//   var checkYmapInit = function() {
//     var sectionContactsTop = sectionContacts.getBoundingClientRect().top;
//     var scrollTop = window.pageYOffset;
//     var sectionContactsOffsetTop = scrollTop + sectionContactsTop;

//     if (scrollTop + window.innerHeight > sectionContactsOffsetTop) {
//       ymapLoad();
//       window.removeEventListener('scroll', checkYmapInit);
//     }
//   };

//   window.addEventListener('scroll', checkYmapInit);
//   // checkYmapInit();
// })();
// /* map end */

/* form start */
// ;(function() {
//   var forms = document.querySelectorAll('.form-send');
//   if (forms.length === 0) {
//     return;
//   }

//   var serialize = function(form, add_obj) {
//     var items = form.querySelectorAll('input, select, textarea');
//     var str = '';
//     var obj = {}; //
//     var val_category=Object.values(add_obj);
//     for (var i = 0; i < items.length; i += 1) {
//       var item = items[i];
//       var name = item.name;
//       var value = item.value;
//       var separator = i === 0 ? '' : '&';

//       if (value) {
//         str += separator + name + ':...' + value;
//         if (name.includes('-')) {
//           let name1 = name.split('-');
//           obj[name1[name1.length-1]] = value;//
//         } //
//         obj[name] = value;
//       }
//     }
//     str = 'Категория' + ':...' + val_category + separator + str;
//     obj['str'] = str;
//     obj['Категория']=val_category;
//      //
//     return obj;//
//   };
//   // var _obj = serialize(form);// =>{return obj};
//   var formSend = function(form, add_obj) {


//     var data = serialize(form, add_obj)['str'];
//     //var tg_data = serialize(form);
//     //delete tg_data.str;
//     console.log(add_obj);


//     var xhr = new XMLHttpRequest();
//     var url = '/content/zakazDataForm/';// + '?action=send_email';
    
//     xhr.open('POST', url);
//     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
//     xhr.responseType = 'json'; //см. обработчик хитрая доработка  -- https://developer.mozilla.org/ru/docs/Learn/JavaScript/Objects/JSON
//     xhr.onload = function() {
//       var activePopup = document.querySelector('.popup.is-active');

//       if (activePopup) {
//         activePopup.classList.remove('is-active');
//        } else {
//         myLib.toggleScroll();
//       }

//       if (xhr.response.ok === true) {
//         document.querySelector('.popup-thanks').classList.add('is-active');
//         data1 = data.split( '&',);// replace(/&/g, '\n');
//         chek_order(data1);  //данные в popup-oorder для информирования
//         //console.log(tg_data);
//         document.dispatchEvent(new CustomEvent('reset-cart'));
//       } else {
//         document.querySelector('.popup-error').classList.add('is-active');
//       }

//       form.reset();
//     };

//     xhr.send(data);
// 	sendMessage(data);

//   };

//   for (var i = 0; i < forms.length; i += 1) {
//     forms[i].addEventListener('submit', function(e) {
//       e.preventDefault();
//       var form = e.currentTarget;
//     // этапный способ сбора инфы о товаре в базу  -- можно закоминтать
//     const cart1 = JSON.parse(localStorage.getItem('cart')) || {};
//     const key_cart = Object.keys(cart1);
//     //console.log(cart1, key_cart[0]);
//     for (var i = 0; i < key_cart.length; i += 1) {
//     var cart3 = cart1[key_cart[i]];
//     const val_cart1 = Object.values(cart3)[6] || '';
//     var category_obj={};
//     //var type_obj_in_data={'product': cart1[key_cart[i]]}
//     var type_obj_in_data=cart1[key_cart[i]]

//     category_obj['Категория'] = val_cart1;
//     console.log(type_obj_in_data, cart1[key_cart[i]], category_obj );
//     // send_data_db(type_obj_in_data, category_obj);
//   }
   

//         //----------------------------------------
//         // "name"  TEXT,
//         // "description" TEXT,
//         // "price" TEXT,
//         // "slug"  TEXT,
//         // "category"  TEXT,
//         // "attribute" TEXT,
//         // "src"
//     formSend(form, category_obj);
//     //setTimeout(sendMessage(data), 1000);//вызов функции отсылки в чат, можно переделать забор из формы 
//     });
//   }
// })();
/* form end */

//   start   popup__chek__order*/
var valueAttr = function(id) {
  var node = document.querySelector('#' + id);
  while(node) {
    var attrValue = node.getAttribute('data-value');
    if (attrValue) {
      return attrValue;
    }

    node = node.parentElement;
  }

  return null;
};
const delete_popup__chek__order = (id) => {
const cartDOMElement = document.querySelector('.popup__chek__order');
  const chek__orderDOMElement = cartDOMElement.querySelector(`[data-chek__order-id="${id}"]`);

  cartDOMElement.removeChild(chek__orderDOMElement);
};
function chek_order(resp) {
  const cartDOMElement = document.querySelector('.popup__chek__order');

  if (!cartDOMElement) {
    return;
  }
    var resp1='';
    for (var i = 0; i < resp.length; i += 1) {
      resp1 += `<p>${resp[i]}</p>`;
    }
    var d = new Date();
    var n = d.toLocaleTimeString().slice(3,).replace(':', '_');
    const chek__orderDOMElement = document.createElement('div');
    const chek__orderTemplate = `
      <p class="popup__subtitle">Чек-ордер №${n}-д</p>
       ${resp1}`;
    chek__orderDOMElement.innerHTML = chek__orderTemplate;
    chek__orderDOMElement.setAttribute('data-chek__order-id', 'chek__order_id');
    // cartItemDOMElement.classList.add('js-cart-item');

    cartDOMElement.appendChild(chek__orderDOMElement);
  // };
}
//   end popup__chek__order*/
function closess(popupclass) {
  target=document.querySelector('.popup.'+popupclass);
  var opacity = 1; 
  var interval = setInterval(function() { opacity -= 0.05; 
      target.style.opacity=opacity;
  if (opacity < 0) { clearInterval(interval);
  if (document.querySelector('body').classList.contains('no-scroll')) { myLib.toggleScroll();} target.classList.remove('is-active');
         target.removeAttribute("style"); return; } }, 50);
}
/* cart start */
;(function() {
  const cartDOMElement = document.querySelector('.js-cart');

  if (!cartDOMElement) {
      return;
  }
  const cart = JSON.parse(localStorage.getItem('cart')) || {};
  const cartItemsCounterDOMElement = document.querySelector('.js-cart-total-count-items');
  const cartTotalPriceDOMElement = document.querySelector('.js-cart-total-price');
  const cartTotalPriceInputDOMElement = document.querySelector('.js-cart-total-price-input');
  const cartWrapperDOMElement = document.querySelector('.js-cart-wrapper');

  const renderCartItem = ({ id, name, attribute, src, price, quantity }) => {
      const cartItemDOMElement = document.createElement('div');

      const attributeTemplate = "" //attribute
          ?
          `<p class="cart-item__attribute">${attribute}</p><input type="hidden" name="${id}-Аттрибут" value="${attribute}">` :
          '';

      const cartItemTemplate = `
      <div class="cart-item cart__item">
      <div class="cart-item__main">
        <div class="cart-item__start">1
          <button style="display: none;class="cart-item__btn cart-item__btn--remove js-btn-cart-item-remove" type="button"></button>
        </div>
        <div style="display: none;" class="cart-item__img-wrapper">
          <img class="cart-item__img" src="${src}" alt="">
        </div>
        <div class="cart-item__content">
          <h3 class="cart-item__title">${name}</h3>
          <input type="hidden" name="Изделие" value="${name}">
          <input class="js-cart-input-quantity" type="hidden" name="Количество" value="${quantity}">
          <input class="js-cart-input-price" type="hidden" name="Цена" value="${price * quantity}">
          ${attributeTemplate}
        </div>
      </div>
      <div class="cart-item__end">
        <div class="cart-item__actions">
          <button class="cart-item__btn js-btn-product-decrease-quantity" type="button">-</button>
          <span class="cart-item__quantity js-cart-item-quantity">${quantity}</span>
          <button class="cart-item__btn js-btn-product-increase-quantity" type="button">+</button>
        </div>
        <p class="cart-item__price" style="display: none;"><span class="js-cart-item-price">${price * quantity}</span> ₽</p>
      </div>
      </div>
      `;
      cartItemDOMElement.innerHTML = cartItemTemplate;
      cartItemDOMElement.setAttribute('data-product-id', id);
      cartItemDOMElement.classList.add('js-cart-item');

      cartDOMElement.appendChild(cartItemDOMElement);
  };

  const saveCart = () => {
      localStorage.setItem('cart', JSON.stringify(cart));
  };

  // const updateCartTotalPrice = () => {
  //   const totalPrice = Object.keys(cart).reduce((acc, id) => {
  //     const { quantity, price } = cart[id];
  //     return acc + price * quantity;
  //   }, 0);

  //   if (cartTotalPriceDOMElement) {
  //     cartTotalPriceDOMElement.textContent = totalPrice;
  //   }

  //   if (cartTotalPriceInputDOMElement) {
  //     cartTotalPriceInputDOMElement.value = totalPrice;
  //   }
  // };

  // const updateCartTotalItemsCounter = () => {
  //   const totalQuantity = Object.keys(cart).reduce((acc, id) => {
  //     const { quantity } = cart[id];
  //     return acc + quantity;
  //   }, 0);

  //   if (cartItemsCounterDOMElement) {
  //     cartItemsCounterDOMElement.textContent = totalQuantity;
  //   }

  //   return totalQuantity;
  // };
  // function resursTukTuk() {
  //     // fetch("https://fastapi-pgstarterkit-test.onrender.com/status")
  //     //     .then(res => (res.json()))
  //     //     .then(data => {
  //     //         console.log(data);
  //     //     });
  //     console.log('ok')
  //     //         $.ajax('https://fastapi-pgstarterkit-test.onrender.com/status', {

  //     //     success: function (result) {
  //     //         console.log(result.json());
  //     //         if (result.ok) {
  //     //             alert('Hash is correct');

  //     //         } else {
  //     //             alert('Unknown error');
  //     //         }
  //     //     },
  //     //     error: function (xhr) {
  //     //             alert('No correct');
  //     //         }
  //     // });Access-Control-Allow-Origin
  // }
  const updateCart = () => {
      const totalQuantity = updateCartTotalItemsCounter();
      updateCartTotalPrice();
      saveCart();

      //   if (totalQuantity === 0) {
      //     cartWrapperDOMElement.classList.add('is-empty');
      //   } else {
      //     cartWrapperDOMElement.classList.remove('is-empty');
      //   }
      // };

      // const deleteCartItem = (id) => {
      //   const cartItemDOMElement = cartDOMElement.querySelector(`[data-product-id="${id}"]`);

      //   cartDOMElement.removeChild(cartItemDOMElement);
      //   delete cart[id];
      //  // updateCart();
  };

  const addCartItem = (data) => {
      const { id } = data;

      if (cart[id]) {
          increaseQuantity(id);
          return;
      }

      cart[id] = data;
      // renderCartItem(data);
      // updateCart();
  };

  const updateQuantity = (id, quantity) => {
      const cartItemDOMElement = cartDOMElement.querySelector(`[data-product-id="${id}"]`);
      const cartItemQuantityDOMElement = cartItemDOMElement.querySelector('.js-cart-item-quantity');
      //const cartItemPriceDOMElement = cartItemDOMElement.querySelector('.js-cart-item-price');
      //const cartItemInputPriceDOMElement = cartItemDOMElement.querySelector('.js-cart-input-price');
      const cartItemInputQuantityDOMElement = cartItemDOMElement.querySelector('.js-cart-input-quantity');
      //cart[id].quantity = quantity;
      cartItemQuantityDOMElement.textContent = quantity;
      //cartItemPriceDOMElement.textContent = quantity * cart[id].price;
      //cartItemInputPriceDOMElement.value = quantity * cart[id].price;
      cartItemInputQuantityDOMElement.value = quantity;
      //updateCart();
  };

  const decreaseQuantity = (id, value_default) => {
      const newQuantity = parseInt(value_default) - 1;
      if (newQuantity >= 1) {
          updateQuantity(id, newQuantity);
      }
  };

  const increaseQuantity = (id, value_default) => {
      const newQuantity = parseInt(value_default) + 1;
      updateQuantity(id, newQuantity);
  };

  const generateID = (string1, string2) => {
      const secondParam = string2 ? `-${string2}` : '';
      return `${string1}${secondParam}`.replace(/ /g, '-');
  };

  const getProductData = (productDOMElement) => {
    for (var i = 0; i < productDOMElement.length; i++) {
        var r = productDOMElement[i];
        console.log(r);
        if (r.attributes[0].value == "1") {
            var category = productDOMElement[i].getElementsByClassName('form__input')[0].value;
            console.log(category);
        }


        if (r.attributes[0].value == "3") {
            var URL_vacancy = productDOMElement[i].getElementsByClassName('form__input')[0].value;
            console.log(URL_vacancy);
        }

        const initDataUnsafe = Telegram.WebApp.initDataUnsafe || {}
        if (r.attributes[0].value == "2") {
            productDOMElement[i].getElementsByClassName('form__input')[0].value = -1002040372211 || initDataUnsafe.user.id;
            var ID_chat = -1002040372211 || initDataUnsafe.user.id;
            console.log(ID_chat);
        }

        if (r.attributes[0].value == "4") {
            var quantity_get_vacancy = r.children[0].children[0].children[1].children[1].value; //getEelmentsByClassName('js-cart-input-quantity').textContent;

            console.log(quantity_get_vacancy);
        }

        if (r.attributes[0].value == "5") {
            //productDOMElement[i].getElementsByClassName('form__input')[0].value = initDataUnsafe.user || "0";
            var number_of_pages = r.children[0].children[0].children[1].children[1].value;
            console.log(number_of_pages);
        }

        if (r.attributes[0].value == "6") {
            //productDOMElement[i].getElementsByClassName('form__input')[0].value = initDataUnsafe.user || "0";
            var days_ago = r.children[0].children[0].children[1].children[1].value;
            console.log(days_ago);
        }
    }
    return { category, URL_vacancy, days_ago, quantity_get_vacancy, number_of_pages, ID_chat };
  };

  const renderCart = () => {
      const ids = Object.keys(cart);
      ids.forEach((id) => renderCartItem(cart[id]));
  };

  const resetCart = () => {
      const ids = Object.keys(cart);
      ids.forEach((id) => deleteCartItem(cart[id].id));
  };

var closePopup = function(target) {
    var opacity = 1;
    var interval = setInterval(function() {
        opacity -= 0.05;
        target.style.opacity = opacity;
        if (opacity < 0) {
            clearInterval(interval);
            if (document.querySelector('body').classList.contains('no-scroll')) { myLib.toggleScroll(); } target.classList.remove('is-active');
            target.removeAttribute("style");
            return;
        }
    }, 40);
};

const cartInit = () => {
//renderCart();
//updateCart();
document.addEventListener('reset-cart', resetCart);
document.querySelector('body').addEventListener('click', (e) => {
  const target = e.target;
     // if (target.classList.contains('js-btn-add-to-cart')) {
     //    e.preventDefault();
     //    const productDOMElement = target.closest('.js-popup-order');
     //    const data = getProductData(productDOMElement);
     //    addCartItem(data);
     //  }
  // if (target.classList.contains('form__btn')) {
  //     e.preventDefault();
  //     // const productDOMElement = target.closest('.js-popup-order');
  //     // console.log(productDOMElement);
  //     const a = productDOMElement.getElementsByClassName('js-cart-item');
  //     var settingsVacancy = getProductData(a);
  //     var data = myLib.dataDocker(settingsVacancy, "settingsVacancy");
  // }

  if (target.classList.contains('js-btn-cart-item-remove')) {
      e.preventDefault();
      const cartItemDOMElement = target.closest('.js-cart-item');
      const productID = cartItemDOMElement.getAttribute('data-product-id');
      deleteCartItem(productID);
  }

  if (target.classList.contains('js-btn-product-increase-quantity')) {
      e.preventDefault();
      const cartItemDOMElement = target.closest('.js-cart-item');
      const cartItemDOMEInput = cartItemDOMElement.querySelector('.js-cart-input-quantity');
      const value_default = cartItemDOMEInput.getAttribute('value');
      const productID = cartItemDOMElement.getAttribute('data-product-id');
      increaseQuantity(productID, value_default);
  }

  if (target.classList.contains('js-btn-product-decrease-quantity')) {
      e.preventDefault();
      const cartItemDOMElement = target.closest('.js-cart-item');
      const cartItemDOMEInput = cartItemDOMElement.querySelector('.js-cart-input-quantity');
      const value_default = cartItemDOMEInput.getAttribute('value');
      const productID = cartItemDOMElement.getAttribute('data-product-id');
      decreaseQuantity(productID, value_default);
  }
  if (target.classList.contains('js-popup-order-close')) {
      e.preventDefault();
      const productDOMElement = target.closest('.popup.popup-order.is-active');
      const a = productDOMElement.getElementsByClassName('js-cart-item');
      var settingsVacancy = getProductData(a);
      var data = myLib.dataDocker(settingsVacancy, "settingsVacancy");
      const attribute = target.getAttribute('data-product-attribute-value') || '';
      const price = target.getAttribute('data-product-attribute-price');
      //const productDOMElement = target.closest('.popup.popup-order.is-active');
      const activeAttributeDOMElement = productDOMElement.getElementsByClassName('popup is-active');
      //const data_setVacancy_last = localStorage.getItem('settingsVacancy');
      //console.log(localStorage.getItem('settingsVacancy'), productDOMElement);
      closePopup(productDOMElement);
  }
});
}
cartInit();
// resursTukTuk();
})();
    //  end cart

    // TG-web-app  start
function _sendMessage(msg, with_webview=1) {
        if (!initDataUnsafe.query_id) {
            alert('WebViewQueryId not defined');
            return;
        }

        //if (!msg_id == '') {let msg_id_m = JSON.stringify(msg_id, null, 2);}
    	   //let msg_id_m = JSON.stringify(msg);
    //---------------------------------------------------------------------
            fetch("/content/sendMessage/", {
                "method": "POST",
                headers: {
                    "Content-Type": "application/json;charset=utf-8"
                },
            "body": JSON.stringify({
            "data": {_auth: initData,
            "msg": msg || '',
            "with_webview": !initDataUnsafe.receiver && with_webview ? 1 : 0}
            })
             })
            .then(res => (res.json()))
            .then(res => {if (res.ok) {
                    //alert('Hash is correct');

                } else {
                    alert('Unknown error');
                }
                return res;
            })
            .then(data => {
                //alert('Server error');
                console.log(data);
            })
}
// Telegram.WebApp.ready();

// const initData = Telegram.WebApp.initData || '';
// const initDataUnsafe = Telegram.WebApp.initDataUnsafe || {};
function selectURL(el) {
  const v = el.value;
  var name_el = el.children; // attributes[0].value;//('data-sel');
       var class_url = "";
    for (var i = 0; i < name_el.length; i++) {

     var val_atr = name_el[i].getAttribute("value");
     if (val_atr == v) {     var class_url = name_el[i].getAttribute("data-sel");
    console.log(class_url);}}
  const sel_el_url = document.querySelector(`#${class_url}`).parentElement.getElementsByTagName('option');//toggleAttribute("selected", true);
  for (var i = 0; i < sel_el_url.length; i++) {
    sel_el_url[i].removeAttribute('selected')
  }
  document.querySelector(`#${class_url}`).toggleAttribute("selected", true);
  console.log(sel_el_url);

  }


function webviewExpand() {
    Telegram.WebApp.expand();
}

// function sendMessagePlusData(data) {
//     Telegram.WebApp.sendData(data);
// }
//;(function(){

let initDataUnsafe_JSON = JSON.stringify(initDataUnsafe, null, 2);
if (initDataUnsafe.query_id && initData) {
    $('#webview_data_status').show();
//------------------------------------------------------------------
    fetch("/content/checkData/", {
        "method": "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8"
        },
        "body": JSON.stringify({
        "data": {_auth: initData},
        "id": initData.id,})
         })
        .then(res => (res.json()))
        .then(res => {if (res.ok) {
                alert('Hash is correct');

            } else {
                alert('Unknown error');
            }
            return res;
        })
        .then(data => {
                //alert('Server error');
            console.log(data);
        })
}
//})();

function send_data_db(obj, obj1) {
     // var obj = {};
    // formData.forEach( ( value,key) => {
    //   obj[key] = value;
    // });
    _json = JSON.stringify(obj);

    console.log(_json, initData, obj );
 
//-----------------------------------------------------------
        fetch("/content/sendDataDB/", {
            "method": "POST",
            headers: {
                "Content-Type": "application/json;charset=utf-8"
            },
            "body": JSON.stringify(obj)//{ 
            //"data": obj}//{"a_uth": obj}}),
              //"item_data": obj, "id_m": 4})
             })
            .then(res => (res.json()))
            .then(res => {if (res.ok) {
                   // alert('Hash is correct');

                } else {
                    alert('Unknown error');
                }
                return res;
            })
            .then(data => {
                console.log(data);
            })
}

function getVacancyPlusSettings(msg_id, with_webview) {
    if (!initDataUnsafe.query_id) {
        alert('WebViewQueryId not defined');
        return;
    }
    //if (!msg_id == '') {let msg_id_m = JSON.stringify(msg_id, null, 2);}
    $('#vacancy_data_img').toggle();
  let msg_id_m = JSON.stringify(msg_id);
        $.ajax('/get_vakancy', {
            type: 'POST',
            data: {
                _auth: initData,
                msg_id: msg_id_m || '--',
                with_webview: !initDataUnsafe.receiver && with_webview ? 1 : 0
                //message: msg_id || "NO"
            },
            jsonp: false,
            jsonpCallback: "callbackName",
            dataType: 'json',
            success: function (result) {
                //$('button').prop('disabled', false);
                  //$('#vacancy_data').html(msg);
                  $('#vacancy_data_img').toggle();//css('display', 'none')

                if (result) {
                   $('#vacancy_data').html(result["data"]);
                   if ($('#btn_vacancy_chanal')) {    $('#btn_vacancy_chanal').toggle()}
                //     if (result.response.ok) {
                //         if (!el) {webviewClose() }
                //         $('#btn_status').html('Message sent successfully!').addClass('ok').show();
                //         $('#vacancy_data').html(result.response);
                //     } else {
                //         $('#btn_status').text(result.response.description).addClass('err').show();
                //         //alert(result.response.description);
                //     }
                } else {
                    $('#btn_status').text('Unknown error').addClass('err').show();
                    //alert('Unknown error');
                }
            },
            error: function (xhr) {
                $('#vacancy_data_img').toggle();//css('display', 'none')
                $('button').prop('disabled', false);
                $('#btn_status').text('Server error').addClass('err').show();
                alert(`${result.error}`);
            },
          //   statusCode: {
          // 200: function () { // выполнить функцию если код ответа HTTP 200
          //   $('#vacancy_data').html('result 200');
          // }}
    });
}
