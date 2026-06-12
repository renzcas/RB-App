let moduleChart, labChart;

function runModule(id) {
    fetch(`/bug-bounty/modules/${id}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("output").textContent =
                JSON.stringify(data, null, 2);
            if (window.dashboardPulse) dashboardPulse();
        })
        .catch(err => {
            document.getElementById("output").textContent = err.toString();
        });
}

function runLab(name) {
    fetch(`/bug-bounty/recon/${name}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("output").textContent =
                JSON.stringify(data, null, 2);
            if (window.dashboardPulse) dashboardPulse();
        })
        .catch(err => {
            document.getElementById("output").textContent = err.toString();
        });
}

function generateWriteup() {
    const vuln = document.getElementById("vulnType").value;
    const endpoint = document.getElementById("endpoint").value;
    const impact = document.getElementById("impact").value;

    fetch(`/bug-bounty/writeup?vuln=${encodeURIComponent(vuln)}&endpoint=${encodeURIComponent(endpoint)}&impact=${encodeURIComponent(impact)}`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("output").textContent = data.writeup || JSON.stringify(data, null, 2);

            const severity = impact.toLowerCase().includes("critical")
                ? "critical"
                : impact.toLowerCase().includes("high")
                ? "high"
                : "medium";

            if (window.createWriteupCrystal) {
                createWriteupCrystal(Date.now(), severity);
            }
            if (window.createPocHologram && data.writeup) {
                createPocHologram(data.writeup.slice(0, 200));
            }
            if (window.dashboardPulse) dashboardPulse();
        })
        .catch(err => {
            document.getElementById("output").textContent = err.toString();
        });
}

function loadProgress() {
    fetch(`/progress/my-progress`)
        .then(res => res.json())
        .then(data => {
            let formatted = data.map(
                p => `${p.item_type} ${p.item_id}: ${p.completed ? "✔" : "✘"}`
            ).join("\n");
            document.getElementById("output").textContent = formatted;
            if (window.updateProgressBars) updateProgressBars(data);
        });
}

function updateProgressBars(data) {
    const modulesCompleted = data.filter(p => p.item_type === "module" && p.completed).length;
    const totalModules = 5;
    const percent = (modulesCompleted / totalModules) * 100;
    document.getElementById("module-progress").style.width = percent + "%";
}

function loadDashboard() {
    fetch(`/dashboard/user`)
        .then(res => res.json())
        .then(data => {
            document.getElementById("output").textContent = JSON.stringify(data, null, 2);
            renderCharts(data.stats);
            if (window.dashboardPulse) dashboardPulse();
        });
}

function renderCharts(stats) {
    const moduleCtx = document.getElementById("moduleChart").getContext("2d");
    const labCtx = document.getElementById("labChart").getContext("2d");

    if (moduleChart) moduleChart.destroy();
    if (labChart) labChart.destroy();

    moduleChart = new Chart(moduleCtx, {
        type: "doughnut",
        data: {
            labels: ["Completed", "Remaining"],
            datasets: [{
                data: [stats.modules_completed, stats.total_modules - stats.modules_completed],
                backgroundColor: ["#00ff99", "#333"]
            }]
        }
    });

    labChart = new Chart(labCtx, {
        type: "doughnut",
        data: {
            labels: ["Completed", "Remaining"],
            datasets: [{
                data: [stats.labs_completed, stats.total_labs - stats.labs_completed],
                backgroundColor: ["#00ccff", "#333"]
            }]
        }
    });
}
