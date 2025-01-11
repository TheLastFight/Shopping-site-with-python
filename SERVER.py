import socket
from html import escape
from http import HTTPStatus

# Define the host and port for the server
HOST = '127.0.0.1'  # Localhost
PORT = 8080  # Port to listen on

# Sample product list
products = {
    1: {"name": "HP 1-EZO1801890", "price": 1550, "description": "Medium vps"},
    2: {"name": "HP 2-XDIOA03123", "price": 1000, "description": "slow vps"},
    3: {"name": "VPS PLUS - HP PERMIUM 3-PER7364", "price": 10000, "description": "ultra fast vps (Permium)"}
}


# Simulate a cart stored in a global variable
cart = []

# CSS for styling
css = """
    body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        background-color: #f4f4f9;
    }
    header {
        background-color: #333;
        color: white;
        padding: 10px 0;
        text-align: center;
    }
    h1, h2 {
        margin: 0;
    }
    .container {
        width: 80%;
        margin: 0 auto;
        padding: 20px;
    }
    .product, .cart-item {
        background-color: white;
        border: 1px solid #ddd;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        border-radius: 8px;
    }
    .product h2, .cart-item h2 {
        margin: 0;
        color: #333;
    }
    .product p, .cart-item p {
        color: #666;
    }
    .product a, .cart-item a {
        color: #fff;
        text-decoration: none;
    }
    .product a:hover, .cart-item a:hover {
        text-decoration: underline;
    }

    /* Button Styles */
    .button {
        padding: 10px 20px;
        background-color: #007bff;
        color: white;
        font-size: 14px;
        text-align: center;
        border: none;
        border-radius: 5px;
        cursor: pointer;
        display: inline-block;
        transition: background-color 0.3s, transform 0.2s ease-in-out;
    }

    .button:hover {
        background-color: #0056b3;
        transform: scale(1.05);
    }

    .button:active {
        background-color: #004085;
        transform: scale(1.02);
    }

    .button:focus {
        outline: none;
        box-shadow: 0 0 5px rgba(0, 123, 255, 0.8);
    }

    footer {
        text-align: center;
        margin-top: 20px;
        padding: 10px 0;
        background-color: #333;
        color: white;
    }
"""

# HTML content for the home page (product listing)
def generate_home_page():
    product_list_html = ""
    for product_id, product in products.items():
        product_list_html += f"""
        <div class="product">
            <h2>{escape(product['name'])}</h2>
            <p>{escape(product['description'])}</p>
            <p>Price: ${product['price']}</p>
            <a href="/product/{product_id}" class="button">View Product</a> | 
            <a href="/cart?add={product_id}" class="button">Add to Cart</a>
        </div>
        """
    return f"""
    <html>
    <head><title>Shopping Site</title><style>{css}</style></head>
    <body>
        <header>
            <h1>Server Shop</h1>
        </header>
        <div class="container">
            <h2>Available Products</h2>
            {product_list_html}
            <hr>
            <a href="/cart" class="button">View Cart</a>
        </div>
        <footer>
            <p>&copy; 2025 Shopping Site by _TheLastFight_</p>
        </footer>
    </body>
    </html>
    """

# HTML content for the product details page
def generate_product_page(product_id):
    product = products.get(product_id)
    if not product:
        return generate_404_page()

    return f"""
    <html>
    <head><title>{escape(product['name'])}</title><style>{css}</style></head>
    <body>
        <header>
            <h1>Shopping Site</h1>
        </header>
        <div class="container">
            <div class="product">
                <h2>{escape(product['name'])}</h2>
                <p>{escape(product['description'])}</p>
                <p>Price: ${product['price']}</p>
                <a href="/" class="button">Back to Home</a> | 
                <a href="/cart?add={product_id}" class="button">Add to Cart</a>
            </div>
        </div>
        <footer>
            <p>&copy; 2025 Shopping Site</p>
        </footer>
    </body>
    </html>
    """

# HTML content for the cart page
def generate_cart_page():
    if not cart:
        return """
        <html>
        <head><title>Your Cart</title><style>{css}</style></head>
        <body>
            <header>
                <h1>Shopping Site</h1>
            </header>
            <div class="container">
                <h2>Your Cart is Empty</h2>
                <a href="/" class="button">Back to Home</a>
            </div>
            <footer>
                <p>&copy; 2025 Shopping Site</p>
            </footer>
        </body>
        </html>
        """
    
    cart_html = "<h2>Your Cart</h2><ul>"
    for item in cart:
        cart_html += f"<li class='cart-item'>{escape(item['name'])} - ${item['price']}</li>"
    cart_html += "</ul><a href='/' class='button'>Back to Home</a>"
    return f"""
    <html>
    <head><title>Your Cart</title><style>{css}</style></head>
    <body>
        <header>
            <h1>Shopping Site</h1>
        </header>
        <div class="container">
            {cart_html}
        </div>
        <footer>
            <p>&copy; 2025 Shopping Site</p>
        </footer>
    </body>
    </html>
    """

# 404 page content
def generate_404_page():
    return """
    <html>
    <head><title>404 Not Found</title><style>{css}</style></head>
    <body>
        <header>
            <h1>Shopping Site</h1>
        </header>
        <div class="container">
            <h2>404 Not Found</h2>
            <p>The page you are looking for does not exist.</p>
            <a href="/" class="button">Back to Home</a>
        </div>
        <footer>
            <p>&copy; 2025 Shopping Site</p>
        </footer>
    </body>
    </html>
    """

# Function to generate an HTTP response header
def generate_http_response(status_code, content_type, content):
    status = HTTPStatus(status_code).phrase
    headers = f"HTTP/1.1 {status_code} {status}\r\n"
    headers += f"Content-Type: {content_type}\r\n"
    headers += "Connection: close\r\n\r\n"  # Close the connection after response
    return headers + content

# Create a socket object for the server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((HOST, PORT))

# Enable the server to accept connections (max 5 connections)
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}...")

while True:
    # Accept incoming client connection
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")

    # Receive the request (up to 1024 bytes)
    request = client_socket.recv(1024).decode()
    print(f"Request received:\n{request}")

    # Check the request type (for simplicity, we only handle GET requests)
    if request.startswith("GET /cart?add="):
        # Add product to cart
        try:
            product_id = int(request.split("GET /cart?add=")[1].split(" ")[0])
            product = products.get(product_id)
            if product:
                cart.append(product)
            response = generate_http_response(200, "text/html", generate_cart_page())
        except ValueError:
            response = generate_http_response(400, "text/plain", "Bad Request")
    elif request.startswith("GET /cart"):
        # Show the cart page
        response = generate_http_response(200, "text/html", generate_cart_page())
    elif request.startswith("GET /product/"):
        # Show product details page
        try:
            product_id = int(request.split("GET /product/")[1].split(" ")[0])
            response = generate_http_response(200, "text/html", generate_product_page(product_id))
        except ValueError:
            response = generate_http_response(404, "text/html", generate_404_page())
    else:
        # Default home page response
        response = generate_http_response(200, "text/html", generate_home_page())

    # Send the response to the client
    client_socket.sendall(response.encode())

    # Close the client connection
    client_socket.close()
