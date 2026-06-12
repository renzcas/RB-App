// === RB-APP 3D CAVE WORLD (v1 minimal) ===

let caveScene, caveCamera, caveRenderer;
let raycaster = new THREE.Raycaster();
let mouse = new THREE.Vector2();
let interactables = [];
let operator;
const clock = new THREE.Clock();

function initCave() {
    const container = document.getElementById("cave-container");

    caveScene = new THREE.Scene();
    caveScene.fog = new THREE.FogExp2(0x000000, 0.15);

    caveCamera = new THREE.PerspectiveCamera(
        60,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
    );

    caveRenderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    caveRenderer.setSize(container.clientWidth, container.clientHeight);
    container.appendChild(caveRenderer.domElement);

    const ambient = new THREE.AmbientLight(0x00ffff, 0.3);
    caveScene.add(ambient);

    // Operator
    createOperator();

    // Simple particles
    for (let i = 0; i < 150; i++) {
        const geo = new THREE.SphereGeometry(0.03, 8, 8);
        const mat = new THREE.MeshBasicMaterial({ color: 0x00ffff });
        const p = new THREE.Mesh(geo, mat);
        p.position.set(
            (Math.random() - 0.5) * 20,
            Math.random() * 5,
            (Math.random() - 0.5) * 20
        );
        caveScene.add(p);
    }

    // Module pillars in front
    createPillar("Module 1", -4, 0, -4, "module", 1);
    createPillar("Module 2", -2, 0, -4, "module", 2);
    createPillar("Module 3",  0, 0, -4, "module", 3);
    createPillar("Module 4",  2, 0, -4, "module", 4);
    createPillar("Module 5",  4, 0, -4, "module", 5);

    // Recon spheres behind
    createSphere("Recon 1", -3, 1, 2, "lab", "lab01_subdomains");
    createSphere("Recon 2", -1, 1, 2, "lab", "lab02_live_hosts");
    createSphere("Recon 3",  1, 1, 2, "lab", "lab03_ffuf");
    createSphere("Recon 4",  3, 1, 2, "lab", "lab04_waybackurls");

    window.addEventListener("click", onClick);
    window.addEventListener("resize", onResize);

    animateCave();
}

function createOperator() {
    const geo = new THREE.CapsuleGeometry(0.3, 1.2, 4, 8);
    const mat = new THREE.MeshBasicMaterial({ color: 0xffffff, wireframe: true });
    operator = new THREE.Mesh(geo, mat);
    operator.position.set(0, 1, 8);
    caveScene.add(operator);

    caveCamera.position.set(0, 1.6, 0);
    operator.add(caveCamera);
}

function createPillar(label, x, y, z, type, id) {
    const geo = new THREE.BoxGeometry(1, 3, 1);
    const mat = new THREE.MeshBasicMaterial({ color: 0x00ff99, wireframe: true });
    const pillar = new THREE.Mesh(geo, mat);
    pillar.position.set(x, y + 1.5, z);
    pillar.userData = { type, id };
    caveScene.add(pillar);
    interactables.push(pillar);
}

function createSphere(label, x, y, z, type, id) {
    const geo = new THREE.SphereGeometry(0.8, 24, 24);
    const mat = new THREE.MeshBasicMaterial({ color: 0x00ccff, wireframe: true });
    const sphere = new THREE.Mesh(geo, mat);
    sphere.position.set(x, y, z);
    sphere.userData = { type, id };
    caveScene.add(sphere);
    interactables.push(sphere);
}

function animateCave() {
    requestAnimationFrame(animateCave);
    const delta = clock.getDelta();
    caveRenderer.render(caveScene, caveCamera);
}

function onClick(event) {
    const container = document.getElementById("cave-container");
    const rect = container.getBoundingClientRect();

    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

    raycaster.setFromCamera(mouse, caveCamera);
    const hits = raycaster.intersectObjects(interactables);

    if (hits.length > 0) {
        const obj = hits[0].object;
        const { type, id } = obj.userData;

        if (type === "module" && window.runModule) runModule(id);
        if (type === "lab" && window.runLab) runLab(id);
    }
}

function onResize() {
    const container = document.getElementById("cave-container");
    caveCamera.aspect = container.clientWidth / container.clientHeight;
    caveCamera.updateProjectionMatrix();
    caveRenderer.setSize(container.clientWidth, container.clientHeight);
}

window.addEventListener("load", initCave);

// Hooks for later expansions:
window.createWriteupCrystal = window.createWriteupCrystal || function () {};
window.createPocHologram = window.createPocHologram || function () {};
