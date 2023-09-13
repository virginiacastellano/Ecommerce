// Configuración del carrusel de imágenes utilizando Owl Carousel
$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true, // Permite que el carrusel sea infinito
    margin: 20, // Margen entre los elementos del carrusel
    responsiveClass: true, // Habilita la capacidad de respuesta del carrusel
    responsive: {
        0: {
            items: 2, // Número de elementos a mostrar en pantallas pequeñas
            nav: false, // Oculta la navegación en pantallas pequeñas
            autoplay: true, // Inicia la reproducción automática
        },
        600: {
            items: 4, // Número de elementos a mostrar en pantallas medianas
            nav: true, // Muestra la navegación en pantallas medianas
            autoplay: true, // Inicia la reproducción automática
        },
        1000: {
            items: 6, // Número de elementos a mostrar en pantallas grandes
            nav: true, // Muestra la navegación en pantallas grandes
            loop: true, // Permite que el carrusel sea infinito en pantallas grandes
            autoplay: true, // Inicia la reproducción automática
        }
    }
})

// Maneja el evento clic en el botón "plus-cart"
$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] // Obtiene el elemento de cantidad asociado
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity // Actualiza la cantidad en la interfaz
            document.getElementById("amount").innerText=data.amount // Actualiza el monto total
            document.getElementById("totalamount").innerText=data.totalamount // Actualiza el monto total con impuestos
        }
    })
})

// Maneja el evento clic en el botón "minus-cart"
$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this.parentNode.children[2] // Obtiene el elemento de cantidad asociado
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            eml.innerText=data.quantity // Actualiza la cantidad en la interfaz
            document.getElementById("amount").innerText=data.amount // Actualiza el monto total
            document.getElementById("totalamount").innerText=data.totalamount // Actualiza el monto total con impuestos
        }
    })
})

// Maneja el evento clic en el botón "remove-cart"
$('.remove-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount // Actualiza el monto total
            document.getElementById("totalamount").innerText=data.totalamount // Actualiza el monto total con impuestos
            eml.parentNode.parentNode.parentNode.parentNode.remove() // Elimina el elemento del carrito en la interfaz
        }
    })
})

// Maneja el evento clic en el botón "plus-wishlist"
$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            // Redirecciona a la página de detalles del producto
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})

// Maneja el evento clic en el botón "minus-wishlist"
$('.minus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/minuswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            // Redirecciona a la página de detalles del producto
            window.location.href = `http://localhost:8000/product-detail/${id}`
        }
    })
})
