
var stripe = Stripe("pk_test_51LyJ17BSE8CSa3qNcJ6w0qOgn3LVmvls7o42PqEBgpc4mSJx5d9j6VmY5U92F7sZmm1YVSfwfUtQ6bRsRm4JYJH700kXoq2qjt")
var elements = stripe.elements();
var style = {
    base: {
        color: "black",
        fontfamily: '"Helvetica Neue", Helvetica, sans-serif"',
        fontSmoothing: "antialiased",
        fontSize: "16px",
        '::placeholder': {
            color: "#aab7c4"
        }
    },
    invalid: {
        color: "#fa755a",
        iconColor: "#fa755a"
    }
};

var card = elements.create("card", {style: style});
card.mount("#card-element");
card.addEventListener("change", function(event){
    var displayError = document.getElementById("card-errors");
    if (event.error){
        displayError.textContent = event.error.message
    }
    else{
        displayError.textContent = "";
    }

});

var form = document.getElementById("payment-form");
form.addEventListener("submit", function(event){
    event.preventDefault();

    stripe.createToken(card).then(function(result){
        if(result.error){
            var errorElement = document.getElementById("card-errors");
            errorElement.textContent = result.error.message;
        }
        else{
            stripeTokenHandler(result.token);
        };
    });
});

var oneorm = document.getElementById("card-element")
function stripeTokenHandler(token){
    var form = document.getElementById("payment-form");
    var hiddenInput = document.createElement("input");
    hiddenInput.setAttribute("name", "stripeToken");
    hiddenInput.setAttribute("id", "strip");
    hiddenInput.setAttribute("value", token.id);

    oneorm.appendChild(hiddenInput);


    document.getElementById("butt12").addEventListener("click", function () {
        form.submit();
      });
}
