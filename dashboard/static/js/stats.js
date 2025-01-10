const renderChart = (data, labels, type) => {
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: 'Last 6 months content',
                data: data,
                backgroundColor: [
                    "rgba(255, 5, 142, 0.2)",
                    "rgba(217, 255, 2, 0.2)",
                    "rgba(255, 97, 255, 0.2)",
                    "rgba(184, 253, 255, 0.2)",
                    "rgba(232, 255, 198, 0.2)",
                    "rgba(204, 255, 164, 0.2)",
                ],
                borderColor: [
                    "rgba(255, 255, 255, 0.2)",
                    "rgba(255, 255, 255, 0.2)",
                    "rgba(255, 0, 55, 0.2)",
                    "rgba(255, 0, 55, 0.2)",
                    "rgba(0, 187, 255, 0.2)",
                    "rgba(0, 255, 13, 0.2)",
                ],
                borderWidth: 1,
            }],
        },
    });
};
const renderChart1 = (data, labels, type) => {
    var ctx = document.getElementById('myChart1').getContext('2d');
    var myChart = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: 'Last 6 months content',
                data: data,
                backgroundColor: [
                    "rgba(255, 5, 142, 0.2)",
                    "rgba(217, 255, 2, 0.2)",
                    "rgba(255, 97, 255, 0.2)",
                    "rgba(184, 253, 255, 0.2)",
                    "rgba(232, 255, 198, 0.2)",
                    "rgba(204, 255, 164, 0.2)",
                ],
                borderColor: [
                    "rgba(255, 255, 255, 0.2)",
                    "rgba(255, 255, 255, 0.2)",
                    "rgba(255, 0, 55, 0.2)",
                    "rgba(255, 0, 55, 0.2)",
                    "rgba(0, 187, 255, 0.2)",
                    "rgba(0, 255, 13, 0.2)",
                ],
                borderWidth: 1,
            }],
        },
    });
};
const renderChart2 = (data, labels, type) => {
    var ctx = document.getElementById('myChart2').getContext('2d');
    var myChart = new Chart(ctx, {
        type: type,
        data: {
            labels: labels,
            datasets: [{
                label: 'Last 6 months content',
                data: data,
                backgroundColor: [
                    "rgba(255, 5, 142, 0.2)",
                    "rgba(217, 255, 2, 0.2)",
                    "rgba(255, 97, 255, 0.2)",
                    "rgba(184, 253, 255, 0.2)",
                    "rgba(232, 255, 198, 0.2)",
                    "rgba(204, 255, 164, 0.2)",
                ],
                borderColor: [
                    "rgba(255, 255, 255, 0.2)",
                    "rgba(255, 255, 255, 0.2)",
                    "rgba(255, 0, 55, 0.2)",
                    "rgba(255, 0, 55, 0.2)",
                    "rgba(0, 187, 255, 0.2)",
                    "rgba(0, 255, 13, 0.2)",
                ],
                borderWidth: 1,
            }],
        },
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Content Per Category',
                },
            },
        },
    });
};


const getChartData = () => {
    fetch('content_summary_by_category').then(response => response.json()).then(
        results => {
            console.log("results", results);
            const category_data = results.content_category_data;
            const [data, labels] = [Object.values(category_data), Object.keys(category_data)];
            renderChart(data, labels, 'pie');
            renderChart1(data, labels, 'doughnut');
            renderChart2(data, labels, 'bar');
        }
    );
};

document.onload = getChartData();
