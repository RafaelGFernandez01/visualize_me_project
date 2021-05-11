console.log('Hello rafa!!');

async function getDashboard(productId) {
    console.log('Fetching dashboard for product id:', productId);

    const response = await fetch(`http://localhost:5001/api/v1.0/dashboard/${productId}`);
    const body = await response.json();

    console.log('Dashboard:', body);

    console.log("Name of first:", body[0].name);
}

async function getProducts() {
    console.log('Fetching products');

    const response = await fetch('http://localhost:5001/api/v1.0/products');
    const body = await response.json();

    console.log('Products:', body);

    console.log("Name of first product:", body[0].name);
}

getProducts()
    .then(() => {
        console.log('Finished');
    })
    .catch((error) => {
        console.error('Error:', error);
    });