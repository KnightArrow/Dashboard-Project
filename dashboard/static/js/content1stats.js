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
        options: {
            plugins: {
                title: {
                    display: true,
                    text: 'Content Per Source',
                },
            },
        },
    });
};

const getRandomChartType = () => {
    const chartTypes = ["bar", "doughnut", "pie"];
    return chartTypes[Math.floor(Math.random() * chartTypes.length)];
};

const getChartData = () => {
    fetch('content1_summary_by_source').then(response => response.json()).then(
        results => {
            console.log("results", results);
            const source_data = results.content1_source_data;
            const [data, labels] = [Object.values(source_data), Object.keys(source_data)];

            const randomType = getRandomChartType();
            renderChart(data, labels, randomType);
        }
    );
};

document.onload = getChartData();
