function format_number(val) {
    return parseFloat(parseFloat(val).toFixed(2)).toLocaleString();
}

function format_name(val) {
    return val.slice(0, 40).toLowerCase();
}

async function fill_products_select() {
    const products = await get_products();

    const selectObject = d3.select("#product-ids");
    selectObject.html("");

    products.forEach((product) => {
        selectObject
            .append("option")
            .attr("class", "text-capitalize")
            .attr("value", product.hts_code)
            .text(format_name(product.hts_code_description));
    });
}

async function get_dashboard_data(productId) {
    console.log('Fetching dashboard for product id:', productId);

    const response = await fetch(`http://localhost:5001/api/v1.0/dashboard/${productId}`);
    const body = await response.json();

    return body;
}

async function get_products() {
    console.log('Fetching products');

    const response = await fetch('http://localhost:5001/api/v1.0/products');
    const { products } = await response.json();
    console.log('Fetched products', products);

    return products;
}

async function render_dashboard(product_id) {
    const data = await get_dashboard_data(product_id);
    render_kpis(data.aggregates);
    render_table_top_importers('top_importers_by_net_kg', data.top_importers_by_net_kg);
    render_table_top_importers('top_importers_by_usd_fob_total', data.top_importers_by_usd_fob_total);
    render_table_top_country('top_country_of_origins_by_net_kg', data.top_country_of_origins_by_net_kg);
    render_table_top_country('top_country_of_origins_by_usd_fob_total', data.top_country_of_origins_by_usd_fob_total);
    render_map('top_country_of_origins_by_net_kg_map', data.top_country_of_origins_by_net_kg);
    render_map('top_country_of_origins_by_usd_fob_total_map', data.top_country_of_origins_by_usd_fob_total);
}

function render_kpis(aggs) {
    for (const key in aggs) {
        const val = aggs[key];
        const kpi_elem = d3.select(`#${key}`);
        kpi_elem.html(format_number(val));
    }
}

function render_table_top_importers (id, data) {
    const table_body = d3.select(`#${id} tbody`);
    table_body.html('');

    data.forEach((elem, idx) => {
        table_body
            .append('tr')
            .attr("class", "text-capitalize")
            .html(`
                <td>${idx + 1}</td>
                <td>${format_name(elem.importer)}</td>
                <td>${format_number(elem.value)}</td>
            `);
    });
}

function render_table_top_country (id, data) {
    const table_body = d3.select(`#${id} tbody`);
    table_body.html('');

    data.forEach((elem, idx) => {
        table_body
            .append('tr')
            .attr("class", "text-capitalize")
            .html(`
                <td>${idx + 1}</td>
                <td>${format_name(elem.country_of_origin)}</td>
                <td>${format_number(elem.value)}</td>
            `);        
    });
};

function render_map(id, dashboard_data) {
    const min_value = dashboard_data.reduce((min, d) => (d.value < min ? d.value : min), Number.MAX_SAFE_INTEGER);
    console.log('min_value', {min_value, dashboard_data});
    const data = [{
        type: 'scattergeo',
        mode: 'markers',
        locations: dashboard_data.map(d => d.country_of_origin_alpha_3),
        marker: {
            size: dashboard_data.map(d => (d.value / min_value) * 5),
            color: [10, 20, 40, 50],
            cmin: 0,
            cmax: 50,
            colorbar: {
                title: 'Some rate',
                ticksuffix: '%',
                showticksuffix: 'last'
            },
            line: {
                color: 'black'
            }
        },
        name: 'europe data'
    }];

    const layout = {
        'geo': {
            'scope': 'world',
            'resolution': 50
        }
    };

    Plotly.newPlot(id, data, layout);
}

// render
(async () => {
    // fill select with products
    await fill_products_select();
    const selected_product = d3.select("#product-ids").property("value");
    render_dashboard(selected_product);

    // register products handler
    d3.select('#product-ids')
        .on('change', () => {
            const selected_product = d3.select("#product-ids").property("value");
            render_dashboard(selected_product);
        });
})()
    .then(() => {
        console.log('Rendered...');
    })
    .catch((error) => {
        console.error('ERROR at render', error);
    });
