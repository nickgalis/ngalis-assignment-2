document.addEventListener('DOMContentLoaded', function () {
    const plot = d3.select("#plot")
        .append("svg")
        .attr("width", 800)
        .attr("height", 600);

    let data = [];
    let centroids = [];
    let labels = [];

    function drawPlot() {
        plot.selectAll("*").remove();

        // Draw centroids
        plot.selectAll(".centroid")
            .data(centroids)
            .enter()
            .append("circle")
            .attr("class", "centroid")
            .attr("cx", d => d[0] * 800)
            .attr("cy", d => d[1] * 600)
            .attr("r", 8)
            .attr("fill", (d, i) => d3.schemeCategory10[i])
            .attr("stroke", "#000")
            .attr("stroke-width", 2);

        // Draw data points
        plot.selectAll(".data-point")
            .data(data)
            .enter()
            .append("circle")
            .attr("class", "data-point")
            .attr("cx", d => d[0] * 800)
            .attr("cy", d => d[1] * 600)
            .attr("r", 5)
            .attr("fill", (d, i) => labels[i] !== undefined ? d3.schemeCategory10[labels[i]] : "#000");
    }

    document.getElementById("gen-data").addEventListener("click", function () {
        fetch("/generate_data", { method: "POST" })
            .then(response => response.json())
            .then(newData => {
                data = newData;
                labels = [];
                centroids = [];
                drawPlot();
            });
    });

    document.getElementById("init-method").addEventListener("change", function () {
        const method = this.value;
        fetch("/initialize", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ method, k: 3 })
        })
        .then(response => response.json())
        .then(newCentroids => {
            centroids = newCentroids;
            drawPlot();
        });
    });

    document.getElementById("step").addEventListener("click", function () {
        if (centroids.length === 0) {
            alert("Initialize centroids first");
            return;
        }

        fetch("/step", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ centroids })
        })
        .then(response => response.json())
        .then(result => {
            labels = result.labels;
            centroids = result.centroids;
            drawPlot();
        });
    });

    document.getElementById("converge").addEventListener("click", function () {
        if (centroids.length === 0) {
            alert("Initialize centroids first");
            return;
        }

        function convergeStep() {
            fetch("/step", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ centroids })
            })
            .then(response => response.json())
            .then(result => {
                labels = result.labels;
                centroids = result.centroids;
                drawPlot();

                // Check for convergence
                const oldCentroids = centroids.slice();
                centroids = result.centroids;

                if (!oldCentroids.some((old, i) =>
                    old[0] !== centroids[i][0] || old[1] !== centroids[i][1])) {
                    console.log("Converged");
                } else {
                    setTimeout(convergeStep, 500); // Small delay for visualization
                }
            });
        }

        convergeStep();
    });

    document.getElementById("reset").addEventListener("click", function () {
        labels = [];
        centroids = [];
        drawPlot();
    });

    drawPlot();
});