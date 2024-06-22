function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll(".add-to-cart");
    const urlsElement = document.getElementById("urls");
    const addToCartUrl = urlsElement.getAttribute("data-add-to-cart-url");
    const updateCartItemUrl = urlsElement.getAttribute("data-update-cart-item-url");

    buttons.forEach((button) => {
        button.addEventListener("click", function () {
            const productId = this.getAttribute("data-product-id");
            fetch(addToCartUrl, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                body: JSON.stringify({
                    product_id: productId,
                }),
            })
            .then((response) => {
                if (!response.ok) {
                    throw new Error("Network response was not ok");
                }
                return response.json();
            })
            .then((data) => {
                updateCartDisplay(
                    data.cart_item_count,
                    data.cart_total,
                    data.cart_items
                );
            })
            .catch((error) =>
                console.error("There was a problem with the fetch operation:", error)
            );
        });
    });

    // Fetch cart data when the page loads
    fetch(addToCartUrl, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
    })
    .then((response) => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();
    })
    .then((data) => {
        updateCartDisplay(data.cart_item_count, data.cart_total, data.cart_items);
    })
    .catch((error) =>
        console.error("There was a problem with the fetch operation:", error)
    );

    function updateCartDisplay(cartItemCount, cartTotal, cartItems) {
        document.getElementById("cart-item-count").innerText = cartItemCount;
        document.getElementById("cart-item-count-text").innerText = cartItemCount;
        document.getElementById("cart-total").innerText = cartTotal.toFixed(2);

        const cartItemsContainer = document.getElementById("cart-items-container");
        cartItemsContainer.innerHTML = ""; // Clear previous items

        cartItems.forEach((item) => {
            const itemElement = document.createElement("div");
            itemElement.classList.add(
                "cart-item",
                "p-2",
                "border-b",
                "border-gray-200"
            );
            itemElement.innerHTML = `
                <div class="flex justify-between items-center">
                    <div>
                        <img src="${item.product_image_url}" alt="${item.product_description}" class="product-image">
                        <p class="font-semibold">${item.product_description}</p>
                        <p class="text-sm text-gray-500">Price: $${item.product_price.toFixed(2)}</p>
                    </div>
                    <div class="flex items-center">
                        <button class="btn btn-outline btn-sm update-cart-item" data-product-id="${item.product_id}" data-action="decrement">-</button>
                        <span class="mx-2">${item.quantity}</span>
                        <button class="btn btn-outline btn-sm update-cart-item" data-product-id="${item.product_id}" data-action="increment">+</button>
                        <p class="font-semibold ml-4">Total: $${item.total_price.toFixed(2)}</p>
                    </div>
                </div>
            `;
            cartItemsContainer.appendChild(itemElement);
        });

        const updateButtons = document.querySelectorAll(".update-cart-item");
        updateButtons.forEach((button) => {
            button.addEventListener("click", function () {
                const productId = this.getAttribute("data-product-id");
                const action = this.getAttribute("data-action");
                fetch(updateCartItemUrl, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "X-CSRFToken": getCookie("csrftoken"),
                    },
                    body: JSON.stringify({
                        product_id: productId,
                        action: action,
                    }),
                })
                .then((response) => {
                    if (!response.ok) {
                        throw new Error("Network response was not ok");
                    }
                    return response.json();
                })
                .then((data) => {
                    updateCartDisplay(
                        data.cart_item_count,
                        data.cart_total,
                        data.cart_items
                    );
                })
                .catch((error) =>
                    console.error("There was a problem with the fetch operation:", error)
                );
            });
        });
    }
});

