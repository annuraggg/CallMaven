const params = new Proxy(new URLSearchParams(window.location.search), {
    get: (searchParams, prop) => searchParams.get(prop),
});

msg = document.getElementById('msg')


let raised = params.raised
let error = params.error

if (raised) {
    msg.innerHTML = "Support Ticket Raised!"
    alert("Support Ticket Raised!")
} else if(error) {
    msg.style.color = "red"
    msg.innerHTML = "Something Went Wrong!"
}